"""Rounding a computed price to a number a person would print on a rate card.

A computed 2,083.47 is not a price. The default rounds to a step that grows with
the magnitude, so small prices stay precise and large ones look deliberate.
Any ``Callable[[float], float]`` can replace it (the ``rounder=`` seam).
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

Rounder = Callable[[float], float]

# (upper bound, step): prices below the bound round to the step.
DFLT_STEPS: tuple[tuple[float, float], ...] = (
    (100, 5),
    (1_000, 10),
    (5_000, 50),
    (20_000, 100),
    (100_000, 500),
    (math.inf, 1_000),
)


def nice_round(x: float, *, steps: Sequence[tuple[float, float]] = DFLT_STEPS, up: bool = False) -> float:
    """Round ``x`` to a magnitude-dependent step.

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
    """
    if x <= 0:
        return 0
    for bound, step in steps:
        if x < bound:
            q = x / step
            n = math.ceil(q - 1e-9) if up else round(q)
            return int(n * step) if float(step).is_integer() else n * step
    raise AssertionError("steps must end with an infinite bound")


def no_round(x: float) -> float:
    """The identity rounder, for inspecting the raw cost-plus figure."""
    return x
