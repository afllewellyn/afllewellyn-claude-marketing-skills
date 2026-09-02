---
name: aeo-geo-audit
description: "Run a full SEO + AEO + GEO audit of a website — AI crawler access, citation/off-site signal, structured data hygiene, and traditional on-page/technical SEO — and produce a prioritized, executive-ready action plan. Use when auditing a site's search or AI-search visibility, prepping a CEO/leadership readout, or checking whether a B2B site is citable by ChatGPT, Perplexity, Google AI Mode, and Gemini, not just rankable on Google."
---

# AEO/GEO Audit

This skill runs a website audit built for how buyers actually find B2B products in 2026: partly through Google rankings, increasingly through what ChatGPT, Perplexity, Google AI Mode, Gemini, and Claude choose to cite. A standard SEO audit (title tags, meta descriptions, backlinks, Core Web Vitals) is necessary but no longer sufficient — it's silent on whether AI crawlers can even reach the site, whether the site's off-domain footprint (G2, Reddit, comparison content) is doing any work, and whether content is structured to be *extracted*, not just *read*.

Go further than a keyword-and-meta-tags checklist. The differentiator of this skill is covering what generic SEO audits miss: machine crawlability, log-verified AI bot access, off-site citation surface, and a real cross-engine visibility baseline.

## Inputs

Gather before starting (ask if not given):

1. **Domain or URL** to audit.
2. **Audience** for the output — a CEO/leadership readout (concise, 5-item priority list, business framing) vs. a working team doc (full checklist detail). Default to leadership readout unless told otherwise.
3. **Competitors** (optional) — 2-4 named competitors for comparison pages and Share-of-Voice framing. If not given, identify 2-3 via web search based on the domain's category.
4. **Known internal context** (optional) — existing G2/Capterra profiles, any AI-search monitoring tool already in place, sales-call transcripts or buyer-language sources available for mining.

## Check for a DataForSEO connection first

Before running passes 4 and 5, check whether a DataForSEO API credential or MCP connector is available in this environment (an MCP tool name containing "dataforseo", or an API key the user has provided/mentioned). DataForSEO's AI Optimization API and its core Keywords Data / SERP API share one account and one credential — it's a single integration, not two.

- **If connected**, use it live in two places (details in passes 4 and 5 below) and label every number in the report with its source ("DataForSEO LLM Mentions API" / "DataForSEO Keywords Data").
- **If not connected**, do not block the audit on it. Fall back to the manual/estimated methods described in each pass, and say plainly in the output which numbers are estimates. Note once, near the top of the report, that connecting a DataForSEO account would upgrade the visibility-baseline and keyword sections from estimates to verified data — do not repeat this caveat after every number.

Never assume the credential exists. Never fail the audit for lacking it.

### Setting one up (optional, for whoever installs this skill)

DataForSEO is a paid third-party API and is **not** required — the audit runs without it, with estimated numbers labeled as such. If you want the verified version, it's one account (from [dataforseo.com](https://dataforseo.com)) covering both the AI Optimization API used in pass 4 and the Keywords Data / SERP APIs used in pass 5, billed per request. Two ways to make it reachable:

- **Via MCP** — configure a DataForSEO MCP server in your Claude client. This skill looks for any MCP tool whose name contains "dataforseo", so no further wiring is needed.
- **Via raw API credentials** — hand the credentials to Claude in the session (or keep them somewhere the session can read) and let it call the endpoints directly.

Check DataForSEO's own docs for current auth details, endpoint paths, and pricing before relying on either — this skill names endpoints as of its writing, and vendor APIs move.

## Process

Run these five passes. Each produces findings that feed the final prioritized report — don't skip straight to writing recommendations.

### 1. Machine crawlability (the gate everything else depends on)

