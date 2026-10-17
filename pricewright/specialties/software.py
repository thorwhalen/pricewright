"""Software and apps: subscriptions, usage, credits, seats, freemium.

Software is priced on value with a cost *floor*, the reverse of services. The
calculator's job here is the floor and the unit economics; the strategy (value
metric, model, tiers, fences, tests) is the expert's job, from the reference
``references/software.md`` of the ``pricing-expert`` skill.

Floor rule: ``floor = variable cost per unit / (1 - target gross margin)``, before
payment fees, computed at the plan's *full* allowance (a user who uses everything
must still leave the target margin).
"""

from __future__ import annotations

from pricewright.base import Cost, Offering
from pricewright.specialties import MarketRef, Specialty, register

DEFAULTS: dict[str, float] = {
    "target_gross_margin": 0.60,  # AI products: aim for 50-60% at full allowance (ICONIQ, Bessemer)
    "fees_pct": 0.05,  # merchant of record (Paddle 5% + 0.50)
    "fees_fixed": 0.50,
    "annual_discount": 0.17,  # annual plans: 15-20% off the monthly price
}


def plan(
    *,
    name: str = "Plan",
    included_units: float = 0,
    cost_per_unit: float = 0.0,
    fixed_cost_per_user_month: float = 0.0,
    target_gross_margin: float | None = None,
    positioning: float = 1.0,
    defaults: dict | None = None,
    **overrides,
) -> Offering:
    """A monthly subscription plan priced at its gross-margin floor (then ``positioning`` for value).

    ``included_units`` of usage (credits, seconds, generations) at ``cost_per_unit``
    of inference, plus per-user fixed costs (hosting, support share).
    """
    D = {**DEFAULTS, **(defaults or {})}
    gm = D["target_gross_margin"] if target_gross_margin is None else target_gross_margin
    costs = (
        Cost(f"inference at full allowance ({included_units:g} units)", included_units * cost_per_unit, kind="cogs"),
        Cost("hosting and support per user", fixed_cost_per_user_month, kind="cogs"),
    )
    return Offering(
        name=name,
        specialty="software",
        unit="per_month",
        delivery="n/a",
        costs=costs,
        contingency=0.0,
        margin=gm,
        fees_pct=D["fees_pct"],
        fees_fixed_per_txn=D["fees_fixed"],
        positioning=positioning,
        family="software",
        **overrides,
    )


def credit_pack(*, credits: float, cost_per_credit: float, target_gross_margin: float | None = None, name: str | None = None, defaults: dict | None = None, **overrides) -> Offering:
    """A one-off top-up of credits, at the same floor rule."""
    D = {**DEFAULTS, **(defaults or {})}
    return plan(
        name=name or f"{credits:g} credits",
        included_units=credits,
        cost_per_unit=cost_per_credit,
        target_gross_margin=target_gross_margin,
        defaults=D,
        **overrides,
    ).with_(unit="per_project")


RESEARCH_NEEDS = (
    "Competitors' published plans: price, included usage or credits, seats, limits (fences).",
    "Inference / variable cost per unit of usage, by model, at current vendor prices.",
    "Customer segments and the value metric each perceives (interviews, Van Westendorp).",
    "Acquisition cost by channel, to set a floor from CAC payback.",
)

SPECIALTY = register(
    Specialty(
        name="software",
        title="Software and apps",
        description=__doc__.split("\n\n")[0],
        templates={"plan": plan, "credit_pack": credit_pack},
        research_needs=RESEARCH_NEEDS,
        market={"plan": MarketRef("as_is", (), units=("per_month", "per_seat_month"), value="unit_price")},
        defaults=DEFAULTS,
    )
)
