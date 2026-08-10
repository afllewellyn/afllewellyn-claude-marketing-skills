# Memory: analyze-search-ad-copy

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-07-08: Re-verify this skill's own export scoping even after a sibling report's scoping bug is fixed ([Account: MedSurg])
A whole-account-vs-in-scope-campaigns scoping fix applied to search_audit does not automatically apply to this skill's ad_copy_audit output. The 2026-06-14 [Account: MedSurg] "display paths resolved" claim had been computed against an unfiltered 52-ad-group whole-account export and stayed wrong (15 of 31 ad groups were actually still missing Path 2) until a 2026-07-08 refresh recomputed it against the correctly-scoped file. Independently confirm this skill loaded the same in-scope-campaign file the other agents used before reporting a display-path or structural finding as resolved; see `analyze-search-campaigns/memory.md` for the fuller scoping-propagation lesson.

### 2026-06-16: Ground copy in the landing page's actual value props ([Account: IWFB])
Write headlines and descriptions to the LP's real value props, not a generic angle. The bottled-water-filtration LP sells on cost, filter life, throughput, fewer changeouts and regulatory compliance (spring-water case study: 180% throughput, 20x cost cut, [Former Parent Co] High Flow 0.5µm) — write to that, not generic "taste/clarity," and use the case studies as ad proof points.

### 2026-06-03: Headline-keyword alignment is "materials, not devices" ([Account: MedTech])
Align headlines to the product reality: [Client] supplies diagnostic materials (tapes, films, adhesives, membranes), not finished devices, so device-intent headlines mismatch the offer. When the user (the account expert) corrects the product framing, re-scope the copy recommendations to match.

### 2026-05-26: Build a Detailed Description Library; copy defects stay agency-side ([Account: MOEM])
On user request ("more detailed vs differentiated descriptions"), build a library of differentiated 90-character-or-fewer description lines grounded in landing-page proof rather than reusing one generic line. Copy defects (a "[Client]" misspelling in a live headline, "How Can [Former Parent Co] Help You?" on a [Client] hero, headlines referencing applications absent from the page) are agency-side housekeeping to fix in-flight, not exec-deck findings.

### 2026-05-24: Do not rewrite brand copy during the [Acquiring Co] transition ([Account: MOEM])
Copy currently mixes [Former Parent Co], [Client], and [Product F]; normalization is deferred because the [Client] to [Acquiring Co] transition is pending and product names stay unchanged for legal reasons. Do not recommend brand-copy rewrites or branded builds for [Account: MOEM].

### 2026-05-06: Branded copy opportunity is a standalone slide when it touches more than two ad groups ([Account: HIS])
When the H1-pinning plus brand-transition play spans more than two ad groups ([Account: HIS] hit six), break it out as a dedicated slide with an examples table (top term, clicks, current H1, recommended H1), not a buried recommendation bullet. Pair it with a forward `/landing-page-audit` follow-up to close the loop.

### 2026-05-05: [Client] branding now lands in RSAs; display paths still empty ([Account: MedTech])
The branding ask is working ([Account: MedTech] RSAs went from 0% to 96% carrying [Client] language), but 100% of RSAs still have empty display URL paths (Path 1 and Path 2 are "--"), so re-raise that as a free CTR signal. Most ad groups still run a single RSA with no within-group rotation or testing.

## Standing preferences (apply every run)

- **Single-RSA and empty display paths are agency housekeeping.** Fix proactively in-flight (a second RSA per ad group is an ad-strength and rotation best practice; populated paths are a free CTR lift). Surface in an exec deck only when there is a structural blocker (for example the client locks creative approval); default to the appendix.
- **Report headers need an Agent/spec attribution line.** Every report `.md` header needs an `**Agent:** Agent N <name> (prompts/<platform>/<spec>.md)` line, not just a data-source line, or the QA linter flags it.
- **Ad copy is in the Google SEM export** (Headline 1-15 plus Description 1-5 columns). Dedupe ad copy by (Campaign, Ad group, headline set) before counting single-RSA ad groups, since ad-level monthly exports repeat each RSA once per month and overstate the raw count.
