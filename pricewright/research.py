"""Market research as an input: comparables packets, normalised and compared.

Research is kept apart from the model on purpose. A packet is a YAML (or JSON)
list of comparable prices, gathered by an agent or supplied by the user, in the
schema below; it can be swapped or refreshed without touching any offering.
The model produces a cost-based price; a packet only tells you where that price
sits in the market (:func:`position`).

Schema (one record)::

    id, specialty, offering, provider, region, price | price_low + price_high,
    currency, unit, contact_hours, duration_s, group_size, delivery,
    provider_tier, evidence (fetched | secondary | snippet | inferred), date, url, notes
"""

from __future__ import annotations

import json
import statistics
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass, fields
from pathlib import Path

EVIDENCE_WEIGHT: Mapping[str, float] = {"fetched": 1.0, "secondary": 0.7, "snippet": 0.5, "inferred": 0.3}


@dataclass(frozen=True)
class Comparable:
    id: str
    specialty: str
    offering: str
    price: float | None = None
    price_low: float | None = None
    price_high: float | None = None
    currency: str = "EUR"
    unit: str = "per_group"
    provider: str = ""
    region: str = ""
    contact_hours: float | None = None
    duration_s: float | None = None
    group_size: float | None = None
    delivery: str = ""
    provider_tier: str = ""
    evidence: str = "snippet"
    date: str = ""
    url: str = ""
    notes: str = ""

    @property
    def mid(self) -> float | None:
        if self.price is not None:
            return float(self.price)
        lo, hi = self.price_low, self.price_high
        if lo is not None and hi is not None:
            return (lo + hi) / 2
        return lo if lo is not None else hi

    @property
    def weight(self) -> float:
        return EVIDENCE_WEIGHT.get(self.evidence, 0.3)


_FIELDS = {f.name for f in fields(Comparable)}


def _records(path: Path) -> list[dict]:
    text = path.read_text()
    if path.suffix == ".json":
        return json.loads(text)
    import yaml

    return yaml.safe_load(text) or []


def load_packet(*paths: str | Path) -> list[Comparable]:
    """Read one or more packets. Unknown keys are kept out, with no error.

    Raises a ``ValueError`` naming the file and record when a record has no id,
    specialty or offering, since such a record cannot be compared to anything.
    """
    out = []
    for p in map(Path, paths):
        for i, rec in enumerate(_records(p)):
            missing = {"id", "specialty", "offering"} - set(rec)
            if missing:
                raise ValueError(f"{p}: record #{i} lacks {sorted(missing)}: {rec}")
            out.append(Comparable(**{k: v for k, v in rec.items() if k in _FIELDS}))
    return out


# --- normalisation -------------------------------------------------------------------
Metric = Callable[[Comparable], "float | None"]


def per_person_contact_hour(c: Comparable) -> float | None:
    """Price per participant per delivered hour (needs hours, and a group size for group prices)."""
    m, h = c.mid, c.contact_hours
    if m is None or not h:
        return None
    if c.unit == "per_person":
        return m / h
    if c.unit in ("per_group", "per_event") and c.group_size:
        return m / (h * c.group_size)
    return None


def per_contact_hour(c: Comparable) -> float | None:
    """Price per delivered hour for the whole room (group, event or session prices)."""
    m, h = c.mid, c.contact_hours
    if m is None:
        return None
    if c.unit == "per_hour":
        return m
    if h and c.unit in ("per_group", "per_event", "per_session"):
        return m / h
    return None


def per_finished_minute(c: Comparable) -> float | None:
    m = c.mid
    if m is None:
        return None
    if c.unit == "per_finished_minute":
        return m
    if c.unit == "per_finished_second":
        return m * 60
    if c.unit == "per_project" and c.duration_s:
        return m / (c.duration_s / 60)
    return None


def as_is(c: Comparable) -> float | None:
    """The price in its own unit (use with a filter that fixes the unit)."""
    return c.mid


METRICS: Mapping[str, Metric] = {
    "per_person_contact_hour": per_person_contact_hour,
    "per_contact_hour": per_contact_hour,
    "per_finished_minute": per_finished_minute,
    "as_is": as_is,
}


def select(
    comparables: Iterable[Comparable],
    *,
    specialty: str | None = None,
    offerings: Sequence[str] | None = None,
    units: Sequence[str] | None = None,
    delivery: Sequence[str] | None = None,
    exclude_tiers: Sequence[str] = (),
) -> Iterator[Comparable]:
    for c in comparables:
        if specialty and c.specialty != specialty:
            continue
        if offerings and c.offering not in offerings:
            continue
        if units and c.unit not in units:
            continue
        if delivery and c.delivery not in delivery:
            continue
        if c.provider_tier in exclude_tiers:
            continue
        yield c


@dataclass(frozen=True)
class Position:
    """Where a value sits among normalised comparables (in the target currency)."""

    value: float
    n: int
    q10: float
    median: float
    q90: float
    percentile: float  # share of evidence weight at or below value
    used: tuple[tuple[str, float], ...]  # (id, normalised value)

    @property
    def verdict(self) -> str:
        if self.n < 3:
            return "thin evidence"
        if self.value < self.q10:
            return "below market (under p10)"
        if self.value > self.q90:
            return "above market (over p90)"
        return "within market"


def _wquantile(pairs: Sequence[tuple[float, float]], q: float) -> float:
    pairs = sorted(pairs)
    total = sum(w for _, w in pairs)
    acc = 0.0
    for v, w in pairs:
        acc += w
        if acc >= q * total - 1e-12:
            return v
    return pairs[-1][0]


def position(
    value: float,
    comparables: Iterable[Comparable],
    *,
    metric: str | Metric = "per_person_contact_hour",
    fx: Mapping[str, float] | None = None,
    currency: str = "EUR",
) -> Position | None:
    """Locate ``value`` (already in ``metric`` units and ``currency``) among comparables.

    ``fx`` maps a currency to its value in ``currency`` (e.g. ``{"USD": 0.87}`` when
    ``currency='EUR'``). A comparable in a currency missing from ``fx`` is skipped
    rather than silently treated as equal.

    >>> cs = [Comparable(str(i), "training", "x", price=p, unit="per_person",
    ...                  contact_hours=1, evidence="fetched") for i, p in enumerate([40, 50, 60, 70, 80])]
    >>> position(65, cs).verdict, position(65, cs).median
    ('within market', 60.0)
    """
    fx = {currency: 1.0, **(fx or {})}
    fn = METRICS[metric] if isinstance(metric, str) else metric
    used = []
    for c in comparables:
        v = fn(c)
        if v is None or c.currency not in fx:
            continue
        used.append((c.id, v * fx[c.currency], c.weight))
    if not used:
        return None
    pairs = [(v, w) for _, v, w in used]
    below = sum(w for v, w in pairs if v <= value)
    return Position(
        value=value,
        n=len(used),
        q10=_wquantile(pairs, 0.10),
        median=_wquantile(pairs, 0.5),
        q90=_wquantile(pairs, 0.90),
        percentile=below / sum(w for _, w in pairs),
        used=tuple((i, round(v, 2)) for i, v, _ in used),
    )


def summary(values: Sequence[float]) -> dict:
    """Plain (unweighted) summary, for a quick look at a list of numbers."""
    return {"n": len(values), "median": statistics.median(values), "min": min(values), "max": max(values)}
