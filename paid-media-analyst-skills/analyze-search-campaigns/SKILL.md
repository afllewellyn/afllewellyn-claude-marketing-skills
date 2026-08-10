---
name: analyze-search-campaigns
description: Run the full Google Search campaign analysis pipeline (Agent 1 + Agent 2, plus Agent 3 if RSA ad copy columns are detected) on Google Ads CSV exports. Generates audit reports and actionable recommendation CSVs for keyword management, negative keywords, bid adjustments, structural improvements, and ad copy optimization.
argument-hint: "[product-name or data-file-path]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# Google Search Campaign Analyzer

Run the full Search campaign analysis pipeline on Google Ads CSV data exports. This skill combines Agent 1 (Search Performance Analyst) and Agent 2 (Keyword & Negative Manager) into a single workflow, and conditionally runs Agent 3 (Ad Copy Analyst) when RSA ad copy columns are detected in the data.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## Cross-Reference Reconciliation (mandatory on every pass)

Running a search account is fundamentally a reconciliation job: never read any one file
in isolation. On every pass, each agent cross-checks the uploaded files against each other
— the **Search Terms Report against the active keyword set**, and both against the
performance / Impression-Share / conversion reports — to surface, every time:
- **Gaps to fill** — search terms or themes that have demand or are performing but are
  **not yet targeted as keywords** (→ `ADD_KEYWORD_EXACT` / `CREATE_AD_GROUP`), and any
  coverage the reports show is missing.
- **Terms to pause / narrow** — keywords or ad groups capturing irrelevant, low-quality,
  or off-intent queries (→ `PAUSE_KEYWORD` / `NARROW_MATCH_TYPE` / negatives).

Before you characterize, pause, narrow, or consolidate any keyword or ad group, look at
**what it actually captures** in the Search Terms Report — never judge it from the keyword
list or aggregate metrics alone. (Common example: a low-performing Broad keyword / ad group
is often a brand-query catch-all — quantify the brand share and stand up a [Client] branded
ad group to capture it before pausing.) This is the core analyst loop — run it on every pass,
for every subagent, not only when something looks wrong.

## What You Receive as Arguments

- `$ARGUMENTS` — Either a product/division name to auto-detect files in `data/raw/google/`, OR an explicit path to a data file.

## Step 1: Detect and Load Data Files

Scan `data/raw/google/` for CSV files matching the argument. For each file:

1. **Detect encoding**: Try UTF-8 first, fall back to UTF-16 LE. Real Google Ads Editor exports are typically UTF-16 LE with tab separators. Use `iconv -f UTF-16LE -t UTF-8` for conversion, then parse as TSV.
2. **Parse structure**: Row 1 = report name, Row 2 = date range (quoted), Row 3 = headers, Row 4+ = data.
3. **Classify file type** by header columns:
   - **Keyword Performance / Full Export**: Contains `Campaign`, `Ad group`, `Search keyword`, `Clicks`, `Impr.`, `CTR`, `Avg. CPC`, `Cost`. May also include RSA ad copy columns (Headline 1–15, Description 1–4) and `Impr. (Abs. Top) %`.
   - **Search Terms Report**: Contains `Search term`, `Search terms match type`, `Campaign`, `Ad group`, `Search keyword`.
   - **Dedicated Search Impression Share Report**: Contains `Search Impr. share` (and lacks search-term / keyword identifiers). Expected columns: `Campaign`, `Ad group`, `Impressions`, `Clicks`, `Cost`, `Search Impr. share`, `Search Lost IS (Budget)`, `Search Lost IS (Rank)`, `Search Top IS`, `Search Abs. Top IS`. Pass to Agent 1 as the IS source of truth.
   - **Conversion Report**: Contains `Conversions` AND (`Cost / conv.` OR `Conv. rate`). Expected columns: `Campaign`, `Ad group`, `Conversions`, `Conv. value`, `Cost / conv.`, `Conv. rate`. Pass to Agent 1 to enable conversion-aware IS prioritization and Module 14/15 rendering in Agent 6.
