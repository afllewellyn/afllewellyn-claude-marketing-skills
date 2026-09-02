# Pontiac Intelligence: SEO + AEO + GEO Audit

**Sites audited:** https://pontiac.media/ (marketing site) and https://wiki.pontiac.media/ (documentation)
**Date:** 2 September 2026
**Data sources:** DataForSEO (On-Page crawl, Labs rank data, Backlinks, Google SERP with AI Overview, LLM Mentions, LLM Responses across ChatGPT / Claude / Gemini / Perplexity), Pontiac MCP wiki search, web search. Every number below names its source. No server or CDN logs were available; pass 2 is a follow-up.

**Audience:** leadership readout first, full working document after it.

---

## Part 1: Leadership readout

### State of play

Pontiac is known to the AI engines but not discoverable through them. When a buyer types the name, all four engines (ChatGPT, Claude, Gemini, Perplexity) find Pontiac, describe it accurately and mostly favourably, and Google's AI Overview does the same. When a buyer asks the question that comes before knowing the name ("best self-serve DSP with no minimum", "most transparent DSPs", "Trade Desk alternatives under $10k"), Pontiac appears in 4 of 44 answers (9%) and the engines name StackAdapt, The Trade Desk, AdLib, Vibe, Roku and Simpli.fi instead, sourced from those competitors' own comparison articles, Reddit and G2. The competitors winning those answers are doing it with listicle content ("best self-serve DSPs with no minimums") that Pontiac has never published, even though Pontiac's actual offer (no minimum, 20% flat margin, Netflix/Disney CTV access, log-level data, an MCP server) fits those queries better than most of the brands being cited.

Across the full 20-prompt, four-engine baseline (80 observations, DataForSEO LLM Responses, 2 Sept 2026) Pontiac was mentioned in 33 (41%), but 29 of those 33 came from prompts that contained its name. Three more numbers frame the gap (all DataForSEO, 2 Sept 2026):

| Metric | pontiac.media | StackAdapt | Vibe.co | Simpli.fi | SmartyAds | AdLib |
|---|---|---|---|---|---|---|
| Logged AI answers citing the domain (LLM Mentions DB) | 1 | 2,357 | 946 | 246 | 236 | 135 |
| Google organic keywords ranking (top 100, US) | 10 | 4,003 | n/a | 523 | 3,527 | 241 |
| Referring domains (backlinks) | 157 | n/a | n/a | n/a | n/a | n/a |

The one AI answer citing pontiac.media is for the query "pontiac advertising", and it is mostly about 1960s General Motors car ads. All 10 of pontiac.media's ranking keywords are brand or near-brand terms; none are category terms like "self-serve DSP" (110 searches/month, $189 CPC) or "CTV advertising platform" (320/month, $142 CPC).

The marketing site has not published a blog post since June 2024, and the wiki, which holds roughly 300 pages and 90,000+ words of genuinely useful, citable product documentation, has no robots.txt, no sitemap, no meta descriptions, no H1 tags, and query-string URLs, so search engines and AI crawlers treat it as low-priority.

### The five priorities

