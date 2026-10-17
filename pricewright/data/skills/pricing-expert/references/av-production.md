# Audiovisual production

`pricewright.specialties.av_production` prices a film from twelve crafts (research, story and script, character design, look, storyboard and animatic, performance and voice, generation, selection and continuity, music, sound, edit, finishing). Each style in `STYLES` gives every craft a fixed part (once per film) and a part per finished minute. Review rounds, producing time (share of craft hours), variants, generation credits (finished seconds x shooting ratio x price per generated second), tools, music licence and voice talent are separate lines; usage on paid media is an uplift on the fee (`USAGE`). Pilots build a share of the setup at cost and are credited against the production; retainers reuse the setup and carry a commitment discount.

How to use the market for AV: compare like for like, same style and a runtime within 0.5-2x (`like_for_like`), and exclude tiers the client is not buying from (national broadcast, traditional crews) with `market: {exclude_ids: [...]}`. Per-minute rates are quoted for long-form; they do not scale down to 15-second spots. Labour, not credits, is the main cost: tools come to roughly 30-600 USD per finished minute.

Calibrate the `STYLES` table to the studio's own timesheets after the first jobs. The evidence (baseline 2026-10-17) follows.

---


Research packet for a two-person European studio (writer/documentary filmmaker + musician/AI engineer) making AI-assisted films with human-led story, look, performance, music and edit. Compiled 2026-10-17. Machine-readable comparables: `av-comparables.yaml` (same folder).

Conventions: prices are kept in their original currency, never converted. "Fetched" means the page itself was read; "snippet" means only search-engine text was seen; "secondary" means a figure reported by one source about another; "inferred" means arithmetic done here on sourced inputs (the inputs are cited). Most published price ranges come from vendors selling the service being priced; that bias is flagged where it matters. Where nothing could be sourced, the cell is left empty rather than guessed.

## 1. Synthesis

### 1.1 Benchmarks by style (traditional unless marked AI)

| Style | Benchmark | Unit | Region | Source | Evidence |
|---|---|---|---|---|---|
| Animated explainer, 1 min (all styles) | median $5,400, mean $10,983, range $600–$250,000 (Wyzowl survey, 242 companies, 2024) | per 1-min video | global/US | [1] | fetched (secondary) |
| Whiteboard explainer | $1,000–$2,000 | per minute | US | [1] | fetched (secondary, Blue Carrot) |
| Motion graphics explainer | $2,500–$3,000 | per 60 s | US | [1] | fetched (secondary) |
| 2D character animation | $2,000–$4,000 | per minute | US | [1] | fetched (secondary) |
| 3D animation | $4,000–$10,000 | per minute | US | [1] | fetched (secondary) |
| Premium 2D/3D, well-funded clients | $10,000–$25,000 | per 60 s | US | [2] | snippet |
| Motion design project, France | median €8,000, mean €12,245, range €600–€90,000 (155 projects) | per project | FR | [3] | snippet (page 403) |
| Corporate/company video, France | median €6,500, core €4,600–€15,000 (170+ projects, 2026 grid) | per project | FR | [4] | snippet (page 403) |
| Corporate video, UK | £1,000–£3,000 per finished minute (London +15–25%) | per finished minute | UK | [5] | snippet |
| Corporate/brand video, London agency | £4,000–£10,000 per minute | per minute | UK | [6] | snippet |
| TV commercial, small brand UK | £5,000–£30,000 | per spot | UK | [7] | snippet |
| TV commercial, regional/national UK live action | £30,000–£100,000; celebrity/bespoke music £100,000–£500,000+ | per spot | UK | [7] | snippet |
| 30 s commercial, US tiers | local $3,000–$15,000; regional $15,000–$50,000; national $50,000–$500,000+; celebrity $500,000–$1M+ | per spot | US | [8] | fetched |
| 30 s brand video, US agency | $15,000–$50,000+ | per video | US | [9] | fetched |
| 30 s spot, Italy (mid-market traditional) | €15,000–€60,000 (itemised €17,300–€58,500) | per spot | IT/EU | [10] | fetched |
| Music video, indie | $1,000–$10,000 | per video | US/global | [11] | snippet |
| Music video, professional / label | $5,000–$30,000 typical; label-backed regularly >$100,000; high-end $50,000–$500,000+ | per video | US | [11] | snippet |
| Documentary de création, France (CNC-aided, 2024) | €225.5k per hour (1,810 h aided) | per hour of runtime | FR | [12] | fetched |
| Animation TV, France (CNC-aided, 2024) | €931.6k per hour | per hour of runtime | FR | [12] | fetched |
| Fiction TV, France (CNC-aided, 2024) | €1,068.7k per hour | per hour of runtime | FR | [12] | fetched |
| BBC YouTube documentary strand (Aug 2026) | £50,000 per documentary, min 25 min, ~3 months delivery | per film | UK | [13] | snippet |
| Sizzle reel | $1,000–$3,000 / $4,000–$10,000 / $10,000+ | per reel | US | [14] | snippet |
| Animatic | $300–$3,000 per 30 s; $10–$100+ per second; ads $1,000–$3,000 | per project / per second | US | [14] | snippet |
| Social video retainer | $750–$2,000 / $2,000–$5,000 / $5,000–$10,000+ / $10,000–$20,000+ per month | per month | US | [15] | fetched |
| Social video per asset | $500–$1,500 per reel with guaranteed monthly volume | per asset | US | [15] | fetched |
| AI 30 s commercial (studio) | Lemonlight from $5,000; 1BVP $7,500 flat incl. paid/web/broadcast usage; MaiDreamsLab €2,000–€4,500 | per spot | US / IT | [9], [16], [10] | fetched |
| AI commercial market tiers | AI-native agency $2,000–$9,000 per 30 s (5–14 days); hybrid AI studio $15,000–$75,000 (3–8 weeks) | per spot | US | [16] | fetched |
| AI commercial tiers, Italy | freelance €300–€1,000 (single shot, no post, no licence); mid-market studio €1,500–€3,500 (15–60 s); premium €5,000–€15,000 (60 s+, custom characters, multi-language) | per spot | IT/EU | [10] | fetched |
| AI comedy series episode | from €5,000 per episode | per episode | IT/EU | [10] | fetched |
| AI turnkey cinematic | $500–$12,000 per finished minute (YOPRST) | per finished minute | global | [17] | fetched |
| AI short films (documented) | $315–$750 per finished minute, $750–$5,000 total (tool/credit-centred) | per finished minute | global | [18] | fetched |
| AI freelance video | $500–$5,000 per project ($500–$3,000 single video) | per project | US | [9] | fetched |
| Fiverr AI commercials | listing starts $30–$4,875; Fiverr Pro agency $5,000–$10,000 scaled by 15/30/60 s | per gig | global | [19] | snippet |
| AI music video packages | visualizer $100–$300; lyric $200–$600; AI narrative $600–$1,200; hybrid $800–$1,500+; compute $250–$700 per finished video | per video | global | [20] | snippet |

