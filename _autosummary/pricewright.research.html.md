# pricewright.research

Market research as an input: comparables packets, normalised and compared.

Research is kept apart from the model on purpose. A packet is a YAML (or JSON)
list of comparable prices, gathered by an agent or supplied by the user, in the
schema below; it can be swapped or refreshed without touching any offering.
The model produces a cost-based price; a packet only tells you where that price
sits in the market ([`position()`](#pricewright.research.position)).

Schema (one record):

```default
id, specialty, offering, provider, region, price | price_low + price_high,
currency, unit, contact_hours, duration_s, group_size, delivery,
provider_tier, evidence (fetched | secondary | snippet | inferred), date, url, notes
```

### Functions

| [`as_is`](#pricewright.research.as_is)(c)                                        | The price in its own unit (use with a filter that fixes the unit).                         |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [`load_packet`](#pricewright.research.load_packet)(\*paths)                            | Read one or more packets.                                                                  |
| [`per_contact_hour`](#pricewright.research.per_contact_hour)(c)                             | Price per delivered hour for the whole room (group, event or session prices).              |
| `per_finished_minute`(c)                                                                         |                                                                                            |
| [`per_person_contact_hour`](#pricewright.research.per_person_contact_hour)(c)                      | Price per participant per delivered hour (needs hours, and a group size for group prices). |
| [`position`](#pricewright.research.position)(value, comparables, \*[, metric, ...]) | Locate `value` (already in `metric` units and `currency`) among comparables.               |
| `select`(comparables, \*[, specialty, ...])                                                      |                                                                                            |
| [`summary`](#pricewright.research.summary)(values)                                 | Plain (unweighted) summary, for a quick look at a list of numbers.                         |

### Classes

| [`Comparable`](#pricewright.research.Comparable)(id, specialty, offering[, price, ...])   |                                                                           |
|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| [`Position`](#pricewright.research.Position)(value, n, q10, median, q90, ...)           | Where a value sits among normalised comparables (in the target currency). |

### *class* pricewright.research.Comparable(id, specialty, offering, price=None, price_low=None, price_high=None, currency='EUR', unit='per_group', provider='', region='', contact_hours=None, duration_s=None, group_size=None, delivery='', provider_tier='', evidence='snippet', date='', url='', notes='')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### *class* pricewright.research.Position(value, n, q10, median, q90, percentile, used)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Where a value sits among normalised comparables (in the target currency).

### pricewright.research.as_is(c)

The price in its own unit (use with a filter that fixes the unit).

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float) | [`None`](https://docs.python.org/3/builtins/constants.html#None)

### pricewright.research.load_packet(\*paths)

Read one or more packets. Unknown keys are kept out, with no error.

Raises a `ValueError` naming the file and record when a record has no id,
specialty or offering, since such a record cannot be compared to anything.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Comparable`](#pricewright.research.Comparable)]

### pricewright.research.per_contact_hour(c)

Price per delivered hour for the whole room (group, event or session prices).

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float) | [`None`](https://docs.python.org/3/builtins/constants.html#None)

### pricewright.research.per_person_contact_hour(c)

Price per participant per delivered hour (needs hours, and a group size for group prices).

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float) | [`None`](https://docs.python.org/3/builtins/constants.html#None)

### pricewright.research.position(value, comparables, , metric='per_person_contact_hour', fx=None, currency='EUR')

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
  [`Position`](#pricewright.research.Position) | [`None`](https://docs.python.org/3/builtins/constants.html#None)

### pricewright.research.summary(values)

Plain (unweighted) summary, for a quick look at a list of numbers.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
