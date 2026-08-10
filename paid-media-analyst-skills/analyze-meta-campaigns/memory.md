# Memory: analyze-meta-campaigns

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-07-09: Quarterly wrap-up decks need per-platform breakdown + per-creative detail slides ([Account: Dental] Q2)
For a "how did our optimizations perform" deck, pair the top-line KPI cards with a full per-platform breakdown (spend/clicks/CTR/output) and per-campaign detail slides showing top creatives with labeled screenshot placeholders — this client wants to "get into the details," not just a summary. Also compute MoM for the current quarter and check `outputs/reports/ppt/` for a prior-quarter deck to use as a named benchmark before assuming none exists.

### 2026-07-09: A Meta ad-level export can't see an audience swapped into an existing ad set ([Account: Dental] Q2)
The Meta ad-level performance export has no audience/targeting column, so a new custom audience swapped into an EXISTING ad set is invisible — only a brand-new ad set name shows up. Before crediting or measuring an "audience added" optimization from ad-level data alone, check whether the ad set name itself is new; if not, state plainly the change isn't independently verifiable and get the exact audience name + launch date from the account team for the next pull. Watch for a decoy: an ad set literally named for the change (e.g. "...Retargeting...") can be a dormant $0-spend shell while the real activity sits on a same-audience sibling with a different suffix (e.g. "...- Engagers").

### 2026-07-09: Label client-reported figures not in the export as "per the client," never as verified ([Account: Dental] Q2)
A client-relayed figure that can't be corroborated in the platform's own export (e.g. a lead count mentioned verbally that isn't in the Meta export's Leads/Website leads/Meta leads fields) must be labeled "per the client" everywhere it appears, not presented as independently verified. Recommend the instrumentation gap that would fix it (pixel/CRM matchback) rather than silently trusting or silently omitting the figure.

### 2026-06-24: Size a WTB budget reallocation off the UNSPENT pool, weight by cost-per-WTB + headroom ([Product Line A] EMEA WTB)
When a WTB pass turns into "how much do we move," size it off the **unspent mid-flight pool** (each platform's plan − spent; a spent-out platform like LinkedIn is not a lever), and weight markets by **cost-per-WTB + headroom**, not buy-intent rate. Recompute **Meta-only** $/WTB (filter `cid` platform `fb` → Meta WTB ÷ Meta per-market spend; the market-read table's all-platform-WTB ÷ Meta-clicks blend slightly inflates a few markets). Rate alone over-indexes a tiny near-tapped market (Portugal 12.5% rate / 316 WTB / $0.61) and under-funds the scalable engine (UK $2.43/WTB, most headroom). Express each campaign's move as an explicit **+/− dollar shift vs run-rate** (pro-rata of the pool at current mix → shifts net to ~$0, budget-neutral), not target-minus-current. Move the inefficient reach platform → the engine as a small **test tranche** with a $/WTB trigger (TikTok −$2,000 → Meta, scale if ≤~$4/WTB); frame a high-spend low-intent market (Germany, 24% of Meta spend / $5.55/WTB) as a **cap + diagnose LP/audience**, not a hard cut.

### 2026-06-24: "Where to Buy" on-site click data = down-funnel buy-intent; judge by WTB-per-link-click, not CTR ([Product Line A] EMEA WTB)
A client on-site export (Adobe report-suite, keyed by the campaign `cid`) of Where-to-Buy button / distributor-link / Buy-Now clicks is the campaign's first purchase-intent signal — judge platforms and creatives by WTB ÷ paid link clicks, not by CTR. The `cid` self-describes platform (`fb`→Meta/`lin`→LinkedIn/`tiktok`), market and creative, so you do not need the creative-template join (that file is secondary enrichment, joined case-insensitively on `lower(cid)` — beware the `Personalised`/`personalised` case mismatch). Parse: header is the metric-ID row (3410/3820/1162), skip metadata rows, drop the `TOTAL` footer, recompute B+C+D (col E is a SUM formula → `data_only=True`); reconcile to the footer. The lens reordered [Product Line A] (Meta 95% of buy-intent at $2.95/WTB = engine; LinkedIn best rate 13.66% but $62.65/WTB; TikTok 48,525 clicks → 37 WTB = cheap reach ≠ cheap intent) and showed the best-CTR creative (carclassic 1.92%) was NOT the buy-intent driver (single-image/story beat carousel/video 2–18×).

