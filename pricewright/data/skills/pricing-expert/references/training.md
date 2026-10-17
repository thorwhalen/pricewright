# Training, talks, workshops, courses and coaching

How `pricewright.specialties.training` prices, and the rules of thumb behind its defaults. The evidence (baseline 2026-10-17) follows below the line; refresh it before quoting a real client.

## The effort model

- **Development** of reusable material: delivered hours x a ratio, amortised over the runs you expect to sell. Defaults: new 60-min talk 40:1 (range 20-60), hands-on day 8:1 (3-20), live cohort 8:1 per live hour (5-15), live online session 6:1 (3-15).
- **Per run**: tailoring (talk 4 h, keynote 6-10 h, private day ~1:1), organiser/client admin, prep per facilitator, tech checks per online session, setup and local commute on site, listing and registrations for open sessions.
- **Per participant**: pre-work review and feedback (hands-on day 0.5 h, course 1.5 h, series 0.5 h).
- **Facilitators**: one lead up to ~12 hands-on participants, a second above.
- **Costs**: generation credits, venue (Paris ~605-650/day, London ~450 GBP), catering, printed materials, marketing per open run, platform; fees on open card sales (Stripe EEA 1.5% + 0.25; Maven 10%; Eventbrite UK 6.95% + 0.59).
- **Open sessions are priced at expected fill**, never at cap; the card shows the seats needed to pay the target rate.

## Rules of thumb to check a card against

- Talk fee = 0.25-0.45 of the same person's private full-day fee; per hour a talk is ~2-3.5x the day.
- Half day = 0.6-0.7 of a full day.
- Private day = 3-10 open seats of the same day (typically 4-6): the buyer's break-even group size.
- Online: training 0-25% below on site (BDVT: none); talks 30-60% below on site, but that gap mostly reflects travel days bundled into speaker fees. Bill travel separately and the remaining gap is the hours.
- Trainer/consultant day rates: France 400-1,200 EUR (TJM median ~795), AI-expert trainer 1,100-1,800; UK contract trainer median 413 GBP; Germany BDVT 950-3,300 EUR (design and prep billed at the full rate); Netherlands ~95 EUR/h.
- Coaching: Western Europe average ~277 USD/h (ICF 2023); BDVT 200-440 EUR/h.
- Live cohorts per person-hour: creative ~25-50, corporate one-day AI courses 100-150 (local currency).
- French buyers expect OPCO-fundable training, which needs Qualiopi certification of the provider.

## Templates

`talk(delivery=..., minutes, qa_minutes, customisation_hours, runs, dev_ratio)`, `open_workshop(cap, expected, contact_hours, delivery)`, `private_workshop(group, contact_hours, delivery, customisation_hours)`, `online_course(weeks, session_hours, office_hours_per_week, cap, expected, private)`, `series(sessions, session_hours, cap, expected)`, `private_series(...)`, `coaching(sessions)`, `team_programme(workshop_days, audit_days, playbook_days, checkins, group)`. Every number has a keyword default from `DEFAULTS`; pass `defaults={...}` to override several at once.

---


Date: 2026-10-17. Scope: the cost-and-effort side of pricing talks, workshops, live courses and coaching for a new two-person studio (AI filmmaking, AI for writers, AI for musicians), plus a European refresh of the market numbers. It builds on the earlier review at an earlier internal pricing review (not published) (cited as [R]) and does not repeat its sources; the solid items from [R] are carried into `training-comparables.yaml` with their evidence quality marked.

Evidence labels used throughout: **fetched** (page or PDF read in this session), **snippet** (search-result text only; the page failed or was not opened), **secondary** (a number quoted by another source, not by its originator). Currencies are left as published. "Judgment" marks a recommendation that no source states directly.

## 1. Recommended defaults

### 1a. Effort ratios: preparation hours per delivered hour

The published benchmarks (Chapman, ATD/Kapp and Defelice) measure full instructional-design teams (designer, SME, media, QA, project manager) building courseware for corporations. A two-person studio teaching its own craft is closer to the practitioner numbers (trainers quoting their own design time). Both are shown; the default is for the studio.

