# pricewright.model

The cost-and-effort model: from an [`Offering`](pricewright.base.html.md#pricewright.base.Offering) to a price.

The formula, per run of the offering:

```default
labour   = sum(hours x hourly rate)        # development hours / amortize_runs,
                                           # participant hours x participants
direct   = sum(third-party costs, with markup)
base     = (labour + direct) x (1 + contingency)
net      = base / (1 - margin)             # margin is a share of the price
revenue  = (net + fixed fees x transactions) / (1 - fees_pct)
revenue *= positioning                     # a stated launch discount or premium
unit price = revenue / participants_expected   (open, per-person sales)
           = revenue                          (everything else)
```

then the unit price is rounded (`rounder=`) and every metric (effective rate per
hour worked, price per contact hour, break-even seats) is recomputed from the
*rounded* price, so the rationale describes the number actually printed.

### Functions

| [`price`](#pricewright.model.price)(offering[, rates, rounder])   | Price one offering from its effort and costs.   |
|--------------------------------------------------------------------------------------|-------------------------------------------------|

### Classes

| [`Line`](#pricewright.model.Line)(label, kind, amount[, hours, role])    | One row of a quote's breakdown, already per run.                    |
|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| [`Quote`](#pricewright.model.Quote)(offering, rates, labour, direct, ...) | A priced offering, with the full arithmetic kept for the rationale. |

### *class* pricewright.model.Line(label, kind, amount, hours=0.0, role='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

One row of a quote’s breakdown, already per run.

### *class* pricewright.model.Quote(offering, rates, labour, direct, labour_total, direct_total, contingency_amount, margin_amount, fees_amount, revenue_raw, unit_price_raw, unit_price, revenue, hours_total, hours_by_role=dict())

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

### pricewright.model.price(offering, rates=None, \*, rounder=<function nice_round>)

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
  [`Quote`](#pricewright.model.Quote)
