# pricewright

pricewright: price services and products from a model of their costs and effort.

Simple things simple:

```default
>>> from pricewright import price, Rates
>>> from pricewright.specialties.training import talk
>>> q = price(talk(delivery="online"), Rates({"founder": 900}))
>>> q.unit_price > 0
True
```

A whole rate card, checked for consistency and compared with a market packet:

```default
from pricewright import load_spec, build_card, render
print(render(build_card(load_spec("card.yaml"))))
```

Layers: [`base`](pricewright.base.html.md#module-pricewright.base) (data), [`model`](pricewright.model.html.md#module-pricewright.model) (the arithmetic),
[`travel`](pricewright.travel.html.md#module-pricewright.travel) (on-site add-on), [`ratecard`](pricewright.ratecard.html.md#module-pricewright.ratecard) (card-wide
checks), [`research`](pricewright.research.html.md#module-pricewright.research) (market packets), [`specialties`](#pricewright.specialties)
(templates per kind of offering, in a registry), [`spec`](pricewright.spec.html.md#module-pricewright.spec) and
[`report`](pricewright.report.html.md#module-pricewright.report) (YAML in, Markdown out).

### Functions

| [`build_card`](#pricewright.build_card)(spec, \*[, rounder])                 | Price, check, position and stress-test every offering of a spec.                        |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [`check_card`](#pricewright.check_card)(quotes, \*[, checks])                | Run every check over a card; errors first.                                              |
| [`day_rate_from_income`](#pricewright.day_rate_from_income)(target_annual_income, \*)  | The day rate that pays a target income, given how many days are really billed.          |
| `get_specialty`(name)                                                                            |                                                                                         |
| [`load_packet`](#pricewright.load_packet)(\*paths)                            | Read one or more packets.                                                               |
| `load_spec`(path)                                                                                |                                                                                         |
| [`make_offering`](#pricewright.make_offering)(item, \*[, defaults])             | Build one offering from a spec item: `{specialty, template, params, positioning, ...}`. |
| [`position`](#pricewright.position)(value, comparables, \*[, metric, ...]) | Locate `value` (already in `metric` units and `currency`) among comparables.            |
| [`price`](#pricewright.price)(offering[, rates, rounder])               | Price one offering from its effort and costs.                                           |
| `register`(specialty)                                                                            |                                                                                         |
| `render`(card, \*[, intro])                                                                      |                                                                                         |
| [`specialties`](#pricewright.specialties)()                                   | All registered specialties, by name.                                                    |
| `template`(specialty, name)                                                                      |                                                                                         |
| [`travel_addon`](#pricewright.travel_addon)(trip, \*[, policy, rates])         | The travel line of a quote: time fee plus estimated expenses.                           |

### Classes

| [`Card`](#pricewright.Card)(title, spec, rates, entries, findings)       |                                                                            |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`Comparable`](#pricewright.Comparable)(id, specialty, offering[, price, ...]) |                                                                            |
| [`Cost`](#pricewright.Cost)(label, amount[, per, kind, markup])          | Money paid out to a third party.                                           |
| [`Effort`](#pricewright.Effort)(label, hours[, role, per, kind])           | Hours of one role.                                                         |
| [`Finding`](#pricewright.Finding)(check, severity, message[, offerings])    |                                                                            |
| [`Offering`](#pricewright.Offering)(name, specialty, unit[, delivery, ...])  | One thing on a rate card, described by its inputs, not by its price.       |
| [`Quote`](#pricewright.Quote)(offering, rates, labour, direct, ...)       | A priced offering, with the full arithmetic kept for the rationale.        |
| [`Rates`](#pricewright.Rates)([day_rates, hours_per_day, currency])       | The provider's target rates: what one day of each role must earn.          |
| [`Specialty`](#pricewright.Specialty)(name, title, description, templates)    |                                                                            |
| [`TravelPolicy`](#pricewright.TravelPolicy)([free_hours_each_way, ...])          | The provider's travel terms.                                               |
| [`Trip`](#pricewright.Trip)(one_way_hours[, transport_round_trip, ...])  | One engagement's travel, as the provider would estimate it before quoting. |

### *class* pricewright.Card(title, spec, rates, entries, findings, travel=(), sensitivity=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.Comparable(id, specialty, offering, price=None, price_low=None, price_high=None, currency='EUR', unit='per_group', provider='', region='', contact_hours=None, duration_s=None, group_size=None, delivery='', provider_tier='', evidence='snippet', date='', url='', notes='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.Cost(label, amount, per='run', kind='materials', markup=0.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Money paid out to a third party. `markup` is added on top when re-billed.

### *class* pricewright.Effort(label, hours, role='founder', per='run', kind='delivery')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Hours of one role. `per` says what the hours scale with.

### *class* pricewright.Finding(check, severity, message, offerings=())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.Offering(name, specialty, unit, delivery='online', contact_hours=0.0, duration_s=None, participants_expected=1, participants_cap=None, efforts=(), costs=(), amortize_runs=1.0, fees_pct=0.0, fees_fixed_per_txn=0.0, contingency=0.1, margin=0.1, positioning=1.0, family='', includes=(), terms=(), notes='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One thing on a rate card, described by its inputs, not by its price.

#### *property* transactions *: [int](https://docs.python.org/3/builtins/functions.html#int)*

one per seat for open sales, else one.

* **Type:**
  How many payments one run produces

#### with_(\*\*changes)

A copy with some fields changed (`dataclasses.replace`).

* **Return type:**
  [`Offering`](pricewright.base.html.md#pricewright.base.Offering)

### *class* pricewright.Quote(offering, rates, labour, direct, labour_total, direct_total, contingency_amount, margin_amount, fees_amount, revenue_raw, unit_price_raw, unit_price, revenue, hours_total, hours_by_role=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

A priced offering, with the full arithmetic kept for the rationale.

#### *property* break_even_participants *: [float](https://docs.python.org/3/builtins/functions.html#float) | [None](https://docs.python.org/3/builtins/constants.html#None)*

Seats needed at the printed price to cover cost plus contingency (no margin).

#### *property* earned_for_labour *: [float](https://docs.python.org/3/builtins/functions.html#float)*

What is left for the people after fees and third-party costs.

#### *property* effective_hourly *: [float](https://docs.python.org/3/builtins/functions.html#float)*

Revenue net of fees and costs, per hour actually worked (all roles).

#### *property* per_contact_hour *: [float](https://docs.python.org/3/builtins/functions.html#float)*

Revenue per delivered hour, for the whole room.

#### *property* prep_ratio *: [float](https://docs.python.org/3/builtins/functions.html#float)*

Hours worked per contact hour (the ‘iceberg’ ratio).

#### *property* priced_hourly *: [float](https://docs.python.org/3/builtins/functions.html#float)*

target rate with contingency and margin.

* **Type:**
  What a fully priced hour should earn

#### *property* rate_ratio *: [float](https://docs.python.org/3/builtins/functions.html#float)*

1.0 means priced exactly by the model.

* **Type:**
  Effective hourly over fully priced hourly

#### *property* target_hourly *: [float](https://docs.python.org/3/builtins/functions.html#float)*

The hours-weighted target hourly rate of the roles involved.

### *class* pricewright.Rates(day_rates=<factory>, hours_per_day=7.0, currency='EUR')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The provider’s target rates: what one day of each role must earn.

```pycon
>>> r = Rates({"founder": 910})
>>> r.hourly("founder")
130.0
```

### *class* pricewright.Specialty(name, title, description, templates, research_needs=(), market=dict(), checks=(), defaults=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.TravelPolicy(free_hours_each_way=1.0, time_billing='hourly', time_rate_fraction=0.5, travel_day_min_hours=4.0, travel_day_cap_fraction=0.5, half_day_hours=3.5, overnight_threshold_hours=1.5, same_day_latest_start=11.0, max_travel_same_day_hours=4.0, no_work_flight_hours=8.0, hotel_per_night=140.0, per_diem=45.0, per_night_fee=0.0, expense_markup=0.0, role='founder')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The provider’s travel terms. Defaults follow the research packet
(`travel-practice.md`: APA crew terms, URSSAF, speaker bureaus, consultancies).

### *class* pricewright.Trip(one_way_hours, transport_round_trip=0.0, working_days=1, travellers=1, start_hour=9.5, end_hour=17.5, hotel_per_night=None, local_transport=0.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One engagement’s travel, as the provider would estimate it before quoting.

### pricewright.build_card(spec, \*, rounder=<function nice_round>)

Price, check, position and stress-test every offering of a spec.

* **Return type:**
  [`Card`](pricewright.spec.html.md#pricewright.spec.Card)

### pricewright.check_card(quotes, \*, checks=(<function effective_rate_spread>, <function dominance>, <function private_vs_seats>, <function online_vs_onsite>, <function volume_per_hour>))

Run every check over a card; errors first.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Finding`](pricewright.ratecard.html.md#pricewright.ratecard.Finding)]

### pricewright.day_rate_from_income(target_annual_income, , billable_days=110, annual_overhead=0.0, social_charges_rate=0.0)

The day rate that pays a target income, given how many days are really billed.

A freelancer or a two-person studio bills far fewer days than it works: selling,
admin, development and gaps eat the rest. `billable_days` is that real number,
not 220.

```pycon
>>> round(day_rate_from_income(60_000, billable_days=100, annual_overhead=10_000))
700
```

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

### pricewright.load_packet(\*paths)

Read one or more packets. Unknown keys are kept out, with no error.

Raises a `ValueError` naming the file and record when a record has no id,
specialty or offering, since such a record cannot be compared to anything.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Comparable`](pricewright.research.html.md#pricewright.research.Comparable)]

### pricewright.make_offering(item, , defaults={})

Build one offering from a spec item: `{specialty, template, params, positioning, ...}`.

* **Return type:**
  [`Offering`](pricewright.base.html.md#pricewright.base.Offering)

### pricewright.position(value, comparables, , metric='per_person_contact_hour', fx=None, currency='EUR')

Locate `value` (already in `metric` units and `currency`) among comparables.

`fx` maps a currency to its value in `currency` (e.g. `{"USD": 0.87}` when
`currency='EUR'`). A comparable in a currency missing from `fx` is skipped
rather than silently treated as equal.

```pycon
>>> cs = [Comparable(str(i), "training", "x", price=p, unit="per_person",
...                  contact_hours=1, evidence="fetched") for i, p in enumerate([40, 50, 60, 70, 80])]
>>> position(65, cs).verdict, position(65, cs).median
('within market', 60.0)
```

* **Return type:**
  [`Position`](pricewright.research.html.md#pricewright.research.Position) | [`None`](https://docs.python.org/3/builtins/constants.html#None)

### pricewright.price(offering, rates=None, \*, rounder=<function nice_round>)

Price one offering from its effort and costs.

```pycon
>>> from pricewright.base import Effort
>>> o = Offering("1:1 session", "training", "per_session", contact_hours=1,
...              efforts=(Effort("session", 1), Effort("notes", 0.5, kind="prep")),
...              contingency=0, margin=0)
>>> q = price(o, Rates({"founder": 700}))
>>> q.unit_price, round(q.effective_hourly)
(150, 100)
```

* **Return type:**
  [`Quote`](pricewright.model.html.md#pricewright.model.Quote)

### pricewright.specialties()

All registered specialties, by name.

* **Return type:**
  [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str), [`Specialty`](#pricewright.Specialty)]

### pricewright.travel_addon(trip, , policy=None, rates=None)

The travel line of a quote: time fee plus estimated expenses.

```pycon
>>> q = travel_addon(Trip(one_way_hours=3, transport_round_trip=120),
...                  rates=Rates({"founder": 700}))
>>> q.nights, q.billable_travel_hours, round(q.time_fee)
(1, 6.0, 300)
```

* **Return type:**
  [`TravelQuote`](pricewright.travel.html.md#pricewright.travel.TravelQuote)

### Modules

| [`base`](pricewright.base.html.md#module-pricewright.base)         | The data model of a price: who works how long, what it costs, and on what terms.                                                   |
|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| [`model`](pricewright.model.html.md#module-pricewright.model)       | The cost-and-effort model: from an [`Offering`](pricewright.base.html.md#pricewright.base.Offering) to a price. |
| [`ratecard`](pricewright.ratecard.html.md#module-pricewright.ratecard) | Consistency across a whole rate card.                                                                                              |
| [`report`](pricewright.report.html.md#module-pricewright.report)     | Render a [`Card`](pricewright.spec.html.md#pricewright.spec.Card) as a Markdown rate card with its rationale.   |
| [`research`](pricewright.research.html.md#module-pricewright.research) | Market research as an input: comparables packets, normalised and compared.                                                         |
| [`rounding`](pricewright.rounding.html.md#module-pricewright.rounding) | Rounding a computed price to a number a person would print on a rate card.                                                         |
| [`spec`](pricewright.spec.html.md#module-pricewright.spec)         | A rate card as data: one YAML spec in, priced and checked card out.                                                                |
| [`travel`](pricewright.travel.html.md#module-pricewright.travel)     | Travel as explicit variables: time away, nights, subsistence, transport.                                                           |
