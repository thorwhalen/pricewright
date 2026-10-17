# Travel, time overhead and expenses

`pricewright.travel` implements the formula in section 1 below with the defaults in its table (`TravelPolicy`). The rule: **on site = core fee + a separate travel line**; the core fee covers the home city. Present the formula and a worked example in every quote that involves travel, and list cancellation terms next to it. The evidence (baseline 2026-10-17) follows.

---


Research packet for the pricing calculator, specialty `travel`. Observed 2026-10-17. Europe (FR, UK, DE, NL) first, US for contrast. Every number below has a source; where a source was only seen as a search snippet, the claim is marked **(snippet)**; claims from a page that was actually read are marked **(fetched)**. Nothing here is invented: where no source was found, the gap is stated.

## 1. The standard practice, as a formula

The pattern across all four professions is the same: **the core fee prices the work; on-site delivery adds a separately quoted travel block made of (a) time overhead and (b) expenses at cost or at an official flat rate.** The calculator should model on-site as `core fee + travel block`, and online as `core fee × online factor`, rather than as two unrelated prices.

```
onsite_total  = core_fee
              + travel_time_fee
              + nights × (hotel_cap_or_actual)
              + days_away × per_diem
              + transport (at cost, or km × mileage_rate)
              + equipment_transport (crews)
              + expense_markup × reimbursables

travel_time_fee (per one-way leg, t = door-to-door hours):
    t <= free_threshold_h                   -> 0
    travel on a working day                 -> (t - free_threshold_h) × hourly_rate × travel_rate_factor
    travel on a dedicated travel day        -> max(travel_day_min_h, t) × hourly_rate × travel_rate_factor,
                                               capped at travel_rate_factor × day_rate
    hourly_rate = day_rate / day_hours

nights = onsite_days - 1 + (arrive_night_before ? 1 : 0)
arrive_night_before = (start_time < same_day_latest_start AND t > overnight_threshold_h)
                      OR t > max_travel_h_same_day_as_work
                      OR flight_h > no_work_flight_h

online_total  = core_fee × online_factor        (no travel block)
```

### Default parameters (and range seen)

| Parameter | Default | Range seen | Basis |
|---|---|---|---|
| `free_threshold_h` (travel absorbed, per leg) | 1 h | 0 to 1 h; "local" work unbilled | APA first hour of each leg unpaid [1]; Talan first hour never billable [2]; short local trips unbilled [3][4] |
| `travel_rate_factor` (share of rate paid for travel time) | 0.5 | 0 to 1.0 | Travel day = half day rate [5][4]; consultants 50–75% [6][7]; Talan 50% (100% in business hours on long trips) [2]; crews in UK/US paid at straight (1.0) hourly time [1][8]; ~half of German consultancies include travel in the day fee, 1 in 5 bill it fully [9] |
| `travel_day_min_h` (minimum paid on a travel-only day) | 4 h (= half day) | 4 to 5 h; max 8 h | IATSE commercial travel-only day 4–8 h straight time [8]; APA travel on non-shooting day minimum 5 h [1] |
| `day_hours` | 8 | 8 to 12 | APA, IATSE 8 h basis [1][8]; one UK crew's day rate covers up to 12 h [5] |
| `overnight_threshold_h` (one-way) | 1.5 h | 1.5 to 3 h | URSSAF grand déplacement test: ≥50 km and ≥1h30 by public transport [10]; Talan lodging billed >1h30 one-way, multi-day [2]; speakers bureau: >3 h strongly favours overnight [11] |
| `same_day_latest_start` (else arrive the night before) | 11:00 | — | Speakers Bureau of Canada: morning events require arrival the evening before; same-day drive-and-present only if start after 11:00 [11] |
| `max_travel_h_same_day_as_work` | 4 h | 4 h | SBC: avoid >4 h travel per day around an engagement [11]; APA: flight >4 h means no shooting that day [1] |
| `no_work_flight_h` (rest day after long flight) | 8 h | 8 h | APA: flight >8 h means no shooting until 24 h after arrival [1] |
| Air class | economy | economy (refundable) to business for top-tier | Talan non-refundable economy [2]; SBC highest economy, business only for fees ≥ CA$25k [11]; IATSE "not less than coach" [8]; speakers sometimes business/first [12] |
| `expense_markup` | 0% | 0% to 15% | Talan states none [2]; French practice: at cost or with a margin if agreed [13]; AICP-discussed bid terms cap handling at 15% [14] |
| Speaker travel buyout (flat, alternative to at-cost) | none (at cost) | US$1,000 to 5,000 | Key Speakers Bureau [15] |
| Half-day fee as share of day fee | 0.5 | 0.5 to 0.55 | UK training price sheets £900/£1,750 and £1,000/£2,000 [16]; half-day minimum advice [17] |
| `online_factor` (training/workshop core fee) | 1.0 | 0.5 to 1.2 | Same content and value online, no discount [18]; one vendor prices virtual 21% above on-site [19]; some discount online [19] |
| `online_factor` (keynote/talk) | 0.7 | 0.5 to 1.0 | Bureaus report virtual at ~50%, ~70%, 60–90%, 75–100% of in-person [20]; "10–50% cheaper" [15] |

