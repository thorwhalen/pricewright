# Software and apps

Software is priced on value with a cost floor, the reverse of services. `pricewright.specialties.software.plan` computes the floor of a tier at its full allowance (`variable cost / (1 - target gross margin)` plus payment fees); `credit_pack` does the same for top-ups. Everything else (value metric, model, tiers, fences, billing terms, tests) is the procedure in section 1 below. The evidence (baseline 2026-10-17) follows.

---


Research packet for the pricing expert agent. Compiled 2026-10-17. Every number below carries a reference; where only secondary sources (vendor blogs, aggregators) were available, the text says so. Treat secondary figures as starting priors, not facts. Plan prices of comparable AI creative tools are in `software-comparables.yaml` next to this file.

## 1. Decision procedure (follow in order)

### Inputs to collect before proposing anything

1. **Cost per unit of usage (COGS).** For each billable action (a generation, a minute of audio, a second of video, an agent run, a GB stored): inference or compute cost, storage, third-party API pass-through, and payment fees (Section 6). For AI products this is not negligible: ICONIQ's 2026 survey reports average AI-product gross margin of 45% in 2025, projected 53% in 2026 [10]. Ask for the distribution, not just the mean: the heaviest 5-10% of users usually decide whether a flat price works.
2. **Customer segments.** Who buys (hobbyist, prosumer, SMB team, enterprise), how each gets value, budget owner, and whether they buy self-serve or through sales.
3. **Value delivered per segment.** Time saved, revenue gained, cost replaced (e.g. a freelancer, a stock-footage licence, a support agent). Quantify in the customer's currency. Ramanujam's rule: hold the willingness-to-pay conversation before the product is built, framed as a "value talk" [2].
4. **Competitors' and substitutes' prices.** Including the non-software substitute (hiring a person, doing it by hand). Use `software-comparables.yaml` for AI creative tools.
5. **Go-to-market motion and CAC.** Self-serve vs sales-assisted; current or expected CAC; target payback (Section 6).
6. **Constraints.** App-store distribution (fees and rules), merchant-of-record needs (VAT/sales tax), currencies and regions, contracts already signed.

### Steps

1. **Pick the value metric** (Section 3): the unit that scales with customer value, that the customer can predict, and that the vendor can measure and explain [1]. If marginal cost per unit is material (AI), the metric must also track cost, or there must be a fence that caps it.
2. **Pick the model** from Section 2 using the fit table. Default for AI products in 2026: hybrid, meaning a subscription that includes an allowance of credits or usage, plus top-ups or overage [10][12].
3. **Compute the price floor** per tier: `floor = (expected variable cost per account per month at the tier's allowance, used in full) / (1 - target gross margin)`, then add payment fees on top (Section 6). Check the floor against value: if value per month is not several times the floor, the product or the metric is wrong, not the price.
4. **Set the ceiling and anchor** from value and from substitutes: price is a share of value delivered, bounded by the alternatives the customer actually considers.
5. **Package into Good-Better-Best** with fences (Section 3): 3 paid tiers plus free or trial; a decoy or anchor tier at the top (Enterprise "contact us" or a high-volume tier) [3][4][5].
6. **Set the billing terms**: annual discount (commonly 15-20%, Section 3), credit rollover and expiry rules, top-up price per credit (above the in-plan effective rate, so upgrading is the better deal), regional prices if selling outside high-income markets.
7. **Validate with research** (Section 5): WTP interviews first, then Van Westendorp or Gabor-Granger on a sample, conjoint if the packaging decision is the hard part; then a live test on new visitors only.
8. **Check unit economics** (Section 6): gross margin per tier at full allowance, CAC payback, LTV:CAC. If any tier loses money at full use, tighten its allowance or fence rather than raise every price.
9. **Plan the next change**: how you will raise prices or migrate customers later (grandfathering window, notice period), and the metric you will watch (conversion, ARPA, NRR, gross margin by cohort).

### Outputs to return

- Model and value metric, with one sentence of justification each.
- Tier table: name, target segment, monthly and annual price, included usage (credits or units), key fences, top-up/overage price.
- Floor and margin check per tier at full allowance, with the cost assumptions stated.
- Positioning against 3-5 named comparables.
- Test plan: research method, sample, success metric, and the decision rule.
- Risks: heavy-user exposure, app-store fees, arbitrage across regions, migration of existing customers.

