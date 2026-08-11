---
name: analyze-search-ad-copy
description: Analyze RSA ad copy across Google Search campaigns. Diagnoses headline-keyword mismatches, landing page alignment, and description redundancy. Generates updated ad copy recommendations to improve Quality Score and CTR.
argument-hint: "[product-name or data-file-path]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit, WebFetch
---

# Google Search Ad Copy Analyzer

Run the Ad Copy Analyst (Agent 3) on Google Ads CSV data exports containing RSA ad copy columns. This skill analyzes headline-to-keyword alignment, landing page messaging gaps, description redundancy, display URL paths, and conquest copy issues, then generates specific copy rewrite recommendations.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## What You Receive as Arguments

- `$ARGUMENTS` — Either a product/division name to auto-detect files in `data/raw/`, OR an explicit path to a data file.

## Step 1: Detect and Load Data Files

Scan `data/raw/` for CSV files matching the argument. For each file:

1. **Detect encoding**: Try UTF-8 first, fall back to UTF-16 LE. Real Google Ads Editor exports are typically UTF-16 LE with tab separators. Use `iconv -f UTF-16LE -t UTF-8` for conversion, then parse as TSV.
2. **Parse structure**: Row 1 = report name, Row 2 = date range (quoted), Row 3 = headers, Row 4+ = data.
3. **Classify file type** by header columns:
   - **Full Export with RSA columns**: Contains `Campaign`, `Ad group`, `Headline 1`, `Description 1`, `Final URL`, `Path 1`, `Path 2`, plus performance columns (`Clicks`, `Impr.`, `CTR`, `Avg. CPC`, `Cost`).
   - **Search Terms Report**: Contains `Search term`, `Search terms match type`, `Campaign`, `Ad group`, `Search keyword`.
4. **Report what was found**: List each detected file, its type, encoding, row count, and date range.

If no file with RSA ad copy columns (Headline 1–15, Description 1–4) is found, stop and report: "No RSA ad copy data found. This skill requires a Google Ads export containing Headline and Description columns."

## Step 2: Calculate Baselines

From the ad copy performance data, calculate:
- Total and per-campaign: spend, clicks, impressions
- Account average CTR (weighted by impressions)
- Account average CPC (weighted by clicks)
- Creative count by campaign and ad group
- Intent type distribution (Branded / Non-Branded / Conquest)

If Search Terms Report available, also calculate:
- Top search terms by clicks per ad group
- Search term coverage (% of search terms with headline alignment)

## Step 3: Fetch Landing Page Content

Extract unique Final URLs from the ad data. For each URL:
1. Fetch via WebFetch
2. Extract key messaging: taglines, differentiators, proof points, CTAs
3. Store for cross-reference in Step 4

If a landing page cannot be fetched, note the limitation and proceed with ad-copy-only analysis.

## Step 4: Run Agent 3 — Ad Copy Analysis

Reference spec: `prompts/google/agent_3_ad_copy_analyst.md`

### Ad Creative Inventory
Extract all unique creatives (Campaign + Ad group + headline/description combo). Classify as Branded, Non-Branded, or Conquest. Aggregate performance metrics.

### Headline-to-Keyword Alignment
For each ad group, compare top search terms against RSA headlines. Score alignment:
- **YES**: Primary search term language in H1 or H2
- **PARTIAL**: Search term in H3+ only
- **NO**: Not in any headline

Prioritize mismatches by click volume.

### Landing Page Alignment
Cross-reference LP content against ad copy. Flag:
- LP messaging not echoed in any headline
- Contradictory claims between ad and LP
- Missing proof points that could boost CTR
- CTA mismatches (ad CTA vs LP CTA)

### Structural Copy Issues
Flag:
- Identical descriptions across ad groups with different intent
- Empty display URL paths (Path 1 / Path 2)
- Conquest ad groups using same copy as branded
- Missing brand transition language (if a rebrand is detected in the data)
- Brand name in H1 on non-branded ad groups (category language performs better)

### Recommended Copy Rewrites
For each flagged issue, provide:
- Current copy → Recommended copy (respecting character limits: 30 chars headlines, 90 chars descriptions)
- Position (H1, H2, D1, etc.)
- Rationale tied to search term data and LP messaging
- Estimated CTR impact (HIGH / MEDIUM / LOW)

## Step 5: Generate Outputs

### Report
`outputs/reports/google/ad_copy_audit_YYYY-MM-DD.md`

Sections:
1. Header metadata (account, date range, data source, agent attribution)
2. Executive Summary (key metrics + top findings)
3. Current Ad Copy Inventory (full creative table)
4. Issue Analysis (detailed breakdown by issue type)
5. Recommended Copy by Campaign/Ad Group (current vs. recommended)
6. Search Term Alignment Matrix
7. LP Alignment Matrix
8. Priority Action Plan (HIGH → MEDIUM → LOW)

### Actions CSV
`outputs/recommendations/google/ad_copy_audit_actions_YYYY-MM-DD.csv`

Columns: `priority,action_type,campaign,ad_group,position,current_copy,recommended_copy,rationale,estimated_ctr_impact`

Action types: `REWRITE_HEADLINE`, `REWRITE_DESCRIPTION`, `ADD_DISPLAY_PATH`, `DIFFERENTIATE_CONQUEST_COPY`, `ADD_BRAND_TRANSITION`

### Excel Workbook
`outputs/recommendations/google/ad_copy_audit_YYYY-MM-DD.xlsx`

5 tabs:
1. Executive Summary
2. Ad Copy Recommendations
3. Search Term Alignment
4. Priority Actions
5. Landing Page Alignment

## Step 6: Update CLAUDE.md

After generating outputs, append key findings to the `## Session Learnings` → `### Analysis Run Log` table in `CLAUDE.md`:
- Date, account, platform (Google Agent 3), period, spend, key finding, report paths

## Important Notes

- **Encoding**: Always check for UTF-16 LE first on real Google Ads exports. Use `iconv -f UTF-16LE -t UTF-8` for conversion.
- **CSV parsing**: Never use naive `split(',')` — impression values like `"5,676"` contain commas. Use `csv.DictReader` or pandas.
- **Character limits**: Headlines max 30 characters, descriptions max 90 characters. Always verify recommended copy fits.
- **B2B context**: Accounts are typically B2B (healthcare, industrial, etc.). Infer the division, product category, and professional audience from campaign names and keywords in the data. Ad copy recommendations should target the relevant professional audience, not consumers.
- **Be specific in recommendations**: Include current copy, recommended copy, position, rationale, and estimated impact.
- **Commit outputs**: After generating reports, commit the output files to the repository.
