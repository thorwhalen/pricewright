# The method: cost and effort first, consistency second, market third

Every specialty follows this. It exists because the usual failure is a card of prices each copied from a different market median, which then contradict each other (a 60-minute talk at 10,000 next to a 6,000 private day), and because "the market says" explains nothing to the person who has to defend the number.

## 1. The model, per run of the offering

```
labour   = sum over effort lines of hours x hourly rate of the role
           development hours are divided by the runs you expect to sell (amortised)
           per-participant hours (feedback, pre-work review) x participants
direct   = third-party money: credits, tools, venue, catering, materials, licences, subcontractors (+ markup if re-billed)
base     = (labour + direct) x (1 + contingency)
net      = base / (1 - margin)                     margin is a share of the price
revenue  = (net + fixed fee per payment x payments) / (1 - percentage fees)
revenue *= positioning                              a named launch discount (< 1) or premium (> 1)
unit price = revenue / expected paying seats        open, per-person sales
           = revenue                                everything else
```

Then the unit price is rounded to a printable number and **every metric is recomputed from the rounded price**: effective rate per hour worked, price per contact hour, per person-hour, break-even seats.

## 2. Inputs, and who sets them

| Input | Who | Default | Why it matters |
|---|---|---|---|
| Day rate per role | **provider** | 900 EUR/day, 7 h | everything is linear in it; derive it from income with `day_rate_from_income(income, billable_days=100-120, annual_overhead=...)` rather than from a market median |
| Expected runs (amortisation) | **provider** | talk 8, workshop 6, course 4, series 4 | the single biggest reason talk and workshop prices per hour differ |
| Expected paid fill | **provider** | ~65% of cap | open sessions are priced at expected fill, never at cap |
| Positioning | **provider** | 1.0 | a deliberate launch discount or a premium, visible on the card |
| Development ratio (h per delivered h) | expert, then provider's timesheets | talk 12, workshop 6, course 8 | see the specialty reference |
| Prep, admin, feedback hours | expert | per template | the iceberg under each delivered hour |
| Facilitators | expert | 1 per 8 hands-on participants | a 16-person hands-on day needs two people |
| Credits, tools, venue, catering | expert, then actual invoices | per template | real cash out |
| Fees | expert | 4% + 0.25 on open card sales; 0 on invoices | |
| Contingency | expert | 5% talks, 10% training, 12% production, 15% programmes | risk of overrun scales with novelty and scope |
| Margin | provider | 10% | the business's own reserve (selling time, dry months), on top of the people's rate |
| Travel policy | provider, from practice | see travel.md | |

Always list, in the report, which inputs were defaulted and which the provider confirmed.

## 3. The card-wide checks (`pricewright.check_card`)

- **effective_rate_spread**: each offering's effective hourly rate (after fees and costs, over all hours worked) against the card's median. A big gap is either an error or a positioning choice; make it explicit.
- **dominance**: an offering with fewer contact hours *and* fewer hours worked must not cost more in total than another. Catches "talk dearer than a full day".
- **private_vs_seats**: a private group price must not exceed cap x the open seat price.
- **online_vs_onsite**: same content, the online unit price must not exceed the on-site one (before travel). The gap is reported; it comes from the hours (commute, setup, venue, printing), not from a guessed percentage.
- **volume_per_hour**: within a family, more contact hours should not cost more per hour (packs, longer formats).

Read every finding and resolve it by changing an *input*. If an offering is still off after honest inputs, that is information: the format may not be viable at the provider's rate (say so), or it is a loss leader (set `positioning` and say so).

## 4. The market, as a check

A research packet is a list of comparables (schema in `research-packets.md`). For each template the specialty says which comparables are like-for-like and which metric to compare (per person-hour, per contact hour, per event, per finished minute). The result is a position: p10, median, p90, the price's percentile, weighted by evidence quality (page read 1.0, secondary 0.7, search snippet 0.5).

How to read it:

- **Within market**: done; say where (a new provider below the median is normal).
- **Above p90**: check the inputs (too many hours? too few expected seats? one-off prep that should be amortised?). If they are honest, the provider either accepts a lower effective rate (`positioning < 1`, shown), changes the format (fewer facilitators, recorded parts, bigger cohort), or does not sell it.
- **Below p10**: usually under-counted hours or a missing cost (credits, venue, travel). Or real leverage (a talk reused 20 times); then a modest premium is available.
- **Thin evidence (n < 3)**: say so; do not lean on it.

## 5. Sensitivity

Report the card at three day rates (e.g. 700, 900, 1,100). It shows the provider that the whole card moves together, and which offerings stay viable at a lower rate.

## 6. The mistakes this method prevents

1. One logic per offering (speaker-bureau talk, per-seat course, per-team programme) on the same card.
2. Pricing an open session at full capacity.
3. Ignoring development time, or charging all of it to a single run of reusable material.
4. A flat "on-site premium" instead of travel computed from the trip.
5. Treating a single, snippet-only comparable as the market.
6. Private prices above the sum of the seats.
7. Packs more expensive per hour than singles.
8. A price nobody can decompose.