## 2. Models and when each fits

| Model | What it is | Fits when | Watch out for |
|---|---|---|---|
| Flat subscription | One price, one plan | One segment, low and uniform marginal cost, simple product | No expansion revenue; leaves money on the table with heterogeneous customers |
| Tiered Good-Better-Best | 3 plans differing in features or allowance | Segments differ in WTP and needs; the default for most apps [3][4] | Too many differing attributes blur the choice; see packaging rules below |
| Per seat | Price per user | Value scales with people using it (collaboration tools) | AI that replaces people shrinks seat counts; Growth Unhinged reported seat-based pricing falling from 21% to 15% of surveyed companies in a year (secondary) [15] |
| Usage-based / pay-as-you-go | Pay per unit consumed | Value and cost both scale with usage; API and infrastructure products | Bill unpredictability; customers ration use. Stripe's test: the customer must be able to estimate the bill [1] |
| Credits / prepaid wallet | Customer buys a pool of credits that different actions consume at different rates | Many actions with different costs (image vs video vs voice); multi-product suites | Opaque exchange rates erode trust; set expiry and rollover rules explicitly. HubSpot uses one universal credit across products [12] |
| Hybrid (platform fee + usage) | Base subscription including an allowance, plus overage or top-ups | AI products with material inference cost; the 2026 default. Growth Unhinged: 76% of AI-native companies use variable or hybrid pricing vs 49% of SaaS [12]; ICONIQ: companies blend 1.7 pricing models on average [10] | Two meters at once (Descript runs media hours plus AI credits [35]) add cognitive load |
| Freemium | Permanent free tier, paid upgrade | Large top of funnel, low marginal cost of a free user, network or virality effects | Free users cost real money in AI products; cap with daily credits (Suno: 50 credits/day free [33]) |
| Free trial | Full or partial product, time-limited | Value is visible within days; sales-assisted motions | Lower sign-up rate than freemium (5% vs 9% in the Lenny/Poyar data) [6] |
| Reverse trial | Start on the paid tier for a period, then drop to free | Want both the trial's conversion and freemium's retained base [8][9] | Requires a meaningful free tier to fall back to |
| One-time licence | Pay once, own a version | Desktop or offline tools with near-zero ongoing cost; buyers hostile to subscriptions | No recurring revenue to fund updates; charge for major versions |
| Lifetime deal (LTD) | One payment for permanent access, often via a marketplace such as AppSumo | Early cash and feedback for a product with negligible marginal cost | Gives up recurring revenue, attracts deal-hunters, makes later price rises hard; marketplace splits are reported inconsistently (50-70% to the founder by one guide, worse by forum reports) [29]. Never for products with per-use inference cost |
| Outcome-based | Pay per result (a resolved ticket, a qualified lead) | Outcome is attributable, countable and agreed by both sides | Definition disputes (Fin counts a resolution when the customer stays silent 24 hours, per commentary); revenue volatility. ICONIQ: outcome-based use rose from 18% to 23% of respondents in six months [10] |

### Outcome and per-action price points observed (2025-2026)

- Intercom Fin: $0.99 per outcome, at most one outcome charged per conversation; seat plans $29 / $85 / $132 per seat per month [13].
- Salesforce Agentforce: Flex Credits at $500 per 100,000 credits, 20 credits ($0.10) per action; the older model was $2 per conversation [14].
- Zendesk: $1.50 per committed automated resolution, $2.00 pay-as-you-go (launched August 2024; secondary source) [15].
- Gumloop passes tokens and compute through at cost plus an 8% orchestration fee [12].

## 3. Value metric, packaging, anchoring, terms

**Value metric.** Stripe's three tests: it scales with the value the customer gets; the customer can estimate the bill before signing; the vendor can show how the charge was computed [1]. Add for AI: it must track marginal cost, or be fenced so that it cannot run away from it. Typical candidates: seats, active users, outputs (images, songs, minutes of audio, seconds of video), projects, API calls, resolved outcomes.