| # | Priority | Why it matters | Effort | Owner |
|---|---|---|---|---|
| 1 | **Publish the comparison and category content AI engines actually cite.** Four pages on pontiac.media: "Pontiac vs StackAdapt", "Pontiac vs Simpli.fi", "Best self-serve DSPs with no minimum spend (2026)", "The Trade Desk alternatives for agencies under $10k/month". Answer-first paragraphs, a comparison table with real fees and minimums, and a named author. Add a fifth page on the Pontiac MCP server for ChatGPT and Claude Code, and list it in the MCP directories Perplexity and Claude cited. | Unbranded discovery share is 3 of 28 (11%). The two comparison prompts Pontiac lost outright are its own positioning. Every engine cited competitor listicles (AdLib, Epom, Vibe, StackAdapt) for these answers. Pontiac's MCP docs exist but were cited 0 times in 8 MCP-prompt observations. | Medium | Marketing lead, with founders for the fee/positioning claims |
| 2 | **Put the full pricing on pontiac.media and correct the third-party listings.** One pricing page ($100 one-time entry, 20% self-serve fee on all-in media cost, $25/month minimum user fee, no campaign minimum, 30% managed service with a $1,000/month requirement), then update G2 pricing (dated 2022), SourceForge and Slashdot ("$25/month, free version") and Clutch ("$1,000 minimum"). | Perplexity is telling buyers Pontiac "starts at $25/month with a free version"; Claude reports "a $99 fee and a $1,000 minimum". Both are fragments of real wiki numbers (the minimum user fee, the managed-service requirement) stripped of context, because pontiac.media has no pricing page and the engines read SourceForge and Clutch instead. | Low | Marketing lead (one afternoon) |
| 3 | **Make the wiki citable.** Add robots.txt and an XML sitemap, promote doc titles to H1, generate meta descriptions, fix 47 duplicate titles, turn the 89,000-word hub pages into indexes, expose last-updated dates, add Organization and TechArticle schema. | 700+ pages of the most specific DSP documentation in the category rank for zero keywords, have 3 referring domains, and were cited in 0 of 80 AI answers. The 90k-word hubs are un-extractable. | Medium | Web developer (theme template work, about a week) |
| 4 | **Fix the marketing site's crawl signals.** Replace the stale 8-URL `sitemap.txt` with the WordPress XML sitemap; fix the Organization schema that points at `http://172.31.40.15/`; 301 the four legacy `.html` pages; promote blog post titles to H1; server-render the contact form. | The schema bug undermines entity disambiguation for a brand that shares its name with a car company (319 logged AI answers for "Pontiac Intelligence" are about Firebirds). AI agents cannot find a form to request a demo. | Low | Web developer (one day) |
| 5 | **Show up where the engines are reading, and keep the baseline running.** Founders answer the r/programmatic threads the engines cite ("self-serve DSP recs", "buy CTV without minimum", "fully transparent DSPs"). Post the 2025-26 news (Peer39/InterMedia show-level CPA, MCP launch, Beet.TV) on pontiac.media, which has had no new post since June 2024. Re-run the 20-prompt baseline monthly ($3.35 per run) and pull the AI-bot server logs once. | Reddit was the most-cited domain across all 80 answers (18) and already recommends Pontiac organically in one thread. The blog's freshness signal is 14 months stale. Visibility is volatile, so the number only means something as a trend. | Low to medium, ongoing | CEO or co-founder for Reddit voice; marketing for cadence; hosting admin for logs |

**Not in the top five but worth knowing:** the raw HTML on both sites already carries full copy and links without JavaScript, robots.txt blocks no AI crawler, and G2 sentiment is strong (4.8 from 16 reviews). The gates are open; there is just very little on the other side of them for an engine to cite.

**Companion document:** `pontiac-content-brief-2026-09.md` specifies every page and post recommended here, with target prompts, keywords, answer-first drafts, table specs and sources.

---

## Part 2: Working document

### Pass 1: Machine crawlability

**robots.txt** (fetched via DataForSEO On-Page, raw body retrieved 2 Sept 2026)

| Check | pontiac.media | wiki.pontiac.media |
|---|---|---|
| robots.txt present | Yes | **No (404)** |
| Googlebot | Allowed (`User-agent: *` / `Allow: /`) | Allowed by default (no file) |
| Google-Extended | Not mentioned, so allowed | Allowed by default |
| GPTBot, OAI-SearchBot, ChatGPT-User | Not mentioned, so allowed | Allowed by default |
| ClaudeBot, Claude-User | Not mentioned, so allowed | Allowed by default |
| PerplexityBot, Perplexity-User | Not mentioned, so allowed | Allowed by default |
| Sitemap directive | Points to `https://pontiac.media/sitemap.txt` | None |
| Sitemap contents | **Stale.** Lists 8 legacy URLs (`pricing.html`, `tech.html`, `platform.html`, `wiki.html`, `register.html`, `history.html`, `algorithm.html`, `contact.html`). `wiki.html` is a 404. None of the 40 live WordPress pages are in it. | No sitemap at any standard path (`/sitemap.xml`, `/wp-sitemap.xml`, `/sitemap_index.xml` all 404) |

The pontiac.media file contains a duplicated, empty `User-agent: *` group, which is harmless but suggests it was hand-edited and never revisited.

Nothing in either robots.txt blocks an AI crawler, so the robots gate is open. Two caveats from the skill apply here. First, the marketing site sits behind Apache and the wiki behind nginx with no evidence of a CDN or WAF in response headers, but a hosting-level bot filter would not be visible from outside, so whoever manages hosting should confirm no bot-management rule 403s these user agents. Second, Google's AI Overviews depend on Googlebot, not Google-Extended, and Googlebot is allowed on both sites.

**Raw vs rendered HTML** (DataForSEO On-Page instant fetch, no-JS vs headless-browser render, homepage of each site)

| Element | pontiac.media raw | pontiac.media rendered | wiki raw | wiki rendered |
|---|---|---|---|---|
| Title | Home - Pontiac Intelligence | same | Pontiac Wiki – Pontiac Wiki | same |
| H1 | 2 (hero + "Ready to get started?") | same | **none** | **none** |
| Canonical | self | same | self | same |
| Internal links | 18 | 19 (one wiki login link added) | 21 | 21 |
| Visible words | 564 | 603 | 99 | 105 |

