"""pricewright: price services and products from a model of their costs and effort.

Simple things simple::

    >>> from pricewright import price, Rates
    >>> from pricewright.specialties.training import talk
    >>> q = price(talk(delivery="online"), Rates({"founder": 900}))
    >>> q.unit_price > 0
    True

A whole rate card, checked for consistency and compared with a market packet::

    from pricewright import load_spec, build_card, render
    print(render(build_card(load_spec("card.yaml"))))

Layers: :mod:`~pricewright.base` (data), :mod:`~pricewright.model` (the arithmetic),
:mod:`~pricewright.travel` (on-site add-on), :mod:`~pricewright.ratecard` (card-wide
checks), :mod:`~pricewright.research` (market packets), :mod:`~pricewright.specialties`
(templates per kind of offering, in a registry), :mod:`~pricewright.spec` and
:mod:`~pricewright.report` (YAML in, Markdown out).
"""

from pricewright.base import Cost, Effort, Offering, Rates, day_rate_from_income
from pricewright.model import Quote, price
from pricewright.ratecard import Finding, check_card
from pricewright.report import render
from pricewright.research import Comparable, load_packet, position
from pricewright.spec import Card, build_card, load_spec, make_offering
from pricewright.specialties import Specialty, get_specialty, register, specialties, template
from pricewright.travel import TravelPolicy, Trip, travel_addon

__all__ = [
    "Card",
    "Comparable",
    "Cost",
    "Effort",
    "Finding",
    "Offering",
    "Quote",
    "Rates",
    "Specialty",
    "TravelPolicy",
    "Trip",
    "build_card",
    "check_card",
    "day_rate_from_income",
    "get_specialty",
    "load_packet",
    "load_spec",
    "make_offering",
    "position",
    "price",
    "register",
    "render",
    "specialties",
    "template",
    "travel_addon",
]
