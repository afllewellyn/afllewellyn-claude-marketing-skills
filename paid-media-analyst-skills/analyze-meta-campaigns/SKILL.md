---
name: analyze-meta-campaigns
description: Run the full Meta Ads analysis pipeline (Agents 0–5) on a Meta Ads Manager CSV export. Generates creative, audience, budget scaling, cross-KPI, and cross-platform audit reports plus actionable recommendation CSVs. Use this skill whenever the user drops a Meta Ads export into data/raw/meta/, asks to analyze Meta campaigns, wants a Meta performance audit, or types /analyze-meta-campaigns — even if they don't use those exact words. Also use this skill when the user asks to re-run, update, or refresh Meta analysis outputs.
argument-hint: "[optional: specific CSV filename in data/raw/meta/]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# Meta Ads Campaign Analyzer

Run the full Meta Ads analysis pipeline on a Meta Ads Manager export. This skill orchestrates Agent 0 (Data Validator) through Agent 5 (Cross-Platform Synthesizer) in sequence, producing 5 audit reports and 5 action CSVs.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## What You Receive as Arguments

- `$ARGUMENTS` — Optional. A specific CSV filename in `data/raw/meta/`. If empty, auto-detect the most recently modified CSV in `data/raw/meta/`.

## Step 0: Detect and Validate the Data File

### File Detection

```python
import glob, os
files = glob.glob("data/raw/meta/*.csv")
target = $ARGUMENTS if $ARGUMENTS else max(files, key=os.path.getmtime)
```

Read the file with `encoding='utf-8-sig'` (BOM-prefixed UTF-8). Report the filename, row count, and file size.

### Infer Key Parameters

Before validation, derive the two values that drive all output file naming:

1. **Account name** — Scan unique values in the `Campaign name` column. Look for a consistent prefix or recurring pattern (e.g., all campaigns starting with "CORE-" → account = `account_dental`). Normalize to lowercase with underscores.

2. **Report date** — Find the maximum value in `Reporting starts`. This is the period end date used in output filenames (`YYYY-MM-DD`).

### Column Validation

Confirm all 19 required columns are present:

| Required Column | Notes |
|---|---|
| Campaign name | |
| Ad set name | |
| Ad name | |
| Reporting starts | Primary date column (= Reporting ends for daily rows) |
| Reporting ends | |
| Impressions | |
| Reach | |
| Frequency | |
| Amount spent (USD) | |
| CPM (cost per 1,000 impressions) (USD) | |
| CPC (cost per link click) (USD) | |
| CTR (link click-through rate) | |
| Link clicks | |
| Results | Used by traffic/consideration campaigns |
| Result indicator | Should contain `actions:link_click` for traffic campaigns |
| Cost per results | Used by traffic/consideration campaigns |
| Leads | Used by lead gen campaigns |
| Cost per lead (USD) | Used by lead gen campaigns |
| Ad delivery | Tracks active/paused/not_delivering/rejected status |

Full validation spec: `prompts/meta/agent_0_data_validator.md`

### Data Granularity Detection

Detect whether the export contains **daily** or **aggregate** (lifetime) data:
- **Daily**: `Reporting starts` == `Reporting ends` on most rows (one row per ad per day). Enables full trend/WoW analysis.
- **Aggregate**: `Reporting starts` != `Reporting ends` on most rows (one row per ad for the full period). Limits analysis to total performance comparisons — skip all WoW trend sections, frequency trajectory, and fatigue detection that require time-series data.

Set `DATA_GRANULARITY = DAILY | AGGREGATE` and carry this flag through all agents. Print it in the validation summary.

### Validation Status

Output a status:

- **GREEN** — All 19 columns present, date range ≥ 14 days, no critical data gaps. Proceed.
- **YELLOW** — Minor issues (missing optional columns, partial weeks). Note limitations and proceed.
- **RED** — Critical columns missing, or zero rows with spend. Stop and report what's needed to fix the file.

If RED, print the full issue list and stop. Do not proceed to analysis.

### Print Validation Summary

```
## Data Validation Summary
File: <filename>
Account: <inferred_account>
Date range: <YYYY-MM-DD> to <YYYY-MM-DD> (<N> days, <N> weeks)
Campaigns: <N unique campaigns>
Ad sets: <N unique ad sets>
Ads: <N unique ads>
Total rows: <N>
Missing columns: <list or "None">
Status: GREEN / YELLOW / RED
```

---

## Step 1: Calculate Account-Level Baselines

Before running any agent, compute these benchmarks from the full dataset. Every agent uses them for relative comparisons.

**Handle both data granularities:**

