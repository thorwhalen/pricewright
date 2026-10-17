"""Consistency across a whole rate card.

A single price can be defended on its own and still be absurd next to its
neighbours (the 10,000 talk next to a 6,000 private day). These checks look at
the card as a whole. Each returns :class:`Finding` objects; :func:`check_card`
runs them all. A check is any ``Callable[[Sequence[Quote]], Iterable[Finding]]``,
so a specialty can add its own (``checks=``).

Families: offerings that are the same content sold differently (open vs private,
online vs on site, single vs pack) share ``Offering.family``.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Iterable, Iterator, Sequence

from pricewright.model import Quote


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str  # "error" (contradiction) | "warn" (worth a look) | "info"
    message: str
    offerings: tuple[str, ...] = ()


Check = Callable[[Sequence[Quote]], Iterable[Finding]]


def effective_rate_spread(quotes: Sequence[Quote], *, tolerance: float = 0.2) -> Iterator[Finding]:
    """Every offering should pay the people about the same per hour actually worked.

    Compares each offering's effective hourly rate (net of fees and costs, per hour
    including prep and admin) to its target; flags those more than ``tolerance``
    away from the card's median ratio. Deliberate positioning shows up here too,
    which is the point: a discount should be visible as a choice.
    """
    ratios = {q.offering.name: q.rate_ratio for q in quotes if q.hours_total}
    if len(ratios) < 2:
        return
    med = statistics.median(ratios.values())
    for name, r in ratios.items():
        if abs(r / med - 1) > tolerance:
            sev = "warn"
            yield Finding(
                "effective_rate_spread",
                sev,
                f"{name} earns {r:.0%} of its fully priced hourly rate; the card's median is {med:.0%}",
                (name,),
            )


def dominance(quotes: Sequence[Quote], *, slack: float = 0.05, fewer: float = 0.9) -> Iterator[Finding]:
    """An offering that needs clearly fewer hours of work (at most ``fewer`` x) and no more
    contact hours than another must not cost more in total (group, event, project or session units)."""
    group_like = [q for q in quotes if q.offering.unit in ("per_group", "per_event", "per_project", "per_pack", "per_session")]
    for a, b in combinations(group_like, 2):
        for small, big in ((a, b), (b, a)):
            so, bo = small.offering, big.offering
            if (
                so.contact_hours <= bo.contact_hours
                and small.hours_total <= big.hours_total * fewer
                and small.revenue > big.revenue * (1 + slack)
            ):
                yield Finding(
                    "dominance",
                    "error",
                    f"{so.name} ({so.contact_hours:g} h delivered, {small.hours_total:.0f} h worked) costs "
                    f"{small.revenue:,.0f}, more than {bo.name} ({bo.contact_hours:g} h, {big.hours_total:.0f} h) "
                    f"at {big.revenue:,.0f}",
                    (so.name, bo.name),
                )


def private_vs_seats(quotes: Sequence[Quote]) -> Iterator[Finding]:
    """A private group should never cost more than buying every seat of the open version."""
    by_family = _families(quotes)
    for fam, qs in by_family.items():
        opens = [q for q in qs if q.offering.unit == "per_person" and q.offering.participants_cap]
        privs = [q for q in qs if q.offering.unit == "per_group"]
        for o in opens:
            for p in privs:
                if p.offering.delivery != o.offering.delivery:
                    continue
                seats = o.unit_price * o.offering.participants_cap
                if p.revenue > seats:
                    yield Finding(
                        "private_vs_seats",
                        "error",
                        f"{p.offering.name} at {p.revenue:,.0f} costs more than all "
                        f"{o.offering.participants_cap} seats of {o.offering.name} ({seats:,.0f})",
                        (p.offering.name, o.offering.name),
                    )


def online_vs_onsite(quotes: Sequence[Quote]) -> Iterator[Finding]:
    """Within a family and unit, the online version should not cost more than the on-site one."""
    for fam, qs in _families(quotes).items():
        for a, b in combinations(qs, 2):
            if a.offering.unit != b.offering.unit or {a.offering.delivery, b.offering.delivery} != {"online", "onsite"}:
                continue
            if abs(a.offering.contact_hours - b.offering.contact_hours) > 0.25 * max(a.offering.contact_hours, b.offering.contact_hours):
                continue
            if a.offering.participants_cap != b.offering.participants_cap:
                continue
            on, off = (a, b) if a.offering.delivery == "online" else (b, a)
            if on.unit_price > off.unit_price:
                yield Finding(
                    "online_vs_onsite",
                    "error",
                    f"{on.offering.name} (online, {on.unit_price:,.0f}) costs more than "
                    f"{off.offering.name} (on site, {off.unit_price:,.0f})",
                    (on.offering.name, off.offering.name),
                )
            else:
                gap = 1 - on.unit_price / off.unit_price if off.unit_price else 0
                yield Finding(
                    "online_vs_onsite",
                    "info",
                    f"{on.offering.name} is {gap:.0%} below {off.offering.name} (before travel)",
                    (on.offering.name, off.offering.name),
                )


def volume_per_hour(quotes: Sequence[Quote], *, slack: float = 0.10) -> Iterator[Finding]:
    """Within a family and unit, more contact hours should not cost more per hour (packs, longer formats)."""
    for fam, qs in _families(quotes).items():
        for a, b in combinations(qs, 2):
            if a.offering.unit != b.offering.unit or a.offering.delivery != b.offering.delivery:
                continue
            short, long_ = sorted((a, b), key=lambda q: q.offering.contact_hours)
            if short.offering.contact_hours == long_.offering.contact_hours:
                continue
            if long_.per_contact_hour > short.per_contact_hour * (1 + slack):
                yield Finding(
                    "volume_per_hour",
                    "warn",
                    f"{long_.offering.name} costs {long_.per_contact_hour:,.0f}/h, more than the shorter "
                    f"{short.offering.name} at {short.per_contact_hour:,.0f}/h",
                    (long_.offering.name, short.offering.name),
                )


def _families(quotes: Sequence[Quote]) -> dict[str, list[Quote]]:
    out: dict[str, list[Quote]] = {}
    for q in quotes:
        if q.offering.family:
            out.setdefault(q.offering.family, []).append(q)
    return out


DFLT_CHECKS: tuple[Check, ...] = (effective_rate_spread, dominance, private_vs_seats, online_vs_onsite, volume_per_hour)


def check_card(quotes: Sequence[Quote], *, checks: Sequence[Check] = DFLT_CHECKS) -> list[Finding]:
    """Run every check over a card; errors first."""
    order = {"error": 0, "warn": 1, "info": 2}
    found = [f for chk in checks for f in chk(quotes)]
    return sorted(found, key=lambda f: order.get(f.severity, 3))