Cancellation (separate from the formula, but quoted alongside travel): default **crew** tiers ≥7 days 0%, 4–6 days 50%, 2–3 days 75%, day before 100% [1]; default **speaker/trainer** 50% deposit at signing, non-refundable, 100% due if the client cancels within 60 days [15][21]; any travel already booked is payable on top [21][22].

## 2. Travel time billing: evidence

**Film and video crews (UK).** The APA Recommended Crew Terms (July 2018) are the most explicit document found **(fetched)** [1]: travel time is "always paid at single time, regardless of time, or day of the week"; on working days the crew is paid for travel "less the first hour of the outward and homeward journey, at your basic hourly rate"; a travel-only (non-shooting) day is paid hourly "subject to a minimum of five hours"; if travel plus work totals under 11 hours no travel time is payable; collecting equipment counts as working time; flights over 4 h mean no shooting that day, over 8 h no shooting for 24 h after arrival. A 2023 Bectu rate card states "Travel days are Working Days" and that the daily rate excludes travel, accommodation and subsistence, which are charged at Bectu's travel and subsistence rates **(snippet)** [23].

**Film crews (US).** Under the IATSE commercial agreement as summarised by Wrapbook (2022, citing the 2019 AICP–IATSE agreement) **(fetched)** [8]: travel-only days are paid at straight time for a minimum of 4 and a maximum of 8 hours; daily travel to and from housing is capped at one hour, beyond which it is work time; outside the LA 30-mile zone, mileage at the IRS rate plus travel time at the regular hourly rate; commercial jet travel not less than coach; per diem only for meals not provided. The DGA commercial schedule counts travel within the work day for those starting outside LA/NYC **(snippet)** [24].

**Freelance crew and photographers.** One UK crew's published terms: "Travel Days are charged at half Day Rate. ALL travel time is chargeable" **(fetched)** [5]. A UK photographers' agent: "The standard practice is to charge your travel fees at roughly 50% of your basic shoot rate", pro-rata on an 8-hour day, and local (within the M25) shoots carry no travel fee **(fetched)** [4]. Forum reports: camera operators at 50%, photographers 70% when flying, hirers paying 50–75% **(snippet)** [7].

**Management consultants.** Talan's published T&E policy **(fetched)** [2]: the first hour of a start- or end-of-day commute is never billable; outside Quebec, on 100–150 km trips time beyond the first hour is billed at 50%; beyond 150 km, 50% outside business hours and 100% during them. The German BDU fee study (about 190 firms, survey July–September 2022, published January 2023) **(snippet)** [9]: for almost half of consultancies travel time is already included in the day fee; one in three bills only part of the travel time; one in five bills it in full; smaller firms include it more often. US guidance sites put travel time at 50–75% of the hourly rate, with law firms billing full rate **(snippet)** [6].