```python
import pandas as pd
df = pd.read_csv(target, encoding='utf-8-sig')

# Detect granularity
is_daily = (df['Reporting starts'] == df['Reporting ends']).mean() > 0.5
DATA_GRANULARITY = 'DAILY' if is_daily else 'AGGREGATE'

# For DAILY data: aggregate daily rows to ad level before computing totals
# For AGGREGATE data: each row is already a total — use directly
if DATA_GRANULARITY == 'DAILY':
    # Group by ad to get totals
    ad_totals = df.groupby(['Campaign name', 'Ad set name', 'Ad name']).agg({
        'Amount spent (USD)': 'sum', 'Impressions': 'sum', 'Link clicks': 'sum',
        'Leads': 'sum', 'Reach': 'max', 'Frequency': 'max'
    }).reset_index()
else:
    ad_totals = df  # Already aggregated

lead_gen = ad_totals[ad_totals['Leads'].notna() & (ad_totals['Leads'] > 0)]
traffic  = df[df['Result indicator'].str.contains('link_click', na=False)] if 'Result indicator' in df.columns else pd.DataFrame()

# Account-level baselines
total_spend     = ad_totals['Amount spent (USD)'].sum()
total_leads     = ad_totals['Leads'].sum()
lead_gen_spend  = lead_gen['Amount spent (USD)'].sum()
blended_cpl     = lead_gen_spend / total_leads if total_leads > 0 else None
kill_threshold  = blended_cpl * 3 if blended_cpl else None
total_impressions = ad_totals['Impressions'].sum()
avg_cpm         = total_spend / total_impressions * 1000 if total_impressions > 0 else None
avg_ctr         = ad_totals['Link clicks'].sum() / total_impressions if total_impressions > 0 else None
avg_frequency   = ad_totals['Frequency'].mean()
```

Print a baseline summary table before starting agents. Include `Data Granularity: DAILY / AGGREGATE` in the summary.

**If AGGREGATE**: Print a note at the top: _"Data is lifetime-aggregated (not daily). Trend analysis (WoW comparisons, fatigue detection, pacing) is not available. Reports will focus on total campaign performance, ranking, and budget allocation."_

**Key thresholds to carry through all agents:**

| Threshold | Value | Rule |
|---|---|---|
| Kill threshold | 3× blended lead gen CPL | Pause any ad set with CPL above this |
| Frequency saturation | 4.0 | Flag for creative refresh if frequency ≥ 4.0 |
| Creative fatigue — CTR | −20% WoW | Flag 3 consecutive weeks of decline |
| CPM spike | +20% WoW | Flag as auction pressure or delivery issue |
| CPL improvement trend | −15% WoW for 3+ weeks | Strong positive — protect or scale |

---

## Step 2: Run Agent 1 — Creative Performance Audit

Reference spec: `prompts/meta/agent_1_creative_analyst.md`

**Key tasks:**
- Aggregate daily rows to ad level (or use directly if AGGREGATE); compute per-ad totals for spend, impressions, clicks, leads, CPL, CTR, frequency
- Classify ads by type (Single Image, Carousel, Video, Lead Gen Form, Collection) based on ad name conventions when format column is unavailable
- Calculate account-level creative benchmarks (avg CTR, avg CPL, avg CPM by ad type)
- Rank top 3 and bottom 3 performers per ad set by CPL (lead gen) or CTR (traffic)
- Flag creative fatigue: frequency > 4.0, CTR declining ≥ 20% WoW for 2+ consecutive weeks, spend with zero results
- Note: Ad copy text is not in the export. Base all analysis on performance signals and ad name patterns only.

**If `DATA_GRANULARITY == AGGREGATE`:** Skip CTR decline WoW fatigue detection (requires daily time-series). Still perform frequency snapshot flags (> 4.0) and spend-with-zero-results checks. All other sections (ad ranking, benchmarks, type classification) work normally on aggregate data.

**Output files:**
- `outputs/reports/meta/creative_audit_<account>_<date>.md`
- `outputs/recommendations/meta/creative_audit_actions_<account>_<date>.csv`

Action CSV columns: `priority, action_type, account, campaign, ad_set, ad_name, current_metric, recommendation, estimated_impact`

Common action types: `PAUSE_AD`, `REFRESH_CREATIVE`, `TEST_NEW_FORMAT`, `SCALE_CREATIVE`, `INVESTIGATE_DELIVERY`

---

## Step 3: Run Agent 2 — Audience & Ad Set Audit

Reference spec: `prompts/meta/agent_2_audience_analyst.md`

**Key tasks:**
- Aggregate daily rows to weekly buckets per ad set (or use totals directly if AGGREGATE); compute weekly CPM, CTR, frequency, leads, CPL
- Identify audience saturation signals: frequency > 4.0, CPM rising >20% WoW with CTR flat or declining
- Flag ad sets with delivery issues: `Ad delivery` column showing `not_delivering` or `rejected`
- Identify period-over-period trends: CPL direction (improving/declining/volatile), CPM trajectory, reach vs. frequency tradeoff
- Flag ad sets where both ads are rejected (complete delivery failure vs. partial)
- Assess whether ad set consolidation would reduce audience overlap within the same campaign

