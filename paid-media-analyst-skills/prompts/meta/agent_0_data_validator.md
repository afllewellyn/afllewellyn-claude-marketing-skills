# Agent 0: Data Validator (Pre-Flight Check)

## Mission
Validate Meta Ads report files before any analysis agents run. Confirm required columns are present, detect the reporting date range, surface data quality issues, and give a green/yellow/red readiness status so analysis agents don't run on incomplete data.

## When to Run
Run this agent FIRST, before any other Meta agent. If this agent returns RED status, do not proceed with analysis until the data issue is resolved.

---

## Instructions for Claude Code

When I run this agent, you will:

### 1. FILE DETECTION
- Look in `data/raw/meta/` for all CSV files (ignore `.gitkeep`)
- List each file found with its filename and approximate row count
- The expected input is a **single performance CSV** exported from Meta Ads Manager at the ad level with a daily date breakdown. See CLAUDE.md for the recommended export settings.
- If no CSV files are found, return RED status immediately:
  > "No Meta report files found in data/raw/meta/. Export from Meta Ads Manager and place the performance CSV here before running analysis."

### 2. DATE RANGE & GRANULARITY DETECTION
For each file, identify:
- The earliest and latest dates present in the data
- The total number of days covered
- **Data granularity** — detect whether the export is **daily** or **aggregate**:
  - **Daily**: Multiple rows per ad with different `Reporting starts` dates. Each row = one ad × one day. This is the recommended format for trend analysis.
  - **Aggregate (lifetime)**: One row per ad with `Reporting starts` = period start and `Reporting ends` = period end (dates differ). Totals are pre-aggregated across the full date range.
  - **Detection logic**: If `Reporting starts` != `Reporting ends` on most rows, the data is aggregate. If they match, it's daily.
- Flag if the date range is less than 7 days — this limits period-over-period analysis
- **Set the `DATA_GRANULARITY` flag** to `DAILY` or `AGGREGATE` — all downstream agents reference this to decide whether trend/WoW analysis is possible

**Granularity impact on analysis:**
- `DAILY` → Full trend analysis: WoW comparisons, fatigue detection, pacing charts, frequency trajectory
- `AGGREGATE` → Total performance analysis only: campaign ranking, CPL/CTR/CPM comparisons, budget allocation, top/bottom performers. Skip all WoW trend sections and frequency trajectory analysis. Flag this limitation clearly in each report header.

### 3. COLUMN VALIDATION

**Detect the account's reporting currency first.** The cost columns are currency-qualified — a non-USD account exports headers like `Amount spent (CAD)` or `CPC (cost per link click) (EUR)`, not the literal `(USD)` string. Scan the header row for a column matching `Amount spent (<CODE>)` and use that `<CODE>` (e.g. `USD`, `CAD`, `EUR`) as `CURRENCY` for the rest of validation and analysis — do not hard-require the `(USD)` variant specifically.

Check each file for the following columns, substituting the detected `CURRENCY` code where shown. Mark each as PRESENT or MISSING:

**Required for all analysis:**
- Campaign name
- Ad set name
- Ad name
- Reporting starts (daily date column — this is the date field for trend analysis)
- Reporting ends
- Impressions
- Reach
- Frequency
- Amount spent (CURRENCY)
- CPM (cost per 1,000 impressions) (CURRENCY)
- CPC (cost per link click) (CURRENCY)
- CTR (link click-through rate)
- Link clicks
- Results (all-objective result count)
- Cost per results
- Leads (lead-specific result count — populated for lead gen campaigns)
- Cost per lead (CURRENCY)
- Campaign ID
- Ad set ID
- Ad ID

**Useful but optional:**
- Ad delivery (active / inactive / rejected status)
- Attribution setting
- Ad set budget + Ad set budget type
- Ends (campaign end date)
- Result indicator (describes what "Results" is counting for each row)

**Note — ad copy text is not available in this export format.** Agent 1 creative analysis is limited to performance metrics and ad name conventions. Copy theme analysis requires a separate export that Meta does not reliably support at scale.

### 4. AD HIERARCHY CHECK
Confirm the data contains all three levels of the campaign hierarchy in a single file:
- Campaign level: Campaign name + Campaign ID columns populated
- Ad set level: Ad set name + Ad set ID columns populated
- Ad level: Ad name + Ad ID columns populated

Flag if any level is missing — the recommended export includes all three levels in one file.

### 5. CAMPAIGN INVENTORY
- List all unique Campaign names found in the data with their Campaign IDs
- Count unique ad sets and unique ads
- Note the advertiser/account name to use in output file naming (infer from campaign name prefix, e.g., "[Account: Dental]" from "CORE-2026-Q1-FB-DENTAL-CORE-...")
- Flag if campaigns with no name are present (ID only) — these cannot be labeled in analysis reports

### 6. DATA QUALITY FLAGS
Flag any of the following:
- Rows with zero impressions and non-zero spend (billing anomaly)
- Date gaps of more than 3 consecutive days (missing export days)
- Duplicate rows (same campaign + ad set + ad + date appearing twice)
- Columns present but entirely empty or null
- Mixed objectives in a single file (note this — Agent 4 needs to segment by objective)

### 7. OUTPUT GENERATION

Print a validation summary directly in the conversation (no file needed). Format:

---

**META ADS DATA VALIDATION REPORT**
**Run date:** [today's date]
**Files found:** [N]

---

**FILE INVENTORY**
| File | Rows | Date Range | Days Covered | Granularity |
|---|---|---|---|---|
| [filename] | [N] | [start] – [end] | [N days] | DAILY / AGGREGATE |

---

**COLUMN CHECK**
| Column | Status |
|---|---|
| Campaign name | PRESENT / MISSING |
| Ad set name | PRESENT / MISSING |
| ... | ... |

---

**AD HIERARCHY**
- Campaign level: PRESENT / MISSING
- Ad set level: PRESENT / MISSING
- Ad level: PRESENT / MISSING

---

**ACCOUNTS DETECTED**
- [Account name(s)]

---

**DATA QUALITY FLAGS**
- [List any issues found, or "None detected"]

---

**READINESS STATUS**

🟢 GREEN — All required columns present. Proceed with Meta Agent 1–4.

🟡 YELLOW — Minor issues detected (list them). Analysis can proceed but results may be partial. Recommended: re-export with missing columns before acting on recommendations.

🔴 RED — Critical columns missing or no data found. Do not proceed. (List what is missing and how to fix the export.)

---

**RECOMMENDED NEXT STEP**
- [e.g., "Run the Meta Orchestrator: prompts/meta/run_meta_analysis.md"]
- [or: "Re-export with columns X, Y, Z added before proceeding"]