**Packaging and fences (Good-Better-Best).** Mohammed (HBR, 2018), as summarised secondarily: keep the number of attributes that differ between neighbouring tiers small (no more than four), keep Good no more than 25% below Better and Best no more than 50% above Better, and pick "fence" attributes that stop current buyers trading down [3]. Versioning theory (Shapiro and Varian) grounds this: sell variations of one underlying good priced to segments' value, not to cost [4]. In AI tools the common fences are: commercial-use rights (Suno Free has none [33]), watermark removal (Runway Free watermarks [30]), output resolution or length, parallel jobs and priority queues (Runway 5/15/20 parallel generations [30]), privacy or "stealth" mode (Midjourney Pro and up [31]), voice cloning, seats, and the size of the credit allowance.

**Anchoring and decoys.** Adding an option that is dominated by one tier but not the other raises the share choosing the dominating tier (asymmetric dominance; Huber, Payne and Puto, 1982, Journal of Consumer Research 9(1)); the authors' 2014 commentary argues the effect is robust under replication [5]. Practice: a high top tier (Enterprise or a volume tier such as ElevenLabs Business at $990/month [32]) anchors the middle tier; the middle tier is the one designed to be chosen.

**Annual vs monthly.** Secondary sources converge on 15-20% as the common annual discount, with "two months free" (about 17%) frequent; the ProfitWell figure of a 16% average is cited secondhand only [26]. Observed in AI tools: ElevenLabs annual = 10x monthly (about 17%) [32]; Runway 20% [30]; Suno 20% [33]; Pika 20% [42]; Krea up to 40% [45]; Descript up to 35% [35]; Claude Pro $17 vs $20 [38].

**Regional pricing / PPP.** Practice reported by vendors: group countries into 3-6 tiers rather than pricing per country, start from World Bank or IMF PPP conversion rates, discounts in the 10-60% range; arbitrage (VPNs, foreign cards) is the main risk, so check billing country, card country and IP together [27]. These figures are vendor rules of thumb, not published studies. App stores price per storefront already; on the web a merchant of record handles local tax.

**Price increases and grandfathering.** Secondary guidance: grandfather existing customers for a defined window (12-24 months) rather than forever; give 30-90 days' notice, with annual subscribers told 45-60 days before renewal; raise prices for new customers first; offer an annual lock-in at the old price as an off-ramp [28]. Credit products have a lever subscriptions lack: change credit costs per action or allowance per plan instead of the sticker price, but announce it as a price change, because customers experience it as one.

## 4. AI products specifically

**Inference is COGS.** Every generation has a marginal cost, so the classic SaaS assumption (marginal cost near zero) breaks. Benchmarks: ICONIQ reports AI-product gross margin of 45% in 2025, projected 53% in 2026 and 59% in 2027 (Q2 2026 survey of about 300 executives) [10]. Bessemer's State of AI 2025: fast-growing "Supernovas" average about 25% gross margin, often negative; "Shooting Stars" about 60%, "slightly lower than SaaS peers" [11]. Classic SaaS baselines cited range from 65-70% (Bessemer cloud benchmark) to 80-90% depending on source, so state which baseline you compare to. Two-thirds of ICONIQ respondents report improved per-query unit economics, via inference cost management, model routing and scale [10].

**Margin target to plan with.** No single authoritative target exists. A defensible planning rule from the sources above: design every paid tier to clear at least 50-60% gross margin when its allowance is fully consumed, and expect the blended margin to be higher because most users do not exhaust their allowance. State the assumed utilisation explicitly.

**How the leading tools structure plans (observed October 2026; details in the YAML).**

