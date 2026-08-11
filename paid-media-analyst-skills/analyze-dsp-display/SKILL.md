---
name: analyze-dsp-display
description: Run the [DSP Platform] Intelligence DSP display campaign analysis pipeline on [DSP Platform] CSV exports. Generates an audit report and an actionable recommendation CSV covering line-item performance, creative rotation, exchange / inventory mix, domain blocklists, audience segments, frequency diagnostics, and creative fatigue. Use this skill whenever the user drops a [DSP Platform] export into data/raw/dsp/, asks to analyze a [DSP Platform] campaign, or types /analyze-dsp-display.
argument-hint: "[account stem or path to CSV file in data/raw/dsp/]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# [DSP Platform] Display Analyzer

Run the [DSP Platform] analysis pipeline on [DSP Platform] Intelligence campaign exports. This skill executes Agent 1 (Display Performance Analyst) and produces a markdown audit report + a recommendation CSV.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## What You Receive as Arguments

- `$ARGUMENTS` — Optional. An account stem (to match against filenames) or an explicit path to a CSV in `data/raw/dsp/`. If empty, auto-detect the most recently modified CSV in `data/raw/dsp/`.

## Step 1: Detect Data Files

```python
import glob, os

dsp_files = glob.glob("data/raw/dsp/*.csv")

if not dsp_files:
    print("ERROR: No CSV files found in data/raw/dsp/. Please export your [DSP Platform] campaign report and place it in data/raw/dsp/.")
    exit()

if "$ARGUMENTS":
    arg = "$ARGUMENTS".strip()
    if os.path.exists(arg):
        target_files = [arg]
    else:
        target_files = [f for f in dsp_files if arg.lower() in f.lower()]
        if not target_files:
            target_files = dsp_files
else:
    target_files = sorted(dsp_files, key=os.path.getmtime, reverse=True)[:1]
```

[DSP Platform] exports are **UTF-8 CSV** (sniff for BOM and use `encoding='utf-8-sig'` if present). Header row is row 1, data starts row 2. Use `csv.DictReader` or pandas — never `split(',')`.

## Step 2: Classify the File

Read headers and identify the column schema. The [DSP Platform] display agent supports a flexible schema — populate the "Detected columns" table in `prompts/dsp/agent_1_display_analyst.md` with the actual column names on first run for a new account.

Key columns to look for (canonical → typical [DSP Platform] field):
- Date → `Date` / `Day`
- Line item → `Line Item` / `Insertion Order` / `Campaign`
- Creative → `Creative Name` / `Ad Name`
- Format → `Creative Type` / `Format`
- Audience → `Audience` / `Segment`
- Exchange → `Exchange` / `Inventory Source`
- Domain → `Domain` / `App Bundle` / `Site`
- Impressions, Clicks, CTR, Spend, CPM, CPC
- Reach, Frequency
- Viewable Impressions, Viewability Rate, Measurable Impressions
- Video Starts, Video Completes, VTR
- Conversions, CPA (may be absent — that's OK)

Report what columns were found, group them under canonical KPIs, and note which canonical KPIs have no matching column.

## Step 3: Determine Account Stem

If the user passed an account stem in `$ARGUMENTS`, use it. Otherwise infer from the filename (e.g., `account_iwfb_dsp_may_2026.csv` → `account_iwfb`). Confirm with the user if ambiguous.

## Step 4: Run Agent 1 — [DSP Platform] Display Performance Analyst

Read the full agent spec: `prompts/dsp/agent_1_display_analyst.md`

Execute Agent 1 with the detected file. This produces:
- `outputs/reports/dsp/display_audit_<account>_YYYY-MM-DD.md`
- `outputs/recommendations/dsp/display_audit_actions_<account>_YYYY-MM-DD.csv`

If this is the first run for a new account, update the spec's "Detected columns" block in-place so the schema becomes durable.

## Step 5: Print Summary

```
## [DSP Platform] Analysis Complete

### Files Generated
| File | Status |
|---|---|
| display_audit_<account>_YYYY-MM-DD.md | ✅ |
| display_audit_actions_<account>_YYYY-MM-DD.csv | ✅ |

### Data Availability
[Bulleted list of canonical KPIs present vs. absent. Explicit callout when no conversion tracking — all rollups are click-volume weighted.]

### Top 3 Priority Actions
[List the 3 highest-priority actions from the action CSV]
```

## Important Notes

- **Encoding**: [DSP Platform] exports are UTF-8 CSV. Sniff for BOM and use `encoding='utf-8-sig'` if present.
- **Schema is account-specific**: The spec's "Detected columns" block is intentionally blank until first run. Once populated for an account, it serves as durable schema knowledge for follow-on sessions.
- **Conversion tracking is often absent on DSP** — fall back to click-volume weighting and label every rollup accordingly.
- **Never use "waste" or "wasted spend"** — reframe as efficiency, learning, or optimization.
- **Implementation references**: Recommendations should reference "[DSP Platform] Intelligence" specifically (the DSP), not generic "DSP" language.
