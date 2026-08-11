---
name: analyze-bing-campaigns
description: Run the full Bing/Microsoft Ads search campaign analysis pipeline (Agent 1 + Agent 2, plus Agent 3 if RSA ad copy columns are detected) on Bing Ads CSV exports. Generates audit reports and actionable recommendation CSVs for keyword management, negative keywords, bid adjustments, structural improvements, and ad copy optimization. Use this skill whenever the user drops a Bing Ads export into data/raw/bing/, asks to analyze Bing or Microsoft Ads campaigns, or types /analyze-bing-campaigns.
argument-hint: "[product name or path to CSV file in data/raw/bing/]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit, WebFetch
---

# Bing/Microsoft Ads Campaign Analyzer

Run the full Bing Ads search analysis pipeline on Microsoft Ads CSV exports. This skill orchestrates Agent 1 (Search Analyst) + Agent 2 (Keyword & Negative Manager), and conditionally Agent 3 (Ad Copy Analyst) if RSA columns are detected.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## Cross-Reference Reconciliation (mandatory on every pass)

Running a search account is fundamentally a reconciliation job: never read any one file
in isolation. On every pass, each agent cross-checks the uploaded files against each other
— the **Search Query Report against the active keyword set**, and both against the
campaign-performance / Impression-Share data and the network split (MS sites vs Syndicated
Search Partners) — to surface, every time:
- **Gaps to fill** — search queries or themes that have demand or are performing but are
  **not yet targeted as keywords** (→ `ADD_KEYWORD_EXACT` / `CREATE_AD_GROUP`).
- **Terms to pause / narrow** — keywords or ad groups capturing irrelevant, low-quality,
  or off-intent queries (→ `PAUSE_KEYWORD` / `NARROW_MATCH_TYPE` / negatives), including
  Syndicated-only query clusters worth excluding.

Before you characterize, pause, narrow, or consolidate any keyword or ad group, look at
**what it actually captures** in the Search Query Report — never judge it from the keyword
list or aggregate metrics alone. (Common example: a low-performing Broad keyword / ad group
is often a brand-query catch-all — quantify the brand share and stand up a [Client] branded
ad group to capture it before pausing.) Bing conversion tracking is frequently absent — when
it is, reconcile on click volume + query relevance, not conversions. This is the core analyst
loop — run it on every pass, for every subagent, not only when something looks wrong.

## What You Receive as Arguments

- `$ARGUMENTS` — Optional. A product name (to match against filenames) or an explicit path to a CSV in `data/raw/bing/`. If empty, auto-detect the most recently modified CSV in `data/raw/bing/`.

## Step 1: Detect Data Files

```python
import glob, os

# Find all CSV files in the Bing data directory
bing_files = glob.glob("data/raw/bing/*.csv")

if not bing_files:
    print("ERROR: No CSV files found in data/raw/bing/. Please export your Bing Ads reports and place them in data/raw/bing/.")
    exit()

# If argument provided, try to match by product name or use as path
if "$ARGUMENTS":
    arg = "$ARGUMENTS".strip()
    if os.path.exists(arg):
        target_files = [arg]
    else:
        # Match by product name in filename (case-insensitive)
        target_files = [f for f in bing_files if arg.lower() in f.lower()]
        if not target_files:
            target_files = bing_files  # Fall back to all files
else:
    target_files = bing_files
```

Bing exports are **UTF-8 CSV** with standard headers in row 1, data from row 2. No encoding conversion needed.

## Step 2: Classify Files

For each CSV file found, read the headers and classify:

- **Keyword Performance Report**: Contains `Campaign name`, `Ad group`, `Keyword`, `Clicks`, `Impressions`, `CTR`, `Avg. CPC`, `Spend`
- **Search Query Report**: Contains `Search query`, `Campaign name`, `Ad group`, `Keyword`, `Clicks`, `Impressions`
- **Full Export with RSA columns**: Contains `Headlines` or `Headline 1` through `Headline 15`, `Descriptions` or `Description 1` through `Description 4`, `Final URL`
- **Dedicated Search Impression Share Report**: Contains `Impr. share %` and lacks search-query / keyword identifiers. Expected columns: `Campaign name`, `Ad group`, `Impressions`, `Clicks`, `Spend`, `Impr. share %`, `Lost IS (budget) %`, `Lost IS (rank) %`, `Top IS %`, `Abs. top impression rate %`. Pass to Agent 1 as the IS source of truth.
- **Conversion Report**: Contains `Conversions` AND (`Cost per conv.` OR `Conv. rate`). Expected columns: `Campaign name`, `Ad group`, `Conversions`, `Cost per conv.`, `Conv. rate`. Many Bing accounts do not have conversion tracking — when absent, Agent 1 falls back to click-volume-weighted prioritization and the downstream PPT labels conversions as "not tracked on this account".

