# Memory: firecrawl-scrape

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-05-26: WAF 403s are a fingerprint or IP problem, not a content problem ([Client])
WebFetch and any datacenter-IP browser (including the sandbox) get blocked by [Client]-class WAFs; the fix is a managed scraper with residential or stealth proxies, which is exactly this skill. If Firecrawl also returns nothing, skip the URL and note the limitation. Do not retry.

## Standing preferences (apply every run)

- **`FIRECRAWL_API_KEY` lives in the Claude Code environment config** (never the repo), and `api.firecrawl.dev` must be in `sandbox.network.allowedDomains`. Both apply at session start, so after adding the key or editing the allowlist, start a fresh session or the sandbox returns `403 x-deny-reason: host_not_allowed` and the key reads as unset.
- **The helper escalates the default proxy (1 credit) to stealth (5 credits) only on failure**, so non-WAF pages stay cheap; it never raises (it returns None, so skip and note).
- **Scope is scrape-only** (single, known URLs), not crawl or site mapping.