**If `DATA_GRANULARITY == AGGREGATE`:** Skip WoW CPM trend analysis and period-over-period performance sections. Replace CPM trends with static CPM comparison (each ad set vs. account avg, flag >150% as HIGH COST). Still perform ad set inventory, frequency snapshot, delivery status, overlap detection, and structural assessment.

**Output files:**
- `outputs/reports/meta/audience_audit_<account>_<date>.md`
- `outputs/recommendations/meta/audience_audit_actions_<account>_<date>.csv`

Action CSV columns: `priority, action_type, account, campaign, ad_set, current_metric, recommendation, estimated_impact`

Common action types: `PAUSE_ADSET`, `INVESTIGATE_DELIVERY`, `CONSOLIDATE_ADSETS`, `REFRESH_AUDIENCE`, `MONITOR_FREQUENCY`, `MONITOR_CPM`

---

## Step 4: Run Agent 3 — Budget & Scaling Audit

Reference spec: `prompts/meta/agent_3_budget_scaling.md`

**Key tasks:**
- Map spend distribution: % of budget in traffic vs. lead gen; % in top 2 campaigns vs. rest
- Identify budget concentration risk (top 2 campaigns > 50% of spend)
- Assess scaling candidates: lead gen ad sets at CPL below kill threshold with frequency headroom (< 3.0) and improving or stable CPL trend
- Identify budget drains: ad sets at or above kill threshold, or spending with zero results
- Model reallocation scenarios: what additional leads would result from redirecting drain spend to efficient lead gen ad sets
- Flag any campaigns that have been paused at efficient CPLs — this is an operational issue, not a budget issue

**If `DATA_GRANULARITY == AGGREGATE`:** Use the alternate static decision tree (Section 3B in Agent 3 spec) instead of the WoW-based decision tree. Decisions are based on CPL vs. account average, kill threshold, spend concentration, and frequency level. Still perform spend distribution mapping and cross-campaign reallocation analysis.

**Output files:**
- `outputs/reports/meta/budget_scaling_<account>_<date>.md`
- `outputs/recommendations/meta/budget_scaling_actions_<account>_<date>.csv`

Action CSV columns: `priority, action_type, account, campaign, ad_set, current_metric, recommendation, estimated_impact`

Common action types: `SCALE_BUDGET`, `REDUCE_BUDGET`, `PAUSE_ADSET`, `REACTIVATE`, `REALLOCATE`, `HOLD_AND_MONITOR`

---

## Step 5: Run Agent 4 — Cross-KPI & Funnel Audit

Reference spec: `prompts/meta/agent_4_cross_kpi_analyst.md`

**Key tasks:**
- Map the full funnel: awareness → traffic/consideration → lead gen → conversion. Identify which stages are funded vs. gaps.
- Aggregate weekly KPI trends for all active campaigns; note trajectory (improving / declining / volatile / stable)
- Detect KPI conflicts: cases where one metric is improving but another is worsening (e.g., CTR rising while CPL rising — click quality may be declining)
- Assess whether traffic spend is generating a retargetable warm audience that is being converted downstream; flag if no retargeting layer exists
- Lead volume stagnation analysis: flag ad sets with flat or zero leads for 3+ consecutive weeks
- Synthesize cross-account structural gaps (e.g., 83% of spend in traffic with no conversion layer)

**If `DATA_GRANULARITY == AGGREGATE`:** Skip WoW trend analysis and lead volume stagnation detection. Replace campaign trajectory (IMPROVING/STABLE/MIXED/DECLINING) with static classification (PERFORMING/UNDERPERFORMING/NEUTRAL based on CPL vs. account avg). Use static KPI conflict equivalents instead of WoW triggers. Still perform funnel mapping, account-level summary, and structural gap analysis.

**Output files:**
- `outputs/reports/meta/cross_kpi_audit_<account>_<date>.md`
- `outputs/recommendations/meta/cross_kpi_actions_<account>_<date>.csv`

Action CSV columns: `priority, action_type, account, campaign, ad_set, current_metric, recommendation, estimated_impact`

Common action types: `REACTIVATE`, `PAUSE_ADSET`, `ADD_LEAD_GEN_LAYER`, `INVESTIGATE_DELIVERY`, `CONSOLIDATE_ADSETS`, `MONITOR_CPM`, `ESTABLISH_BASELINES`

---

## Step 6: Run Agent 5 — Cross-Platform Synthesizer (Conditional)

**Only run this step if Google outputs exist.** Check:
```bash
ls outputs/reports/google/*.md 2>/dev/null | head -5
```

If no Google outputs exist, skip this step and note it in the final summary.

