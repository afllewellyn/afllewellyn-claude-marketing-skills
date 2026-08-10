# Meta Ads Analysis Orchestrator

## Purpose
Run all Meta Ads analysis agents in sequence from a single prompt. Drop your Meta performance CSV export in `data/raw/meta/` and run this orchestrator — it will execute Agent 0 through Agent 4 in order, then optionally trigger Agent 5 (cross-platform synthesis) if Google outputs are also present.

**Expected input:** A single performance CSV exported from Meta Ads Manager at the ad level. Two data formats are supported:
- **Daily breakdown (recommended):** One row per ad per day — enables full trend/WoW analysis, fatigue detection, and pacing.
- **Aggregate/lifetime:** One row per ad with totals for the full period — enables campaign ranking, budget allocation, and performance comparisons but skips trend-based sections.

See CLAUDE.md for the recommended export settings and required columns. Ad copy text analysis is not available in this export format — Agent 1 covers performance signals and creative fatigue only.

---

## Instructions for Claude Code

When I run this orchestrator, you will execute the following steps in order. Do not skip steps. If a step returns a RED status or critical failure, pause and report before continuing.

---

### STEP 0 — Pre-Flight Validation (Agent 0)
Run the data validator as defined in `prompts/meta/agent_0_data_validator.md`.

- Detect all files in `data/raw/meta/`
- Validate required columns, date range, ad hierarchy
- **Detect data granularity:** `DAILY` or `AGGREGATE` (see Agent 0 spec for detection logic)
- Report GREEN / YELLOW / RED status

**Carry the `DATA_GRANULARITY` flag** through all subsequent steps. If `AGGREGATE`, each agent will skip WoW-dependent sections and use static analysis alternatives as defined in their specs. Print the granularity in the validation summary.

**If RED:** Stop here. Report what is missing. Do not proceed with analysis until the data issue is resolved.

**If YELLOW:** Note the warnings, then continue with analysis. Flag data limitations in each subsequent report.

**If GREEN:** Proceed immediately to Step 1.

---

### STEP 1 — Creative Performance Analysis (Agent 1)
Run as defined in `prompts/meta/agent_1_creative_analyst.md`.

- Analyze ad-level creative performance using metrics and ad name conventions only (no copy text available)
- Classify ad types, detect fatigue, surface top/bottom performers
- Generate:
  - `outputs/reports/meta/creative_audit_[account]_[date].md`
  - `outputs/recommendations/meta/creative_audit_actions_[account]_[date].csv`

Confirm both files are written before proceeding.

---

### STEP 2 — Audience & Ad Set Analysis (Agent 2)
Run as defined in `prompts/meta/agent_2_audience_analyst.md`.

- Analyze ad set-level CPM trends, frequency, period-over-period performance
- Detect audience overlap and structural issues
- Generate:
  - `outputs/reports/meta/audience_audit_[account]_[date].md`
  - `outputs/recommendations/meta/audience_audit_actions_[account]_[date].csv`

Confirm both files are written before proceeding.

---

### STEP 3 — Budget Scaling Analysis (Agent 3)
Run as defined in `prompts/meta/agent_3_budget_scaling.md`.

- Apply the budget scaling decision tree to all campaigns and ad sets
- Incorporate frequency signals from Step 2 outputs when relevant
- Generate:
  - `outputs/reports/meta/budget_scaling_[account]_[date].md`
  - `outputs/recommendations/meta/budget_scaling_actions_[account]_[date].csv`

Confirm both files are written before proceeding.

---

### STEP 4 — Cross-KPI & Funnel Analysis (Agent 4)
Run as defined in `prompts/meta/agent_4_cross_kpi_analyst.md`.

- Map funnel structure, detect KPI conflicts, surface lead volume stagnation
- Synthesize campaign-level account health view
- Generate:
  - `outputs/reports/meta/cross_kpi_audit_[account]_[date].md`
  - `outputs/recommendations/meta/cross_kpi_actions_[account]_[date].csv`

Confirm both files are written before proceeding.

---

### STEP 5 — Cross-Platform Synthesis (Agent 5) — CONDITIONAL
Check if Google Ads outputs exist in `outputs/reports/google/`:
- If YES: Run as defined in `prompts/meta/agent_5_cross_platform_synthesizer.md`
  - Read all Meta outputs from Steps 1–4 plus Google reports
  - Generate:
    - `outputs/reports/meta/cross_platform_synthesis_[account]_[date].md`
    - `outputs/recommendations/meta/cross_platform_actions_[account]_[date].csv`
- If NO: Note that Google outputs are not present and skip this step. Flag: "Run Google Agent 1 first to enable cross-platform synthesis."

---

### FINAL SUMMARY
After all steps complete, print a summary in the conversation:

```
META ADS ANALYSIS COMPLETE
===========================
Account: [account name]
Date range analyzed: [start] – [end]
Data granularity: [DAILY / AGGREGATE]
Run date: [today]

FILES GENERATED:
Reports:
  - creative_audit_[account]_[date].md
  - audience_audit_[account]_[date].md
  - budget_scaling_[account]_[date].md
  - cross_kpi_audit_[account]_[date].md
  [- cross_platform_synthesis_[account]_[date].md  (if run)]

Recommendations:
  - creative_audit_actions_[account]_[date].csv
  - audience_audit_actions_[account]_[date].csv
  - budget_scaling_actions_[account]_[date].csv
  - cross_kpi_actions_[account]_[date].csv
  [- cross_platform_actions_[account]_[date].csv  (if run)]

TOP PRIORITY ACTIONS (High priority items across all agents):
[List all High priority recommendations from all output CSVs, deduplicated]

DATA LIMITATIONS NOTED:
[List any YELLOW flags from Agent 0 or data gaps noted during analysis]
[If AGGREGATE: "Data is lifetime-aggregated. Trend analysis sections (WoW, fatigue detection, pacing, lead stagnation) were skipped. Re-export with Time → Day breakdown for full analysis."]
```

---

## File Naming Convention
All output files use the format:
`[report_type]_[account_id]_YYYY-MM-DD.[ext]`

The account ID and date are auto-detected:
- **Account ID**: from the account name or ID column in the report data (lowercase, underscores for spaces)
- **Date**: the last date present in the report data (represents the end of the analysis period)

If multiple accounts are present in the data, generate separate output files per account.
