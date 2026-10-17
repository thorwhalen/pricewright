"""Travel as explicit variables: time away, nights, subsistence, transport.

An on-site engagement costs the provider three things an online one does not:
**time** (travel hours that could have been billed elsewhere), **nights away**
(when the schedule cannot be done in a day), and **expenses** (transport, hotel,
meals). Industry practice quotes them separately from the professional fee, so a
client in the same city and a client a flight away see the same fee and a
different travel line. This module turns a :class:`Trip` into that line, under a
:class:`TravelPolicy` that holds the provider's terms.

Two ways of billing travel time are in common use, and both are offered:

- ``"hourly"``: door-to-door hours beyond a free allowance each way, billed at a
  fraction of the hourly rate (the default fraction is 0.5);
- ``"day_blocks"``: each travel leg rounded up to half or full days, billed at a
  fraction of the day rate (speakers and crews often quote a "travel day").

Expenses are passed through at cost by default (``expense_markup=0``), estimated
up front from the policy's hotel cap and per diem, and invoiced against receipts.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from pricewright.base import Rates
from pricewright.model import Line

TimeBilling = Literal["hourly", "day_blocks"]


@dataclass(frozen=True)
class TravelPolicy:
    """The provider's travel terms. Defaults follow the research packet
    (``travel-practice.md``: APA crew terms, URSSAF, speaker bureaus, consultancies)."""

    free_hours_each_way: float = 1.0  # first hour of each leg absorbed (APA, Talan)
    time_billing: TimeBilling = "hourly"
    time_rate_fraction: float = 0.5  # travel paid at half rate (seen 0 to 1.0)
    travel_day_min_hours: float = 4.0  # a travel-only day pays at least this (IATSE 4 h, APA 5 h)
    travel_day_cap_fraction: float = 0.5  # ... and at most this share of a day rate
    half_day_hours: float = 3.5  # "day_blocks": legs up to this are half a day
    overnight_threshold_hours: float = 1.5  # one-way; above it a morning start means the night before
    same_day_latest_start: float = 11.0  # starts before 11:00 need the night before (above the threshold)
    max_travel_same_day_hours: float = 4.0  # never more than this of travel on a working day
    no_work_flight_hours: float = 8.0  # longer trips add a rest night on arrival
    hotel_per_night: float = 140.0  # cap per traveller; city tiers override per Trip
    per_diem: float = 45.0  # meals per traveller per day away (two URSSAF meals ~ 43)
    per_night_fee: float = 0.0  # optional fee for each night away from home
    expense_markup: float = 0.0  # handling on re-billed expenses (0 = at cost; seen up to 15%)
    role: str = "founder"


@dataclass(frozen=True)
class Trip:
    """One engagement's travel, as the provider would estimate it before quoting."""

    one_way_hours: float  # door to door
    transport_round_trip: float = 0.0  # per traveller, estimated, at cost
    working_days: int = 1
    travellers: int = 1
    start_hour: float = 9.5
    end_hour: float = 17.5
    hotel_per_night: float | None = None  # overrides the policy (city tier)
    local_transport: float = 0.0  # taxis, parking, per traveller for the whole trip


@dataclass(frozen=True)
class TravelQuote:
    trip: Trip
    policy: TravelPolicy
    nights: int
    days_away: int
    billable_travel_hours: float
    lines: tuple[Line, ...] = field(default_factory=tuple)

    @property
    def time_fee(self) -> float:
        return sum(ln.amount for ln in self.lines if ln.kind == "travel_time")

    @property
    def expenses(self) -> float:
        return sum(ln.amount for ln in self.lines if ln.kind != "travel_time")

    @property
    def total(self) -> float:
        return self.time_fee + self.expenses


