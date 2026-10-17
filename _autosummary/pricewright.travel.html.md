# pricewright.travel

Travel as explicit variables: time away, nights, subsistence, transport.

An on-site engagement costs the provider three things an online one does not:
**time** (travel hours that could have been billed elsewhere), **nights away**
(when the schedule cannot be done in a day), and **expenses** (transport, hotel,
meals). Industry practice quotes them separately from the professional fee, so a
client in the same city and a client a flight away see the same fee and a
different travel line. This module turns a [`Trip`](#pricewright.travel.Trip) into that line, under a
[`TravelPolicy`](#pricewright.travel.TravelPolicy) that holds the provider’s terms.

Two ways of billing travel time are in common use, and both are offered:

- `"hourly"`: door-to-door hours beyond a free allowance each way, billed at a
  fraction of the hourly rate (the default fraction is 0.5);
- `"day_blocks"`: each travel leg rounded up to half or full days, billed at a
  fraction of the day rate (speakers and crews often quote a “travel day”).

Expenses are passed through at cost by default (`expense_markup=0`), estimated
up front from the policy’s hotel cap and per diem, and invoiced against receipts.

### Functions

| [`nights_needed`](#pricewright.travel.nights_needed)(trip[, policy])           | (night before, night after, total nights) for a trip under a policy.   |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| [`travel_addon`](#pricewright.travel.travel_addon)(trip, \*[, policy, rates]) | The travel line of a quote: time fee plus estimated expenses.          |

### Classes

| [`TravelPolicy`](#pricewright.travel.TravelPolicy)([free_hours_each_way, ...])          | The provider's travel terms.                                               |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`TravelQuote`](#pricewright.travel.TravelQuote)(trip, policy, nights, days_away, ...) |                                                                            |
| [`Trip`](#pricewright.travel.Trip)(one_way_hours[, transport_round_trip, ...])  | One engagement's travel, as the provider would estimate it before quoting. |

### *class* pricewright.travel.TravelPolicy(free_hours_each_way=1.0, time_billing='hourly', time_rate_fraction=0.5, travel_day_min_hours=4.0, travel_day_cap_fraction=0.5, half_day_hours=3.5, overnight_threshold_hours=1.5, same_day_latest_start=11.0, max_travel_same_day_hours=4.0, no_work_flight_hours=8.0, hotel_per_night=140.0, per_diem=45.0, per_night_fee=0.0, expense_markup=0.0, role='founder')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The provider’s travel terms. Defaults follow the research packet
(`travel-practice.md`: APA crew terms, URSSAF, speaker bureaus, consultancies).

### *class* pricewright.travel.TravelQuote(trip, policy, nights, days_away, billable_travel_hours, lines=tuple())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.travel.Trip(one_way_hours, transport_round_trip=0.0, working_days=1, travellers=1, start_hour=9.5, end_hour=17.5, hotel_per_night=None, local_transport=0.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One engagement’s travel, as the provider would estimate it before quoting.

### pricewright.travel.nights_needed(trip, policy=None)

(night before, night after, total nights) for a trip under a policy.

```pycon
>>> nights_needed(Trip(one_way_hours=1))
(False, False, 0)
>>> nights_needed(Trip(one_way_hours=2))
(True, False, 1)
>>> nights_needed(Trip(one_way_hours=2, start_hour=11.5))
(False, False, 0)
>>> nights_needed(Trip(one_way_hours=5, working_days=2))
(True, True, 3)
```

* **Return type:**
  [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple)[[`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`bool`](https://docs.python.org/3/builtins/functions.html#bool), [`int`](https://docs.python.org/3/builtins/functions.html#int)]

### pricewright.travel.travel_addon(trip, , policy=None, rates=None)

The travel line of a quote: time fee plus estimated expenses.

```pycon
>>> q = travel_addon(Trip(one_way_hours=3, transport_round_trip=120),
...                  rates=Rates({"founder": 700}))
>>> q.nights, q.billable_travel_hours, round(q.time_fee)
(1, 6.0, 300)
```

* **Return type:**
  [`TravelQuote`](#pricewright.travel.TravelQuote)
