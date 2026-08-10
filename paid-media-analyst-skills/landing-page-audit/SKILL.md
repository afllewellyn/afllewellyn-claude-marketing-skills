---
name: landing-page-audit
description: Batch-audit landing pages for ad-to-page messaging alignment. Extracts Final URLs from Google Ads RSA exports, fetches each page, and runs a 3-type gap analysis (ad claims not on page, page messaging not in ads, keywords absent from LP). Generates prioritized actions with recommended copy rewrites.
argument-hint: "[product-name or data-file-path]"
allowed-tools: Read, Bash, Grep, Glob, Write, Edit, WebFetch
---

# Landing Page Audit

Systematically audit all landing pages referenced in Google Ads RSA exports for ad-to-page messaging alignment. Extracts unique Final URLs, fetches each page, and runs a structured gap analysis to identify mismatches between ad copy and landing page content.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## What You Receive as Arguments

- `$ARGUMENTS` — Either a product/division name to auto-detect files in `data/raw/google/`, OR an explicit path to a data file.

## Step 1: Detect and Load Data Files

Scan `data/raw/google/` for CSV files matching the argument. For each file:

1. **Detect encoding**: Try UTF-8 first, fall back to UTF-16 LE. Real Google Ads Editor exports are typically UTF-16 LE with tab separators. Use `iconv -f UTF-16LE -t UTF-8` for conversion, then parse as TSV.
2. **Parse structure**: Row 1 = report name, Row 2 = date range (quoted), Row 3 = headers, Row 4+ = data.
3. **Require RSA columns**: The file must contain `Campaign`, `Ad group`, `Headline 1` through `Headline 15`, `Description 1` through `Description 4`, `Final URL`, plus performance columns (`Clicks`, `Impr.`, `CTR`, `Avg. CPC`, `Cost`).
4. **Report what was found**: List each detected file, its encoding, row count, date range, and unique Final URL count.

If no file with RSA ad copy columns is found, stop and report: "No RSA ad copy data found. This skill requires a Google Ads export containing Headline, Description, and Final URL columns."

## Step 2: Extract and De-duplicate URLs

1. Read the `Final URL` column (clean base URL — do NOT use `Ad final URL` which contains tracking suffixes).
2. Strip tracking parameters: remove `?cid=...`, `?utm_...`, and any query string appended for tracking. Keep the base URL path.
3. De-duplicate to unique base URLs.
4. If more than 15 unique URLs exist, rank by total clicks and cap at the top 15 by click volume.
5. Report the final URL list with click volume per URL.

## Step 3: Build URL-to-Ad-Copy Mapping

For each unique base URL, collect all ad creatives (rows) pointing to it:

- All populated headlines (H1–H15) across those rows
- All populated descriptions (D1–D4) across those rows
- Campaign and ad group names
- Aggregate performance: total clicks, impressions, cost, weighted CTR

This mapping is used in Step 5 to cross-reference ad claims against page content.

## Step 4: Fetch Landing Pages

For each unique URL (up to 15) — **WebFetch first, Firecrawl fallback**:

1. Fetch via WebFetch with the prompt: "Extract the following from this page: 1) Hero headline and subheadlines, 2) All CTAs (button text, form labels), 3) Key value propositions and benefits listed, 4) Proof points (clinical data, certifications, awards, statistics, testimonials), 5) Product names and brand mentions, 6) Any offers or promotions, 7) Primary keywords and terminology used throughout the page."
2. **If WebFetch is blocked or empty** (HTTP 403 from a bot-management WAF, timeout, or JS-only rendering), fall back to Firecrawl's hosted scraper: run `python scripts/firecrawl_fetch.py "<url>"`, then run the same 7-point extraction prompt against the returned markdown. Known-WAF domains (e.g. `[client-domain].com`) may skip WebFetch and go straight to Firecrawl. This requires `FIRECRAWL_API_KEY` in the environment and sandbox egress to `api.firecrawl.dev` — see the `firecrawl-scrape` skill.
3. Store the extracted content for gap analysis.
4. If **both** WebFetch and Firecrawl fail (or `FIRECRAWL_API_KEY` is unset), note the limitation and skip that URL in the gap analysis. Do not retry — move to the next URL.

## Step 5: Run 3-Type Gap Analysis

For each successfully fetched URL, compare the extracted page content against the ad copy mapping from Step 3.

### Gap A — Ad Claims Not on Page

Identify ad copy elements that the landing page does not substantiate:

- **CTA mismatches**: Ad says "Buy Now" but LP says "Schedule a Demo" — the user expectation set by the ad doesn't match the page action
- **Unsubstantiated claims**: Ad headline promises a benefit or feature not mentioned anywhere on the LP
- **Offer mismatches**: Ad references a promotion, discount, or trial not present on the LP
- **Product mismatches**: Ad names a product or service the LP doesn't cover

Severity scoring:
- **HIGH**: CTA mismatch or primary value prop in H1/H2 not on page (directly harms conversion)
- **MEDIUM**: Secondary headline claim (H3+) not on page
- **LOW**: Description-only claim not on page

### Gap B — Page Messaging Not in Ads

Identify strong LP content elements that no ad headline or description uses:

- **Proof points unused**: LP mentions clinical data, certifications, awards, or statistics that could strengthen ad credibility — but no headline references them
- **Differentiators unused**: LP highlights competitive advantages (e.g., "only FDA-cleared", "rosin-free") not reflected in any ad copy
- **Product features unused**: Specific features or capabilities on the LP that would make strong headlines but aren't used
- **Social proof unused**: Testimonials, case studies, or customer logos on the LP not leveraged in ad copy

