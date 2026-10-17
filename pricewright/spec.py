"""A rate card as data: one YAML spec in, priced and checked card out.

The spec names the provider's rates, the offerings (each a specialty template plus
parameters), the research packets to compare against, travel scenarios, and the day
rates to test for sensitivity. :func:`build_card` does the rest. Everything a user
must decide sits in the spec, never in code.

Minimal spec::

    title: My rate card
    rates: {day_rates: {founder: 900}}
    offerings:
      - {id: talk, specialty: training, template: talk}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from pricewright.base import Offering, Rates
from pricewright.model import Quote, price
from pricewright.ratecard import DFLT_CHECKS, Finding, check_card
from pricewright.research import Comparable, Position, load_packet, position, select
from pricewright.rounding import nice_round
from pricewright.specialties import get_specialty, template
from pricewright.travel import Trip, TravelPolicy, TravelQuote, travel_addon

_OFFERING_FIELDS = {"positioning", "contingency", "margin", "fees_pct", "fees_fixed_per_txn", "amortize_runs", "family", "terms", "includes", "notes"}


@dataclass(frozen=True)
class Entry:
    id: str
    specialty: str
    template: str
    quote: Quote
    position: Position | None = None
    rationale: str = ""
    market_value: str = ""  # which Quote attribute the position compares


@dataclass(frozen=True)
class Card:
    title: str
    spec: Mapping[str, Any]
    rates: Rates
    entries: tuple[Entry, ...]
    findings: tuple[Finding, ...]
    travel: tuple[tuple[str, TravelQuote], ...] = ()
    sensitivity: Mapping[float, Mapping[str, float]] = field(default_factory=dict)

    @property
    def quotes(self) -> list[Quote]:
        return [e.quote for e in self.entries]

    def __getitem__(self, entry_id: str) -> Entry:
        for e in self.entries:
            if e.id == entry_id:
                return e
        raise KeyError(f"No entry {entry_id!r}; entries: {[e.id for e in self.entries]}")


def load_spec(path: str | Path) -> dict:
    import yaml

    path = Path(path)
    spec = yaml.safe_load(path.read_text())
    spec.setdefault("_base_dir", str(path.parent))
    return spec


def _rates(spec: Mapping) -> Rates:
    r = spec.get("rates", {})
    return Rates(
        day_rates=r.get("day_rates", {"founder": 900.0}),
        hours_per_day=r.get("hours_per_day", 7.0),
        currency=spec.get("currency", "EUR"),
    )


def make_offering(item: Mapping, *, defaults: Mapping[str, Mapping] = {}) -> Offering:
    """Build one offering from a spec item: ``{specialty, template, params, positioning, ...}``."""
    tpl = template(item["specialty"], item["template"])
    params = dict(item.get("params", {}))
    sdefaults = defaults.get(item["specialty"])
    if sdefaults:
        params["defaults"] = {**sdefaults, **params.get("defaults", {})}
    if "name" in item:
        params["name"] = item["name"]
    o = tpl(**params)
    extra = {k: (tuple(v) if isinstance(v, list) else v) for k, v in item.items() if k in _OFFERING_FIELDS}
    return o.with_(**extra) if extra else o


BASELINE_PACKETS = Path(__file__).parent / "data" / "packets"


def _resolve_packet(p: str, base: Path) -> Path:
    """A packet path: absolute, relative to the spec, or the name of a baseline packet shipped here."""
    for cand in (Path(p), base / p, BASELINE_PACKETS / p):
        if cand.exists():
            return cand
    shipped = sorted(x.name for x in BASELINE_PACKETS.glob("*.yaml"))
    raise FileNotFoundError(f"No packet {p!r} next to the spec ({base}) or among the baseline packets {shipped}")


def _packets(spec: Mapping) -> list[Comparable]:
    m = spec.get("market") or {}
    base = Path(spec.get("_base_dir", "."))
    paths = [_resolve_packet(p, base) for p in m.get("packets", [])]
    return load_packet(*paths) if paths else []


def _position(quote: Quote, item: Mapping, comps: Sequence[Comparable], spec: Mapping) -> Position | None:
    if not comps:
        return None
    s = get_specialty(item["specialty"])
    ref = s.market.get(item["template"])
    if ref is None:
        return None
    over = item.get("market", {})
    exclude_ids = set(over.get("exclude_ids", ()))
    chosen = [c for c in (
        select(
            comps,
            specialty=s.name,
            offerings=over.get("offerings", ref.offerings),
            units=over.get("units", ref.units) or None,
            delivery=over.get("delivery"),
            exclude_tiers=over.get("exclude_tiers", spec.get("market", {}).get("exclude_tiers", ())),
        )
    ) if c.id not in exclude_ids]
    value = _quote_value(quote, over.get("value", ref.value))
    metric = over.get("metric", ref.metric)
    if ref.match is not None and "metric" not in over:
        metric = lambda c: ref.match(c, quote.offering)  # noqa: E731
    return position(value, chosen, metric=metric, fx=spec.get("market", {}).get("fx"), currency=quote.rates.currency)


def _value_attr(item: Mapping) -> str:
    ref = get_specialty(item["specialty"]).market.get(item["template"])
    return item.get("market", {}).get("value", ref.value if ref else "")


def _quote_value(quote: Quote, attr: str) -> float:
    return getattr(quote, attr)


def build_card(spec: Mapping, *, rounder=nice_round) -> Card:
    """Price, check, position and stress-test every offering of a spec."""
    rates = _rates(spec)
    defaults = spec.get("defaults", {})
    comps = _packets(spec)
    items = spec.get("offerings", [])
    entries = []
    for item in items:
        q = price(make_offering(item, defaults=defaults), rates, rounder=rounder)
        entries.append(
            Entry(item["id"], item["specialty"], item["template"], q, _position(q, item, comps, spec), item.get("rationale", ""), _value_attr(item))
        )
    extra_checks = tuple(c for name in dict.fromkeys(i["specialty"] for i in items) for c in get_specialty(name).checks)
    findings = check_card([e.quote for e in entries], checks=DFLT_CHECKS + extra_checks)
    travel = tuple(_travel(spec, rates))
    sens = {}
    for dr in spec.get("sensitivity", {}).get("day_rates", []):
        r = Rates({k: dr * v / rates.day_rates.get("founder", v) for k, v in rates.day_rates.items()}, rates.hours_per_day, rates.currency)
        sens[dr] = {item["id"]: price(make_offering(item, defaults=defaults), r, rounder=rounder).unit_price for item in items}
    return Card(spec.get("title", "Rate card"), spec, rates, tuple(entries), tuple(findings), travel, sens)


def _travel(spec: Mapping, rates: Rates):
    t = spec.get("travel") or {}
    policy = TravelPolicy(**t.get("policy", {}))
    for sc in t.get("scenarios", []):
        yield sc["name"], travel_addon(Trip(**sc["trip"]), policy=policy, rates=rates)
