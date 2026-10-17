# pricewright.rounding

Rounding a computed price to a number a person would print on a rate card.

A computed 2,083.47 is not a price. The default rounds to a step that grows with
the magnitude, so small prices stay precise and large ones look deliberate.
Any `Callable[[float], float]` can replace it (the `rounder=` seam).

### Functions

| [`nice_round`](#pricewright.rounding.nice_round)(x, \*[, steps, up])   | Round `x` to a magnitude-dependent step.                       |
|-----------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`no_round`](#pricewright.rounding.no_round)(x)                      | The identity rounder, for inspecting the raw cost-plus figure. |

### pricewright.rounding.nice_round(x, , steps=((100, 5), (1000, 10), (5000, 50), (20000, 100), (100000, 500), (inf, 1000)), up=False)

Round `x` to a magnitude-dependent step.

```pycon
>>> nice_round(2083.47)
2100
>>> nice_round(437)
440
>>> nice_round(437, up=True)
440
>>> nice_round(431, up=True)
440
>>> nice_round(87.2)
85
```

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)

### pricewright.rounding.no_round(x)

The identity rounder, for inspecting the raw cost-plus figure.

* **Return type:**
  [`float`](https://docs.python.org/3/builtins/functions.html#float)