- **Runway**: credits per month by tier (Free 125 one-time; Standard 625 at $15; Pro 2,250 at $35; Max 9,500 at $95, up to one month rollover); credits priced per second of video and per model (Gen-4.5 at 12 credits/second, Aleph 2.0 at 28 credits/second) [30]. Metric = credits; fences = parallel jobs, projects, brand kits, voice clones, storage; some models "unlimited" on higher tiers.
- **Midjourney**: GPU time, not credits: Basic $10 (about 3.3 fast hours), Standard $30 (15 fast hours plus unlimited Relax), Pro $60 (30 hours, Stealth), Mega $120 (60 hours); about 20% off annually; extra fast hours about $4 (secondary) [31]. "Relax mode" is the rate-limit-as-fence pattern: unlimited, but slow.
- **ElevenLabs**: credits roughly mapping to characters/minutes: Starter $6 / 30,000; Creator $22 / 121,000; Pro $99 / 600,000; Scale $299 / 1.8M; Business $990 / 6M [32]. Steep ladder, deep first-month promotions.
- **Suno**: Free 50 credits/day with no commercial rights; Pro $10 monthly ($8 annual) 2,500 credits; Premier $30 ($24) 10,000 credits; a generation costs 10 credits for two songs (secondary); download caps of 20 and 60 per month on the paid tiers per the official page [33].
- **Kling**: Standard 660, Pro 3,000, Premier 8,000, Ultra 26,000 credits per month; prices vary by source and include first-month offers (secondary) [34].
- **Descript**: two meters, media hours plus AI credits: Hobbyist $24 (10 h, 400 credits), Creator $35 (30 h, 800), Business $65 (40 h, 1,500) [35].
- **Cursor**: moved from request counts to a usage pool in 2025; the October 2026 pricing page shows usage described as multiples of a base plan (4x, 15x, 50x) with allowances refreshing weekly and top-ups; third-party trackers record a restructuring in April 2026 [37]. Verify before citing tier names.
- **Claude**: Pro $20 ($17 annual); Max from $100 with 5x or 20x Pro usage; Team Standard $25/$20 and Premium $125/$100 per seat; Enterprise $20/seat (20-seat minimum) plus usage at API rates [38]. This is the "multiples of the base allowance" pattern, with rate limits per 5-hour session as the fence.
- **ChatGPT**: Free (with ads, per secondary sources), Go about $8, Plus $20, Pro tiers at $100 and $200, Business about $20-25 per user (secondary; official page not reachable) [39].

**Patterns to reuse.**

1. **Credits decouple price from model cost.** When a cheaper or more expensive model ships, change its credit cost, not the plan prices (Runway prices each model in credits per second [30]).
2. **Rate limits and queues are fences.** Unlimited-but-slow (Midjourney Relax [31]) or per-session caps (Claude [38]) sell "unlimited" while bounding cost.
3. **Usage multiples sell tiers.** "5x / 20x Pro" (Claude) and "4x / 15x / 50x" (Cursor) communicate value without exposing token math [37][38].
4. **Pass-through for third-party models.** Charge external model use at list price or at cost plus a fee (Cursor bills third-party models at API list price above the allowance [37]; Gumloop cost plus 8% [12]).
5. **Make variable bills predictable**: universal credits, hard budget caps per account and user, annual drawdown of committed usage, platform fee with baseline usage included [12].
6. **Outcome pricing only where the outcome is countable and attributable** (support resolutions, qualified leads) [13][14][15].

## 5. Benchmarks

