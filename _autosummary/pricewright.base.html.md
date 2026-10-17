# pricewright.base

The data model of a price: who works how long, what it costs, and on what terms.

Everything here is a frozen dataclass, so an offering is a value you can build,
compare, serialise and re-price. The arithmetic lives in [`pricewright.model`](pricewright.model.html.md#module-pricewright.model).

Vocabulary:

- an [`Effort`](#pricewright.base.Effort) line is hours of one role, spent per *run* of the offering,
  per *participant*, or once for *development* (amortised over the expected runs);
- a [`Cost`](#pricewright.base.Cost) line is money paid to someone else (credits, venue, materials),
  with the same three bases;
- an [`Offering`](#pricewright.base.Offering) bundles them with the commercial frame: unit of sale,
  delivery mode, contact hours, seats, fees, contingency and margin;
- [`Rates`](#pricewright.base.Rates) holds the provider’s own economics (the day rate per role).

### Functions

| [`day_rate_from_income`](#pricewright.base.day_rate_from_income)(target_annual_income, \*)   | The day rate that pays a target income, given how many days are really billed.   |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|

### Classes

| [`Cost`](#pricewright.base.Cost)(label, amount[, per, kind, markup])         | Money paid out to a third party.                                     |
|---------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| [`Effort`](#pricewright.base.Effort)(label, hours[, role, per, kind])          | Hours of one role.                                                   |
| [`Offering`](#pricewright.base.Offering)(name, specialty, unit[, delivery, ...]) | One thing on a rate card, described by its inputs, not by its price. |
| [`Rates`](#pricewright.base.Rates)([day_rates, hours_per_day, currency])      | The provider's target rates: what one day of each role must earn.    |

### *class* pricewright.base.Cost(label, amount, per='run', kind='materials', markup=0.0)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Money paid out to a third party. `markup` is added on top when re-billed.

### *class* pricewright.base.Effort(label, hours, role='founder', per='run', kind='delivery')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Hours of one role. `per` says what the hours scale with.

### *class* pricewright.base.Offering(name, specialty, unit, delivery='online', contact_hours=0.0, duration_s=None, participants_expected=1, participants_cap=None, efforts=(), costs=(), amortize_runs=1.0, fees_pct=0.0, fees_fixed_per_txn=0.0, contingency=0.1, margin=0.1, positioning=1.0, family='', includes=(), terms=(), notes='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One thing on a rate card, described by its inputs, not by its price.

#### *property* transactions *: [int](https://docs.python.org/3/builtins/functions.html#int)*

one per seat for open sales, else one.

* **Type:**
  How many payments one run produces

#### with_(\*\*changes)

A copy with some fields changed (`dataclasses.replace`).

* **Return type:**
  [`Offering`](#pricewright.base.Offering)

### *class* pricewright.base.Rates(day_rates=<factory>, hours_per_day=7.0, currency='EUR')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

The provider’s target rates: what one day of each role must earn.

```pycon
>>> r = Rates({"founder": 910})
>>> r.hourly("founder")
130.0
```

### pricewright.base.day_rate_from_income(target_annual_income, , billable_days=110, annual_overhead=0.0, social_charges_rate=0.0)

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