**Freelance trainers / formateurs (France).** No French source gave a percentage or a half-day rule **(fetched)** [3]. Lefreelance.fr recommends separating time from transport expenses, naming a "forfait temps de trajet", and notes a travel rate can be set below the service rate; its worked example (600 € HT/day, 2 h round trip) adds 150 € per visit, i.e. the 2 h of travel billed at the full hourly equivalent (75 €/h) [3]. French trainer rate tables are quoted "hors TVA et hors frais de déplacement/hébergement" **(snippet)** [25]. A French freelance forum view is that under a TJM a travel day is a paid day **(snippet)** [25].

**Speakers.** Bureaus quote travel separately from the fee: either the speaker invoices actual costs, or a flat "travel buyout" of US$1,000–5,000 covering flights and home-city ground transport, with the client booking the hotel and local transport **(fetched)** [15]. SPEAKING.com: travel and lodging are "in addition to the speaker honorarium", flat fee negotiable, international fees "generally 50% to 100% higher due to extra travel time" **(fetched)** [12]. No bureau source quoted a separate per-day "travel day fee"; the time cost is folded into the fee or the international uplift.

## 3. Overnight stays

URSSAF presumes a worker cannot return home daily when the one-way distance is ≥50 km **and** public transport takes ≥1h30 **(fetched, secondary summary)** [10]. Talan bills lodging for trips of more than one day to places more than 1h30 one-way **(fetched)** [2]. Speakers Bureau of Canada (2026) **(fetched)** [11]: morning events require arriving the evening before; full-day, evening or winter events may justify two nights; >3 h away strongly favours an overnight; hotels capped at CA$250/night (standard city) and CA$400 (big cities), plus tax; the host may book hotel and ground transport but not flights. Key Speakers: the client usually books the event-city hotel [15]. IATSE: if a day exceeds 16 h including travel and the location is more than 30 miles beyond the zone, the employer must offer a hotel or return transport [8].

## 4. Per diem and subsistence: official defaults

**France, URSSAF 2026** (exemption ceilings, per meal / per day) **(snippet of urssaf.fr; corroborated, fetched, by [10])** [26]: meal at restaurant while travelling 21,40 €; meal outside a restaurant 10,40 €; grand déplacement, first 3 months: meal 21,40 €, lodging + breakfast 76,60 € (Paris, 92, 93, 94) and 56,80 € (other départements); months 4–24: meal 18,20 €; months 25–72: meal 15,00 €. Lodging step-downs differ slightly between sources (65,10 / 48,30 € per the urssaf.fr snippet vs 64,26 / 47,69 € per [10]); use the first 3-month tier, which is the one any short engagement falls in. Audiovisual: the cinema/advertising production convention (IDCC 3097) set the meal allowance at 18,56 € and casse-croûte at 7,54 € in its 2024 salary amendment **(snippet)** [27].

**Germany 2026** **(fetched, secondary)** [28]: Verpflegungsmehraufwand 14 € for >8 h away or arrival/departure day, 28 € per full 24 h day, nothing ≤8 h; reductions when meals are provided: breakfast 5,60 €, lunch or dinner 11,20 € each; Übernachtungspauschale 20 €/night without receipts (actual hotel cost reimbursable with receipt, breakfast 5,60 € deducted); car 0,30 €/km actually driven.

**UK, HMRC benchmark scale rates** (current, under EIM30240) **(snippet)** [29]: £5 for qualifying travel ≥5 h, £10 for ≥10 h, £25 for ≥15 h continuing past 8 pm, plus a £10 supplement when a 5 h or 10 h journey runs past 8 pm; no receipts needed at benchmark rates since 6 April 2019. The older 2009–2016 table (breakfast £5, one meal £5, two meals £10, late evening £15) and the absence of any HMRC benchmark for overnight subsistence are **(fetched)** [30]. UK trainer suppliers state "Travel & Subsistence is charged at the standard HMRC rate" **(snippet)** [16].

