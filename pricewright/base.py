"""The data model of a price: who works how long, what it costs, and on what terms.

Everything here is a frozen dataclass, so an offering is a value you can build,
compare, serialise and re-price. The arithmetic lives in :mod:`pricewright.model`.

Vocabulary:

- an :class:`Effort` line is hours of one role, spent per *run* of the offering,
  per *participant*, or once for *development* (amortised over the expected runs);
- a :class:`Cost` line is money paid to someone else (credits, venue, materials),
  with the same three bases;
- an :class:`Offering` bundles them with the commercial frame: unit of sale,
  delivery mode, contact hours, seats, fees, contingency and margin;
- :class:`Rates` holds the provider's own economics (the day rate per role).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Literal

Per = Literal["run", "participant", "development"]
Unit = Literal["per_person", "per_group", "per_event", "per_project", "per_pack", "per_month", "per_session"]
Delivery = Literal["online", "onsite", "recorded", "n/a"]

DFLT_HOURS_PER_DAY = 7.0
DFLT_CURRENCY = "EUR"


@dataclass(frozen=True)
class Rates:
    """The provider's target rates: what one day of each role must earn.

    >>> r = Rates({"founder": 910})
    >>> r.hourly("founder")
    130.0
    """

    day_rates: Mapping[str, float] = field(default_factory=lambda: {"founder": 900.0})
    hours_per_day: float = DFLT_HOURS_PER_DAY
    currency: str = DFLT_CURRENCY

    def hourly(self, role: str) -> float:
        try:
            return self.day_rates[role] / self.hours_per_day
        except KeyError:
            raise KeyError(
                f"No day rate for role {role!r}. Known roles: {sorted(self.day_rates)}. "
                "Add it to Rates(day_rates={...})."
            ) from None


def day_rate_from_income(
    target_annual_income: float,
    *,
    billable_days: float = 110,
    annual_overhead: float = 0.0,
    social_charges_rate: float = 0.0,
) -> float:
    """The day rate that pays a target income, given how many days are really billed.

    A freelancer or a two-person studio bills far fewer days than it works: selling,
    admin, development and gaps eat the rest. ``billable_days`` is that real number,
    not 220.

    >>> round(day_rate_from_income(60_000, billable_days=100, annual_overhead=10_000))
    700
    """
    gross_needed = target_annual_income * (1 + social_charges_rate) + annual_overhead
    return gross_needed / billable_days


@dataclass(frozen=True)
class Effort:
    """Hours of one role. ``per`` says what the hours scale with."""

    label: str
    hours: float
    role: str = "founder"
    per: Per = "run"
    kind: str = "delivery"  # development | prep | delivery | feedback | admin | travel | production


@dataclass(frozen=True)
class Cost:
    """Money paid out to a third party. ``markup`` is added on top when re-billed."""

    label: str
    amount: float
    per: Per = "run"
    kind: str = "materials"  # tools | credits | venue | materials | catering | licence | subcontract
    markup: float = 0.0


@dataclass(frozen=True)
class Offering:
    """One thing on a rate card, described by its inputs, not by its price."""

    name: str
    specialty: str
    unit: Unit
    delivery: Delivery = "online"
    contact_hours: float = 0.0
    duration_s: float | None = None  # finished runtime, for productions
    participants_expected: int = 1
    participants_cap: int | None = None
    efforts: tuple[Effort, ...] = ()
    costs: tuple[Cost, ...] = ()
    amortize_runs: float = 1.0
    fees_pct: float = 0.0
    fees_fixed_per_txn: float = 0.0
    contingency: float = 0.10
    margin: float = 0.10
    positioning: float = 1.0  # deliberate multiplier over cost-plus (launch discount < 1, premium > 1)
    family: str = ""  # offerings sharing a family are compared online vs onsite, open vs private
    includes: tuple[str, ...] = ()
    terms: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self):
        if not 0 <= self.margin < 1:
            raise ValueError(f"{self.name}: margin is a share of the price, in [0, 1); got {self.margin}")
        if not 0 <= self.fees_pct < 1:
            raise ValueError(f"{self.name}: fees_pct must be in [0, 1); got {self.fees_pct}")
        if self.amortize_runs <= 0:
            raise ValueError(f"{self.name}: amortize_runs must be > 0; got {self.amortize_runs}")
        if self.participants_expected < 1:
            raise ValueError(f"{self.name}: participants_expected must be >= 1")

    def with_(self, **changes) -> Offering:
        """A copy with some fields changed (``dataclasses.replace``)."""
        return replace(self, **changes)

    @property
    def transactions(self) -> int:
        """How many payments one run produces: one per seat for open sales, else one."""
        return self.participants_expected if self.unit == "per_person" else 1