Claimed AI savings vs traditional: Lemonlight about 60% (60–70% in FAQ) at "comparable quality" [9]; 1BVP's $7,500 "about 82% below" Clutch's $42,280 agency-project average [16]; MaiDreamsLab about 85–94% for a 30 s spot [10]; YOPRST "5–10 times" cheaper [17]; invideo up to 99.7% (vendor, tool-cost basis) [18]. Kalshi's NBA Finals AI ad: prompting cost "under $2,000"; comparable ads "hundreds of thousands of dollars"; director fee undisclosed [21]. Advids reports that agencies delivered the same quality at a 15% lower budget than the previous year thanks to AI tools (2025 survey) [22].

Reading: the credible AI-studio band for a finished, licensed 30 s commercial clusters at roughly €2,000–€4,500 (EU) and $5,000–$7,500 (US), about one-fifth to one-tenth of a small-to-mid traditional spot. The sub-$1,000 per minute figures are tool-cost-centred and exclude most human labour, licensing and revisions.

### 1.2 Effort: person-days per finished minute

| Style | Traditional | AI-assisted | Source |
|---|---|---|---|
| 2D animation (professional, 1 min) | 80–300 hours ≈ 10–37 person-days/min (inferred at 8 h/day) | | [23] snippet |
| Frame-by-frame animation, solo | 12–18 s finished per animator-week ≈ 3.3–5 weeks/min (animation only, excludes boards, voice, music, backgrounds) | | [23] snippet (forum) |
| Explainer (studio, 60–90 s), calendar | 4–8 weeks kickoff to delivery; 20 working days standard (TruScribe) | | [1] fetched |
| Simple motion graphic | 2–3 working days (excl. script/boards) | | [23] snippet |
| Documentary edit | 1 month of editing per 10 min finished ≈ 2 editor-days/min (inferred, ~21 working days/month); series: 16–18 weeks per 42 min, 20–24 weeks per 60 min ≈ 1.9–2.1 editor-days/min (inferred, 5-day weeks) | | [24] fetched |
| 30 s commercial, calendar | 30–44 working days traditional; typical :30 shoot 8 weeks | 5–7 days to broadcast master; first cut 3–5 days; "The Stillness" :30 in 7 days | [10] fetched, [25] fetched |
| Kalshi 30 s TV ad (Veo 3) | | 1 person × 2 days ≈ 4 person-days per finished minute (inferred); 300–400 generations for 15 usable clips | [21] fetched |
| AI 3-min animated episode | | 2 people × 2 days ≈ 1.3 person-days/min (inferred); 164 clips generated, 41 used | [18] fetched |
| AI 2-min brand film | | 1 person × 3 days ≈ 1.5 person-days/min (inferred) | [18] fetched |
| AI music video (YOPRST) | | ~40 h for 120 keyframe images + ~230 h animating transitions ≈ 270 h (runtime not given) | [17] fetched |
| Coca-Cola "Holidays Are Coming" 2025 | | ~100 people involved, 5 gen-AI specialists, >70,000 clips, about one month (vs a year) | [26] snippet |
| 30 s AI spot (Italy) | | five production days (spec spot) | [10] fetched |