**EU Commission missions (intra-EU)** **(fetched, secondary)** [31]: daily allowance / hotel ceiling: France 127 € / 212 €; Germany 123 € / 154 €; Netherlands 137 € / 190 €; Belgium 132 € / 171 €. The same France and Germany figures are attributed to Commission Delegated Regulation (EU) 2025/693 **(snippet)** [32], while [31] says the figures have not changed since 2017; the dating is unresolved, the values agree.

**US, GSA** **(fetched, secondary)** [33]: FY2027 (1 Oct 2026 – 30 Sep 2027) standard CONUS lodging US$113/night (a ceiling, actual cost reimbursed up to it), M&IE US$68/day; FY2026 was US$110 / US$68 **(snippet)** [34]. Non-standard-area M&IE tiers stay at US$68–92 [33].

**Private-sector comparators.** Talan: US$100/day meals (20 / 25 / 55) **(fetched)** [2]. Speakers Bureau of Canada: CA$150/day per speaker **(fetched)** [11].

## 5. Transport

**Rule.** At cost is the norm for rail and air (economy) [2][11][12][15]; car use is reimbursed per km/mile at an official or rate-card figure; tolls, congestion charges and parking pass through at cost [5]. Speaker flat buyouts are the main flat-fee exception [15].

**Mileage rates.**

| Country | Rate | Year / status | Evidence |
|---|---|---|---|
| France | 0,636 €/km (5 CV), 0,697 €/km (7 CV+), up to 5,000 km/yr; 3 CV 0,529, 4 CV 0,606, 6 CV 0,665; +20% for electric | barème 2026 (revenus 2025), frozen since 2023 | fetched [35] |
| UK | 45p/mile first 10,000 miles, 25p after | unchanged since 6 April 2011 | snippet [36] |
| UK crew rate cards | 50p/mile (APA 2018), 51p (Bectu commercials 2021), 55p (one freelance crew) | rate cards | fetched [1][5]; snippet [23] |
| Germany | 0,30 €/km actually driven | 2026 | fetched [28] |
| Netherlands | 0,25 €/km untaxed (was 0,23 €) | from 1 Jan 2026, retroactive | fetched [37] |
| US | 72.5 ¢/mile (70 ¢ in 2025) | 2026, IR-2025-128 | fetched [38]; a mid-year rise to 76 ¢ from 1 July 2026 is reported **(snippet, unverified on irs.gov)** [39] |

**Markup on expenses.** Talan's policy states none [2]. French guidance: refacturation at the exact amount or with a margin, as agreed with the client beforehand **(snippet)** [13]. German consultancies: one in three bill travel costs as a lump sum, about one in five as a percentage, 21% include them in the day fee, and the average travel-cost surcharge is 11% per consultant day **(snippet)** [9]. US commercial production: bid terms analysed by the AICP cap handling on cost-plus items at 15% **(snippet)** [14].

## 6. Minimum engagement, cancellation, deposits

**Minimums.** UK training providers price a half day at about half the day fee (£900 vs £1,750; £1,000 vs £2,000 + VAT), with travel extra **(snippet)** [16]; a UK freelance trainer suggests a minimum charge of half a day **(snippet)** [17]. Crews: travel-only days carry a 4 h (IATSE) or 5 h (APA) minimum [8][1].

**Cancellation tiers.**

| Source | Tiers | Evidence |
|---|---|---|
| APA crew terms (UK, 2018) | ≥7 days: 0%; 6–4 days: 50%; 3–2 days: 75%; day before: 100%; engagements ≤3 days treated as a whole | fetched [1] |
| UK freelance crew terms | <2 weeks: 25%; <7 days: 50%; <48 h: 100% | fetched [5] |
| Bectu TV editors (2019) | 50% for up to 2 weeks if cancelled with <2 business days' notice | snippet [40] |
| Bectu photographic technicians (2024) | 100% of the booking incl. expenses; date change = cancellation | snippet [40] |
| Speakers bureau contract (US) | deposit forfeited >60 days; full fee due ≤60 days | snippet [21] |
| Key Speakers (US) | 50% deposit with signed agreement; balance ≥2 weeks before; full payment soon after signing if the event is within a month | fetched [15] |
| UK council training service | late cancellation: full fee plus travel/hotel already incurred | snippet [22] |