Both sites are server-rendered WordPress (Elementor on the marketing site; a "Docly" docs theme with the weDocs plugin on the wiki). The raw HTML carries the full navigation, copy, links and structured data, so AI crawlers that do not execute JavaScript see the same page a human does. This is the one thing both sites already get right. The rendered version adds only Elementor's mega-menu JSON and a "Let's talk" form, and the rendered homepage is 400 KB against 128 KB raw because of inlined Elementor settings.

The wiki category pages, however, load the entire section into one page: "Bidder Documentation" is a single URL of 89,098 words, "Platform Updates" 26,700 words, "Analytics Documentation" 25,394 words. That is not a rendering problem but it is an extraction problem: an AI engine chunking a 90,000-word page cannot reliably attribute a passage to a topic, and the same passages also exist on the individual child pages, so 63 pages are flagged as duplicate content by the crawl.

**Interactive elements.** On the pontiac.media homepage, 48 of 60 Elementor "button" elements are rendered as `<div>` or `<span>`, not `<a>` or `<button>`. The primary "Request a demo" and the four "Take Control of Your Buying" CTAs are real links, so an agent can follow the main conversion path, but the tab switchers (CTV / OLV / OOH / Audio) that reveal most of the product copy are non-semantic divs. The contact page contains no `<form>` element in raw HTML: the form is injected by JavaScript, so an AI agent asked to "request a demo from Pontiac" cannot find a form to fill. The wiki has one real search form and semantic buttons.

**Site structure.** The marketing site is 40 crawlable pages. The wiki crawl hit its 300-page cap with 434 URLs still queued, so the wiki is at least 700 URLs. All wiki content lives at `?docs=slug` query-string URLs with a self-referencing canonical, which is indexable but is the weakest URL form for both search and AI citation (the crawl flags 290 of 300 wiki pages for non-SEO-friendly URLs).

### Pass 2: Log-verified AI bot access (follow-up)

No server, CDN or WAF logs were available in this session, so this pass could not be run. Robots.txt says "allowed"; only logs say "actually crawled". Recommended follow-up, about one hour for whoever administers the two servers:

1. Pull the last 30 days of Apache access logs (pontiac.media) and nginx access logs (wiki.pontiac.media).
2. Filter user agents for `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User`, `Google-Extended`, `Googlebot`.
3. For each, count requests and response codes. Any 403, 429 or 5xx on these agents is a blocker that robots.txt cannot reveal.
4. Verify hits against each vendor's published IP ranges (OpenAI, Anthropic, Perplexity and Google all publish them) to discard spoofed traffic.
5. Note which wiki URLs the AI bots fetch most. That is a free signal of which documentation topics AI engines already consider relevant.

A DataForSEO-only proxy for this exists: the LLM Mentions database logged pontiac.media as a cited source exactly once, which means the domain is at least reachable by Google's AI systems. It does not tell us whether OpenAI or Anthropic crawlers reach it.

### Pass 3: Off-site citation surface

**Review platforms** (web search and DataForSEO SERP, 2 Sept 2026)

| Platform | Status | Detail |
|---|---|---|
| G2 | Claimed, active | 4.8 / 5 from 16 reviews, 93.8% from small-business users, Quality of Support 10.0. G2's profile banner reads "It's been two months since this profile received a new review." Pricing listed as "Pay As You Go". G2 auto-generates comparison pages: Pontiac vs StackAdapt, vs Simpli.fi, vs SmartyAds, vs AdLib. G2 is cited by Google's AI Overview for "pontiac intelligence vs stackadapt". |
| SourceForge / Slashdot | Listed, empty | 0 reviews, "starting at $25/month, free version available" (inaccurate: the wiki says a $100 one-time entry fee and 20% margin). Auto-generated compare pages exist (vs Roku Advertising, vs ASTRAD, vs Active Agent). |
| Capterra / GetApp / Software Advice | Not found | No listing surfaced. G2 completed its acquisition of these three in February 2026, so a single G2 listing may propagate; worth checking. |

**Comparison content.** Every "Pontiac vs X" query today is answered by G2's auto-generated page, and Google's AI Overview for "pontiac intelligence vs stackadapt" leans on G2, LiveRamp's partner directory, AdRoll's and Vibe's own comparison blogs. Pontiac has no comparison page on its own domain for any competitor. Competitors publish them aggressively: AdLib ("StackAdapt vs DV360", "Simpli.fi alternatives"), Vibe ("7 best StackAdapt competitors"), AdRoll ("AdRoll vs StackAdapt"). That content is what the AI engines cite for the "alternatives" and "vs" prompts in pass 4.

