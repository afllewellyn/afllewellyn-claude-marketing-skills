# Memory: landing-page-audit

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-10-16: Jev guardrails and exact-text fetches
Never report a Gap A "contradicted" unless the page text itself contains the conflicting figure, and run literal checks with word boundaries (`\bAI\b`, since "ai" matches "said"). Treat Jev judgments below about 0.5 confidence, or with a split distribution, as PARTIAL rather than a finding. WebFetch summaries can drop figures and acronyms, so fetch full text with Firecrawl when a claim depends on an exact figure or word.