4. **Report what was found**: List each detected file, its type, encoding, row count, and date range.

If no Search Terms Report is found, note the limitation and skip negative keyword analysis (Section 4 of Agent 2). If no IS or conversion report is found, Agent 1 falls back to embedded IS columns / click-volume-weighted prioritization respectively.

## Step 2: Calculate Baselines

From the keyword performance data, calculate:
- Total and per-campaign: spend, clicks, impressions
- Account average CTR (weighted by impressions)
- Account average CPC (weighted by clicks)
- Campaign-level benchmarks for comparison

If Search Terms Report available, also calculate:
- Search term average CTR and CPC
- Match type distribution (Broad, Phrase, Exact, close variants)
- Total unique search terms

## Step 3: Run Agent 1 — Search Performance Audit

Reference spec: `prompts/agent_1_search_analyst.md`

### Wasted Spend Detection
Flag keywords where:
- `clicks > 50 AND ctr < (account_avg_ctr * 0.5)` → Low CTR waste
- `cpc > (account_avg_cpc * 1.5) AND clicks < 10` → High CPC, low volume waste

### Impression Share Analysis
If `Impr. (Abs. Top) %` is available:
- Identify keywords with high CTR but low Abs Top % (headroom for bid increases)
- Flag campaigns with systematically low positioning

If `Search Lost IS (Budget)` or `Search Lost IS (Rank)` available:
- `lost_is_budget > 20%` → Budget-constrained
- `lost_is_rank > 20%` → Rank-constrained

### Structural Issues
Flag:
- Ad groups with >20 keywords (too broad)
- Ad groups with <5 keywords AND <100 impressions (too narrow)
- RSA coverage (if ad copy columns present)

### Campaign Health Scorecard
Rank campaigns by efficiency: CTR, CPC, cost, click volume. Identify the best and worst performers.

## Step 4: Run Agent 2 — Keyword & Negative Manager

Reference spec: `prompts/agent_2_keyword_negative_manager.md`

> Run the **Cross-Reference Reconciliation** above before emitting any promote / add / pause / narrow actions — every pass yields both gaps to fill and terms to pause.

### Keyword Promotion Analysis
Flag keywords where:
- `ctr > (account_avg_ctr * 1.5) AND clicks > 20` → Strong performer
- For each, recommend bid increases based on `Impr. (Abs. Top) %` headroom
- Rank by `impressions × (1 - impr_abs_top_pct)` for prioritization

**Optional search-volume enrichment (DataForSEO MCP).** If the `dataforseo` MCP
server is connected, enrich the promotion shortlist + net-new keyword candidates
with market search volume / competition / top-of-page CPC via
`mcp__dataforseo__keywords_data_google_ads_search_volume` (see Agent 2 spec
Section 3b). **Respect the API rate limits — do not blast the endpoint:** batch
the de-duplicated keyword list into ONE call (the hard cap is 1,000 keywords/request
and 12 req/min; stay conservatively at ≤500 keywords/request and ≤6 req/min, spacing
any extra calls ~10s apart). If the server is not connected, skip silently and note
it in Data Limitations — never block the pipeline on it.

### Negative Keyword Detection (requires Search Terms Report)
Flag search terms where:
- `ctr < 1% AND impressions > 100` → Low relevance
- `clicks = 0 AND impressions > 50` → Zero engagement
- `cpc > (account_avg_cpc * 2.0) AND clicks < 3` → High-cost irrelevant

Run semantic relevance check — flag consumer/off-topic patterns. [Client] is a B2B healthcare company, so consumer-oriented queries are waste. Build the off-topic pattern list dynamically based on the division's product category:

1. **Review the campaign names, ad groups, and keywords** to understand what products/services are being advertised (e.g., surgical supplies, wound care, infection prevention, dental products, health information systems).
2. **Identify consumer vs. professional intent** based on the division's context:
   - Consumer retail patterns: amazon, walmart, buy online, coupon, cheap, discount, for sale
   - Consumer intent patterns: at home, diy, near me, for kids, for children, for baby
   - Informational/research patterns: what is, how to, how does, can i, how do
   - Job/career patterns: jobs, salary, career, training, school, course
   - Off-category patterns: Identify product categories clearly outside the division's scope (e.g., food products triggering on "warmer" keywords, consumer OTC products triggering on professional medical keywords)