Report what files were found and their classifications.

## Step 3: Run Agent 1 — Search Performance Analyst

Read the full agent spec: `prompts/bing/agent_1_search_analyst.md`

Execute Agent 1 with the keyword performance data. This produces:
- `outputs/reports/bing/search_audit_YYYY-MM-DD.md`
- `outputs/recommendations/bing/search_audit_actions_YYYY-MM-DD.csv`

## Step 4: Run Agent 2 — Keyword & Negative Manager

Read the full agent spec: `prompts/bing/agent_2_keyword_negative_manager.md`

> Run the **Cross-Reference Reconciliation** above before emitting any promote / add / pause / narrow actions — every pass yields both gaps to fill and terms to pause.

Execute Agent 2 with the keyword performance data + search query report (if available). This produces:
- `outputs/reports/bing/keyword_management_YYYY-MM-DD.md`
- `outputs/recommendations/bing/keyword_management_actions_YYYY-MM-DD.csv`

**Optional search-volume enrichment (DataForSEO MCP).** If the `dataforseo` MCP
server is connected, Agent 2 enriches the promotion shortlist + net-new keyword
candidates with market search volume / competition / top-of-page CPC via
`mcp__dataforseo__keywords_data_google_ads_search_volume` (see Agent 2 spec
Section 3b; Google-sourced volume used as a directional proxy for Microsoft Ads).
**Respect the API rate limits — do not blast the endpoint:** batch the
de-duplicated keyword list into ONE call (hard cap 1,000 keywords/request and
12 req/min; stay conservatively at ≤500 keywords/request and ≤6 req/min, spacing
any extra calls ~10s apart). If the server is not connected, skip silently and note
it in Data Limitations — never block the pipeline on it.

## Step 5: Conditionally Run Agent 3 — Ad Copy Analyst

Check if RSA ad copy columns are present in any of the detected files.

If RSA columns found:
- Read the full agent spec: `prompts/bing/agent_3_ad_copy_analyst.md`
- Execute Agent 3
- Produces:
  - `outputs/reports/bing/ad_copy_audit_YYYY-MM-DD.md`
  - `outputs/recommendations/bing/ad_copy_audit_actions_YYYY-MM-DD.csv`

If no RSA columns:
- Print: "No RSA ad copy columns detected — skipping Agent 3 (Ad Copy Analyst). To run ad copy analysis, export a report with Headline and Description columns from Microsoft Ads."

## Step 6: Optional — Generate Executive PPT (Agent 6)

If the user passes `--ppt` in `$ARGUMENTS` or asks for a deck, invoke Agent 6 (`prompts/meta/agent_6_executive_ppt.md`) after Agents 1 + 2 (+ 3) finish. Agent 6 is the canonical multi-platform PPT generator and supports Bing-only as well as blended Google + Bing decks.

When Bing has no conversion tracking on the account (the common case), Agent 6 will:
- Skip conversion lines on the MoM Performance trend slide (Module 6) for Bing.
- Use Google conversion data only on the Top Ad Groups & Keywords laddered slides (Module 11) when Google is also present, with a footer label "Google: tracked. Bing: no conversion tracking on this account."
- Drop the conversion column from Bing-only blended tables and label the omission.

For any blended Google + Bing engagement: run `/analyze-bing-campaigns <account>` and `/analyze-search-campaigns <account>` first, then invoke Agent 6 once across the combined outputs to produce a single blended deck.

## Step 7: Print Summary

```
## Bing Ads Analysis Complete

### Files Generated
| File | Status |
|---|---|
| search_audit_YYYY-MM-DD.md | ✅ |
| search_audit_actions_YYYY-MM-DD.csv | ✅ |
| keyword_management_YYYY-MM-DD.md | ✅ |
| keyword_management_actions_YYYY-MM-DD.csv | ✅ |
| ad_copy_audit_YYYY-MM-DD.md | ✅ / ⚠️ skipped (no RSA data) |
| ad_copy_audit_actions_YYYY-MM-DD.csv | ✅ / ⚠️ skipped |

### Top 3 Priority Actions
[List the 3 highest-priority actions from all generated action CSVs]
```

## Important Notes

- **Encoding**: Bing exports are UTF-8 CSV. No UTF-16 LE conversion needed.
- **Column names**: Bing uses `Impressions` (not `Impr.`), `Spend` (not `Cost`), `Campaign name` (not `Campaign`).
- **Search queries**: Bing calls them "Search queries" (not "Search terms"). The report is called "Search query report."
- **Implementation references**: Use "Microsoft Ads Editor" (not "Google Ads Editor") in all action recommendations.
- **Never use "waste" or "wasted spend"** — reframe as efficiency, learning, or optimization opportunities.