## 7. Online vs on-site differential

The evidence splits by profession. **Workshops/training:** the content fee is often unchanged online, and the on-site price is higher because of travel time, not content. Bernoff keeps the same price online (same value, same demand) and adds an in-person premium of about US$2,000 plus travel; his online format is two 90-minute sessions vs one 3.5–4 h day, with groups capped at 20 online vs 40 in person **(fetched)** [18]. One vendor prices virtual above on-site (US$3,400 vs US$2,800 for a one-day class) while another lists online below in-person **(snippet)** [19]. 12% of German consultancies offer specific remote day rates **(snippet)** [9]. **Speakers:** bureaus report virtual at about 50% of in-person, about 70% (from 2020 experience), 60–90%, or 75–100% for top names **(snippet)** [20]; Key Speakers says virtual is "10–50% cheaper" **(fetched)** [15]. **Personal fitness trainers** (a different market) cut 50–80% for virtual during COVID **(fetched)** [41]; treat as an outlier. Reasoning given: no travel time, shorter sessions, smaller groups, less time commitment [18][20].

## 8. Equipment transport for crews

No source gave numbers for excess baggage, carnet fees or hire-vs-fly. Qualitative practice **(snippet)** [42]: an ATA carnet is the safer route for temporary import of camera, lighting, sound and drone kit (re-export within 12 months; consumables excluded); hiring bulky items (e.g. tripods) locally is often cheaper and "you will probably save money and stress"; lithium batteries over 160 Wh are banned on passenger flights and most must travel in the cabin; excess-baggage charges are routine and inconsistently applied. Collecting or delivering equipment counts as working time for UK crew [1]. Model as `equipment_transport = excess_baggage + carnet + local_hire` with all three user-entered; no defaults are sourceable.

## Gaps

No source found for: a French or German film-crew Reisetag/temps de trajet rule (IDCC 2642 and TV FFS texts were not retrieved); a published Malt rule on travel; current Bectu outside-broadcast T&S figures; carnet and excess-baggage prices.

## REFERENCES