3. **Flag division-specific irrelevance**: For each division, identify the specific consumer product terms that bleed into professional B2B campaigns (these vary by division — dental has toothpaste/mouthwash, surgical has consumer first-aid, wound care has home remedies, etc.)

Group negatives by theme with recommended match type and scope (account-level vs campaign-level).

### Keyword Expansion (requires Search Terms Report)
Identify high-performing search terms NOT already targeted as keywords:
- Aggregate search terms (same term may appear multiple times across campaigns)
- Filter: 3+ clicks, CTR > 3%, not consumer/off-topic, not already a keyword
- Tier by volume: Tier 1 (20+ clicks), Tier 2 (10-20 clicks), Tier 3 (new themes)
- Flag search terms triggered by many different keywords across campaigns (structural gap — may need a dedicated ad group)
- Check for brand navigation queries (parent brand "[Client]" or legacy "[Former Parent Co]" + product terms) that lack dedicated branded keywords

### Match Type Performance
If match type data available from Search Terms Report:
- Compare CTR and CPC across Broad, Phrase, Exact, and close variants
- Flag Broad match keywords triggering excessive unique search terms (>500 terms)
- Recommend narrowing high-spread keywords from Broad to Phrase

### Keyword Consolidation & Deduplication
Detect near-duplicates:
- Word-order variants (e.g., "product category device" vs "device product category")
- Normalize keywords (lowercase, sort words, remove punctuation)
- For each duplicate set: identify the stronger performer, recommend pausing the weaker

### Zero-Impression Keywords
Flag keywords with 0 impressions over the full period. Recommend investigation for negative keyword conflicts or low search volume status.

## Step 5: Run Agent 3 — Ad Copy Analyst (Conditional)

**Only run this step if RSA ad copy columns are detected in the data** (Headline 1 through Headline 15, Description 1 through Description 4).

If RSA columns are present:

Reference spec: `prompts/google/agent_3_ad_copy_analyst.md`

### Ad Creative Inventory
Extract all unique creatives (Campaign + Ad group + headline/description combo). Classify as Branded, Non-Branded, or Conquest. Aggregate performance metrics.

