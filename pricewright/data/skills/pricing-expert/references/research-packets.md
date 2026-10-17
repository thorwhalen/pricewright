# Research packets: the market as a separate, swappable input

The model never reads the market; it only gets compared with it. A packet is one YAML (or JSON) file: a list of comparable prices. The user may write one by hand, an agent may gather one, and baseline packets dated 2026-10 ship in `pricewright/data/packets/` (refresh them before quoting a real client; prices move).

## Schema (one record)

```yaml
- id: bcm-private-day            # unique slug
  specialty: training            # training | av_production | software | travel
  offering: private_day          # talk, keynote, webinar, open_workshop_day, private_day, half_day, online_cohort, series, coaching,
                                 # commercial, brand_film, explainer, animation, documentary, music_video, short_film, social_series, pitch_previs, pilot, retainer,
                                 # plan, credit_pack, crew_day_rate, per_diem, travel_day, ...
  provider: Building Creative Machines
  region: EU                     # EU | FR | UK | DE | US | global ...
  price: 10000                   # or price_low + price_high for a range
  currency: EUR                  # keep the original; convert with `fx` in the spec
  unit: per_group                # per_person | per_group | per_event | per_finished_minute | per_finished_second | per_project | per_day | per_hour | per_month | per_seat_month | per_credit | ...
  contact_hours: 8
  duration_s: null               # finished runtime (AV)
  group_size: 20
  delivery: onsite               # online | onsite | either | recorded | n/a
  provider_tier: established     # new | established | bureau | institution | celebrity | agency | freelancer | union_rate | government
  evidence: fetched              # fetched (page read) | secondary (cited by another source) | snippet (search text only) | inferred
  date: 2026-10
  url: https://...
  notes: travel and VAT extra
```

Omit what you do not know; never fill a field by guessing. A record with no contact hours cannot be compared per hour, and is simply skipped for that metric.

## What to ask the user for, per specialty

Run `pricewright specialties` for the live list. In short:

- **training**: talk fees for non-celebrity speakers (online, on site, length); open one-day workshop seat prices with hours and group size; private day and half-day prices with group size; live cohort courses with weeks, live hours and cohort size; short series; coaching rates; local trainer/consultant day rates; development-time ratios.
- **av_production**: price per finished minute (or per project with runtime) by style; AI studio and freelancer published prices, pilots and retainers; freelance day rates per role; person-days per finished minute; tool prices per generated second and shooting ratios; terms (deposits, revision rounds, usage uplifts).
- **software**: competitors' plans (price, included usage, seats, limits); inference cost per unit; segments and value metric; acquisition cost.
- **travel**: the provider's actual trips (door-to-door hours, fares), the official per diem and lodging scales of the country, the provider's own terms.

## Gathering one (an agent's brief)

Send a research subagent, not your main context. Ask for: a synthesis Markdown file (Vancouver references with links, each claim marked fetched or snippet), and the YAML packet in this schema. Require original currencies, contact hours or runtime wherever stated, and the provider tier. Tell it that a missing number is better than an invented one.

## Using one

In the spec:

```yaml
market:
  packets: [training-comparables.yaml, travel-comparables.yaml]
  fx: {USD: 0.87, GBP: 1.16, CAD: 0.63, AUD: 0.57, NZD: 0.52}   # value of 1 unit in the card currency
  exclude_tiers: [celebrity]
offerings:
  - id: talk_online
    specialty: training
    template: talk
    market: {offerings: [talk, webinar], delivery: [online]}       # optional override of the specialty's default selection
```
