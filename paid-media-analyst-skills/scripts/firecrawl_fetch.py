"""Fetch a web page through Firecrawl's hosted scraper (WAF/JS fallback).

Used by the `landing-page-audit` skill as a fallback when WebFetch is blocked
by a bot-management WAF (HTTP 403) or the page is JS-rendered. WebFetch and
the sandbox both run from a datacenter IP that [Client]-class WAFs reject;
Firecrawl runs the headless browser + residential/stealth proxies on its own
infrastructure, so the origin sees a real residential browser.

Requires the FIRECRAWL_API_KEY environment variable (set in the Claude Code
environment config — never committed). The sandbox must allow egress to
`api.firecrawl.dev` (see `.claude/settings.json` → sandbox.network.allowedDomains).

Provider-agnostic surface: callers use `fetch_page(url)` only, so swapping the
scraping provider later is a one-function change inside this module.

Credit model (Firecrawl): a normal scrape is 1 credit; the stealth-proxy retry
that defeats a WAF is 5 credits. We only escalate to stealth when the default
proxy fails, so non-WAF pages stay at 1 credit.

Usage:
    from scripts.firecrawl_fetch import fetch_page
    markdown = fetch_page("https://example.com/page")  # -> str | None

CLI:
    python scripts/firecrawl_fetch.py <url> [<url> ...]
    # one URL  -> prints the page markdown to stdout
    # many URLs -> writes /tmp/firecrawl_<slug>.md per page, prints "<url>\t<path>"
"""

import os
import re
import sys

import requests

API_URL = "https://api.firecrawl.dev/v2/scrape"
ENV_KEY = "FIRECRAWL_API_KEY"


def _scrape(url, api_key, *, proxy=None, timeout=60):
    """Single Firecrawl /v2/scrape call. Returns the page content (markdown
    preferred, HTML fallback) on success, or None. Never raises."""
    payload = {
        "url": url,
        "formats": ["markdown", "html"],
        "onlyMainContent": True,
    }
    if proxy:
        payload["proxy"] = proxy
    try:
        resp = requests.post(
            API_URL,
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )
    except requests.RequestException as exc:
        print(f"firecrawl: request error for {url}: {exc}", file=sys.stderr)
        return None

    if resp.status_code != 200:
        # 401/403/429/5xx etc. — surface the code (not the body, which may echo the key)
        print(f"firecrawl: HTTP {resp.status_code} for {url}", file=sys.stderr)
        return None

    try:
        data = (resp.json() or {}).get("data") or {}
    except ValueError:
        return None
    content = data.get("markdown") or data.get("html")
    return content or None


def fetch_page(url, *, timeout=60):
    """Fetch `url` via Firecrawl, returning page markdown (HTML fallback) or None.

    Tries the default proxy first (1 credit); if that yields nothing, retries
    once with the stealth residential proxy (5 credits) that beats most WAFs.
    Returns None on any failure — callers should treat None as "skip + note",
    never as an exception.
    """
    api_key = os.getenv(ENV_KEY)
    if not api_key:
        print(
            f"firecrawl: {ENV_KEY} is not set — cannot fetch {url}. "
            "Set it in the Claude Code environment config.",
            file=sys.stderr,
        )
        return None

    content = _scrape(url, api_key, timeout=timeout)
    if content:
        return content
    # Escalate to the residential stealth proxy for WAF-protected / blocked pages.
    return _scrape(url, api_key, proxy="stealth", timeout=timeout)


def _slug(url):
    return re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")[:80] or "page"


def main(argv):
    urls = argv[1:]
    if not urls:
        print(f"usage: {argv[0]} <url> [<url> ...]", file=sys.stderr)
        return 2

    failures = 0
    for url in urls:
        content = fetch_page(url)
        if content is None:
            print(f"firecrawl: FAILED {url}", file=sys.stderr)
            failures += 1
            continue
        if len(urls) == 1:
            print(content)
        else:
            path = f"/tmp/firecrawl_{_slug(url)}.md"
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            print(f"{url}\t{path}")
    return 1 if failures and failures == len(urls) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