- Fetch and read `robots.txt`. Check explicitly for directives on: `Googlebot`, `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`, `Google-Extended`. Note any that are blocked, and flag that CDN/WAF rules (Cloudflare, etc.) can block these bots by default even when robots.txt allows them — call this out as something to verify with whoever manages the CDN, since it isn't visible from the outside.
  - `Googlebot` and `Google-Extended` are not interchangeable, and conflating them is the most common way this check goes wrong: Google's AI Overviews and AI Mode are served off Google's **search** index, so they depend on `Googlebot`. `Google-Extended` is a narrower control over whether content is used for Gemini training and grounding — it does not gate AI Overviews or AI Mode. A site that allows `Google-Extended` but blocks `Googlebot` has the Google AI-search gate shut, not open, so test the two separately and report them separately.
- Diff raw server HTML against fully-rendered HTML for each major page template (homepage, product/feature pages, blog post, pricing/comparison page if one exists). Most AI crawlers do not execute JavaScript — a nav, CTA, or body copy that only appears after JS execution is invisible to them even though it looks fine to a human. Use `curl` for raw HTML and a headless browser (or the browser tools available in this session) for rendered HTML; diff the two for title, H1, canonical tag, internal links, and main copy.
- Check for interactive elements (buttons, forms, "request demo"/"add to cart") implemented as non-semantic markup (e.g. a `<span>` or `<div>` styled to look like a button rather than a real `<button>`/`<a>`). These are invisible to AI agents attempting to act on the page even when a human sees no difference.

### 2. Log-verified AI bot access (skip if server logs aren't available — note it as a follow-up instead of skipping the audit)

- If server/CDN logs are available, filter for the AI bot user-agents listed above and check: are they actually hitting the site (not just theoretically allowed)? What response codes are they getting (flag any 403/404/5xx on AI-bot requests specifically)? Verify hits against each vendor's published IP ranges to rule out spoofed traffic.
- This is the difference between "should be crawlable" and "is actually being crawled" — treat it as higher-value evidence than the robots.txt check alone.

### 3. Off-site citation surface

Given that roughly 85% of brand mentions in AI search originate from third-party pages rather than the brand's own site, this pass matters as much as anything on-domain:

- **Review platforms**: is there a claimed, complete G2 (and/or Capterra, TrustRadius as relevant to category) profile? G2 in particular is heavily cited for B2B "X vs Y" queries. Note review count, recency, and completeness.
- **Comparison content**: search for "[brand] vs [competitor]" for each named competitor, both on-site and off-site. Note what currently answers that query in AI engines today (if anything) — this is usually the single highest-leverage content gap for a B2B site.
- **Community presence**: check Reddit, relevant forums, and YouTube for organic mentions or lack thereof — these platforms show up disproportionately in AI citations relative to their weight in traditional SEO.
- **Third-party proof already in hand but unused**: ask whether sales-call transcripts, support tickets, or customer reviews contain real buyer language that could ground new content — generic category content competes against thousands of near-identical versions already in AI training data; content built from a brand's actual buyer conversations doesn't.

### 4. Cross-engine visibility baseline

