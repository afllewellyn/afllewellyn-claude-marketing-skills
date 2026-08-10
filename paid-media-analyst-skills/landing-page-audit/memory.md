# Memory: landing-page-audit

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-06-21: Firecrawl now fetches both [Account: MOEM] LPs; coverage gaps still open ([Account: MOEM])
Firecrawl now fetches both [Account: MOEM] LPs live (the [Client] WAF still 403s WebFetch). All prior coverage gaps remain open: Medical hemodialysis zero coverage, and Industrial Food & Beverage plus Microelectronics zero coverage. The hemodialysis exact-match terms were bulk-paused Jun 18, which strengthens the "structure an ad group around the LP's named products" case rather than resolving it.

### 2026-06-17: Firecrawl fetched the surgical-solutions LPs; both still lead with [Former Parent Co] ([Account: MedSurg])
Firecrawl (`scripts/firecrawl_fetch.py`) fetched the [Client] surgical-solutions LPs (bair-hugger, skin-and-nasal) that WebFetch 403s. The pages confirmed strong keyword scent (core temperature monitoring / normothermia; preoperative nasal decolonization / SSI / povidone-iodine), which supported the net-new keyword recs. Both LPs still lead with "[Former Parent Co]" branding, so the on-page transition is pending.

### 2026-06-16: Dedicated bottled-water LP fetched past the WAF; ground copy in its language ([Account: IWFB])
A dedicated bottled-water LP is live (`/purification-filtration/manufacturing/lp/bottled-water-filtration/`) and Firecrawl (firecrawl-scrape) fetched it past the [Client] WAF this session. When grounding ad copy or keyword themes, read the LP's actual value-prop language (cost / filter life / throughput here) and match it, and use the LP's case studies as ad proof points (a spring-water site lifted throughput 180%).

### 2026-05-28: Check ad-to-page scent on promo campaigns ([Account: Dental])
A Q2 Warmer promo ad drove to a generic "Explore [Client]'s Dental Solutions" lead form with no Q2 promo content, so the ad-to-page scent was broken. Two cheap fixes: add the offer language to the landing page, and add a sitelink announcing the promo so no new campaign is needed.

### 2026-05-26: Application-coverage gaps are exec-worthy; copy defects are not ([Account: MOEM])
The exec-deck rule: landing-page application-coverage gaps (whole page sections with zero ad coverage, for example Medical hemodialysis or Industrial Food and Beverage) are exec-deck-worthy, while copy defects (misspelling, broken ad-to-page scent) stay agency-side housekeeping. When the WAF blocks fetching, the user can paste page text into chat; two landing pages served the entire [Account: MOEM] program. On user request, build differentiated descriptions grounded in on-page proof.

## Standing preferences (apply every run)

- **[Client] and similar WAF sites return HTTP 403 to WebFetch** (a datacenter-IP fingerprint). Fall back to `python scripts/firecrawl_fetch.py "<url>"` (the `firecrawl-scrape` skill); env vars and `allowedDomains` apply at session start, so a fresh session may be needed.
- **Cap at 15 URLs per run**, prioritize by click volume, strip tracking params (`?cid=`, `?utm_*`) before de-duplicating, and use the `Final URL` column (clean), not `Ad final URL`.
- **3-type gap analysis:** Gap A (ad claims not on page), Gap B (page messaging not in ads), Gap C (keywords absent from the landing page).
