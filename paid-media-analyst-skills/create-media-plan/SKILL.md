---
name: create-media-plan
description: Generate a formula-driven Excel media plan and markdown strategic plan for an upcoming paid media campaign. Grounds projections in historical account data when available, or B2B industry benchmarks for net-new proposals. Use when the user wants to create a media plan, campaign proposal, budget recommendation, or Q2/Q3/Q4 planning document — even if they don't use those exact words.
argument-hint: "[platform] [account name]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit
---

# Media Plan Generator

Create a comprehensive, formula-driven media plan proposal. Works in two modes:
- **Historical**: grounded in account performance data from existing reports or raw CSVs
- **Net-New**: grounded in B2B industry benchmarks when no historical data is available

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## What You Receive as Arguments

- `$ARGUMENTS` — Optional. Platform and account name (e.g., `meta account_dental`). If empty, ask the user.

## Step 1: Read the Agent Spec

Read the full agent specification:
```
prompts/planning/agent_1_media_plan_generator.md
```

This contains the complete instructions for:
- Gathering the campaign brief (budget, offers, timing, audience, market, objective)
- Extracting historical benchmarks from existing reports or raw CSVs
- Designing campaign structure
- Building performance projections
- Generating Excel and markdown outputs

## Step 2: Gather Campaign Brief

Ask the user conversationally for the required inputs. Don't require a structured template — gather information naturally. At minimum you need:

1. **Platform** (Meta, Google, Bing, multi-platform)
2. **Account** (brand/account name)
3. **Market** (US, CA, etc.)
4. **Budget** (total campaign budget)
5. **Objective** (awareness, traffic, lead gen, conversions)
6. **Offers/Products** (what's being promoted)
7. **Success Metrics** (how success is measured)
8. **Timing** (campaign dates)
9. **Audience** (target audience — existing saved audiences or new)

If the user has already provided some of this context in the conversation, don't re-ask for it.

## Step 3: Determine Planning Mode & Locate Benchmark Data

Check for existing data that can provide benchmarks **for the specific account the user named** — not the platform as a whole. Multiple accounts share each platform folder, so a platform-wide glob can wrongly pull another account's data.

```python
import glob, os, re

platform = "meta"  # or "google" / "bing"
account = "account_dental"  # from $ARGUMENTS — normalize to lowercase, underscores

# Build case-insensitive account tokens (e.g. "account_dental" → ["account_dental", "dental-core", "dental core", "dentalcore"])
tokens = {account, account.replace("_", "-"), account.replace("_", " "), account.replace("_", "")}

def account_match(path):
    name = os.path.basename(path).lower()
    return any(t in name for t in tokens)

# Account-scoped lookups
reports = [p for p in glob.glob(f"outputs/reports/{platform}/*audit*.md") if account_match(p)]
csvs    = [p for p in glob.glob(f"data/raw/{platform}/*.csv") if account_match(p)]
```

**Decision logic:**
- If **account-scoped** reports or raw CSVs are found for the target platform → **Historical mode**: extract benchmarks from the most recent matching reports, or parse the matching raw CSVs per the agent spec.
- If platform files exist but **none match the named account** → treat as net-new. Show the user the non-matching files found and ask: *"I found Meta files for [account X, account Y] but nothing tagged to [account Z] — proceed with industry benchmarks for [Z], or did you want to use one of the existing files?"*
- If no data exists OR the user explicitly says "no historical data" / "new account" / "use industry benchmarks" → **Net-New mode**: use B2B industry benchmarks from §2B in the agent spec. Inform the user which mode you're using and proceed — do not block or require a file upload.

The user can also provide partial benchmarks (e.g., "our CPL is usually around $100") — override the corresponding industry default with their input.

## Step 4: Check for Excel Template

Check if the user provided a template:
```python
templates = glob.glob("data/raw/*Proposal*.xlsx") + glob.glob("data/raw/*media*plan*.xlsx")
```

If a template exists, use it as the base and edit in place. If not, create from scratch per the agent spec.

## Step 5: Execute the Agent

Follow the full instructions in `prompts/planning/agent_1_media_plan_generator.md`:

1. Extract/compute benchmarks (historical if available, industry if not)
2. Design campaign structure based on brief + benchmarks
3. Build performance projections (all formula-based)
4. Generate Excel workbook (6 tabs: Media Plan Summary, Weekly Pacing, Gantt Chart, Benchmarks [named "Q1 Benchmarks" in Historical mode or "Industry Benchmarks" in Net-New mode], Audience Details, IO if template provided)
5. Generate markdown strategic plan
6. Verify outputs (no #REF! errors, benchmarks match source data)

## Step 6: Save Outputs

Save to the appropriate platform folder:
- `outputs/reports/[platform]/[plan_name]_[account]_YYYY-MM-DD.xlsx`
- `outputs/reports/[platform]/[plan_name]_[account]_YYYY-MM-DD.md`

Print a summary of what was generated and the key projections (budget, estimated impressions, clicks, conversions, CPL range).

## Important Notes

- **All projection cells in Excel must be formulas** — if an assumption changes, all downstream numbers should recalculate automatically.
- **Use the Benchmarks tab as the single source of truth** — Weekly Pacing and Media Plan Summary should reference it. The tab is named "Q1 Benchmarks" in Historical mode and "Industry Benchmarks" in Net-New mode; pick one name and use it consistently throughout the workbook.
- **Present projections as ranges** (conservative / optimistic) — never false precision.
- **Flag assumptions explicitly** — distinguish data-driven estimates from judgment calls.
- **Never combine USD and CAD** in a single total without labeling.
