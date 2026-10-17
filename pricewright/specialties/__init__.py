"""Specialties: one module per kind of offering, found through a registry.

A :class:`Specialty` is data: its offering *templates* (functions with keyword-only
defaults that return an :class:`~pricewright.base.Offering`), the research it needs
(so an agent can ask for it or run it), how its prices are compared to the market,
and any rate-card checks of its own.

Adding a specialty is one module that ends with ``register(Specialty(...))`` and one
line in ``_BUILTIN`` below (or a call to :func:`register` from your own code).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Callable, Mapping

from pricewright.base import Offering
from pricewright.ratecard import Check

Template = Callable[..., Offering]


@dataclass(frozen=True)
class MarketRef:
    """How a template's price is compared with a research packet."""

    metric: str  # a key of pricewright.research.METRICS
    offerings: tuple[str, ...]  # packet `offering` labels that are like-for-like (empty: any)
    units: tuple[str, ...] = ()
    value: str = "per_person_contact_hour"  # the Quote attribute compared
    # optional: (comparable, offering) -> comparable's value in the Quote's terms, or None to skip.
    # Use when like-for-like depends on the offering itself (style, runtime band).
    match: Callable | None = None


@dataclass(frozen=True)
class Specialty:
    name: str
    title: str
    description: str
    templates: Mapping[str, Template]
    research_needs: tuple[str, ...] = ()
    market: Mapping[str, MarketRef] = field(default_factory=dict)
    checks: tuple[Check, ...] = ()
    defaults: Mapping[str, object] = field(default_factory=dict)


_REGISTRY: dict[str, Specialty] = {}
_BUILTIN = ("training", "av_production", "software")


def register(specialty: Specialty) -> Specialty:
    _REGISTRY[specialty.name] = specialty
    return specialty


def _load_builtins():
    for name in _BUILTIN:
        if name not in _REGISTRY:
            importlib.import_module(f"pricewright.specialties.{name}")


def specialties() -> Mapping[str, Specialty]:
    """All registered specialties, by name."""
    _load_builtins()
    return dict(_REGISTRY)


def get_specialty(name: str) -> Specialty:
    _load_builtins()
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(f"No specialty {name!r}. Registered: {sorted(_REGISTRY)}") from None


def template(specialty: str, name: str) -> Template:
    s = get_specialty(specialty)
    try:
        return s.templates[name]
    except KeyError:
        raise KeyError(f"Specialty {specialty!r} has no template {name!r}. Templates: {sorted(s.templates)}") from None