### Headline-to-Keyword Alignment
For each ad group, compare top search terms (from Agent 2's search terms analysis) against RSA headlines. Score alignment as YES / PARTIAL / NO. Prioritize mismatches by click volume.

### Landing Page Alignment
Fetch unique Final URLs via WebFetch. Extract key messaging and cross-reference against ad copy. Flag gaps, contradictions, and missing proof points.

### Structural Copy Issues
Flag: description redundancy across ad groups, empty display URL paths, conquest copy identical to branded, missing brand transition language (if rebrand detected), brand name in H1 on non-branded ad groups.

### Recommended Copy Rewrites
For each flagged issue, provide current → recommended copy with position, rationale, and estimated CTR impact (HIGH/MEDIUM/LOW).

### Agent 3 Outputs
- Report: `outputs/reports/google/ad_copy_audit_YYYY-MM-DD.md`
- Actions CSV: `outputs/recommendations/google/ad_copy_audit_actions_YYYY-MM-DD.csv`
- Excel workbook: `outputs/recommendations/google/ad_copy_audit_YYYY-MM-DD.xlsx`

If RSA columns are NOT present, skip this step and note in the Agent 1 report: "No RSA ad copy columns detected — run `/analyze-search-ad-copy` separately with a full export containing Headline/Description columns."

## Step 6: Generate Agent 1 + 2 Outputs

### Report Files

- Search audit report: `outputs/reports/google/search_audit_YYYY-MM-DD.md`
- Keyword management report: `outputs/reports/google/keyword_management_YYYY-MM-DD.md`

Both go in `outputs/reports/google/`. Structure of each report:

Structure:
1. **Header metadata**: account, date range, data sources, agent attribution
2. **Data availability table**: what columns/reports were available vs missing
3. **Executive summary**: key metrics table + top 3-5 findings
4. **Match type performance** (if available)
5. **Campaign health scorecard**: ranked by efficiency
6. **Wasted spend analysis**: flagged keywords with cost quantification
7. **Keywords to promote**: bid increase recommendations with headroom data
8. **Negative keywords to add**: grouped by theme with match type and scope
9. **Keyword expansion opportunities**: tiered by volume
10. **Search term spread analysis**: keywords triggering too many unique terms
11. **Keyword consolidation**: near-duplicates with recommended actions
12. **Prioritized actions summary**: High / Medium / Low with estimated impact
13. **Total estimated monthly impact**: savings + incremental opportunity

### Actions CSV: `outputs/recommendations/search_audit_actions_YYYY-MM-DD.csv`

Columns: `priority,action_type,account_id,campaign,ad_group,keyword,current_metric,recommendation,implementation,estimated_impact`

Action types:
- `ADD_NEGATIVE_PHRASE` / `ADD_NEGATIVE_EXACT`: Negative keyword additions
- `ADJUST_BID_UP`: Max CPC increases on high-performers
- `ADD_KEYWORD_EXACT`: New keyword additions from search term mining
- `CREATE_AD_GROUP`: Structural additions (e.g., new branded ad group)
- `NARROW_MATCH_TYPE`: Broad → Phrase/Exact changes
- `CONSOLIDATE_KEYWORDS`: Pause weaker near-duplicates
- `PAUSE_KEYWORD`: Zero-impression or confirmed waste keywords

Sort by priority (High → Medium → Low), then by estimated_impact.

## Step 7: Optional — Generate Executive PPT (Agent 6)

If the user passes `--ppt` in `$ARGUMENTS` or asks for a deck, invoke Agent 6 (`prompts/meta/agent_6_executive_ppt.md`) after Agents 1 + 2 (+ 3) finish. Despite the file path, Agent 6 is the canonical multi-platform PPT generator and supports Google-only, Bing-only, blended, and Meta-aware decks.

Agent 6 will:
- Detect platform availability across `outputs/reports/{google,bing,meta}/` and `data/raw/{google,bing}/`.
- Render only the slide modules whose data is present (variable slide count).
- Anchor the deck on the Impression Share deep-dive (Module 14) when IS data is present, with Recommendations on Module 15 and Next Steps on Module 16.
- Label per-platform conversion availability explicitly so a missing-Bing-conversion line is never misread as zero.

For any blended Google + Bing engagement: run `/analyze-search-campaigns <account>` and `/analyze-bing-campaigns <account>` first, then invoke Agent 6 once across the combined outputs to produce a single blended deck.

## Step 8: Update CLAUDE.md

After generating outputs, append key findings to the `## Session Learnings` section of `CLAUDE.md`:
- Data format notes (encoding, column availability)
- Account profile summary (campaigns, keywords, spend, CTR, CPC)
- Top findings and structural issues discovered
- Output file paths generated

## Important Notes

- **Encoding**: Always check for UTF-16 LE first on real Google Ads exports. Use `iconv -f UTF-16LE -t UTF-8` for conversion.
- **Missing columns**: Gracefully handle missing Quality Score, Impression Share, and Match Type columns. Note limitations in the report.
- **B2B context**: [Client] is a B2B healthcare company (formerly [Former Parent Co] Health Care) spanning multiple divisions — surgical solutions, infection prevention, wound care, dental, health information systems, and more. Consumer queries are waste; professional/clinical queries are relevant. Adapt the consumer vs. professional distinction to each division's product category.
- **Bidding strategy**: Maximize Clicks with Max CPC caps. NOT conversion-focused. KPIs are traffic efficiency metrics.
- **Be specific in recommendations**: Include current values, specific new bid amounts, exact negative keyword text and match types, and quantified estimated impact.
- **Commit outputs**: After generating reports, commit the output files to the repository.
