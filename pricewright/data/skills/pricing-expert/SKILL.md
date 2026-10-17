---
name: pricing-expert
description: >-
  Price a service or product with a real rationale: a cost-and-effort model at the core (prep and development hours per delivered hour, facilitators or crew, the provider's day rate, credits and tools, fees, contingency, margin), travel as explicit variables, consistency checks across a whole rate card, and market comparables as a separate, swappable input. Routes by offering type to a specialty: training, talks, workshops, courses and coaching; audiovisual production (commercials, brand films, music videos, animation, documentary, explainers, pilots, retainers); software and apps (subscriptions, pay-as-you-go, credits, seats, freemium, tiers). Use for "price this", "what should we charge", "make a rate card", "is this price consistent", "day rate", "how much for a talk / workshop / course / video", "on-site vs online price", "travel costs in a quote", "per diem", "pricing tiers", "subscription vs usage pricing", "credits pricing", "check our prices against the market". Backed by the `pricewright` Python package (calculator + CLI).
metadata:
  audience: agents
  package: pricewright
---

# pricing-expert — price from the work, check against the card, then the market

A price is an argument, and this skill makes it in three layers, always in this order:

1. **Cost and effort.** What does one run of this offering take: whose hours, for how long (delivery *and* the iceberg under it: development, prep, admin, feedback), what third-party money (credits, venue, tools), what fees, what risk? Priced at the provider's own target rate. This is the floor and the explanation. It is computed, never guessed: `pricewright`.
2. **Consistency across the card.** Every offering on one rate card is priced with the same rates, so each pays the people the same per hour actually worked, unless a deliberate, named `positioning` says otherwise. Private never costs more than buying every seat; online never more than on site; a shorter, lighter offering never more than a longer, heavier one. `pricewright` runs these checks.
3. **The market.** Comparables say where the computed price sits (p10, median, p90, evidence-weighted). They do not set the price. If the cost floor is above the market, say so and show the levers (rate, fill, amortisation, scope); do not quietly price at the median.

## Route to the specialty

| The offering | Read | Templates in `pricewright.specialties` |
|---|---|---|
| Talk, keynote, webinar, workshop (open or private), online course, short series, 1:1 coaching, consulting + training programme | `references/training.md` | `training`: `talk`, `open_workshop`, `private_workshop`, `online_course`, `series`, `private_series`, `coaching`, `team_programme` |
| Commissioned film or video: commercial, brand film, narrative short, explainer, animation, documentary, music video, pitch/previs, social series; pilot; monthly retainer | `references/av-production.md` | `av_production`: `production(style=...)`, `pilot`, `retainer` |
| Software, app, API, AI tool: subscription tiers, seats, usage, credits, freemium, trials | `references/software.md` | `software`: `plan`, `credit_pack` (floors only; strategy is in the reference) |
| Anything on site, anywhere | `references/travel.md` | `pricewright.travel.travel_addon` |
| None of these | `references/method.md`, then add a specialty (`references/adding-a-specialty.md`) | |

Always read `references/method.md` first: it is the procedure every specialty follows, and the list of mistakes this skill exists to prevent.

## The procedure, short

1. **Name the offering's unit and frame**: per person, per group, per event, per project, per month; online or on site; contact hours; seats (cap *and* expected paid fill).
2. **Collect the inputs** (method.md lists them). The ones only the provider can set: day rate per role, expected runs to amortise development over, expected fill, positioning. If missing, use the defaults and **say which were defaulted**.
3. **Ask for research, or run it.** Each specialty states its research needs (`pricewright specialties`). Take a packet the user supplies (YAML, schema in `references/research-packets.md`), or use the dated baseline packets shipped in `pricewright/data/packets/`, or gather fresh evidence with web research (a subagent, not your main context), marking each record fetched / secondary / snippet.
4. **Write the spec** (one YAML: rates, offerings, packets, travel scenarios, sensitivity), run `pricewright card spec.yaml -o card.md`, read the findings.
5. **Resolve every contradiction** the checks report. Change inputs, not outputs: a price that "feels wrong" is a wrong hour count, rate, fill or amortisation; find which.
6. **Report** the card with its rationale: the summary table, the inputs the user must confirm (with defaults), the travel formula and worked examples, the day-rate sensitivity, and per offering its hours and the arithmetic.

## Rules

- Never print a price you cannot decompose into hours, costs and named multipliers.
- Expected fill, not capacity, divides an open session's cost. Show break-even seats.
- Development is amortised over the runs you expect to sell; say the number. A one-off custom talk carries all of its prep.
- On-site is the core fee plus a separate travel line (time beyond 1 h each way at half rate, nights by rule, expenses at cost). Never fold travel into a "from" price, never guess an on-site premium.
- A market median is evidence, not a target. A new provider usually prices below established ones; record that as `positioning`, visible in the card.
- Keep research out of the model: packets are files, refreshable and replaceable.
- Prices are ex VAT unless the user's market says otherwise; state the currency.

## The tool

```bash
pip install pricewright           # or: the local checkout, editable
pricewright specialties           # templates and the research each needs
pricewright card spec.yaml -o card.md
pricewright travel 3.5 --transport 180 --days 2 --travellers 2 --day-rate 900
```

```python
from pricewright import build_card, load_spec, render, price, Rates
from pricewright.specialties.training import talk
price(talk(delivery="onsite"), Rates({"founder": 900})).unit_price
```

A worked spec for a two-person studio (training + production) is in `references/example-spec.yaml`.