Iteration ratios reported: 300–400 generations per 15 kept clips, i.e. 20–27 generations per kept shot (Kalshi) [21]; 164 → 41, i.e. 4 generations per kept clip, "budget about 3 generations per usable shot" (invideo, vendor) [18]; MindStudio planning estimate 300–500 s raw footage for a 3-min short, i.e. about 1.7–2.8:1 by seconds (projection, not a case) [27]; Coca-Cola >70,000 clips for a campaign film [26]. The spread is wide: craft-quality broadcast work sits near 20:1 or above; vendor-reported social/animated work near 3–4:1.

### 1.3 Generation tool cost per finished minute

Per-second list prices (USD unless stated):

| Tool / model | Price | Source | Evidence |
|---|---|---|---|
| Google Veo 3.1 Standard (Gemini API, with audio) | $0.40/s 720p–1080p; $0.60/s 4K | [28] | fetched |
| Veo 3.1 Fast | $0.10/s 720p; $0.12/s 1080p; $0.30/s 4K | [28] | fetched |
| Veo 3.1 Lite | $0.05/s 720p; $0.08/s 1080p | [28] | fetched |
| Lyria 3.5 full song (Gemini API) | $0.08 per song | [28] | fetched |
| Runway API (credit = $0.01) | Gen-4.5 12 cr/s ($0.12/s); Gen-4 Turbo 5 cr/s; Aleph 2 28 cr/s; Kling 3.0 Pro 12/17 cr/s (no audio/audio); Kling 3.0 4K 43 cr/s; Veo 3.1 40/20 cr/s (audio/no audio); Seedance 2 36–150 cr/s; ProRes +5 cr/s, HDR +20 cr/s | [29] | fetched |
| Runway app plans | Standard $15/mo (625 cr), Pro $35 (2,250 cr), Max $95 (9,500 cr); Gen-4.5 12 cr/s | [30] | fetched |
| Kling API direct | $0.06–$0.42/s across plans (aggregator, Aug 2026) | [31] | snippet |
| OpenAI Sora 2 / Sora 2 Pro API | $0.10/s (720p); Pro $0.30/s 720p, $0.50/s 1024p, $0.70/s 1080p; batch half price. Reported shut down 2026-09-24 per OpenAI deprecation notice; not on OpenAI's current pricing page | [32] | fetched (secondary) |
| Luma Ray3.2/3.14 | 4 cr/s draft; 10 cr/s 540p; 20 cr/s 720p; 80 cr/s 1080p; Plus $30/mo 10,000 cr, Pro $90/40,000, Ultra $300/150,000 | [33] | fetched |
| Midjourney | Basic $10, Standard $30, Pro $60, Mega $120/mo (3.3/15/30/60 fast GPU h); video consumes fast hours; no official per-second price | [34] | snippet |
| ElevenLabs | Starter $6/mo 30k cr; Creator $22 121k; Pro $99 600k; Scale $299 1.8M; Business $990 6M; ~1 min TTS per 1,000 credits; music 900 cr/min | [35] | fetched |
| Suno | Pro $8/mo (2,500 cr), Premier $24/mo (10,000 cr); commercial use on paid plans | [36] | fetched |
| Udio | Standard $10/mo, Pro $30/mo; commercial rights reported on Pro only; download restrictions after 2025 UMG settlement | [37] | snippet |
| OpenAI gpt-image-2 | $30 per 1M image output tokens | [38] | fetched |