### 2026-06-24: Paid-social export parsing traps — TikTok double aggregate, LinkedIn embedded newlines ([Product Line A] EMEA v3)
TikTok exports can carry BOTH a `Total of N results` footer row AND a separate `-` (dash) aggregate row equal to the sum of the real creatives — exclude both or a naive rollup doubles the total. LinkedIn UTF-16 exports embed newlines inside some fields (the French medical-device disclaimer), so parse with a proper `csv.reader`, not a line-split (line-split breaks mid-record and undercounts clicks).

### 2026-06-23: "Ads to pause" is usually the ad-set level, not the creative ([Product Line A] EMEA)
When every creative clears the blended CTR, drop to the ad-set rollup: parse audience + geo from `Ad set name`/`Campaign name`, find weak audience x geo cells (e.g. Spain-Students at 0.72% CTR), and recommend pause + reallocate to the better sibling (Spain-Medical 2.45%) or stronger audience (Medical vs Students). Put clicks/CTR in `current_metric`.

### 2026-06-23: Trust platform in-flight reporting over IO dates for flight windows ([Product Line A] EMEA)
Use the platform's own in-platform fields for flight windows and pause status, not the IO/plan dates (they can disagree). For LinkedIn read `Campaign End Date` + `Ad Status` (Active/Paused). A campaign can be 99.5% budget-exhausted yet still inside its flight window, so frame "spent out, in flight," not "finished."

### 2026-06-22: Meta export cannot give dimensions and daily in one file ([Product Line A] EMEA)
A Meta ad x day export came back dimensionless (no campaign, ad set, or geo), and re-exporting with dimensions added `Campaign name` + `Ad set name` but went period-aggregate. Pull both files: take the daily granularity from the dimensionless one and the campaign/ad-set/geo split from the aggregate one. Parse the Medical vs Students audience and the geo from the ad-set and campaign names (pattern "{Geo} Ads - {Medical|Students}", with some variants missing the "Ads" token).

### 2026-05-28: Order Meta lead slides by leads; footnote LP-pixel leads ([Account: Dental])
Reorder the "leads by campaign" view by lead count, and footnote any campaign whose leads are landing-page-pixel-tracked rather than native Meta form leads. Two small lead-gen campaigns drove 28 of 32 leads; identify the single best lead creative (lowest CPL) explicitly.

### 2026-05-27: Aggregate exports skip trend sections; confirm leads reach Salesforce ([Account: Dental])
An aggregate or lifetime Meta export (Reporting starts not equal to Reporting ends) supports campaign ranking and budget allocation but not WoW, fatigue, or pacing, so say so rather than fabricating trends. The client action is to confirm the reported leads flow into Salesforce and to validate lead quality before scaling. For blended Dental decks the user may convert CAD to USD at 0.73 with a per-table footnote.

### 2026-02-28: B2B lead-gen quality proxy is the lead-volume trend ([Account: Dental])
With no CPA targets and sparse downstream signal, use the lead-volume trend (flat or declining over three-plus weeks) as the primary quality proxy. Lead-gen campaigns populate Leads and Cost per lead; traffic or consideration campaigns populate Results and Cost per results with `Result indicator = actions:link_click`, so use the right column per objective.

## Standing preferences (apply every run)

- **Read with `encoding='utf-8-sig'`** (Meta exports carry a BOM). Use `Reporting starts` as the date field.
- **Judge ads/campaigns by clicks with strong CTRs, not spend.** Do not build spend-only bar charts unless the user asks. Put link clicks on every table and chart. For the "full metrics" visual use a single account-overview-by-channel table (one row per channel + total: spend/impr/clicks/CTR/CPC/CPM); on other slides lean on rich tables plus a few select dual-axis link-clicks-bars + CTR-line combo charts.
- **Two granularities:** daily (one row per ad per day, enables WoW, fatigue, and pacing) vs aggregate or lifetime (one row per ad, skip the trend sections).
- **Ad body copy is not in the export.** Creative analysis is limited to performance signals and ad-name conventions.
- **B2B constraints:** do not flag learning phase (50 conversions per week), audience size (under 50K), or attribution-window settings (not present in the data); all scaling is trend-based and relative.
- **Fatigue and kill signals:** Frequency over 4.0 (audience exhaustion), CPM WoW up 20%, CTR WoW down 20%, CPL WoW up 15%, impression drop WoW down 30%, and spend with zero results above account-average CPL times three.