**Community and video.**

- **Reddit.** Pontiac is organically recommended in r/programmatic ("What DSPs are fully transparent?", 2024-12) and that thread is the first source Google's AI Overview cites for "pontiac dsp pricing". Reddit threads are also the top cited source across the pass-4 prompts on Perplexity and ChatGPT ("looking for self-serve DSP recs", "how to buy CTV inventory without minimum spend"). Pontiac does not appear in those threads. This is the highest-leverage, lowest-cost citation gap in the audit.
- **YouTube.** Pontiac Intelligence has a channel; recent uploads include "Inside Pontiac's CTV-First DSP" (Nov 2025) and a Beet.TV interview with CEO Keith Gooberman ("Legacy DSPs are like battleships", Aug 2025). YouTube is cited by Google's AI Overview for the pricing query. Video titles carry the brand but not the category terms ("self-serve DSP", "no minimum").
- **Trade press.** AdExchanger has a Pontiac Intelligence tag page and covered the July 2026 InterMedia / Peer39 / Pontiac show-level CPA collaboration (94% of CTV impressions). MediaPost, Business Wire (2022 CTV bidder launch), ExchangeWire ("A new type of DSP is emerging") and Beet.TV have all covered the company. This press is not linked from, or summarised on, pontiac.media.

**Backlinks** (DataForSEO Backlinks API, 2 Sept 2026)

| Metric | pontiac.media (incl. subdomains) | wiki.pontiac.media |
|---|---|---|
| Backlinks | 1,415 | 112 |
| Referring domains | 157 | 3 |
| Domain rank | 190 | 114 |
| Spam score | 18 | 2 |
| Nofollow referring domains | 50 | 0 |

