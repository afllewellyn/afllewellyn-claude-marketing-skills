---
name: analyze-linkedin-campaigns
description: Run the LinkedIn Campaign Manager analysis pipeline (Agent 1, LinkedIn Campaign Analyst) on a LinkedIn export. Generates an audit report and an actionable recommendation CSV covering delivery vs plan, ad-set (audience/market) and ad (creative) performance, lead gen, video, and budget reallocation. Use this skill whenever the user drops a LinkedIn export into data/raw/linkedin/ or a project's linkedin/ folder, asks to analyze LinkedIn campaigns, or types /analyze-linkedin-campaigns.
argument-hint: "[account stem or path to a LinkedIn export] [--outdir <dir>]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# LinkedIn Campaign Analyzer

Run Agent 1 (LinkedIn Campaign Analyst) on a LinkedIn Campaign Manager export and produce a
markdown audit report and a recommendation CSV. This skill is the LinkedIn-only analysis.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

If you keep per-account notes or prior-run summaries (for example `data/accounts/<slug>/`),
read them for prior flights, standing issues and findings, and pass their paths to the agent.
Account-specific lessons go there, not in this skill's `memory.md`.

## What You Receive as Arguments

- `$ARGUMENTS`: optional. An account stem to match against filenames, or an explicit path.
  Empty means the newest LinkedIn export.
- `--outdir <dir>`: optional dry run. See "Dry runs" below.

## Dry runs (`--outdir`)

Use this to test the skill or a spec change without touching the record. With `--outdir`:
- The compute JSON, report and actions CSV go to `<dir>/` under their normal filenames,
  not `data/processed/` or `outputs/`.
- Step 5 runs `python scripts/qa_lint.py` on both files but skips the `qa-review` skill, so no
  run-log or memory write happens.
- Do not edit account notes or this skill's `memory.md`. Say in the
  summary that it was a dry run.

## Step 1: Find the export

LinkedIn exports land in `data/raw/linkedin/` or in a project folder's `linkedin/`
subfolder (for example `data/raw/<project>/linkedin/`).

```bash
ls -t data/raw/linkedin/*.csv data/raw/*/linkedin/*.csv 2>/dev/null
```

With an argument, use the path if it exists, else the newest file whose path contains the
stem. A folder can hold exports from different programs and quarters: pick the one whose
campaign name and dates match the request, and among pulls of that same program and period
prefer the one marked final. Say which file you used and why. A demographics `.xlsx`, or an Audience Insights screenshot, in the same folder is an
optional input for the audience section, but only once its period is established (spec §1).

## Step 2: Compute

One run computes and writes the JSON. `{end}` in the path becomes the export's last data
day (`YYYY-MM-DD`), which is also the date in every report and CSV filename:

```bash
python scripts/linkedin_compute.py "<export>" -o data/processed/linkedin_<account>_{end}.json
```

(With `--outdir`, pass `-o <dir>/linkedin_<account>_{end}.json` instead.) The printed
`wrote` line shows the resolved filename.

Read the printed summary: date range, spend, clicks, ad count and whether any ad names are
shared by several Ad IDs. If the script exits on a missing column, stop and show the user
the export's header.

## Step 3: Determine the account

Use the argument. Otherwise compare the campaign names in the JSON with each
your account notes when you keep them; ask the user when no single account clearly fits. `<account>` in
filenames is a short account slug.

## Step 4: Run Agent 1

Read the full spec, `prompts/linkedin/agent_1_campaign_analyst.md` (sibling to this skill folder), and execute it with the
compute JSON, the account notes (if any) and any plan or demographics file,
plus the output folder when this is a dry run. It writes:
- `outputs/reports/linkedin/linkedin_audit_<account>_YYYY-MM-DD.md`
- `outputs/recommendations/linkedin/linkedin_audit_actions_<account>_YYYY-MM-DD.csv`

The date is the analysis date (the export's end date), not today's date.

## Step 5: QA and summary

Run the `qa-review` skill on the two files (on a dry run, only `qa_lint.py`). Then print:

```
## LinkedIn Analysis Complete

| File | Status |
|---|---|
| linkedin_audit_<account>_YYYY-MM-DD.md | ✅ |
| linkedin_audit_actions_<account>_YYYY-MM-DD.csv | ✅ |

Data available: [leads / video / conversions present or absent; click-weighted if none]

Top 3 actions: [from the CSV]
```

## Important Notes

- Never parse the export by hand: the compute script owns encoding, preamble, Ad ID keying
  and the `Impressions` vs `Card Impressions` trap.
- Flight dates and pause state come from the export, not the IO.
- No Insight Tag and no lead form means no conversions: report clicks to LP, labelled as such.
