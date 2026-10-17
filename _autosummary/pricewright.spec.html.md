# pricewright.spec

A rate card as data: one YAML spec in, priced and checked card out.

The spec names the provider’s rates, the offerings (each a specialty template plus
parameters), the research packets to compare against, travel scenarios, and the day
rates to test for sensitivity. [`build_card()`](#pricewright.spec.build_card) does the rest. Everything a user
must decide sits in the spec, never in code.

Minimal spec:

```default
title: My rate card
rates: {day_rates: {founder: 900}}
offerings:
  - {id: talk, specialty: training, template: talk}
```

### Functions

| [`build_card`](#pricewright.spec.build_card)(spec, \*[, rounder])     | Price, check, position and stress-test every offering of a spec.                        |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `load_spec`(path)                                                                    |                                                                                         |
| [`make_offering`](#pricewright.spec.make_offering)(item, \*[, defaults]) | Build one offering from a spec item: `{specialty, template, params, positioning, ...}`. |

### Classes

| [`Card`](#pricewright.spec.Card)(title, spec, rates, entries, findings)   |    |
|------------------------------------------------------------------------------------------------|----|
| [`Entry`](#pricewright.spec.Entry)(id, specialty, template, quote[, ...])  |    |

### *class* pricewright.spec.Card(title, spec, rates, entries, findings, travel=(), sensitivity=dict())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.spec.Entry(id, specialty, template, quote, position=None, rationale='', market_value='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### pricewright.spec.build_card(spec, \*, rounder=<function nice_round>)

Price, check, position and stress-test every offering of a spec.

* **Return type:**
  [`Card`](#pricewright.spec.Card)

### pricewright.spec.make_offering(item, , defaults={})

Build one offering from a spec item: `{specialty, template, params, positioning, ...}`.

* **Return type:**
  [`Offering`](pricewright.base.html.md#pricewright.base.Offering)