Severity scoring:
- **HIGH**: Unique differentiator or strong proof point on LP not in any headline (missed CTR opportunity)
- **MEDIUM**: Product feature or benefit on LP not in any headline
- **LOW**: Secondary content element (e.g., blog links, resource mentions) not in ads

### Gap C — Keyword Absent from Landing Page

Check whether the primary keywords driving clicks to this URL actually appear on the landing page:

1. From the ad data, identify the top keywords (by clicks) mapped to each URL via campaign/ad group
2. Check whether each keyword's core language appears on the landing page (in headings, body copy, meta content)
3. Flag keywords with significant click volume that are absent from the LP — this is a Quality Score risk (landing page relevance is a QS factor)

Severity scoring:
- **HIGH**: Primary keyword (top by clicks) absent from LP — direct Quality Score impact
- **MEDIUM**: Secondary keyword absent from LP
- **LOW**: Long-tail variant absent (but root term is present)

## Step 6: Generate Recommended Copy

For each gap flagged in Step 5, generate specific copy recommendations:

- **Gap A fixes**: Recommend LP content updates (flag for web team) OR ad copy adjustments to match what the LP actually says
- **Gap B fixes**: Recommend new headlines or descriptions incorporating the unused LP messaging. Respect character limits: 30 chars for headlines, 90 chars for descriptions.
- **Gap C fixes**: Recommend LP content additions (flag for web team) to include missing keyword language

For each recommendation, include:
- Gap type (A, B, or C)
- Severity (HIGH / MEDIUM / LOW)
- Current state (what the ad says vs. what the page says, or what's missing)
- Recommended action with specific copy
- Rationale tied to conversion or Quality Score impact

## Step 7: Cross-Reference Existing Ad Copy Audit (Optional)

If an existing `ad_copy_audit_*.md` report exists in `outputs/reports/google/`, scan it for related findings:
- Note any LP alignment issues already flagged by Agent 3
- Highlight new gaps this audit found that Agent 3 did not cover
- Reference the existing report for context

If no prior audit exists, skip this step and note it in the report.

## Step 8: Generate Outputs

### Report
`outputs/reports/google/landing_page_audit_YYYY-MM-DD.md`

Sections:
1. **Header metadata**: account (inferred from campaign names), date range, data source file(s), skill attribution
2. **Executive Summary**: URL count, pages fetched, total gaps found by type and severity, top 3 findings
3. **URL Inventory**: Table of all unique URLs with click volume, fetch status, and gap count
4. **Per-URL Analysis**: For each URL:
   - Page content summary (hero headline, CTAs, key messaging)
   - Ad copy pointing to this URL (campaigns, ad groups, headline/description inventory)
   - Gap A findings with severity
   - Gap B findings with severity
   - Gap C findings with severity
   - Recommended actions
5. **Cross-Reference with Ad Copy Audit** (if applicable)
6. **Priority Action Plan**: All actions ranked HIGH → MEDIUM → LOW, grouped by gap type

### Actions CSV
`outputs/recommendations/google/landing_page_audit_actions_YYYY-MM-DD.csv`

Columns: `priority,gap_type,severity,url,campaign,ad_group,current_state,recommended_action,recommended_copy,rationale,impact_area`

- `gap_type`: GAP_A_AD_NOT_ON_PAGE, GAP_B_PAGE_NOT_IN_AD, GAP_C_KEYWORD_ABSENT
- `impact_area`: CONVERSION (Gap A), CTR (Gap B), QUALITY_SCORE (Gap C)

Sort by severity (HIGH → MEDIUM → LOW), then by gap type (A → C → B).

## Step 9: Update CLAUDE.md

After generating outputs, append the run to the `## Session Learnings` → `### Analysis Run Log` table in `CLAUDE.md`:
- Date, account, platform (Google LP Audit), period, spend (from ad data), key finding, report paths

## Important Notes

- **Encoding**: Always check for UTF-16 LE first on real Google Ads exports. Use `iconv -f UTF-16LE -t UTF-8` for conversion.
- **CSV parsing**: Never use naive `split(',')` — impression values like `"5,676"` contain commas. Use `csv.DictReader` or pandas.
- **Use `Final URL` column**: Not `Ad final URL` — the latter contains tracking parameters that break de-duplication.
- **URL cap**: Maximum 15 URLs per run to stay within reasonable WebFetch usage. If more exist, prioritize by click volume.
- **Tracking param stripping**: Remove `?cid=`, `?utm_*`, and other query strings before de-duplicating.
- **Fetch failures**: If WebFetch fails for a URL (403 WAF, timeout, 404, JS-rendered), fall back to `python scripts/firecrawl_fetch.py "<url>"` (see the `firecrawl-scrape` skill; needs `FIRECRAWL_API_KEY`). Only if Firecrawl also returns nothing, skip the URL and note the limitation. Do not retry the same path in a loop.
- **Character limits**: Headlines max 30 characters, descriptions max 90 characters. Always verify recommended copy fits.
- **B2B context**: Accounts are typically B2B (healthcare, dental, industrial). Infer the division and professional audience from campaign names and keywords. Recommendations should target the relevant professional audience, not consumers.
- **No "waste" language**: Never use "waste," "wasted," or "wasted spend." Use learning, efficiency, or optimization framing per project conventions.
