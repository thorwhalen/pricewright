# pricewright

Price services and products from a model of their costs and effort, not from a market median. Travel is an explicit add-on, a whole rate card is checked for consistency, and market comparables are a separate, swappable input.

```bash
pip install pricewright
pricewright card my-card.yaml -o card.md      # price, check, compare, render
pricewright travel 3.5 --transport 220 --travellers 2 --day-rate 900
pricewright specialties                       # templates, and the research each needs
```

```python
from pricewright import price, Rates
from pricewright.specialties.training import talk, private_workshop

rates = Rates({"founder": 900})  # target day rate, 7 h a day
q = price(talk(delivery="online"), rates)
q.unit_price, q.hours_total, q.effective_day  # 1700, 11.2, ~1058
```

## Why

A rate card assembled from different market medians contradicts itself. You get a 60-minute talk at 10,000 next to a 6,000 private day, and "the market says so" explains nothing to whoever has to defend the number. pricewright builds each price from **who works how long** (development amortised over the runs you expect to sell, prep, delivery, admin, feedback) and **what it costs** (credits, venue, tools, fees). It adds contingency and margin, then rounds. Every metric is then recomputed from the printed price: the effective day rate per hour actually worked, the price per contact hour and per person-hour, and the seats needed to pay the target rate.

## Layers

| Module | What it does |
|---|---|
| `base` | `Rates`, `Effort`, `Cost`, `Offering` (frozen dataclasses), `day_rate_from_income` |
| `model` | `price(offering, rates)` turns an offering into a `Quote` with the full arithmetic |
| `travel` | `travel_addon(Trip, policy=TravelPolicy())`: time beyond 1 h each way at half rate, nights by rule, expenses at cost |
| `ratecard` | `check_card(quotes)`: effective-rate spread, dominance, private vs seats, online vs on site, volume per hour |
| `research` | load comparables packets (YAML), normalise them (per person-hour, per contact hour, per finished minute), place a price at an evidence-weighted percentile |
| `specialties` | registry of templates: `training`, `av_production`, `software`; adding a specialty means adding one module |
| `spec`, `report` | a YAML rate card in, a Markdown card with its rationale out |

Baseline research packets (dated 2026-10) ship in `pricewright/data/packets/`. Refresh them before quoting a real client.

## The agent skill

`pricewright/data/skills/pricing-expert/` is the `pricing-expert` skill. It routes an offering to a specialty, states the research it needs, and explains the method and the trade practice of each field. Its references cover training, travel, audiovisual production and software (subscriptions, usage, credits, seats, tiers). It is `gh skill`-discoverable and ships with `pip install`.

## A spec

```yaml
title: My rate card
currency: EUR
rates: {day_rates: {founder: 900}, hours_per_day: 7}
market: {packets: [training-2026-10.yaml], fx: {USD: 0.86, GBP: 1.15}}
travel:
  scenarios:
    - {name: "2 h by train, 2 people", trip: {one_way_hours: 2, transport_round_trip: 150, travellers: 2}}
sensitivity: {day_rates: [700, 900, 1100]}
offerings:
  - {id: talk, specialty: training, template: talk, params: {delivery: online}}
  - {id: day, specialty: training, template: private_workshop, params: {group: 12}}
  - {id: spot, specialty: av_production, template: production, params: {style: commercial, seconds: 30}}
```

A complete example is `pricewright/data/skills/pricing-expert/references/example-spec.yaml`.