1. [APA Recommended Crew Terms, July 2018 (UK)](https://www.a-p-a.net/content/uploads/2018/06/APA-Recommended-Crew-Terms-July-2018-FULL-copy.pdf). Fetched (PDF text extracted).
2. [Talan, Travel and Expense Policy](https://www.talan.com/americas/en/about-us/contractual-policies/travel-and-expense-policy). Fetched.
3. [Le Freelance, Temps de trajet en freelance : comment le facturer au client ?](https://lefreelance.fr/articles/facturer-temps-trajet-freelance/). Fetched.
4. [Lisa Pritchard Agency, Ask an Agent: how much to charge for travel time?](https://www.lisapritchard.com/blog/ask-an-agent-how-much-to-charge-for-travel-time). Fetched.
5. [DD Practical, Freelance Terms (UK crew)](https://www.practical.org.uk/freelance-terms/). Fetched.
6. [Harvest, How to charge for travel time as a contractor](https://www.getharvest.com/time-tracking/how-to-charge-for-travel-time-as-a-contractor); [Everhour, How to bill for travel time](https://everhour.com/calculators/how-to-bill-for-travel-time). Snippet.
7. [Cinematography.com, Travel Day Rate](https://cinematography.com/index.php?%2Fforums%2Ftopic%2F63116-travel-day-rate%2F=); [DPReview, Rate for Travel Days](https://www.dpreview.com/forums/threads/rate-for-travel-days.3009241/); [MetaFilter, How much to charge for travel time?](https://ask.metafilter.com/38736/How-much-to-charge-for-travel-time). Snippet.
8. [Wrapbook, Inside the Zone vs Outside: budgeting travel (2022, IATSE commercial)](https://www.wrapbook.com/blog/inside-the-zone-vs-outside-budgeting-travel). Fetched.
9. [BDU, Honorarstudie Reise- und Nebenkosten (2023)](https://www.bdu.de/media/356786/honorarstudie_reise-und-nebenkosten.pdf). Snippet (PDF returned 404 on fetch).
10. [BM Fiduciaire, Grands déplacements 2026 : indemnités repas et logement](https://www.bmfiduciaire.fr/lindemnite-grands-deplacements/). Fetched.
11. [Speakers Bureau of Canada, Travel Expenses policy (2026)](https://speakerscanada.com/travel-expenses/). Fetched.
12. [SPEAKING.com, Speakers Bureau Services FAQs](https://speaking.com/speakers-bureau-services-faqs). Fetched.
13. [Legalstart, Refacturation](https://www.legalstart.fr/fiches-pratiques/refacturation/). Snippet.
14. [AICP, Heineken Roster Criteria combined AICP analysis](https://aicp.com/assets/editor/HeinekenRosterCriteriaCombinedAICPAnalysis_FINAL.pdf). Snippet.
15. [Key Speakers Bureau, How much do motivational speakers cost?](https://keyspeakers.com/blog/how-much-do-motivational-speakers-cost/). Fetched.
16. UK training supplier price sheets on the G-Cloud 14 Digital Marketplace: [document 721195](https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/documents/721195/437721975530782-pricing-document-2024-05-05-2322.pdf), [document 722550](https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/documents/722550/873835059795318-pricing-document-2024-04-29-2106.pdf), [document 722208](https://assets.applytosupply.digitalmarketplace.service.gov.uk/g-cloud-14/documents/722208/156290316109925-pricing-document-2024-05-07-0831.pdf). Snippet; which figure comes from which sheet was not verified.
17. [TrainingZone, Charging a client](https://trainingzone.co.uk/?p=35746). Snippet.
18. [Josh Bernoff, Should workshops cost more in person?](https://bernoff.com/blog/should-workshops-cost-more-in-person). Fetched.
19. [InterSystems, Request virtual classroom training](https://intersystems.com/request-virtual-classroom-training-for-your-company); [College Board, AP Professional Learning pricing guide](https://apcentral.collegeboard.org/media/pdf/ap-professional-learning-pricing-guide.pdf). Snippet.
20. [BigSpeak, FAQ about online speaking events](https://www.bigspeak.com/planning-tool/frequently-asked-questions-about-online-speaking-events/); [All American Speakers, What we learned about virtual events in 2020](https://www.allamericanspeakers.com/blog/what-we-learned-about-virtual-events-in-2020/amp/); [Futurist Speakers, Keynote speaker fees list](https://www.futuristsspeakers.com/keynote-speaker-fees-list-prices-costs-futurist/); [Executive Speakers Bureau, How much does it cost to book a keynote speaker](https://www.executivespeakers.com/blog/how-much-does-it-cost-to-book-a-keynote-speaker). Snippet; attribution of each percentage to a specific bureau not verified.
21. [Simon & Shuster Speakers Bureau contract (City of Everett public record)](https://lfportal.everettwa.gov/WebLink/0/edoc/1607382/Simon%20%20Shuster%20Speakers%20Bureau%201282023.pdf); [Council on Foundations, Speaker Terms & Conditions](https://cof.org/node/8526). Snippet.
22. [Lancashire PCC, Remuneration Guidance 2026](https://www.lancashire-pcc.gov.uk/wp-content/uploads/2026/05/5-Remuneration-Guidance-2026.pdf). Snippet.
23. Bectu / Prospect rate cards: [2023/00363 (OB freelance terms)](https://library.prospect.org.uk/download/2023/00363), [2021/01291 (commercials)](https://library.prospect.org.uk/download/2021/01291). Snippet (fetch returned 404).
24. [DGA Commercial Rates 2026](https://edge.sitecorecloud.io/directorsguf4d4-dga2c79-dgaprod1615-f6e3/media/Files/Contracts/Commercial/DGACommercialRates2026_251111.pdf). Snippet.
25. [Travail-Industrie, fiche TJM formateur technique](https://travail-industrie.com/fiche-tjm/formateur-technique); [Free-Work forum, Facturation grand déplacement](https://www.free-work.com/fr/tech-it/forum/t/facturation-grand-deplacement). Snippet.
26. [URSSAF, Les frais professionnels](https://www.urssaf.fr/accueil/employeur/beneficier-exonerations/frais-professionnels.html). Snippet (direct fetch of urssaf.fr failed with connection reset).
27. [IDCC 3097, accord salaires techniciens 2024 (Tripalio)](https://presse.tripalio.fr/wp-content/uploads/2024/09/IDCC-3097-Accord-salaires-techniciens.pdf). Snippet.
28. [Taxmaro, Reisekostenpauschalen 2026](https://www.taxmaro.com/post/reisekostenpauschalen-2026). Fetched.
29. [HMRC EIM30240, payments at a benchmark rate](https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim30240); [Spendesk, HMRC meal allowance rates](https://www.spendesk.com/en-eu/blog/hmrc-meal-allowance-rates/). Snippet.
30. [HMRC EIM05231, table of benchmark scale rates (2009–2016)](https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim05231). Fetched.
31. [EU Employment, European Commission mission allowances and hotel ceilings](https://euemployment.eu/european-commission-mission-allowances-and-hotel-ceilings/). Fetched.
32. [Commission Delegated Regulation (EU) 2025/693](https://eur-lex.europa.eu/eli/reg_del/2025/693/oj/eng). Snippet (fetch returned empty).
33. [Texas Lodging, GSA releases FY 2027 per diem rates](https://texaslodging.com/fy-2027-per-diem-rates/); [GSA, FY 2027 per diem highlights](https://www.gsa.gov/system/files/FY2027perdiemhighlights.docx). Fetched (first), snippet (second).
34. [Federal Register, FTR Bulletin 26-01 (19 Aug 2025)](https://www.govinfo.gov/content/pkg/FR-2025-08-19/html/2025-15771.htm). Snippet.
35. [Moneyvox, Impôts 2026 : le barème kilométrique est gelé](https://www.moneyvox.fr/impot/actualites/108318/impots-2026-le-bareme-kilometrique-est-gele-pour-la-3eme-annee-consecutive). Fetched.
36. [UK SI 2011/896 (mileage allowance payments)](https://www.legislation.gov.uk/uksi/2011/896/made/data.html); [Makesworth Accountants, Mileage allowance payments](https://makesworth.co.uk/mileage-allowance-payments-the-maximum-tax-free-amount/). Snippet.
37. [Moore DRV, Onbelaste reiskostenvergoeding 2026](https://www.moore-drv.nl/onbelaste-reiskostenvergoeding-2026/). Fetched.
38. [IRS, IRS sets 2026 business standard mileage rate at 72.5 cents per mile](https://www.irs.gov/newsroom/irs-sets-2026-business-standard-mileage-rate-at-725-cents-per-mile-up-25-cents). Fetched.
39. [IFEBP, IRS increases 2026 standard mileage rates (14 July 2026)](https://www.ifebp.org/detail-pages/news/2026/07/14/irs-increases-2026-standard-mileage-rates). Snippet.
40. [Bectu, TV factual rate card 2019](https://members.bectu.org.uk/filegrab/pp-f-tv-factual-rate-card-2019-web.pdf?ref=2454); [Prospect library 2024/00816](https://library.prospect.org.uk/download/2024/00816). Snippet.
41. [Find Your Trainer, How to charge for virtual training](https://findyourtrainer.com/trainer-faqs/virtual-training/charge-virtual-training/). Fetched.
42. [Shooting People, Taking kit to Europe](https://shootingpeople.org/qna/q/taking-kit-to-europe); [Cinematography Mailing List, Travelling with equipment](https://cinematography.net/edited-pages/TravellingWithEquipment.htm); [Here Now Film](https://www.herenow.film/?p=3777); [Backstage, 9 tips for traveling with your film gear](https://www.backstage.com/magazine/article/tips-traveling-film-gear-1257/). Snippet.