Reference spec: `prompts/meta/agent_5_cross_platform_synthesizer.md`

**Key tasks:**
- Read the available Google reports from `outputs/reports/google/`
- Compare Google spend + click efficiency against Meta spend + lead gen efficiency
- Identify funnel gaps visible only from a cross-platform view: Google search visitors not retargeted on Meta; Meta traffic engagers with no lead gen layer
- Identify shared product lines where both platforms are active, and note where one platform is paused/missing
- Identify budget reallocation opportunities across platforms (e.g., redirect Google conquest spend to Meta lead gen)
- Synthesize the single most important cross-platform action

**Output files:**
- `outputs/reports/meta/cross_platform_synthesis_<account>_<date>.md`
- `outputs/recommendations/meta/cross_platform_actions_<account>_<date>.csv`

Action CSV columns: `priority, action_type, account, platform, campaign_or_source, target_campaign_or_destination, current_metric, recommendation, estimated_impact`

---

## Step 7: Generate Final Summary

After all agents complete, print:

### Generated Files

| File | Type | Status |
|---|---|---|
| `creative_audit_<account>_<date>.md` | Report | ✅ / ⚠️ skipped |
| `creative_audit_actions_<account>_<date>.csv` | Actions | ✅ / ⚠️ skipped |
| `audience_audit_<account>_<date>.md` | Report | ✅ / ⚠️ skipped |
| `audience_audit_actions_<account>_<date>.csv` | Actions | ✅ / ⚠️ skipped |
| `budget_scaling_<account>_<date>.md` | Report | ✅ / ⚠️ skipped |
| `budget_scaling_actions_<account>_<date>.csv` | Actions | ✅ / ⚠️ skipped |
| `cross_kpi_audit_<account>_<date>.md` | Report | ✅ / ⚠️ skipped |
| `cross_kpi_actions_<account>_<date>.csv` | Actions | ✅ / ⚠️ skipped |
| `cross_platform_synthesis_<account>_<date>.md` | Report | ✅ (Google data found) / ⚠️ skipped (no Google data) |
| `cross_platform_actions_<account>_<date>.csv` | Actions | ✅ / ⚠️ skipped |

### Top 3 Priority Actions (across all action CSVs)

Read all generated action CSVs and surface the 3 highest-priority rows (by `priority` = High first, then by estimated_impact if tied):

| # | Priority | Platform | Campaign / Ad Set | Action | Estimated Impact |
|---|---|---|---|---|---|
| 1 | High | Meta | ... | ... | ... |
| 2 | High | Meta | ... | ... | ... |
| 3 | High | Meta / Google | ... | ... | ... |

---

## Step 8: Update CLAUDE.md

Append a brief session learning entry to the `## Session Learnings` section of `CLAUDE.md`:

```markdown
### Meta Ads Analysis — <account> (<date>)
- File: <filename> | <N> campaigns, <N> ad sets, <N> ads | <period>
- Total spend: $<X> | Lead gen: $<X> (<N>%) | Traffic: $<X> (<N>%)
- Blended CPL: $<X> | Kill threshold: $<X> | Total leads: <N>
- Key findings: <2-3 bullet points — top structural issues or wins found>
- Outputs: <list generated file paths>
```

---

## Important Notes

### Data Handling
- **Encoding**: Always use `encoding='utf-8-sig'` — Meta exports use UTF-8 with BOM.
- **Date column**: Use `Reporting starts` as the date field. Daily rows will have matching `Reporting starts` and `Reporting ends`.
- **Lead gen vs. traffic**: Lead gen campaigns populate `Leads` + `Cost per lead (USD)`. Traffic campaigns populate `Results` + `Cost per results` (where `Result indicator` = `actions:link_click`). Never mix these columns when calculating CPL.
- **Aggregation**: Always sum/group daily rows before calculating derived metrics. Raw file has one row per ad per day.

### Analysis Conventions
- **Never use the word "waste"** — reframe as efficiency opportunities, optimization candidates, or budget misallocation.
- **B2B healthcare context**: [Client] dental products target dental professionals, not consumers. This shapes relevance judgments throughout.
- **No learning phase targets**: B2B lead volumes are too low to reach Meta's 50-conversion learning threshold. Don't flag this as an issue.
- **Volatility at low volume**: CPL swings of ±50% week-over-week are statistically normal at 1–5 leads/week. Require 3+ consecutive weeks of directional movement before recommending changes.
- **Operational vs. performance issues**: Distinguish between ads/campaigns paused by the team (operational decision) vs. those with declining performance. Operational pauses of efficient assets should be flagged as reactivation opportunities, not treated as performance failures.

### Commit Outputs
After generating all reports, commit the output files to the repository with a message like:
`Run Meta analysis for <account> — Q1 2026 data (<N> campaigns, <N> leads, $<X> spend)`