| Metric | Value | Source and quality |
|---|---|---|
| Freemium self-serve free-to-paid (6-month window) | good 3-5%, great 6-8% | Lenny/Poyar 2023, 1,000+ products, B2B-weighted [6] |
| Freemium with sales assist | good 5-7%, great 10-15% | same [6] |
| Free trial to paid | good 8-12%, great 15-25% | same [6] |
| Sign-up rate, trial vs freemium | 5% vs 9% | same [6] |
| Median free-to-paid, all models blended | 8% | ChartMogul Conversion Report (secondary summary) [7] |
| Reverse trial conversion | about 15% estimated vs 5% freemium (Verna's experience); 4-6% good, 8-12% great (ChartMogul via Userpilot) | secondary, unverified [8][9] |
| Net revenue retention, private B2B SaaS, ACV $25-50k | median 102%, top quartile 111%, bottom quartile 97% | SaaS Capital 2025 [16] |
| NRR blended median, private B2B SaaS | about 101% | secondary summaries of SaaS Capital/Benchmarkit/KeyBanc [16] |
| AI product gross margin | 45% (2025), 53% projected (2026), 59% (2027) | ICONIQ 2026 [10] |
| AI gross margin by growth profile | Supernovas about 25%; Shooting Stars about 60% | Bessemer 2025 [11] |
| Classic SaaS gross margin baseline | 65-70% (Bessemer cloud) to 80-90% (other sources) | mixed [11] |
| Pricing-model mix in AI companies | consumption 35% to 42%, outcome 18% to 23% in six months; 1.7 models blended | ICONIQ 2026 [10] |
| Variable or hybrid pricing | 76% of AI-native vs 49% of SaaS companies | Growth Unhinged 2026 [12] |
| Annual-plan discount | commonly 15-20%; 16% average (ProfitWell, secondhand) | secondary [26] |
| CAC payback, B2B SaaS median | 15-16 months (2025-2026); under 12 months strong | secondary (Benchmarkit, Optifai via SaaSHero) [21] |
| LTV:CAC | 3:1 rule of thumb; 3-5x healthy | secondary [21] |
| Stripe card fees (EU page) | EEA standard cards 1.5% + €0.25; international 3.15% + €0.25; FX +2%; Billing 0.7%; Tax 0.5%/transaction; Managed Payments (MoR) 3.5% on top | Stripe pricing (fetched, EU) [17] |
| Stripe card fees (US) | 2.9% + 30¢ commonly cited | secondary [17] |
| Paddle (merchant of record) | 5% + 50¢ per transaction, tax and compliance included | Paddle pricing [18] |
| Apple App Store | 30% standard; 15% in Small Business Program (≤ $1M proceeds) and for subscriptions after year one; the SBP page now states 10% for subscriptions after the first year | Apple [19] |
| Google Play | 15% on first $1M, 30% above, 15% on auto-renewing subscriptions (older tier); in AU/EEA/JP/UK/US an updated structure of 10% + 5% billing fee on subscriptions | Google [20] |

## 6. Unit economics and price floors

Definitions (standard; no external numbers needed):

- **Gross margin per account** = (ARPA - variable cost per account) / ARPA, where variable cost includes inference, storage, third-party APIs, support, and payment fees.
- **Payment fees** come off the top: a $10 sale through Paddle costs 5% + $0.50 = $1.00 (10%); through an app store 15-30% [18][19][20]. Small tickets are punished by fixed per-transaction fees, which is one reason to push annual billing on low-price plans.
- **CAC payback (months)** = CAC / (monthly ARPA × gross margin). Lower margin lengthens payback for the same price: an AI product at 50% margin needs roughly 1.6x the ARPA of an 80%-margin SaaS product to pay back CAC in the same time.
- **LTV** = monthly ARPA × gross margin / monthly churn; target LTV:CAC of at least 3 [21].
- **Price floor per tier** = (variable cost at full allowance + fixed per-transaction fees) / (1 - target gross margin - percentage fees). Then check the paid tier against CAC payback: if payback exceeds your target (median benchmark 15-16 months B2B [21]; self-serve consumer apps should aim far lower), raise ARPA (price, packaging, annual billing) or lower CAC; do not cut the price.
- **Free tier cost** is part of CAC: (free users × cost per free user) / paid conversions. With AI inference, this is often the largest hidden cost of freemium; daily credit caps (Suno, Kling, Krea) bound it [33][34][45].

## 7. Price research methods

- **Willingness-to-pay interviews (Ramanujam / Monetizing Innovation).** Before building: frame as a value conversation, ask for the acceptable price range and per-feature value, ask "why" on a share of answers; use the results to decide what to build, segment and bundle [2]. Cheapest and most informative step; do it first.
- **Van Westendorp Price Sensitivity Meter.** Four questions: too cheap (doubt quality), a bargain, getting expensive, too expensive. Cumulative curves give an acceptable range between the point of marginal cheapness and the point of marginal expensiveness; definitions of the optimal and indifference points vary across sources, so state the convention used [22]. Good for a range on a new category; says nothing about demand volume or competitors.
- **Gabor-Granger.** Ask purchase intent at a sequence of prices; build a demand curve and multiply by price for a revenue curve; peak is a candidate price. Overstates WTP (hypothetical bias), ignores competitors and features [23]. Calibrate against real conversion data.
- **Conjoint and MaxDiff.** Choice-based conjoint estimates the value of each feature and of price trade-offs, so it is the method for packaging decisions; MaxDiff ranks features for tier assignment. Sawtooth is the specialist tool; Conjointly and others are cheaper alternatives [24].
- **Live A/B price tests.** Pitfalls: pricing tests convert less often than UI tests and need large samples (rough minimums of 100 conversions per variant, 30-50 for high-price B2B, per practitioner sources); customers discovering different prices for the same product damages trust, so test different packages or plans rather than two prices for one product, test on new visitors only, and give everyone the better deal afterwards; run at least a full sales cycle; judge on retention and revenue, not sign-ups; legal exposure varies by jurisdiction [25].

Recommended sequence for a new product: interviews (10-20 per segment) → Van Westendorp on a few hundred respondents to set the range → conjoint if packaging is contested → launch → one live test of packaging on new traffic.

## REFERENCES

1. Stripe. [Usage-based pricing strategy for SaaS: how to pick a metric, package your offer, and migrate without churn](https://stripe.com/resources/more/usage-based-pricing-strategy-for-saas).
2. Ramanujam M, Tacke G. Monetizing Innovation. Wiley; 2016. Summaries: [Graham Mann book notes](https://grahammann.net/book-notes/monetizing-innovation-georg-tacke-madhavan-ramanujam); [Y. Brikman notes](https://www.ybrikman.com/blog/2023/04/01/monetizing-innovation/).
3. Mohammed R. The Good-Better-Best Approach to Pricing. Harvard Business Review; 2018 Sep. Secondary: [Wikipedia, Good-better-best](https://en.wikipedia.org/wiki/Good%E2%80%93better%E2%80%93best).
4. Shapiro C, Varian HR. Versioning Information. In: Information Rules. Harvard Business School Press; 1998, ch. 3. Related: [Varian, versioning working paper](https://people.ischool.berkeley.edu/%7Ehal/Papers/doc/doc.pdf).
5. Huber J, Payne JW, Puto C. Adding Asymmetrically Dominated Alternatives: Violations of Regularity and the Similarity Hypothesis. J Consum Res. 1982;9(1):90-98. doi:10.1086/208899. See [Wikipedia, Decoy effect](https://en.wikipedia.org/wiki/Decoy_effect); [Huber, Payne, Puto 2014 commentary (JMR)](https://people.duke.edu/~jch8/bio/Papers/HuberPaynePutoJMR%202014.pdf).
6. Poyar K, Rachitsky L. [What is a good free-to-paid conversion rate?](https://www.lennysnewsletter.com/p/what-is-a-good-free-to-paid-conversion) Lenny's Newsletter; 2023 Aug 1.
7. ChartMogul. [The SaaS Conversion Report](https://chartmogul.com/reports/saas-conversion-report/).
8. Poyar K. [Your guide to reverse trials](https://www.growthunhinged.com/p/your-guide-to-reverse-trials). Growth Unhinged.
9. Amplitude. [Reverse trial](https://amplitude.com/blog/reverse-trial); see also [Inflection, guide to reverse trials](https://inflection.io/post/complete-guide-to-reverse-trials).
10. ICONIQ. [2026 State of AI Report: The Builder's Economy](https://www.iconiq.com/growth/reports/state-of-ai-2026). 2026 Jul.
11. Bessemer Venture Partners. [The State of AI 2025](https://www.bvp.com/atlas/the-state-of-ai-2025).
12. Growth Unhinged. [Usage-based pricing for AI](https://growthunhinged.com/p/usage-based-pricing-for-ai). 2026 Oct 7.
13. Intercom. [Pricing](https://www.intercom.com/pricing) (fetched 2026-10-17); [Intercom pricing explained](https://www.intercom.com/learning-center/intercom-pricing).
14. Salesforce. [Agentforce pricing](https://www.salesforce.com/agentforce/pricing/); [Flex Credits announcement, Business Wire, 2025 May 15](https://www.businesswire.com/news/home/20250515332990/en/Salesforce-Introduces-New-Flexible-Agentforce-Pricing-to-Accelerate-the-Digital-Labor-Revolution).
15. CustomerThink. [AI is killing seat-based pricing](https://customerthink.com/?p=1077727) (secondary; cites Growth Unhinged 2025 and Zendesk outcome pricing).
16. SaaS Capital. [SaaS retention benchmarks for private B2B companies](https://www.saas-capital.com/research/saas-retention-benchmarks-for-private-b2b-companies/). 2025 Sep 18.
17. Stripe. [Pricing](https://stripe.com/pricing) (fetched EU/German version 2026-10-17); US rate secondary: [NerdWallet, Stripe fees](https://www.nerdwallet.com/business/software/learn/stripe-fees).
18. Paddle. [Pricing](https://www.paddle.com/pricing) (fetched 2026-10-17).
19. Apple. [App Store Small Business Program](https://developer.apple.com/app-store/small-business-program/) (fetched 2026-10-17).
20. Google. [Play Console Help: service fees](https://support.google.com/googleplay/android-developer/answer/112622) (fetched 2026-10-17).
21. SaaSHero. [CAC payback period benchmarks](https://saashero.net/customer-retention/cac-payback-period-benchmarks-saas/) (secondary; cites Benchmarkit and Optifai).
22. SurveyMonkey. [How to use the Van Westendorp Price Sensitivity Meter](https://uk.surveymonkey.com/market-research/resources/van-westendorp-price-sensitivity-meter/).
23. SurveyMonkey. [The Gabor-Granger method](https://www.surveymonkey.com/learn/gabor-granger/).
24. Sawtooth Software. [Resources: conjoint, MaxDiff, WTP](https://sawtoothsoftware.com/resources/blog); comparison: [OpinionX vs Sawtooth](https://www.opinionx.co/opinionx-vs-sawtooth-software).
25. HubSpot. [Price testing](https://blog.hubspot.com/marketing/price-testing); [Monetizely, A/B testing SaaS pricing pros and cons](https://www.getmonetizely.com/articles/ab-testing-for-saas-pricing-the-complete-guide-to-pros-and-cons).
26. Monetizely. [Should you offer discounts for annual commitments?](https://www.getmonetizely.com/articles/should-you-offer-discounts-for-annual-commitments-a-strategic-guide-for-saas-leaders) (secondary).
27. Dodo Payments. [Purchasing power parity pricing for SaaS](https://dodopayments.com/billing/purchasing-power-parity) (vendor content).
28. Monetizely. [Grandfathering vs forced migration](https://www.getmonetizely.com/articles/grandfathering-vs-forced-migration-the-strategic-approach-to-price-changes-for-existing-customers) (secondary).
29. Freemius. [AppSumo marketplace and lifetime deals](https://freemius.com/blog/appsumo-marketplace-breakdown/).
30. Runway. [Pricing](https://runway.com/pricing) (fetched 2026-10-17).
31. CostBench. [Midjourney plans and pricing](https://www.costbench.com/software/ai-image-generators/midjourney/) (secondary; official docs returned 403).
32. ElevenLabs. [Pricing](https://elevenlabs.io/pricing) (fetched 2026-10-17).
33. Suno. [Pricing](https://suno.com/pricing) (fetched 2026-10-17); [CometAPI, Suno cost](https://www.cometapi.com/how-much-does-suno-ai-cost) (credit-per-song detail, secondary).
34. Wireflow. [Kling AI pricing](https://www.wireflow.ai/blog/kling-ai-pricing) (secondary); [Kling, Video 3.0 credit cost guide](https://home.kling.ai/blog/kling-video-3-0-credit-cost-guide).
35. Descript. [Pricing](https://www.descript.com/pricing) (fetched 2026-10-17).
36. Canva. [Pricing](https://www.canva.com/us/pricing/) (search snippet); [PricingSaaS, Canva Pro price change Sep 2026](https://pricingsaas.com/companies/canva/diffs/2026D254).
37. Cursor. [Pricing](https://cursor.com/pricing) (fetched 2026-10-17); [CostBench changelog, April 2026 restructure](https://costbench.com/changelog/cursor-plans-renamed-2026-04/).
38. Anthropic. [Claude pricing](https://claude.com/pricing) (fetched 2026-10-17).
39. CostBench. [ChatGPT pricing](https://www.costbench.com/software/ai-chatbots/chatgpt/) (secondary; official page returned 403).
40. Adobe. [Firefly plans](https://www.adobe.com/products/firefly/plans.html) (fetched 2026-10-17).
41. Luma AI. [Pricing](https://lumalabs.ai/pricing) (fetched 2026-10-17).
42. Pika. [Pricing](https://pika.art/pricing) (fetched 2026-10-17).
43. HeyGen. [Pricing](https://www.heygen.com/pricing) (fetched 2026-10-17).
44. Synthesia. [Pricing](https://www.synthesia.io/pricing) (fetched 2026-10-17).
45. Krea. [Pricing](https://www.krea.ai/pricing) (fetched 2026-10-17).
46. Bessemer Venture Partners. [The AI pricing and monetization playbook](https://www.bvp.com/node/1710). 2026 Feb 9 (page located; content not extracted).
