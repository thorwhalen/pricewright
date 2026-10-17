# pricewright.ratecard

Consistency across a whole rate card.

A single price can be defended on its own and still be absurd next to its
neighbours (the 10,000 talk next to a 6,000 private day). These checks look at
the card as a whole. Each returns [`Finding`](#pricewright.ratecard.Finding) objects; [`check_card()`](#pricewright.ratecard.check_card)
runs them all. A check is any `Callable[[Sequence[Quote]], Iterable[Finding]]`,
so a specialty can add its own (`checks=`).

Families: offerings that are the same content sold differently (open vs private,
online vs on site, single vs pack) share `Offering.family`.

### Functions

| [`check_card`](#pricewright.ratecard.check_card)(quotes, \*[, checks])               | Run every check over a card; errors first.                                                                                                                                          |
|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`dominance`](#pricewright.ratecard.dominance)(quotes, \*[, slack, fewer])          | An offering that needs clearly fewer hours of work (at most `fewer` x) and no more contact hours than another must not cost more in total (group, event, project or session units). |
| [`effective_rate_spread`](#pricewright.ratecard.effective_rate_spread)(quotes, \*[, tolerance]) | Every offering should pay the people about the same per hour actually worked.                                                                                                       |
| [`online_vs_onsite`](#pricewright.ratecard.online_vs_onsite)(quotes)                       | Within a family and unit, the online version should not cost more than the on-site one.                                                                                             |
| [`private_vs_seats`](#pricewright.ratecard.private_vs_seats)(quotes)                       | A private group should never cost more than buying every seat of the open version.                                                                                                  |
| [`volume_per_hour`](#pricewright.ratecard.volume_per_hour)(quotes, \*[, slack])           | Within a family and unit, more contact hours should not cost more per hour (packs, longer formats).                                                                                 |

### Classes

| [`Finding`](#pricewright.ratecard.Finding)(check, severity, message[, offerings])   |    |
|---------------------------------------------------------------------------------------------------|----|

### *class* pricewright.ratecard.Finding(check, severity, message, offerings=())

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

### pricewright.ratecard.check_card(quotes, \*, checks=(<function effective_rate_spread>, <function dominance>, <function private_vs_seats>, <function online_vs_onsite>, <function volume_per_hour>))

Run every check over a card; errors first.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Finding`](#pricewright.ratecard.Finding)]

### pricewright.ratecard.dominance(quotes, , slack=0.05, fewer=0.9)

An offering that needs clearly fewer hours of work (at most `fewer` x) and no more
contact hours than another must not cost more in total (group, event, project or session units).

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Finding`](#pricewright.ratecard.Finding)]

### pricewright.ratecard.effective_rate_spread(quotes, , tolerance=0.2)

Every offering should pay the people about the same per hour actually worked.

Compares each offering’s effective hourly rate (net of fees and costs, per hour
including prep and admin) to its target; flags those more than `tolerance`
away from the card’s median ratio. Deliberate positioning shows up here too,
which is the point: a discount should be visible as a choice.

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Finding`](#pricewright.ratecard.Finding)]

### pricewright.ratecard.online_vs_onsite(quotes)

Within a family and unit, the online version should not cost more than the on-site one.

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Finding`](#pricewright.ratecard.Finding)]

### pricewright.ratecard.private_vs_seats(quotes)

A private group should never cost more than buying every seat of the open version.

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Finding`](#pricewright.ratecard.Finding)]

### pricewright.ratecard.volume_per_hour(quotes, , slack=0.1)

Within a family and unit, more contact hours should not cost more per hour (packs, longer formats).

* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`Finding`](#pricewright.ratecard.Finding)]
