"""The cost-and-effort model: from an :class:`~pricewright.base.Offering` to a price.

The formula, per run of the offering::

    labour   = sum(hours x hourly rate)        # development hours / amortize_runs,
                                               # participant hours x participants
    direct   = sum(third-party costs, with markup)
    base     = (labour + direct) x (1 + contingency)
    net      = base / (1 - margin)             # margin is a share of the price
    revenue  = (net + fixed fees x transactions) / (1 - fees_pct)
    revenue *= positioning                     # a stated launch discount or premium
    unit price = revenue / participants_expected   (open, per-person sales)
               = revenue                          (everything else)

then the unit price is rounded (``rounder=``) and every metric (effective rate per
hour worked, price per contact hour, break-even seats) is recomputed from the
*rounded* price, so the rationale describes the number actually printed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from pricewright.base import Offering, Rates
from pricewright.rounding import Rounder, nice_round


@dataclass(frozen=True)
class Line:
    """One row of a quote's breakdown, already per run."""

    label: str
    kind: str
    amount: float
    hours: float = 0.0
    role: str = ""


@dataclass(frozen=True)
class Quote:
    """A priced offering, with the full arithmetic kept for the rationale."""

    offering: Offering
    rates: Rates
    labour: tuple[Line, ...]
    direct: tuple[Line, ...]
    labour_total: float
    direct_total: float
    contingency_amount: float
    margin_amount: float
    fees_amount: float
    revenue_raw: float
    unit_price_raw: float
    unit_price: float
    revenue: float
    hours_total: float
    hours_by_role: Mapping[str, float] = field(default_factory=dict)

    # --- metrics computed from the rounded price ---------------------------------
    @property
    def fees_at_price(self) -> float:
        o = self.offering
        return self.revenue * o.fees_pct + o.fees_fixed_per_txn * o.transactions

    @property
    def earned_for_labour(self) -> float:
        """What is left for the people after fees and third-party costs."""
        return self.revenue - self.fees_at_price - self.direct_total

    @property
    def effective_hourly(self) -> float:
        """Revenue net of fees and costs, per hour actually worked (all roles)."""
        return self.earned_for_labour / self.hours_total if self.hours_total else float("nan")

    @property
    def effective_day(self) -> float:
        return self.effective_hourly * self.rates.hours_per_day

    @property
    def target_hourly(self) -> float:
        """The hours-weighted target hourly rate of the roles involved."""
        if not self.hours_total:
            return float("nan")
        return sum(h * self.rates.hourly(r) for r, h in self.hours_by_role.items()) / self.hours_total

    @property
    def priced_hourly(self) -> float:
        """What a fully priced hour should earn: target rate with contingency and margin."""
        o = self.offering
        return self.target_hourly * (1 + o.contingency) / (1 - o.margin)

    @property
    def rate_ratio(self) -> float:
        """Effective hourly over fully priced hourly: 1.0 means priced exactly by the model."""
        return self.effective_hourly / self.priced_hourly if self.hours_total else float("nan")

    @property
    def per_contact_hour(self) -> float:
        """Revenue per delivered hour, for the whole room."""
        ch = self.offering.contact_hours
        return self.revenue / ch if ch else float("nan")

    @property
    def per_person_contact_hour(self) -> float:
        o = self.offering
        if not o.contact_hours:
            return float("nan")
        return self.revenue / (o.contact_hours * o.participants_expected)

    @property
    def per_finished_minute(self) -> float:
        d = self.offering.duration_s
        return self.revenue / (d / 60) if d else float("nan")

    @property
    def prep_ratio(self) -> float:
        """Hours worked per contact hour (the 'iceberg' ratio)."""
        ch = self.offering.contact_hours
        return self.hours_total / ch if ch else float("nan")

    @property
    def break_even_participants(self) -> float | None:
        """Seats needed at the printed price to cover cost plus contingency (no margin)."""
        o = self.offering
        if o.unit != "per_person":
            return None
        n = o.participants_expected
        c = 1 + o.contingency
        variable = sum(ln.amount for ln in self.labour + self.direct if ln.kind.endswith("@participant")) / n
        fixed = (self.labour_total + self.direct_total) - variable * n
        per_seat_net = self.unit_price * (1 - o.fees_pct) - o.fees_fixed_per_txn - variable * c
        return fixed * c / per_seat_net if per_seat_net > 0 else float("inf")


def _scale(per: str, *, offering: Offering) -> float:
    if per == "run":
        return 1.0
    if per == "participant":
        return float(offering.participants_expected)
    if per == "development":
        return 1.0 / offering.amortize_runs
    raise ValueError(f"Unknown basis per={per!r}; use run, participant or development")


def _kind(kind: str, per: str) -> str:
    # tag participant-scaled lines so break-even can separate fixed from variable
    return f"{kind}@participant" if per == "participant" else kind


def price(offering: Offering, rates: Rates | None = None, *, rounder: Rounder = nice_round) -> Quote:
    """Price one offering from its effort and costs.

    >>> from pricewright.base import Effort
    >>> o = Offering("1:1 session", "training", "per_session", contact_hours=1,
    ...              efforts=(Effort("session", 1), Effort("notes", 0.5, kind="prep")),
    ...              contingency=0, margin=0)
    >>> q = price(o, Rates({"founder": 700}))
    >>> q.unit_price, round(q.effective_hourly)
    (150, 100)
    """
    rates = rates or Rates()
    o = offering
    labour, hours_by_role = [], {}
    for e in o.efforts:
        h = e.hours * _scale(e.per, offering=o)
        labour.append(Line(e.label, _kind(e.kind, e.per), h * rates.hourly(e.role), hours=h, role=e.role))
        hours_by_role[e.role] = hours_by_role.get(e.role, 0.0) + h
    direct = [
        Line(c.label, _kind(c.kind, c.per), c.amount * (1 + c.markup) * _scale(c.per, offering=o))
        for c in o.costs
    ]
    labour_total = sum(ln.amount for ln in labour)
    direct_total = sum(ln.amount for ln in direct)
    base = (labour_total + direct_total) * (1 + o.contingency)
    net = base / (1 - o.margin)
    revenue_raw = (net + o.fees_fixed_per_txn * o.transactions) / (1 - o.fees_pct) * o.positioning
    qty = o.participants_expected if o.unit == "per_person" else 1
    unit_raw = revenue_raw / qty
    unit = rounder(unit_raw)
    return Quote(
        offering=o,
        rates=rates,
        labour=tuple(labour),
        direct=tuple(direct),
        labour_total=labour_total,
        direct_total=direct_total,
        contingency_amount=base - labour_total - direct_total,
        margin_amount=net - base,
        fees_amount=revenue_raw / o.positioning - net,
        revenue_raw=revenue_raw,
        unit_price_raw=unit_raw,
        unit_price=unit,
        revenue=unit * qty,
        hours_total=sum(hours_by_role.values()),
        hours_by_role=hours_by_role,
    )