def nights_needed(trip: Trip, policy: TravelPolicy = TravelPolicy()) -> tuple[bool, bool, int]:
    """(night before, night after, total nights) for a trip under a policy.

    >>> nights_needed(Trip(one_way_hours=1))
    (False, False, 0)
    >>> nights_needed(Trip(one_way_hours=2))
    (True, False, 1)
    >>> nights_needed(Trip(one_way_hours=2, start_hour=11.5))
    (False, False, 0)
    >>> nights_needed(Trip(one_way_hours=5, working_days=2))
    (True, True, 3)
    """
    t, p = trip.one_way_hours, policy
    before = (trip.start_hour < p.same_day_latest_start and t > p.overnight_threshold_hours) or t > p.max_travel_same_day_hours
    after = t > p.max_travel_same_day_hours
    rest = int(t > p.no_work_flight_hours)
    between = max(trip.working_days - 1, 0)
    return before, after, int(before) + int(after) + between + rest


def _leg_fee(hours: float, *, travel_only_day: bool, policy: TravelPolicy, rates: Rates) -> tuple[float, float]:
    """(billable hours, fee) for one leg of one traveller."""
    p = policy
    hourly = rates.hourly(p.role)
    day = hourly * rates.hours_per_day
    if hours <= p.free_hours_each_way:
        return 0.0, 0.0
    if p.time_billing == "day_blocks":
        days = 0.5 if hours <= p.half_day_hours else math.ceil(hours / rates.hours_per_day)
        return days * rates.hours_per_day, days * day * p.time_rate_fraction
    if p.time_billing != "hourly":
        raise ValueError(f"Unknown time_billing={p.time_billing!r}; use 'hourly' or 'day_blocks'")
    if travel_only_day:
        h = max(p.travel_day_min_hours, hours)
        return h, min(h * hourly * p.time_rate_fraction, p.travel_day_cap_fraction * day)
    h = hours - p.free_hours_each_way
    return h, h * hourly * p.time_rate_fraction


def travel_addon(trip: Trip, *, policy: TravelPolicy = TravelPolicy(), rates: Rates | None = None) -> TravelQuote:
    """The travel line of a quote: time fee plus estimated expenses.

    >>> q = travel_addon(Trip(one_way_hours=3, transport_round_trip=120),
    ...                  rates=Rates({"founder": 700}))
    >>> q.nights, q.billable_travel_hours, round(q.time_fee)
    (1, 6.0, 300)
    """
    rates = rates or Rates()
    before, after, nights = nights_needed(trip, policy)
    local = trip.one_way_hours <= policy.free_hours_each_way
    days_away = 0 if local else trip.working_days + int(before) + int(after)
    n = trip.travellers
    out_h, out_fee = _leg_fee(trip.one_way_hours, travel_only_day=before, policy=policy, rates=rates)
    back_h, back_fee = _leg_fee(trip.one_way_hours, travel_only_day=after, policy=policy, rates=rates)
    hotel = trip.hotel_per_night if trip.hotel_per_night is not None else policy.hotel_per_night
    up = 1 + policy.expense_markup
    lines = [
        Line(f"travel time, {n} traveller(s), out {out_h:g} h + back {back_h:g} h billable at {policy.time_rate_fraction:.0%}", "travel_time", n * (out_fee + back_fee), hours=n * (out_h + back_h), role=policy.role),
        Line(f"transport, {n} x round trip (at cost)", "transport", n * trip.transport_round_trip * up),
        Line(f"hotel, {n} x {nights} night(s) at up to {hotel:g}", "hotel", n * nights * hotel * up),
        Line(f"per diem, {n} x {days_away} day(s) at {policy.per_diem:g}", "per_diem", n * days_away * policy.per_diem * up),
        Line(f"local transport, {n} x {trip.local_transport:g}", "local_transport", n * trip.local_transport * up),
    ]
    if policy.per_night_fee and nights:
        lines.append(Line(f"night-away fee, {n} x {nights}", "night_fee", n * nights * policy.per_night_fee))
    return TravelQuote(
        trip=trip,
        policy=policy,
        nights=nights,
        days_away=days_away,
        billable_travel_hours=n * (out_h + back_h),
        lines=tuple(ln for ln in lines if ln.amount),
    )