Inferred generation cost per finished minute = 60 s × shooting ratio (generated s / kept s) × price per second. Generation only; excludes images, voice, music, upscaling, failed renders on some APIs, and all labour.

| Model | at 4:1 | at 10:1 | at 25:1 |
|---|---|---|---|
| Veo 3.1 Standard 1080p ($0.40/s) | $96 | $240 | $600 |
| Veo 3.1 Fast 1080p ($0.12/s) | $29 | $72 | $180 |
| Kling 3.0 Pro with audio via Runway ($0.17/s) | $41 | $102 | $255 |
| Runway Gen-4.5 ($0.12/s) | $29 | $72 | $180 |
| Luma Ray 1080p on Plus plan (80 cr/s at $0.003/cr ≈ $0.24/s) | $58 | $144 | $360 |

Cross-check: invideo reports 3,000–6,500 credits for 70 s–2 min films at $0.21–$0.25 per credit [18]; YOPRST quotes Veo at about $30 per minute of raw model usage [17]; an AI music video author estimates $250–$700 compute per finished video [20]. Tool cost is therefore typically low hundreds of USD/EUR per finished minute, small against a fee of several thousand; labour dominates.

### 1.4 Day rates (Europe, freelance unless noted)

| Role | Rate | Region | Source | Evidence |
|---|---|---|---|---|
| Motion designer, France (Malt barometer 2026) | ~€418/day avg; €266 (0–2 y), €333 (3–7 y), €415 (8–15 y) | FR | [39] | snippet (secondary) |
| Motion designer / motion graphics, UK (YunoJuno) | £385/day avg | UK | [40] | fetched |
| Video editor, UK (YunoJuno) | ~£403/day, ~£50/h | UK | [41] | snippet |
| Video editor, England (job adverts, 6 months to May 2025) | median £356/day (n=4) | UK | [41] | snippet |
| Editor + camera, Germany (fairtv producers' letter) | €350–€500/day recommended for 2021/22 | DE | [42] | snippet |
| Sound designer (lead), Germany advertising, on invoice (bvft 2026) | €595/day (10 h), €74/h | DE | [43] | fetched |
| Re-recording mixer, Germany advertising, on invoice (bvft 2026) | €598/day | DE | [43] | fetched |
| Sound editor, Germany advertising, on invoice | €474/day | DE | [43] | fetched |
| Sound designer / mixer, Germany documentary low budget, on invoice | €484 / €486 per day | DE | [43] | fetched |
| Location sound mixer, Germany advertising, on invoice | €750/day | DE | [43] | fetched |
| Animation director (réalisateur), France, salaried minimum (1 Jul 2024) | €201.63/day (7 h), €1,008.13/week (35 h) | FR | [44] | fetched |
| Chef monteur image/son/animatique, France animation minimum | €214.13/day; €1,070.65/week | FR | [44] | fetched |
| Storyboarder, France animation minimum | €156.21/day | FR | [44] | fetched |
| Chef étalonneur (lead colourist), France animation minimum | €144.85/day | FR | [44] | fetched |
| Ingénieur du son, France animation minimum | €144.86/day | FR | [44] | fetched |
| Composer (production/day), UK (PCAM member answer) | £1,800/day production; £250/h | UK | [45] | fetched |
| Composer composition fee, UK commercial | £500–£5,000, average ~£3,500; one member £4,000, others £1,500–£6,000 | UK | [45], [46] | fetched / snippet |
| Producer/director, UK unscripted (Bectu baseline) | £1,380–£1,705 per week (37.5 h) | UK | [47] | snippet |
| Director, US music video | $500–$1,250/day; DP $1,000–$1,800/day | US | [11] | snippet |
| Copywriter (script), US freelance | $75–$200/h | US | [9] | fetched |
| AI video specialist, Upwork | $50–$120/h (vendor blog) | global | [48] | snippet |
| UK camera operator | £500–£1,500/day (single camera) | UK | [5] | snippet |

French CCN figures are salaried minima before employer charges and author's rights, so they are floors, not market freelance prices. bvft states invoiced fees should sit at least 30% above the collective-agreement salaried rates [43]. Bectu publishes card links (post-production short-form 2023–2025, post-sound 2025–2026, camera 2025, commercials and dailies 2026) but the figures sit in member PDFs not retrieved here [49].

### 1.5 Commercial terms

- Deposit structures: 50% to start, balance on final delivery, net 30 [50]; thirds (signing, end of principal photography, balance) in a Lemonlight services agreement filed with the SEC [50]; MaiDreamsLab 40% on activation / 60% on master, and 30/40/30 above €15,000 [10].
- Revision rounds: two rounds per edit typical, extra rounds billed; contradictory feedback that reworks approved elements counts as a new round [50]; Lemonlight-style contract one round of notes [50]; AI studio two contractual cycles vs freelance one courtesy round [10]; Fusion Media's 30 s AI spot one round [16]; out-of-scope revisions billed per minute of video (an animation company) [50].
- Rush fees: +20–50% (Vidico retainer guide) [15]; +20–30% (Vidico commercial guide) [8]; agency practice +50%, general 25–50% [51].
- Cancellation: 20% fee if a shoot is cancelled within 48 h; deposit non-refundable (one company's terms) [50].
- Usage/licensing: four dimensions (media, term, territory, exclusivity) [52]; creator-market rule of thumb 20–50% of base fee per month of use [52]; perpetual or all-media priced sharply higher (+100–150% or 3–5×, conflicting rules of thumb) [52]; voiceover commercial buyouts mostly 12 months [52]; talent fees rise 20–100% moving from social to national TV [8]; 1BVP includes paid, web and broadcast usage in its flat $7,500 [16]; MaiDreamsLab grants an unlimited, perpetual, worldwide licence, with AI characters used as brand assets beyond 24 months quoted separately [10].
- Music: quote split into Production / Composition / Usage (PCAM) [46]; examples: composition £3,000, usage Germany+Benelux 3 months £2,250, additional usage same +10%, demo fee £500–£1,500, singer session £200 + usage 400–800% of session fee [45]; one-year internet usage quoted at 600% of composition fee, or a one-off large venue at 100% [45]; events 25% / 50% / 100% of composition fee by size [45]; renewal: two years 100% of original licence, one year 75% [45]; average UK TV+internet commercial music £15,000–£25,000, overall £1,500–£25,000 [45], [46]; pitch fees £750–£1,000 per company, PCAM proposed £500 per demo minimum [46]. Sync licences: local ad with indie track $500–$2,500; national well-known song $5,000–$250,000; plus a separate master licence [53]. Royalty-free $50–$500/track; licensed popular $5,000–$50,000+ [8]. AI studio licensed tracks €200–€2,000 extra [10].
- Cut-downs and variants: shooting 15/30/60 s versions in one day gives 3–5× assets for +20–30% budget [8]; traditional extra formats €500–€1,500 each, included with AI (MaiDreamsLab) [10]; localisation €400–€800 per language beyond IT/EN [10]; TVC network certification €200–€500 [10].
- Retainers: 3-month trial start; 6–12 month commitments get better rates; month-to-month 10–20% more per video; retainers save 15–25% per video at 4+ videos/month [15]; Fusion Media mentions retainers from $6,000/month (reported in a third-party roundup; its own page says it has no rate card) [16], [25]; UK social video £1,000/month minimum and £3,000+/month video-led programmes [54].
- Pilots/tests: no studio publishing a paid pilot price was found. Free concept storyboards before quoting (Fusion Media) [25]; pitch/demo fees as a paid-test analogue in music (£500–£1,500) [45], [46]; AI Adoption Agency starter $299 for one 15–30 s video, one revision, 5–7 days [55].

## 2. Evidence notes

Explainer and animation. The only quasi-independent benchmark is Wyzowl's 2024 survey (n=242; median $5,400, mean $10,983 for one minute) as reported by TruScribe [1]. All per-style ranges are vendor content (Blue Carrot, Pixune, Prolific, Advids) [1], [2], [22]. Several sources note the first minute is the most expensive because setup is fixed [1]. France: La Fabrique du Net's aggregated quotes (155 motion-design projects, median €8,000; 170+ video projects, median €6,500) are the best French datapoints but the pages refused fetch, so values are from search text [3], [4]. Codeur.com's TJM for motion designers (€130, Oct 2026) reflects a low-end marketplace and is not representative [56].

Commercials. UK small-brand £5,000–£30,000 and mid-range £30,000–£100,000 come from production-company pages [7]. The Vidico tiers (Sept 2026) give the cleanest US ladder plus line items: concept/script $2,000–$10,000, director and crew $5,000–$20,000 per shoot day, editing/post $5,000–$25,000, music $500–$10,000; editing typically 20–30% of total [8].

Documentary. CNC 2024: documentaire de création €225.5k per hour, broadcaster contribution €102.4k/h, CNC €41.6k/h [12]. BBC's YouTube strand: £50,000 per film of at least 25 minutes [13]. ADE scheduling guide (2022): one month of editing per 10 finished minutes; series 16–18 weeks per 42 min [24].

AI production. Kalshi (June 2025): one person, two days, 300–400 Veo 3 generations for 15 usable clips, prompting cost under $2,000 [21]. Coca-Cola 2025: >70,000 clips, ~100 people, about a month [26]. invideo's documented shorts are tool-centred and vendor-reported [18]. YOPRST notes that DIY "dozens of hours" go to prompting, fixing glitches and stitching [17]. Shy Kids' "Air Head" (Sora) needed traditional VFX for consistency fixes; a ratio figure could not be confirmed [57]. Promise (which acquired Curious Refuge in Feb 2025) publishes no per-minute costs; Critterz is reported at under $30M versus $100M+ typical animated features, nine months versus three years [58]. No Curious Refuge survey of client rates was found.

Tool costs. Google's Gemini pricing page and Runway's developer pricing page were read directly [28], [29]. Sora 2 figures are from a tracker that read OpenAI's page in Sept 2026 and reports the Videos API shut down on 2026-09-24; OpenAI's current pricing page no longer lists Sora [32], [38]. Kling direct API pricing is custom-quoted; the aggregator range is indicative [31].

Gaps. No fetched French or German union grid for audiovisual (non-animation) editors/directors; no Bectu figures retrieved (member PDFs); no published paid-pilot prices from AI studios; no independent study of hours per finished minute for AI work; no source pricing cut-downs per unit for traditional post beyond MaiDreamsLab and Vidico.

## REFERENCES

1. TruScribe. [Explainer video cost](https://truscribe.com/feeds/blog/explainer-video-cost) (cites Wyzowl 2024 survey and Blue Carrot 2025). Fetched 2026-10-17.
2. Pixune. [How much does it cost to create an animated explainer video in 2025?](https://pixune.com/?p=50688). Snippet.
3. La Fabrique du Net. [Agences motion design: guide des tarifs](https://www.lafabriquedunet.fr/agences/pages/agences-motion-design/tarifs). Snippet (HTTP 403 on fetch).
4. La Fabrique du Net. [Tarifs des agences vidéo en 2026](https://www.lafabriquedunet.fr/agences/pages/agences-video/tarifs). Snippet (HTTP 403 on fetch).
5. Whito / Shootsta. [Corporate video cost UK (Whito)](https://whito.co.uk/?p=9126); [Corporate video cost UK (Shootsta)](https://shootsta.com/blog/corporate-video-cost-uk). Snippet.
6. Dragonfly. [How much does a corporate video cost?](https://www.dragonfly.co.uk/faq/how-much-does-a-corporate-video-cost/). Snippet.
7. Lambda Films. [Cost to advertise on TV](https://lambdafilms.co.uk/cost-to-advertise-on-tv); South West Film. [TV advertising costs](https://southwestfilm.co.uk/tv-advertising-costs). Snippet.
8. Vidico. [How much do TV commercials cost? (2026)](https://vidico.com/news/how-much-does-a-30-second-commercial-cost/), 2026-09-21. Fetched.
9. Lemonlight. [AI video production cost: what brands should expect](https://www.lemonlight.com/blog/ai-video-production-cost/), 2026-03-26. Fetched.
10. MaiDreamsLab. [How much does an AI-produced commercial cost: 2026 real pricing and timelines](https://maidreamslab.ai/en/blog/how-much-ai-commercial-pricing-2026/). Fetched.
11. Pixo. [How much does a music video cost](https://pixo.video/blog/how-much-does-a-music-video-cost); 171 Entertainment. [Music video budget breakdown](https://171entertainment.com/guides/music-video-budget-breakdown/). Snippet.
12. CNC. [La production audiovisuelle aidée en 2024](https://www.cnc.fr/professionnels/etudes-et-rapports/etudes-prospectives/la-production-audiovisuelle-aidee-en-2024_2428208). Fetched.
13. PPC Land. [BBC offers £50,000 per YouTube documentary for 16–24 year olds](https://ppc.land/bbc-offers-50-000-per-youtube-documentary-for-16-24-year-olds/). Snippet.
14. Motion The Agency. [How much does a sizzle reel cost?](https://www.motiontheagency.com/blog/how-much-does-it-cost-to-produce-a-sizzle-reel); [How much does an animatic cost](https://monitorbp.ne.gov/post/how-much-does-an-animatic-cost); Prolific Studio. [Animatic vs animation](https://prolificstudio.co/blog/animatic-vs-animation/). Snippet.
15. Vidico. [Video retainer packages](https://vidico.com/news/video-retainer-packages/), 2026-05-29. Fetched.
16. 1BVP. [Top 10 AI commercial production agencies in 2026](https://1bvp.com/ai-commercial-production/) (self-listing; cites Clutch $42,280 average). Fetched.
17. YOPRST. [Why cinematic-quality AI videos cannot be cheap](https://prst.media/en/why-cinematic-quality-ai-videos-cannot-be-cheap/). Fetched.
18. invideo. [AI film production cost: what an AI short film actually costs to make](https://invideo.io/blog/ai-film-production-cost/). Fetched (vendor).
19. Fiverr. [AI commercial gigs](https://block.fiverr.com/gigs/ai-commercial); [Fiverr Pro cinematic AI commercials](https://fiverr.com/luigiflorente/craft-unique-ai-music-videos). Snippet.
20. AI Video Bootcamp. [How to make money with AI music videos](https://aivideobootcamp.com/blog/how-to-make-money-ai-music-videos/). Snippet.
21. NPR via GPB. [An AI video ad is making a splash. Is it the future of advertising?](https://www.gpb.org/news/2025/06/23/ai-video-ad-making-splash-it-the-future-of-advertising), 2025-06-23. Fetched.
22. Advids. [How much brand explainer video creation cost](https://advids.co/pricing/how-much-brand-explainer-video-creation-cost). Snippet.
23. Motion The Agency. [How much does 2D animation cost and how long does it take?](https://www.motiontheagency.com/blog/how-much-does-2d-animation-cost); Toon Boom forum. [Timeframes for production](https://forums.toonboom.com/t/help-timeframes-for-production/15738). Snippet.
24. International Documentary Association. [Alliance of Documentary Editors unveils scheduling guide](https://www.documentary.org/feature/alliance-documentary-editors-unveils-scheduling-guide), 2022-04-23. Fetched.
25. Fusion Media. [AI video studio](https://fusionmedia.ai/ultimate-ai-video-studio-for-your-business). Fetched.
26. Implicator / Film Stories. [Coca-Cola debuts AI holiday ads](https://www.implicator.ai/coca-cola-debuts-ai-holiday-ads-animals-replace-actors-after-2024-backlash/); [Coca-Cola Christmas advert 2025 review](https://filmstories.co.uk/features/coca-cola-christmas-advert-2025-review-churning-out-the-christmas-cheer-with-ai/). Snippet.
27. MindStudio. [AI filmmaking cost breakdown 2026](https://www.mindstudio.ai/blog/ai-filmmaking-cost-breakdown-2026/). Snippet.
28. Google. [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing). Fetched 2026-10-17.
29. Runway. [API pricing (developer docs)](https://docs.dev.runwayml.com/guides/pricing/). Fetched 2026-10-17.
30. Runway. [Pricing](https://runway.com/pricing). Fetched 2026-10-17.
31. CostBench. [Kling API pricing](https://costbench.com/software/ai-media-apis/kling-api/); CloudZero. [Kling AI pricing](https://www.cloudzero.com/blog/kling-ai-pricing/). Snippet.
32. BenchLM. [Sora 2 API pricing](https://benchlm.ai/md/media-pricing/sora.md) (OpenAI prices read 2026-09-11; shutdown 2026-09-24). Fetched (secondary).
33. Luma AI. [Pricing](https://lumalabs.ai/pricing). Fetched 2026-10-17.
34. eesel. [Midjourney pricing in 2026](https://eesel.ai/blog/midjourney-pricing). Snippet.
35. ElevenLabs. [Pricing](https://elevenlabs.io/pricing). Fetched 2026-10-17.
36. Suno. [Pricing](https://suno.com/pricing). Fetched 2026-10-17.
37. GPTPrompts / CostBench. [Udio pricing in 2026](https://gptprompts.ai/udio-pricing); [Udio plans](https://costbench.com/software/ai-music-generators/udio/). Snippet.
38. OpenAI. [API pricing](https://developers.openai.com/api/docs/pricing). Fetched 2026-10-17.
39. Join Jump / Abby (citing Malt 2026 barometer). [Motion designer freelance](https://www.join-jump.com/guide/motion-designer-freelance); [Devenir motion designer](https://abby.fr/guide/micro-entreprise/devenir-motion-designer). Snippet.
40. YunoJuno. [Motion graphics freelancer rates](https://yunojuno.com/freelancer-rates-job-role/motion-graphics). Fetched.
41. YunoJuno. [Video editing freelancer rates](https://yunojuno.com/freelancer-rates-job-role/video-editing); ITJobsWatch. [Video editor contracts in England](https://www.itjobswatch.co.uk/contracts/england/video%20editor.do). Snippet.
42. fairtv. [Produzentinnenbrief 2020](https://fairtv.net/downloads/send/22-veroffentlichungen/211-fairtv-produzentinnenbrief2020). Snippet.
43. Berufsvereinigung Filmton (bvft). [Gagenempfehlung Dreh und Postproduktion 2026](https://www.bvft.de/wp-content/uploads/2026/04/bvft_Gagenempfehlung-Set-und-Postproduktion_01.2026.pdf). Fetched (PDF text extracted).
44. SNTPCT. [Films d'animation: salaires minima garantis au 1er juillet 2024](https://sntpct.fr/wp-content/uploads/2020/07/SNTPCT_Films_Animation_Salaires_minima_garantis_au_1er_juillet_2024.pdf). Fetched (PDF text extracted).
45. PCAM. [Helpdesk Q&As Vol 5 (2025)](https://www.pcam.co.uk/wp-content/uploads/2025/05/PCAM-Helpdesk-QAs-Vol-5-2025.pdf). Fetched (PDF text extracted).
46. PCAM. [Helpdesk (site)](https://www.pcam.co.uk/?p=4423); [Helpdesk Volume 1](https://www.pcam.co.uk/wp-content/uploads/2021/06/Helpdesk-Volume-1-1.pdf). Snippet.
47. Broadcast. [Bectu bids to demystify unscripted pay rates](https://www.broadcastnow.co.uk/indies/bectu-bids-to-demystify-unscripted-pay-rates/5166974.article). Snippet.
48. Genra. [AI video freelancer business guide](https://genra.ai/blog/ai-video-freelancer-business-guide). Snippet (vendor).
49. Bectu. [Ratecards](https://bectu.org.uk/about/ratecards/). Fetched (index only; figures in member PDFs).
50. Agiled. [Videography contract template](https://agiled.app/contract-templates/videography); SEC EDGAR. [Lemonlight Media services agreement](https://www.sec.gov/Archives/edgar/data/1509957/000151116416000890/f108.htm); Advids. [Terms of service](https://advids.co/terms-of-services.html); Live Up Media. [Terms](https://www.liveupmedia.co.uk/terms-and-conditions). Snippet.
51. Sakas & Company. [How to charge agency rush fees](https://sakasandcompany.com/rush-fees-for-priority-work/); Memtime. [Rush fee explained](https://www.memtime.com/blog/rush-fee-explained-how-much-to-charge-for-urgent-work). Snippet.
52. PPC Land. [Usage rights](https://ppc.land/usage-rights/); Hubfluence. [Content usage rights](https://www.hubfluence.io/blog/content-usage-rights); Voicebooking. [Organic vs commercial usage](https://kbc.voicebooking.com/en/articles/2326784). Snippet.
53. Foxi Music. [How much does it cost to license music for a commercial (2026)](https://www.foximusic.com/blog/how-much-does-it-cost-to-license-music-for-a-commercial/); Songwriters Portal. [What is sync licensing?](https://songwritersportal.ladesk.com/281662-What-is-Sync-Licensing). Snippet.
54. Videotto. [How much does video editing cost UK 2026](https://www.videotto.com/blog/how-much-does-video-editing-cost-uk-2026); Whito. [UK social media management costs](https://whito.co.uk/research/uk-social-media-management-costs/). Snippet.
55. AI Adoption Agency. [AI commercial video service](https://aiadoptionagency.com/product/ai-commercial-video-service/). Snippet.
56. Codeur.com. [Tarif moyen des motion designers](https://www.codeur.com/motion-designer/tarif). Fetched.
57. Teknófilo. [Air Head / Shy Kids and Sora](https://www.teknofilo.com/?p=235393). Snippet.
58. TechRadar. [OpenAI-backed movie Critterz budget](https://www.techradar.com/streaming/entertainment/this-new-openai-backed-movie-has-a-budget-of-just-usd30-million-but-will-it-prove-ai-can-make-movies-hollywood-cant); Techleap. [Promise acquires Curious Refuge](https://finder.techleap.nl/news/feed/promise-acquires-ai-film-school-curious-refuge). Snippet.