The referring-domain list is thin at the top and noisy at the bottom. The strongest referrers are progmechs.com (the founders' agency, 224 links), Triton Digital, and Blasting News. About 270 backlinks come from `.de` domains and dozens of recent referrers (Aug 2026) are casino, betting and link-directory sites (`bestnz-poker-casinoslot.com`, `betwinnermirror.com`, `websiteslinkdirectory.com`), which explains the spam score of 18. None of the trade-press coverage above shows up as a followed link. The wiki's three referring domains mean nothing external points at the documentation, which is the most citable content Pontiac owns.

**Third-party proof already in hand but unused.** The wiki contains a "Case Studies" section and product pages reference a mattress-company CTV case study and a "23% improvement in CPA" result on the marketing site's case-studies page. G2 reviews contain concrete buyer language ("no minimum spend, access to all major supply platforms, fast QA, attentive support team"). The Pontiac MCP wiki search also surfaces internal recommendations that are exactly what implementation prompts ask for (CTV closing CPMs of $20-40, "set frequency caps to 0", "run through PMPs not open exchange"). None of that language appears on pontiac.media. Sales-call transcripts and support tickets were not available for this audit; they should be mined for the comparison and FAQ content in the priorities.

### Pass 5: Traditional on-page and technical SEO

**Domain footprint** (DataForSEO Labs, US, 2 Sept 2026)

| Domain | Organic keywords in top 100 | Est. monthly organic traffic | Keywords in top 3 |
|---|---|---|---|
| pontiac.media | 10 | 50 | 3 (all brand) |
| wiki.pontiac.media | 0 | 0 | 0 |
| stackadapt.com | 4,003 | 26,868 | 369 |
| simpli.fi | 523 | 9,806 | 62 |
| smartyads.com | 3,527 | 4,904 | 52 |
| choozle.com | 593 | 1,800 | 23 |
| getadlib.com | 241 | 1,683 | 22 |

pontiac.media ranks #1 for "pontiac intelligence" (50/mo), "pontiac dsp" (40/mo) and "pontiac advertising" (70/mo). Its only non-brand rankings are positions 49-86 for "walmart ctv", "oracle moat" and "google contextual", each from a 2024 blog post. The wiki, despite ~700 URLs of documentation, ranks for nothing.

**Crawl summary** (DataForSEO On-Page, JS off, 40 pages pontiac.media, 300 of 700+ pages wiki)

| Check | pontiac.media | wiki.pontiac.media |
|---|---|---|
| OnPage score | 88.7 | 87.0 |
| HTTPS, valid cert | Yes (expires 22 Nov 2026) | Yes (same cert) |
| Pages with no meta description | 2 (privacy, register.html) | **290 of 300** |
| Pages with no H1 | 17 (every blog post) | **290 of 300** |
| Title too short (< 30 chars) | 3 | 112 |
| Title too long (> 65 chars) | 10 (blog posts) | 3 |
| Duplicate titles | 0 | 47 ("Overview" x8, "Boolean Logic" x3, etc.) |
| Duplicate content | 2 | 63 (section hubs replicate child pages) |
| Images missing alt | 27 pages | 229 pages |
| Broken internal links (404 targets) | 2 (`/advaced-features/` typo, `/our-cookieless-audience-research-solution/`) | 3 |
| Redirect chains | 1 (`register.html` http to https to `/register`) | 0 |
| HTTPS pages linking to HTTP | 3 | 9 |
| Render-blocking resources | 26 pages | 290 pages |
| Homepage LCP (headless, desktop) | 2.35 s | 1.34 s |
| Homepage time to interactive | 1.9 s | 1.6 s |
| Homepage fully loaded | 3.5 s | 1.8 s |

**Legacy pages still live.** `platform.html`, `pontiac-landing.html`, `algorithm.html` and `register.html` are pre-WordPress static pages that return 200 with no canonical tag, describe the product as "access to over 10,000 desktop, video and mobile publishers" and use an older Elementor build. `register.html` is also the sitemap's only registration URL. These should 301 to their WordPress equivalents.

**Structured data.** pontiac.media ships Yoast-style JSON-LD (`WebPage`, `WebSite`, `Organization`, `BreadcrumbList`, `Article` with `Person` author on blog posts). One defect: the `WebSite` and `Organization` `@id` and `url` fields point to `http://172.31.40.15/`, an internal AWS private IP, instead of `https://pontiac.media/`. That is a WordPress "Site Address" misconfiguration leaking into every page's schema and it invalidates the Organization entity that AI engines use to disambiguate "Pontiac Intelligence" from "Pontiac" the car brand. The wiki has no structured data at all. Per Google's May 2026 guidance this is hygiene, not a headline item, but the private-IP leak is a five-minute fix that should be made.

**Brand ambiguity is a real entity problem.** DataForSEO's LLM Mentions database returns 319 logged AI answers for the keyword "Pontiac Intelligence", and essentially all of them are about the Pontiac Firebird, Knight Rider's KITT and GM. Google's Knowledge Graph does resolve "pontiac intelligence" to "Software company in Ridgewood, New Jersey", but the Organization schema pointing at a private IP, no Wikipedia or Wikidata entity, and a company name that shares its first token with a famous car brand all work against the AI engines.

**Content freshness** (article:modified_time from page HTML)

- Homepage last modified 10 Oct 2024. Media Buying and Audience Discovery pages 2 Aug 2024. About page 1 Jul 2024.
- Newest blog post: "Two Optimization Models Are Better Than One", 28 Jun 2024. Every one of the 22 blog posts was last modified in June 2024. No post in 14 months.
- The July 2026 InterMedia/Peer39 show-level CPA news, the MCP server for ChatGPT and Claude Code, and the 2025 Beet.TV interview are all absent from the marketing site.
- The wiki is actively maintained (Platform Updates section, 2026 MCP documentation) but exposes no dates in HTML, so neither Google nor AI engines can tell it is fresh.

**Keyword opportunities** (DataForSEO Keywords Data and Labs, US, monthly volume, keyword difficulty 0-100)

| Keyword | Volume | KD | CPC | Intent | Pontiac ranks? | Note |
|---|---|---|---|---|---|---|
| demand side platform | 1,300 | 49 | $38 | commercial | no | Category head term; AI Overview present |
| programmatic advertising platform | 720 | 8 | $56 | commercial | no | Low difficulty for the volume |
| ctv advertising platform | 320 | 0 | $142 | commercial | no | **KD 0, $142 CPC**: best single opportunity |
| connected tv advertising platform | 320 | n/a | $95 | commercial | no | Same page as above |
| what is ctv advertising | 880 | 1 | $25 | informational | no | Wiki glossary could win this |
| best dsp platforms | 320 | 20 | $7 | commercial | no | Listicle; AI engines cite these |
| programmatic advertising software | 210 | 6 | n/a | commercial | no | |
| top dsp platforms | 170 | 3 | $35 | commercial | no | |
| programmatic dooh | 140 | n/a | $82 | commercial | no | Pontiac has a differentiated DOOH offer |
| programmatic audio advertising | 140 | 0 | n/a | commercial | no | |
| audience research tool | 140 | n/a | $63 | commercial | no | Pontiac's product is literally named ART |
| self-serve dsp / self service dsp | 110 each | 1-16 | $189 | navigational | no | Highest CPC in the set |
| best programmatic advertising platforms | 110 | 6 | $112 | commercial | no | |
| ctv dsp | 30 | n/a | n/a | commercial | no | |
| netflix programmatic advertising | 20 | n/a | n/a | informational | no | Pontiac has direct Netflix access |
| stackadapt alternative | 10 | n/a | n/a | commercial | no | Low volume, high AI-citation value |

Two things stand out. CPCs of $95-$189 on the CTV and self-serve terms mean competitors are paying heavily for clicks Pontiac could earn organically, and the keyword difficulty on the CTV platform terms is near zero because the SERPs are dominated by listicles from small vendors (Starti, AdLib, Vibe, SmartyAds) rather than authority sites. Google's SERP for "best self-serve ctv advertising platform" shows an AI Overview citing getadlib.com, starti.ai and vibe.co, and a Reddit thread at position 4.

**Page-level issues** (severity: H = blocks visibility, M = hurts ranking or extraction, L = hygiene)

| Page | Issue | Severity | Fix |
|---|---|---|---|
| pontiac.media/robots.txt | Sitemap points to stale `sitemap.txt` of 8 legacy URLs | H | Enable the WordPress XML sitemap (Yoast/RankMath) and point robots.txt at it |
| wiki.pontiac.media | No robots.txt, no sitemap | H | Add both; list every `?docs=` URL |
| All pages | Organization/WebSite schema `url` is `http://172.31.40.15/` | H | Set WordPress Site Address to `https://pontiac.media`, purge cache |
| wiki (290 pages) | No meta description, no H1 (page title rendered as H2) | M | Theme template change: promote doc title to H1, generate descriptions from the first paragraph |
| wiki hubs (`?docs=ctv-documentation` etc.) | 89k-word pages duplicating all children | M | Make hubs an index of links plus a 2-line summary per child |
| wiki | 47 duplicate titles ("Overview – Pontiac Wiki" x8) | M | Prefix titles with the parent section |
| All 22 blog posts | No H1 (title is an H2), titles 66-130 chars | M | Promote post title to H1; trim titles |
| /newcontact/ | 24 words, no form in HTML, description "Contact us for any issues." | M | Server-render the form; write a real description |
| platform.html, pontiac-landing.html, algorithm.html, register.html | Legacy static pages live with no canonical, outdated claims | M | 301 to current equivalents |
| /advaced-features/ (typo), /our-cookieless-audience-research-solution/ | 404 targets of internal links | L | Fix links |
| 27 marketing pages, 229 wiki pages | Images without alt text | L | Add alt text; the wiki's 306 screenshots on the Bidder hub are the bulk |
| Blog | 22 posts, all last modified June 2024 | M | See freshness above |


### Pass 4: Cross-engine visibility baseline

**Method.** 20 buyer prompts (7 discovery, 5 comparison, 4 evaluation, 4 implementation) were run once each on 2 September 2026 through DataForSEO's LLM Responses API with web search enabled on all four engines: ChatGPT (gpt-5-mini), Claude (Sonnet 4.6), Gemini (3.5 Flash, Google-grounded) and Perplexity (sonar-pro). That is 80 prompt-engine observations, the denominator for every share below. DataForSEO's LLM Mentions database (logged Google AI Overview and ChatGPT answers) was used for the competitor-citation counts in the leadership table; it covers only those two platforms and holds a single logged answer citing pontiac.media, so the live prompt run is the baseline. Gemini's grounding API returns opaque redirect URLs, so owned-domain citation could not be attributed on Gemini. Total API cost of the run: $3.35, so it is cheap to repeat monthly. The prompts and raw observations are in `data/prompts.json` and `data/llm_obs.json`.

**Headline: 33 of 80 observations mention Pontiac (41%). But the split by prompt type is the number that matters.**

| Prompt type | Observations | Pontiac mentioned | Share |
|---|---|---|---|
| Evaluation ("Is Pontiac good for CTV?", "What does Pontiac charge?") | 16 | 16 | 100% |
| Comparison ("Pontiac vs StackAdapt", "Trade Desk alternatives under $10k") | 20 | 13 | 65% |
| Discovery ("best self-serve DSP no minimum", "most transparent DSPs") | 28 | 3 | 11% |
| Implementation ("how to set up CTV with PMP deals", "connect a DSP to ChatGPT via MCP") | 16 | 1 | 6% |
| **Unbranded (discovery + implementation)** | **44** | **4** | **9%** |
| Branded (comparison + evaluation) | 36 | 29 | 81% |

When the buyer already knows the name, every engine finds Pontiac and describes it accurately and positively (18 positive, 12 neutral, 2 mixed, 1 negative of 33 mentions). When the buyer does not know the name, Pontiac appears in 4 of 44 answers, and 3 of those 4 are the one prompt about census/ZIP-code cookieless targeting, where Pontiac's Audience Research Tool is distinctive enough that Claude and Gemini rank it first. The two comparison prompts that did not name Pontiac ("Trade Desk alternatives under $10k/month" and "StackAdapt alternatives with no minimum") are exactly the queries Pontiac's positioning is built for; only Gemini named Pontiac, third, on the second one.

**Per engine** (appearances on that engine divided by 20 prompts)

| Engine | Mentioned | Share | Owned domain cited | Notes |
|---|---|---|---|---|
| ChatGPT (gpt-5-mini, web search) | 8 / 20 | 40% | 7 | Cites pontiac.media terms-and-conditions for pricing because no pricing page exists on the marketing site. On "what do reviews say" it asked whether the user meant a car-audio DSP. |
| Claude (Sonnet 4.6, web search) | 9 / 20 | 45% | 6 | Most likely to rank Pontiac first on cookieless targeting. Reported a "$99 fee", "30% managed fee" and "$1,000 minimum project size" from Clutch and G2, not from Pontiac. |
| Gemini (3.5 Flash, grounded) | 9 / 20 | 45% | n/a | Only engine to name Pontiac on "StackAdapt alternatives". Accurately describes the 20% self-serve / 30% managed structure and the bootstrapped, "speedboat" story. |
| Perplexity (sonar-pro) | 7 / 20 | 35% | 7 | Lowest share. Repeats SourceForge's "$25/month, free version available" as Pontiac's pricing. Cites Reddit in most category answers. |

**Who wins the unbranded prompts instead.** Count of observations naming each competitor: The Trade Desk 41, StackAdapt 31, DV360 31, Amazon DSP 22, Simpli.fi 20, AdLib 14, Basis 13, AdRoll 9, Roku Ads Manager 8, Yahoo 8, Epom 7, Viant 7, Choozle 7. Pontiac at 33 is competitive with these only because 29 of its 33 come from prompts that contain its name.

**What the engines cite.** Across all 80 answers the most-cited domains were reddit.com (18 observations), pontiac.media (18, almost all on branded prompts), linkedin.com (16), g2.com (15), getadlib.com (12), epom.com (11), stackadapt.com (10), drive.pontiac.media (9), adexchanger.com (7). Three things follow:

1. **wiki.pontiac.media was cited zero times in 80 answers**, including the two MCP prompts where Pontiac's own "ChatGPT Setup" and "Claude Code Setup" pages are exactly the content requested. The engines cited Amazon Ads, Meta, Google Ads, AdRoll and third-party MCP directories instead.
2. Competitor blogs (AdLib, Epom, StackAdapt, Vibe, SmartyAds) are cited as often as Reddit and G2. They earn that by publishing the "best X" and "X alternatives" listicles that the discovery prompts pull from.
3. Distorted pricing is now in circulation. SourceForge/Slashdot's "$25/month, free version" and Clutch's "$1,000 minimum" are fragments of the wiki's real schedule ($100 one-time entry fee, 20% fee on all-in media cost, $25/month minimum user fee, $1,000/month required only for managed service) with the context removed, because the full schedule sits on an uncited wiki page and a 2022 G2 pricing entry.

**Full grid** (M = mentioned, digit = position among brands named, c = owned domain cited, - = absent)

| # | Type | Prompt | ChatGPT | Claude | Gemini | Perplexity |
|---|---|---|---|---|---|---|
| D1 | discovery | Best self-serve DSPs for a small agency buying CTV with no minimum | - | - | - | - |
| D2 | discovery | Platforms to buy Netflix, Disney+, Hulu CTV without a large minimum | - | - | - | - |
| D3 | discovery | Most transparent DSPs with lowest take rates and fees | - | - | - | - |
| D4 | discovery | DSPs with log-level data and full reporting transparency | - | - | - | - |
| D5 | discovery | Best self-serve platforms for programmatic DOOH down to the billboard | - | - | - | - |
| D6 | discovery | DSPs with cookieless targeting built on census and ZIP data | M6c | M1c | M1 | - |
| D7 | discovery | DSPs you can manage from ChatGPT or Claude via MCP | - | - | - | - |
| C1 | comparison | Pontiac Intelligence vs StackAdapt for a small agency buying CTV | M2c | M1c | M1 | M2c |
| C2 | comparison | Pontiac Intelligence vs Simpli.fi for local CTV | M1c | M1c | M1 | M2c |
| C3 | comparison | Pontiac DSP vs AdLib on pricing, minimums, inventory | M1c | M1c | M1 | M1c |
| C4 | comparison | Best Trade Desk alternatives for agencies under $10k/month | - | - | - | - |
| C5 | comparison | StackAdapt alternatives with no minimum spend | - | - | M3 | - |
| E1 | evaluation | Is Pontiac Intelligence a good DSP for CTV? | M1c | M1 | M1 | M1c |
| E2 | evaluation | What does Pontiac charge: fees, margin, minimums? | M1c | M1c | M1 | M1c |
| E3 | evaluation | What do users and reviews say about Pontiac? | M1 | M1 | M1 | M1c |
| E4 | evaluation | Who founded Pontiac Intelligence, what is it known for? | M1c | M1c | M1 | M1c |
| I1 | implementation | Set up a CTV campaign on a self-serve DSP with PMP deals | - | - | - | - |
| I2 | implementation | Get show-level transparency and performance data for CTV | - | M1 | - | - |
| I3 | implementation | Run programmatic audio and podcast ads on a small budget | - | - | - | - |
| I4 | implementation | Connect a DSP to ChatGPT or Claude via MCP | - | - | - | - |

**This is a baseline, not a score.** AI answers change materially month to month, and single runs of non-deterministic models carry noise. The value is in re-running these same 20 prompts on the same four engines on a fixed cadence and watching the unbranded share move. At $3.35 per run this should be monthly.

**Google AI Overview check** (DataForSEO SERP API, US desktop, same day). AI Overviews appeared on 6 of 7 category and comparison queries tested. Pontiac appears only on its own branded queries: "pontiac intelligence vs stackadapt" (sources: G2, LiveRamp partner directory, AdRoll, Vibe) and "pontiac dsp pricing" (sources: Reddit r/programmatic, drive.pontiac.media, YouTube). On "self serve dsp no minimum", "best self-serve ctv advertising platform", "self serve dsp" and "demand side platform for small agencies" the overview names Amazon, StackAdapt, Roku, MNTN, Vibe, AdRoll and Simpli.fi, sourced from Reddit, epom.com, getadlib.com, starti.ai, basis.com and vibe.co.

### Quick wins vs strategic investments

**Quick wins (days, low effort)**

- Replace `sitemap.txt` with the WordPress XML sitemap and update the robots.txt Sitemap line (pontiac.media).
- Add robots.txt and an XML sitemap to wiki.pontiac.media.
- Fix the WordPress Site Address so Organization/WebSite schema stops pointing at a private IP.
- 301 `platform.html`, `pontiac-landing.html`, `algorithm.html`, `register.html` to current pages; fix the two 404 internal links.
- Publish a pricing page on pontiac.media; correct G2, SourceForge, Slashdot and Clutch pricing so the $25 minimum user fee and $1,000 managed-service requirement are shown in context.
- Ask hosting to confirm no bot-management rule blocks GPTBot, ClaudeBot, PerplexityBot; pull 30 days of logs (pass 2).
- Submit the Pontiac MCP server to the directories cited by Perplexity and Claude (mcpservers.org, Claude connector directory, ChatGPT apps).
- Founders reply in the three r/programmatic threads named above.

**Strategic investments (weeks to months)**

- The comparison and category content programme (priority 1), built from G2 review language, sales-call transcripts and the wiki's own setup guidance rather than generic category copy.
- Wiki template rebuild for H1, descriptions, dates, schema, hub-page restructuring and pretty URLs (priority 3).
- A publishing cadence on pontiac.media: one substantive post per month, revised claims not date stamps, with the founders as named authors.
- Monthly re-run of the 20-prompt, four-engine baseline plus the Google AI Overview checks, tracked as a trend (unbranded share is the KPI; 9% today).
- An earned-link effort to convert the existing AdExchanger, MediaPost, Beet.TV and ExchangeWire coverage into followed links, and to disavow or ignore the casino/directory spam that is inflating the spam score.

### Appendix: data files

- `data/prompts.json`: the 20 prompts, by type.
- `data/llm_obs.json`: all 80 observations with engine, mention, position, tone, cited owned domains, competitors named and the excerpt around the mention.
- `data/llm_score.txt`: the scoring script output.
- `data/ranked_rows.json`: pontiac.media ranked keywords (DataForSEO Labs).
- `data/kv_rows.json`: keyword volumes and CPCs (DataForSEO Keywords Data).
- `data/pm_pages_rows.json`, `data/wiki_pages_rows.json`: per-page crawl results.


