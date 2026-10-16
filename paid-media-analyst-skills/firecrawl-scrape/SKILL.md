---
name: firecrawl-scrape
description: Fetch a single known web page that WebFetch cannot retrieve (bot-management WAF returning HTTP 403, or JS-rendered content) using Firecrawl's hosted scraper with residential/stealth proxies. Returns clean markdown (HTML fallback). Use when you already have a specific URL and the native fetch is blocked — e.g. [Client] landing pages during a landing-page audit. Scope is scrape-only (single URLs); not crawl or site mapping.
argument-hint: "[url]"
allowed-tools: Bash, Read
---

# Firecrawl Scrape

Retrieve a single page's content through Firecrawl when the native WebFetch is
blocked. [Client] (and similar) sites sit behind a bot-management WAF that
returns **HTTP 403** to WebFetch and to plain `curl` from the sandbox, because
both originate from a datacenter IP. Firecrawl runs a headless browser plus
**residential/stealth proxies on its own infrastructure**, so the origin sees a
real residential browser and serves the page.

This skill is the **scrape-only** Firecrawl capability (single, known URLs). It
intentionally does not cover crawl or site-map — those can be added later if a
small-build site crawl is ever needed.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## Prerequisites

- `FIRECRAWL_API_KEY` is set as an environment variable, or in a gitignored `.env`
  at the `paid-media-analyst-skills/` root (see `.env.example`). Never commit it.
  If it is unset, the helper prints a skip message and returns nothing, and the
  caller should skip the URL and note the limitation.
- The sandbox network policy allows egress to `api.firecrawl.dev` (add it to the
  allowed domains).

## When to use

- A specific URL is known and **WebFetch failed** (403 / timeout / empty body)
  or the page is JS-rendered.
- A domain is known to sit behind a WAF (e.g. `[client-domain].com`) — skip WebFetch
  and come straight here.

Do **not** use this for general web search or to discover URLs — only to fetch
a page whose URL you already have.

## How to fetch

Shell out to the committed helper (do not reimplement the API call inline):

```bash
python scripts/firecrawl_fetch.py "<url>"
```

- One URL → the page **markdown** is printed to stdout (capture it directly).
- Multiple URLs → each page is written to `/tmp/firecrawl_<slug>.md` and the
  helper prints `"<url>\t<path>"` lines; `Read` each file for the content.

The helper returns markdown (preferred for headings/body copy) and falls back
to HTML. It never raises — a blocked or failed page produces no output for that
URL and a `firecrawl: FAILED <url>` line on stderr.

## Prefer Firecrawl when a claim depends on exact text

WebFetch returns a model-written summary of the page, not the page text, and that
summary can drop figures and acronyms (a statistic, a model number, "AI" vs
"said"). When a finding hinges on an exact figure or word, fetch the full text
with Firecrawl and search it directly instead of trusting the WebFetch summary.

## Credit model (be frugal)

- A normal scrape is **1 credit**; the stealth-proxy retry that beats a WAF is
  **5 credits**. The helper only escalates to stealth when the default proxy
  returns nothing, so non-WAF pages stay at 1 credit.
- Prefer WebFetch first for non-WAF pages where a summary is enough; reserve this
  skill for blocked/JS pages and for claims that need exact text.

## On failure

If the helper prints nothing for a URL (WAF still blocks, or
`FIRECRAWL_API_KEY` unset), **skip that URL and note the limitation** in the
calling report. Do not retry in a loop.
