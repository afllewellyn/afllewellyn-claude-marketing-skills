# Learnings: cross-account lessons

Read at the start of any analysis, deck build or QA run. Add generalizable lessons here; skill-specific ones go in that skill's `memory.md`.

## Data handling
- Real Google Ads exports are UTF-16 LE, tab-separated (rows 1-2 are report name and date range, row 3 is headers). Never split CSVs on commas; impressions like "5,676" are quoted.
- Search term reports undercount clicks and spend. Use them for query coverage only; take totals from campaign, ad group or keyword reports.
- Never combine currencies in one total; label each.

## Page fetching and judgments
- WebFetch returns a model summary that can drop figures and acronyms. When a claim hinges on an exact figure or word, fetch full text with Firecrawl (`scripts/firecrawl_fetch.py`) and search it directly.
- Use word-boundary matching for literal checks (`\bAI\b`, not "ai" inside "said").
- Jev (`scripts/jev_judge.py`) answers one narrow question per call; code owns control flow and scoring. Report "contradicted" only if the page contains the conflicting figure; treat confidence under about 0.5 or a split result as PARTIAL.

## Language
- Say "more efficient" or "lower CPC", not "cheap". Do not use "waste" or "consider" in recommendations.