- Draft 15-30 realistic buyer prompts spanning discovery ("best [category] platform"), comparison ("[brand] vs [competitor]"), evaluation ("is [brand] good for [use case]"), and implementation ("how to [task] with [category]") query types.
- **If DataForSEO is connected**: query the `ai_optimization/llm_mentions/search/live` endpoint per prompt/keyword, with `platform` set to cover both `chat_gpt` and `google` (AI Overview), and `search_scope` including `fan_out_queries` where relevant — that scope surfaces the sub-queries a prompt actually expands into, which is useful for finding content gaps competitors don't cover either. Pull `ai_search_volume`, `sources` (citations, with domain/position), and whether the target domain/brand appears. This gives real logged data for the platforms DataForSEO covers, and lets the same prompt set be re-run on a cadence for trend tracking. It does **not** replace the whole pass: check which engines the account's platform list actually covers, and run the prompts by hand (per the next bullet) for every engine in scope that it doesn't — a connected audit must still cover all four engines, not just the ones the API returns. Note per engine which method produced its numbers.
- **If not connected**: run the prompts by hand (or via whatever web-search/AI access is available) across ChatGPT, Perplexity, Google AI Mode, Gemini in fresh, unpersonalized sessions. Log: does the brand appear, where in the answer, and in what tone (neutral/positive/negative)? Note which competitors appear instead. Label these results as manually sampled, not exhaustive.
- Calculate the share figure over **prompt-engine observations**, not prompts: the denominator is (prompts tested × engines tested), counting only the pairs actually checked. So 15 prompts across 4 engines is 60 observations, and 20 brand appearances is 33%, not 133%. Dividing by prompt count alone can exceed 100%, and collapsing to one boolean per prompt hides the difference between appearing on one engine and appearing on all four.
- Report per-engine shares alongside the overall figure (appearances on that engine ÷ prompts tested on it). The per-engine split is usually the more actionable number — it shows which engines the brand is missing from, which the overall figure averages away.
- Frame this explicitly as a *baseline*, not a one-time score — visibility on AI engines is volatile (40-60% of cited sources can change month to month), so the value is in re-running this same prompt set on a cadence, not the single snapshot.

### 5. Traditional on-page and technical SEO (still required, now the shorter half)

Cover the standard fundamentals — don't skip these, just don't let them dominate the report:

- Title tags, meta descriptions, H1/heading hierarchy, internal linking, image alt text, URL structure.
- Core Web Vitals signals, mobile-friendliness, HTTPS, sitemap/canonical hygiene, broken links.
- Keyword opportunities: **if DataForSEO is connected**, pull real search volume, keyword difficulty, and SERP feature data from its Keywords Data / SERP APIs instead of estimating. **If not connected**, use web search to research the keyword landscape and label the volume/difficulty columns as directional estimates, same as the baseline marketing:seo-audit skill does.
- Structured data: check what schema exists, but calibrate expectations — Google's own May 2026 AI-search guidance states structured data/FAQ schema is not required for AI Overviews, and FAQ rich results were deprecated. Treat schema as a hygiene/nice-to-have item, not a headline recommendation. What matters more is genuine Q&A-formatted content structure (answer-first paragraphs of 40-60 words, followed by supporting detail; lists and tables over dense paragraphs; a stat or verifiable fact roughly every 150-200 words; named authors with credentials where the content type supports it).
- Content freshness: flag pages not substantively updated in the last quarter — note that a real update means revised claims/data, not a date-stamp edit.

## Output

Produce a report shaped by the audience input from step 1:

**For a leadership/CEO readout:**
- 3-5 sentence state-of-play summary with 2-3 headline stats that make the stakes concrete (traffic, conversion, or competitive-visibility numbers relevant to the audited business).
- A short SEO/AEO/GEO vocabulary primer only if the audience needs it (skip if they're already fluent).
- **A ranked list of 5 priorities**, not a full checklist. For each: what to do, why it matters (tie to a stat or competitive gap from the findings above), effort level (low/medium/high), and a plausible owner. Order by impact-to-effort, not by audit section order.
- Keep total length to what a leadership audience will actually read in one sitting — err short over comprehensive.

**For a working team doc:**
- Full findings from all 5 passes above, organized under those same headers.
- Tables for: on-page issues (page / issue / severity / fix), keyword or prompt-visibility results, and a technical checklist (check / status / detail).
- A quick-wins vs. strategic-investments split at the end, same as a standard SEO audit would produce, but with AI-crawlability and off-site-citation items included in both buckets rather than only traditional on-page fixes.

Always cite where a claim or stat came from (a fetched source, DataForSEO, a client's own analytics/log data, or manual sampling) rather than presenting industry benchmark figures as this specific site's numbers.

## Follow-up

After presenting the audit, offer to: draft the highest-priority comparison or citation-gap content brief, set up a recurring cadence to re-run the cross-engine visibility baseline (via DataForSEO if connected), or turn any specific finding (e.g. the crawlability check) into a one-off deeper dive.