| Format | Full-team benchmark | Practitioner evidence | Studio default (judgment) | Range |
|---|---|---|---|---|
| New talk or keynote, 45-60 min | none published | 1 h prep per minute of speaking [10][11]; 20 min to 1 h per minute (coach blog, snippet) | 40 h for a new 60-min talk (40:1) | 20:1 to 60:1 |
| Tailoring an existing talk to one client | none | 6-10 h for a 45-min keynote [12] | 8 h per booking | 4 to 12 h |
| New in-person hands-on workshop | ILT 22 / 43 / 82 h per h (low / avg / high, n=249) [1]; ILT 43-185 h (2009) [3]; classroom 38 h (2017, secondary) [4] | 8-10 h per h for "chalk and talk" incl. slides, trainer guide, workbooks [8]; "3 days R&D per delivery day" and 3 h prep per hour for courses of 5 days or less (snippet) [9] | 8:1 (about 56 h, 7 working days, for a 7-h day) | 3:1 to 20:1 |
| New live online session (vILT) | vILT 28 h vs classroom 38 h (2017, secondary) [4]; web-based ILT 49-89 h (2009) [2][3] | none | 6:1 (0.75 x the in-person ratio, from the 28/38 ratio) | 3:1 to 15:1 |
| Re-running an existing workshop for a private client | none | 1 familiarisation day + 3 days to adapt a 1-day workshop from existing material (one trainer, snippet) [9] | 1:1 (half a day of customisation and half a day of logistics per delivery day) | 0.5:1 to 4:1 |
| First run of a multi-week live cohort | none | none | 8:1 per live hour (live sessions plus exercises, examples, feedback rubric) | 5:1 to 15:1 |
| Self-paced e-learning (for reference) | Level 1: 49 / 79 / 125; Level 2: 127 / 184 / 267; Level 3: 217 / 490 / 716 [1]; 80-150 for higher complexity (2026 practitioner aggregate) [6] | 120:1 to 187:1 for Level 2 (one designer's estimates) [7] | not recommended for v1 | |

Three points that matter for pricing:

1. **The talk is the most prep-intensive format per delivered hour.** At 20-60 prep hours per delivered hour, a new 60-minute talk costs about as much preparation as a new 3-7 hour workshop at 8:1. This is the main cost-side reason talks are dearer per hour (section 1c).
2. **Preparation is billable at the full day rate in at least one formal fee scale.** The German trainers' association BDVT sets "Konzeption, Vor- und Nacharbeit" (design, preparation and follow-up) at the same day rate as consulting, the top training tier: from 1,500 / 2,000 / 3,300 EUR per day for starter / professional / senior [37]. The pricing consequence: a private workshop that needs real customisation can be quoted as delivery days plus design days.
3. **AI has not yet cut development time much.** A 2026 practitioner review finds AI speeds the design phase (outlining, objectives, practice ideas) but not production or review [6]. Do not price on an assumed AI productivity gain.

### 1b. Day-rate bands (ex VAT, as published)

| Market | Trainer day | AI or senior consultant day | Source quality |
|---|---|---|---|
| France | 400-600 EUR (formateur, 2iPortage, Dec 2025) [35]; median 795 EUR for Formation/Coaching, formateur IT 600 (P25 500, P75 840, n=10), formateur management 780 (n=13), formateur data 810 (n=4) (TJMetre, 2026) [34]; Malt-displayed formateur confirmé 500-750, senior 750-1,200 incl. Malt's 8-10% commission (compiled guide) [36]; AI/data-science expert trainer 1,100-1,800, junior generalist 400-700 (Kaliio 2026, secondary) [23] | consultant IA median 700 EUR (P25 580, P75 1,000, n=19) [34]; strategy consultant senior 950-1,400, expert 1,400-2,200+ [36] | fetched, small n |
| France, what institutions pay for intra | 900-1,620 EUR per 6-h day (150-270 EUR/h), raised 25% in 2025 "because independent trainers now charge more" [22] | | fetched |
| UK | contract "Trainer" median 413 GBP/day (P10 208, P90 625; 108 quoted rates, 6 months to 17 Oct 2026) [33]; freelance AI trainers 500-750 GBP, boutique 600-900 (secondary) [31] | independent AI consultants 500-2,000 GBP; boutique 900-1,600; Big 4 2,000-5,000 [32] | fetched; [31][32] are a consultancy's own marketing |
| Germany | BDVT 2020 recommendation: delivery-only training from 950 (starter) / 1,200 (professional); standard content from 1,200 / 1,400 / 2,600 (senior); own-designed content from 1,500 / 2,000 / 3,300 EUR [37]; public-sector trainers often under 500 EUR/day [37] | consulting from 1,500 / 2,000 / 3,300 EUR [37] | fetched; 2020 recommendation, not a survey |
| Netherlands | zzp trainer/coach average 95 EUR/h excl. BTW (starter 82, experienced 101), 19 billable h/week (Knab survey of over 20,000 zzp, 2026) [38]; about 665-760 EUR for a 7-8 h day (inferred) | | fetched |

**Recommended band for the studio** (judgment): 800-1,200 EUR per delivered training day as the internal "trainer day" rate, which sits at the Malt senior / TJMetre median / BDVT professional level, and below the AI-expert trainer band of 1,100-1,800.

**Ratio of senior consultant day to trainer day: about 1.0 to 1.5 at the same seniority.** TJMetre's consultant IA median (700) is actually below its Formation/Coaching median (795) [34]; the Malt-based guide gives strategy-senior 950-1,400 against formateur-senior 750-1,200 (about 1.2x) [36]; BDVT prices consulting at the top training tier (1.0x of the own-content tier, 1.25-1.6x of standard-content training) [37]. In the UK the spread is wider (AI consultant 500-2,000 GBP against a trainer median of 413) [32][33], but the trainer figure is a contract-job median, not a senior specialist rate.

### 1c. Talk versus training day

**Default: a talk is 0.25-0.45 of the same person's full-day training fee, so per hour it is about 2-3.5x the day's hourly rate.** Evidence:

| Source | Talk | Half day | Full day | Talk / full day |
|---|---|---|---|---|
| Bill Cole, US speaker rate card [13] | 6,500 USD (up to 90 min) | 10,500 USD (3.5 h) | 15,000 USD (6 h) | 0.43; half/full 0.70 |
| US college planner, list post (snippet) [14] | 1,500-2,000 USD (90-120 min) | 3,000-4,500 USD | 6,000-7,500 USD (two co-facilitators) | about 0.27 |
| Speaker Agency UK, format multipliers [12] | 1x (30-60 min keynote) | workshop (2-4 h) 1.5-2x | masterclass (half or full day) 3-4x | 0.25-0.33 |
| Centre Hubertine Auclert, France (non-profit grid 2026) [21] | 500 EUR (intervention at a colloquium) | 900 EUR (3-h awareness session) | 2,000 EUR (intra day, 15 max) | 0.25; 3h/day 0.45 |
| Building Creative Machines, EU studio [R] | from 2,000 EUR (15-30 min) | 6,000 EUR (4 h) | 10,000 EUR (8 h) | 0.20; half/full 0.60 |

Half-day defaults to **0.6-0.7 of a full day** (0.60 BCM, 0.70 Bill Cole, 0.60 for the London venue below).

How speakers justify the talk premium, in their own words: the fee "pays for four things, and stage time is only one of them": preparation (6-10 h of tailoring for a 45-min keynote), stage time, process support (kick-off call, briefing, prep session, Q&A, follow-up material) and opportunity cost of the date [12]; travel days and accommodation are on top [15]; customised or interactive talks cost more because of prep time [15]; senior or large audiences, last-minute dates and for-profit hosts pay more [16]; recording or distribution rights are an add-on (10-20% above base [12]; 50% of fee for video, 33% for audio [13]). The cost-side arithmetic in 1a supports it: 40 prep hours + 8 h tailoring + 1 h on stage + a travel day is close to a full working week for one hour delivered.

### 1d. Online discount

Talks and training are discounted differently, and the difference is the travel day.

- **Talks online: 30-60% off.** 50% off on a published rate card [13]; "about 50%" (bureau) [17]; virtual fees "50% to 70% lower" [18]; webinar at 0.4-0.6x keynote [12]; one bureau says 60-90% of in-person (snippet) [19]. One agency cautions that virtual "don't always" carry lower rates [15].
- **Training online: 0-25% off.** BDVT: no difference "because the effort is identical", also for preparation [37]; FranceFG intra 1,990 vs 1,790 EUR virtual (-10%) [25]; Dawan inter 875 vs 700 EUR distanciel (-20%) [26]; Swedish consultant -25% (snippet, [R]).
- Studio default (judgment): talk online at 50-60% of on-site; training online at 85-90% of on-site.

### 1e. Private (intra) day versus per-person (inter) day

**Default: one private group day = 4-6 x the open per-person day price (break-even group size about 5).**

| Source | Intra day | Inter per person per day | Break-even (intra / inter) |
|---|---|---|---|
| FranceFG, AI training 2026 [25] | 1,990 EUR HT (max 10) | 590 EUR HT | 3.4 |
| Tensoria, French AI-training market 2026 [23] | 1,500-2,000 EUR per group (4-12 people typical) | 795-1,010 EUR (ORSYS 1,010/day; Cegos 825/day) | 1.5-2.5 computed; the article itself says intra wins "from about 5 participants" |
| Comparateur-ia, France 2026 [24] | about 2,500 EUR (6-15 people) | 600-1,200 EUR per person (1-3 days) | page says intra pays off from 6-8 participants |
| Centre Hubertine Auclert 2026 [21] | 2,000 EUR non-member (15 max) | 350 EUR non-member | 5.7 (member grid: 1,500 / 150 = 10) |

The Tensoria computed ratio mixes a low intra rate from small trainers with ORSYS/Cegos catalogue prices, which is why it is low; within one provider (FranceFG, Hubertine) the ratio is 3.4-5.7. For the studio, at the earlier review's open price of 495 USD per person, 5x gives about 2,500 USD per private day before customisation days are added (judgment).

UK and Germany per-person open prices for one AI day, for scale: Global Knowledge UK 795 GBP ex VAT virtual [29]; Bilginc from 764 GBP (snippet); Haufe Akademie 790 EUR + VAT live online, max 11 [27], 890 EUR + VAT (snippet) [28]; Dawan (FR) 875 EUR HT in person [26]. UK private day: Tutorials.co.uk 1,049 GBP + VAT per day on site, travel included, min 8 [30]; half-day executive briefing from 3,500 GBP for up to 15; two-day intensive from 12,000 GBP for up to 20 (about 600 GBP per person) [31].

### 1f. Group size and facilitators

No source sets a hard rule. The consistent pattern: one facilitator per 5-8 participants for interactive work, two facilitators above about 10-12.

- UBC's Instructional Skills Workshop co-facilitates every session except those with fewer than 12 attendees (snippet) [44].
- One facilitator per 5-8 participants, minimum two; more than 16 calls for a third (Our Whole Lives FAQ, snippet) [45]; a library digital-skills toolkit sets 8-10 participants at 1:5 or better (snippet) [46].
- Market caps observed: intra max 10 [25], 11 [27], 15 [21], 4-12 typical [23], 6-15 [24], 20 (BCM [R]); the one small-cohort creative bootcamp in [R] is max 12 with two instructors.
- Minimum viable group: FranceFG offers inter for 1-3 people and intra from there [25]; Tutorials.co.uk min 8 for its day price [30]; LFW course 10-25 [40]; comparateur says custom intra starts at 4-6 [24].
- Studio default (judgment): hands-on AI workshop 6-12 with one lead, 13-16 needs the second founder in the room (cost the second person as a delivery day); open sessions run at 6 or more.

### 1g. Fees

| Item | Rate | Source |
|---|---|---|
| Stripe, France account: standard EEA cards | 1.5% + 0.25 EUR (premium EEA 2.8% + 0.25) | [47] fetched |
| Stripe, France: UK cards / international | 2.5% + 0.25 EUR / 3.15% + 0.25 EUR; +2% if currency conversion | [47] fetched |
| Stripe, UK account: UK cards / EEA / international | 1.5% + 20p / 2.5% + 20p / 3.15% + 20p; +2% FX | [48] fetched |
| Maven | 10% of gross after Stripe fees; affiliate seats up to 30% combined discount and commission | [49] fetched |
| Teachable | Starter 39 USD/mo (29 annual) with 7.5% fee; Builder 89 (69) and above 0%; card processing on top | [50] fetched |
| Thinkific | Basic 53 EUR/mo (39 annual), Start 107 (79), Grow 213 (159); Thinkific Payments 2.9%; a gateway fee applies with own Stripe/PayPal (amount not published on the page) | [51] fetched |
| Podia | Mover 5% fee; Shaker and above 0% (prices changed June 2026) | [52] snippet, third-party |
| Eventbrite UK | 6.95% + 0.59 GBP per paid ticket (service fee; buyer pays by default) | [53] fetched |
| Eventbrite France | only legacy packages listed: 3.5% + 0.49 EUR (Essentials), 5.5% + 0.99 EUR (Professional) | [53] fetched |
| Venue, Paris, 15-20 people | 605 EUR/day (15e, 15 classroom / 20 theatre, VAT not stated) [54]; 470-1,882 EUR/day across other listings (snippet) [55]; Maison Suger 600 EUR/day (snippet) [56] | |
| Venue, London, 16 at tables | 450 GBP/day ex VAT incl. Wi-Fi, video conferencing, tea and coffee; half day 270 (Cally Yard, N7) [57]; Speak Up London 450 GBP/day (snippet) [58]; CPAG 300-350 GBP + VAT for up to 20 (snippet) [59] | |

A 16-person day in a modest London or Paris room therefore costs about 450-650 in local currency before catering; at 12 paying participants that is roughly 40-55 per head.

### 1h. French funding (OPCO)

Relevant because French corporate buyers expect OPCO-fundable training, and that requires Qualiopi certification of the provider [23]. OPCO Atlas: 40 EUR HT per training hour under AFEST, capped at 150 h (secondary) [23]; Atlas "Plan IA-tlas" funds 100% of AI modules for companies under 50 staff from 1 July to 31 December 2026 [25]. For the creative sector the relevant OPCO is AFDAS; I found no official 2026 hourly ceiling (a provider guide claims 30-45 EUR/h in person, 25-35 online, unverified snippet). Without Qualiopi the studio sells to French companies at full price only.

## 2. Evidence by question

### Q1. Development ratios

- **Chapman Alliance 2010** (fetched slides) [1]: 249 organisations; hours per finished hour: ILT 22 / 43 / 82; e-learning L1 49 / 79 / 125, L2 127 / 184 / 267, L3 217 / 490 / 716 (some simulations above 2,000). Average ILT internal cost 5,934 USD per finished hour. Includes all team members; assumes tasks repeat per hour (no economies for longer courses). The values were read from garbled slide text with "X:1" labels and should be spot-checked against the original.
- **Kapp and Defelice, ASTD 2009** [2][3]: ILT 43-185 (midpoint 114); instructor-led web-based delivery 49-89 (2003: 30-80); e-learning without interactivity 73-116, moderate 97-154, high 132-214. The 2009 figures exclude analysis (40-120 h extra). n=47, 83% with an ID degree (per a critic) [8 via RapidBI].
- **ATD 2017 update (Defelice and Kapp)**: classroom 38, virtual ILT 28, passive e-learning 42, limited interactivity 71 h per h [4] (secondary; the ATD page returned 429 during this session). The 2017 update changed the question to levels of interaction, so it is not like-for-like with 2009 [5] (snippet).
- **2020s**: ATD ran later surveys (2021, 2023, 264 respondents for one of them); the 2023 author warns results vary too much for stand-alone estimates [7]. I could not retrieve their tables (429 errors). A 2026 practitioner aggregate gives 80-150 h per hour for higher-complexity e-learning and says AI speeds design, not build [6].
- **Practitioner, UK**: 8-10 h per h for chalk-and-talk incl. syllabus, slides, trainer guide, workbooks; 15-25 for distance learning; caveat that modifications of existing material vary widely [8] (2001 forum post). Rule attributed to Dugan Laird (1985): 3 h preparation per hour of training for courses of 5 days or less, 2.5 for 5-10 days, 2 for over 10 days (snippet via a slide deck) [9]. Trainers in a TrainingZone thread quote "3 days R&D for each day's delivery" (snippet) [9].
- **Talks**: 1 h prep per minute of speaking as "ideal" (Jon Torrens, 2014) [10]; tracked 19 h plus 5-7 h for a 20-25 min conference talk built on existing blog posts [11]; 6-10 h to tailor a 45-min keynote to an audience [12].
- **Re-runs**: no published ratio found. The only datum is one trainer budgeting 1 familiarisation day plus 3 days to adapt a one-day workshop from existing material [9] (snippet). The default 1:1 in 1a is judgment.

### Q2. Why a talk costs more per hour

Covered in 1c. Additional points: Phil Simon prices keynotes above breakouts and longer talks above shorter ones, adds premiums for senior audiences, esoteric topics and short notice, and discounts for government and non-profits [16]. Futurists says workshops with "extensive preparation, customization, or the development of proprietary materials" command premiums [R-adjacent, fetched in this session, no numbers]. The German speaker-tier article puts beginners at 1,000-3,000 EUR, professionals at 3,000-6,000, known professionals 6,000-12,000 and says more than 6,000 needs public recognition [20].

### Q3. Day rates

Covered in 1b. Extra notes: a 2007/08 German TrainerGuide reported an average published day rate of 1,861 EUR (1,670 without outliers, n=149, 15 years' experience on average) (snippet, old); the BDVT 2020 paper notes public-sector trainers are often paid under 500 EUR/day with prep included [37]. Malt's own 2025/2026 barometer was not reachable; every "Malt" figure found was re-published by a third party, so the Malt line in 1b comes from a compiled guide [36] and is labelled accordingly.

### Q4. Talk fees for emerging speakers in Europe

| Source | Band | Note |
|---|---|---|
| Speaker Agency UK, 2026 [12] | Band A "emerging voices and regional experts" 1,000-3,000 GBP; Band B specialists 3,000-7,500 | fetched; webinar 0.4-0.6x |
| deutsche-startups.de, 2019 [20] | Einsteiger 1,000-3,000 EUR; Profi 3,000-6,000 | fetched; a guide for speakers, not a survey |
| Kaltura, virtual fee tiers [18] | guest speakers 500-2,000 USD virtual; experienced keynote experts 5,000-10,000 | fetched |
| Centre Hubertine Auclert 2026 [21] | 500 EUR per intervention (non-member) | fetched; non-profit public-sector grid |
| UK motivational-speaker guide | experienced professionals 3,000-7,500 GBP | snippet |

So an emerging speaker in Europe sits at about 1,000-3,000 GBP/EUR on site, and about half that online. This brackets the earlier review's proposal (2,000 USD online, 3,500 USD on site) [R]: the online figure is at the top of the European emerging band, the on-site figure slightly above it.

### Q5. Intra and inter prices

Covered in 1e. Also: Lefebvre Dalloz says generative-AI programmes run 1,500-3,000 EUR HT for several days and intra is quoted per group (snippet). Tensoria's worked example: a 1,500 EUR intra day for 10 people costs the employer about 3,950 EUR once 2,450 EUR of salary time is included [23], useful for showing buyers that the training fee is the minor part of their cost.

### Q6. Live cohorts, per contact hour, and coaching

New European or international items (the US items from [R] are in the YAML):

| Provider | Price | Contact hours | Per contact hour | Evidence |
|---|---|---|---|---|
| London Film Workshops, AI Fundamentals for Filmmaking [40] | 475 GBP (or 90 GBP per online session) | 6.5 h in person + 5 x 1.5 h online = 14 h; 10-25 people | about 34 GBP | fetched |
| National Film School of Denmark, Mastering AI for European Film Professionals [41] | 2,500 EUR | 5 modules over 9 months, about 10 on-site + 6 online days; 24 participants; hours not stated | not computable (about 156 EUR per programme day, inferred) | fetched |
| Haufe Akademie, AI for preparing trainings (live online) [27] | 790 EUR + VAT | 09:00-17:00, max 11 | about 99-113 EUR | fetched |
| Dawan, IA pour les managers [26] | 875 EUR HT in person / 700 online | 7 h | 125 / 100 EUR | fetched |
| Emphasis (UK), Superhuman writing with AI [43] | 300 GBP + VAT | 2 h, up to 12 | 150 GBP | snippet |
| NTU Singapore, Suno AI music (online) [42] | 960 SGD | not stated | not computable | fetched |
| Abendakademie Mannheim, Music Production with AI | 59 EUR | 4 h in person | about 15 EUR (adult education) | snippet |

Per contact hour, the small-group live market spreads from about 34 GBP (hybrid film course, up to 25 people) through about 50 USD (small creative cohorts in [R]) to 100-150 in local currency (corporate one-day AI courses with up to 11-12 people). The earlier review's 53 USD per hour default for the studio's live course sits in the creative-cohort band, well below the corporate band.

Coaching: ICF 2023 global study (14,591 responses, fieldwork late 2022) gives an average fee per one-hour session of 277 USD in Western Europe, 272 North America, 244 global, 138 Eastern Europe [39] (fetched). BDVT 2020: coaching from 200 / 275 / 440 EUR per hour (starter / professional / senior) [37]. An AI executive-coaching offer in France: 5,000 EUR HT for 5 x 1.5 h (about 665 EUR/h, secondary) [23]. The earlier review's 200 USD per hour is therefore under the Western European average for an established coach, which is reasonable for a new studio.

### Q7. Ratios and minimum groups

Covered in 1f.

### Q8. Fees and venues

Covered in 1g.

## 3. Gaps and weak spots

- ATD's 2017, 2021 and 2023 tables could not be fetched (HTTP 429); the 2017 numbers are secondary [4].
- No published ratio for re-running or customising an existing workshop; the 1:1 default is judgment.
- Malt's own barometer was not reachable; Malt figures are second-hand.
- No AFDAS official hourly ceiling found.
- No euro-priced weekly live AI cohort for writers or musicians was found; the music and writing evidence is thin and mostly non-European.
- Venue prices for Paris come mostly from marketplace snippets; only one Paris listing was fetched.

## REFERENCES

1. Chapman Alliance (B. Chapman). How long does it take to create learning? Sept 2010 (fetched). [slideshare.net/slideshow/how-long-does-it-take-to-create-learning/5198860](https://www.slideshare.net/slideshow/how-long-does-it-take-to-create-learning/5198860)
2. Kapp K. How long does it take to develop one hour of e-learning, updated for 2009 (fetched). [karlkapp.com/how-long-does-it-take-to-develop-one](https://karlkapp.com/how-long-does-it-take-to-develop-one/)
3. University of Washington. Training development timeline estimation, based on ATD "Time to develop one hour of training" 2009 (fetched PDF). [depts.washington.edu/.../Training-Development-Timeline-Estimation.pdf](https://depts.washington.edu/edutrain/main/wp-content/uploads/2018/05/Training-Development-Timeline-Estimation.pdf)
4. Talented Learning. Starting a customer education program, citing Defelice and Kapp, ATD 2017 (fetched; secondary for the ATD numbers). [talentedlearning.com/how-to-start-customer-education-program](https://talentedlearning.com/how-to-start-customer-education-program/)
5. ATD. How long does it take to develop one hour of training? Updated for 2017 (snippet; 429 on fetch). [td.org/insights/how-long-does-it-take-to-develop-one-hour-of-training-2017](https://www.td.org/insights/how-long-does-it-take-to-develop-one-hour-of-training-2017)
6. Jackson A. More powerful, not necessarily faster. Learning Reframed, 2026 (fetched). [learningreframed.substack.com/p/more-powerful-not-necessarily-faster](https://learningreframed.substack.com/p/more-powerful-not-necessarily-faster)
7. Tucker C. Time estimates for e-learning development (fetched). [christytuckerlearning.com/time-estimates-for-e-learning-development](https://christytuckerlearning.com/time-estimates-for-e-learning-development/)
8. TrainingZone. Estimating course development time (forum, 2001; fetched). [trainingzone.co.uk/estimating-course-development-time](https://trainingzone.co.uk/estimating-course-development-time). RapidBI commentary on the Kapp sample (fetched): [rapidbi.com/what-is-the-ratio-of-development-to-delivery-time](https://rapidbi.com/what-is-the-ratio-of-development-to-delivery-time/)
9. Determining hours of design and development (slide deck attributing the 3:1 rule to Laird 1985; snippet) [slideshare.net/slideshow/design-development-hours/30248650](https://www.slideshare.net/slideshow/design-development-hours/30248650); TrainingZone "The training formula" thread (snippet) [trainingzone.co.uk/?p=38761](https://trainingzone.co.uk/?p=38761)
10. Torrens J. Do your prep before speaking. Cambridge Network, 2014 (fetched). [cambridgenetwork.co.uk/news/do-your-prep-speaking](https://www.cambridgenetwork.co.uk/news/do-your-prep-speaking)
11. Cheley R. DjangoCon US 2024 talk preparation (fetched). [ryancheley.com/2024/10/17/djangocon-us-2024-talk](https://ryancheley.com/2024/10/17/djangocon-us-2024-talk/)
12. Speaker Agency UK. How much does a keynote speaker cost, 2026 (fetched). [speakeragency.co.uk/blog/how-much-does-a-keynote-speaker-cost-2026](https://www.speakeragency.co.uk/blog/how-much-does-a-keynote-speaker-cost-2026)
13. Cole B. Speaking fees and expenses (fetched). [mentalgamecoach.com/SpeakingFeesAndExpenses.html](https://www.mentalgamecoach.com/SpeakingFeesAndExpenses.html)
14. DEOC mailing list, speaker fees/workshop fees, April 2023 (snippet; fetch refused). [lists.ctc.edu/pipermail/deoc_lists.ctc.edu/2023-April/000694.html](https://lists.ctc.edu/pipermail/deoc_lists.ctc.edu/2023-April/000694.html)
15. Outspoken Agency. What's in a speaker fee? 2023 (fetched). [outspokenagency.com/blog/2023/4/18/the-more-you-know-whats-in-a-speaker-fee](https://outspokenagency.com/blog/2023/4/18/the-more-you-know-whats-in-a-speaker-fee)
16. Simon P. Services and rates (fetched). [philsimon.com/services-rates](https://www.philsimon.com/services-rates/)
17. BigSpeak. FAQ about online speaking events (fetched). [bigspeak.com/planning-tool/frequently-asked-questions-about-online-speaking-events](https://www.bigspeak.com/planning-tool/frequently-asked-questions-about-online-speaking-events/)
18. Kaltura. Speaker fees for virtual events (fetched). [corp.kaltura.com/blog/speaker-fees-for-virtual-events](https://corp.kaltura.com/blog/speaker-fees-for-virtual-events/)
19. Futurists Speakers. Keynote speaker fees list (60-90% virtual figure; snippet). [futuristsspeakers.com/keynote-speaker-fees-list-prices-costs-futurist](https://www.futuristsspeakers.com/keynote-speaker-fees-list-prices-costs-futurist/)
20. deutsche-startups.de. Dein Weg zum Keynote-Speaker, 2019 (fetched). [deutsche-startups.de/2019/05/10/dein-weg-zum-keynote-speaker](https://www.deutsche-startups.de/2019/05/10/dein-weg-zum-keynote-speaker/)
21. Centre Hubertine Auclert. Grille tarifaire formations 2026 (fetched PDF). [centre-hubertine-auclert.fr/.../Grille tarifs formation 2026.pdf](https://www.centre-hubertine-auclert.fr/sites/default/files/medias/Grille%20tarifs%20formation%202026.pdf)
22. Comue de Toulouse, Médiad'Oc. Note au CA du 14 mars 2025, modification de tarifs (fetched PDF). [univ-toulouse.fr/.../2025-010_CA_ComueTlse_14.03.2025_note_Modif_tarifs MediadOc.pdf](https://www.univ-toulouse.fr/sites/default/files/INSTANCES/2025-010_CA_ComueTlse_14.03.2025_note_Modif_tarifs%20MediadOc.pdf)
23. Tensoria. Prix d'une formation IA en entreprise, Aug 2026 (fetched; cites ORSYS, Cegos, Flowt, Kaliio, OPCO Atlas, Mister IA). [tensoria.fr/blog/prix-formation-ia-entreprise](https://tensoria.fr/blog/prix-formation-ia-entreprise)
24. Comparateur-ia.com. Formez vos équipes à l'IA, June 2026 (fetched). [comparateur-ia.com/ai-training](https://comparateur-ia.com/ai-training/)
25. FranceFG. Former ses salariés à l'IA, rentrée 2026 (fetched). [francefg.fr/former-salaries-ia](https://francefg.fr/former-salaries-ia/)
26. Dawan. IA pour les managers: initiation, programme PDF (fetched). [dawan.fr/.../ia-pour-les-managers-initiation.pdf](https://www.dawan.fr/formations/intelligence-artificielle/ia-et-management/ia-pour-les-managers-initiation.pdf)
27. Haufe Akademie. Mit KI erfolgreich Schulungen vorbereiten und gestalten (fetched). [haufe-akademie.de/42131](https://www.haufe-akademie.de/42131)
28. Haufe Akademie. ChatGPT Advanced im Steuer- und Rechnungswesen (snippet). [haufe-akademie.de/41310](https://www.haufe-akademie.de/41310)
29. Global Knowledge UK. Generative AI Award (fetched). [globalknowledge.com/en-gb/courses/data_and_ai/artificial_intelligence/genai-award](https://www.globalknowledge.com/en-gb/courses/data_and_ai/artificial_intelligence/genai-award/v/langen)
30. Tutorials.co.uk. Train your team (fetched). [tutorials.co.uk/train-your-team](https://www.tutorials.co.uk/train-your-team)
31. We Call Shotgun (formerly Spicy Advisory). AI training cost UK 2026, July 2026 (fetched; vendor page, market bands cited from SoftBlues). [wecallshotgun.com/blog/ai-training-cost-uk-2026](https://wecallshotgun.com/blog/ai-training-cost-uk-2026)
32. We Call Shotgun. AI consulting costs UK 2026, Aug 2026 (fetched; vendor page). [wecallshotgun.com/blog/ai-consulting-costs-uk-2026](https://wecallshotgun.com/blog/ai-consulting-costs-uk-2026)
33. ITJobsWatch. Trainer contracts, UK, 6 months to 17 Oct 2026 (fetched). [itjobswatch.co.uk/contracts/uk/trainer.do](https://www.itjobswatch.co.uk/contracts/uk/trainer.do)
34. TJMètre. Baromètre TJM freelance 2026 (fetched 17 Oct 2026; small n per line, publication threshold inconsistently applied). [tjmetre.fr/barometre](https://tjmetre.fr/barometre)
35. 2iPortage. Baromètre des tarifs freelances et consultants, Dec 2025 (fetched). [2iportage.com/barometre-des-tarifs-freelances-et-consultants](https://www.2iportage.com/barometre-des-tarifs-freelances-et-consultants/)
36. Olhesashvili L. TJM moyen sur Malt par métier en 2026. profil-score.com, Jan 2026 (fetched; compiled estimate, not an official Malt report). [profil-score.com/guides/tjm-moyen-par-metier-malt](https://profil-score.com/guides/tjm-moyen-par-metier-malt)
37. BDVT. Honorarempfehlung 2020 für Training, Beratung und Coaching (fetched PDF; a 2024 edition exists but was not retrieved). [berlin.de/.../honorarempfehlung-training-coaching_2020.pdf](https://www.berlin.de/sen/europa/_assets/srvice/projektfoerderung/honorarempfehlung-training-coaching_2020.pdf)
38. Knab. Wat verdient een zzp-coach of trainer in 2026? (fetched). [bieb.knab.nl/ondernemen/wat-verdient-een-coach-trainer-zzp-bekijk-het-uurtarief-en-de-winst](https://bieb.knab.nl/ondernemen/wat-verdient-een-coach-trainer-zzp-bekijk-het-uurtarief-en-de-winst)
39. International Coaching Federation / PwC. 2023 ICF Global Coaching Study, executive summary (fetched PDF). [coachingfederation.org/.../2023ICFGlobalCoachingStudy_ExecutiveSummary.pdf](https://coachingfederation.org/app/uploads/2023/04/2023ICFGlobalCoachingStudy_ExecutiveSummary.pdf)
40. London Film Workshops. AI Fundamentals for Filmmaking (fetched). [lfw.org.uk/course/introduction-to-ai](https://lfw.org.uk/course/introduction-to-ai/)
41. National Film School of Denmark. Mastering AI for European Film Professionals (fetched). [filmskolen.dk/en/courses/mastering-ai-for-european-film-professionals-1](https://www.filmskolen.dk/en/courses/mastering-ai-for-european-film-professionals-1)
42. NTU/NIE Singapore. CVP0001 Suno AI music for content creators (fetched). [ntu.edu.sg/nie/admissions/continuing-education-training/cvp0001](https://www.ntu.edu.sg/nie/admissions/continuing-education-training/cvp0001)
43. Emphasis (writing-skills.com). Superhuman writing with AI, individual online, 2025 (snippet; PDF 404). [writing-skills.com/.../Superhuman_writing_AI_Individual–Online-2025-02.pdf](https://www.writing-skills.com/wp-content/uploads/2025/03/Superhuman_writing_AI_Individual–Online-2025-02.pdf)
44. UBC Instructional Skills Workshop. Our facilitators (snippet). [blogs.ubc.ca/tatrainingworkshops/our-facilitators](https://blogs.ubc.ca/tatrainingworkshops/our-facilitators/)
45. UUA Our Whole Lives. What is a good facilitator-to-participant ratio? (snippet). [uua.org/re/owl/faq/sexualityfaith/154595.shtml](https://www.uua.org/re/owl/faq/sexualityfaith/154595.shtml)
46. State Library of North Carolina. Toolkit for digital readiness, workshop structure and staffing (snippet). [statelibrary.ncdcr.gov/hwg-structure-and-staffing/download](https://statelibrary.ncdcr.gov/hwg-structure-and-staffing/download)
47. Stripe. Tarifs, France (fetched). [stripe.com/fr/pricing](https://stripe.com/fr/pricing)
48. Stripe. Pricing, UK (fetched). [stripe.com/gb/pricing](https://stripe.com/gb/pricing)
49. Maven. Expert / instructor policy guidebook (fetched). [help.maven.com/en/articles/12240853](https://help.maven.com/en/articles/12240853-maven-instructor-policy-guidebook)
50. Teachable. Pricing (fetched). [teachable.com/pricing](https://teachable.com/pricing)
51. Thinkific. Pricing (fetched, EUR display). [thinkific.com/pricing](https://www.thinkific.com/pricing/)
52. Schoolmaker. Podia pricing in 2026 (snippet; third-party). [schoolmaker.com/blog/podia-pricing](https://schoolmaker.com/blog/podia-pricing)
53. Eventbrite Help. How much does Eventbrite cost? article 755615, en-GB (fetched). [eventbrite.co.uk/help/en-gb/articles/755615](https://www.eventbrite.co.uk/help/en-gb/articles/755615/[slug]/)
54. Zipcube. Salle de réunion, Paris 15e (fetched). [zipcube.com/fr/ap/meeting/mg1ye432pfeo](https://www.zipcube.com/fr/ap/meeting/mg1ye432pfeo)
55. Zipcube. Location de salles de réunion Paris (snippet). [zipcube.com/fr/salle-de-réunion/paris](https://www.zipcube.com/fr/salle-de-r%C3%A9union/paris)
56. FMSH. Tarifs 2025 Maison Suger, salles de réunion (snippet). [fmsh.fr/.../Tarifs 2025 Maison Suger - salles de réunion.pdf](https://www.fmsh.fr/sites/default/files/media/files/Tarifs%202025%20Maison%20Suger%20-%20salles%20de%20r%C3%A9union.pdf)
57. Terrence Higgins Trust. Cally Yard meeting room hire (fetched). [tht.org.uk/get-help/head-office/cally-yard-meeting-room-hire](https://www.tht.org.uk/get-help/head-office/cally-yard-meeting-room-hire)
58. Zipcube. Speak Up London training rooms (snippet). [zipcube.com/uk/venues/speak-up-london/4615](https://zipcube.com/uk/venues/speak-up-london/4615)
59. CPAG. Room hire (snippet). [cpag.org.uk/training-and-events/room-hire](https://cpag.org.uk/training-and-events/room-hire)

[R] Earlier review, 2026-10-17: an earlier internal pricing review (not published) (its own references 1-26 are not repeated here; its items are in the YAML with their evidence labels).
