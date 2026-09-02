# Claude Marketing Skills

A collection of [Claude skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for marketing, media planning, writing, and AI adoption/governance work. Each skill lives in its own folder and can be installed independently — you don't need all of them.

These are generic templates, not tied to any one company. Where a skill has a company-specific "quick-start" layer (real spend, verified reps, past decisions), it ships blank so you can fill in your own — see each skill's folder for details.

## Groups in this repo

The repo is organized into four groups. Each group is a top-level folder holding one or more related skills.

| Group | What it's for |
|---|---|
| [`healthcare-trade-media-planning/`](healthcare-trade-media-planning/) | Healthcare trade publication research and media planning. |
| [`ai-governance-and-adoption/`](ai-governance-and-adoption/) | Planning and grounding AI adoption and governance work in PMI's published AI standard. |
| [`paid-media-analyst-skills/`](paid-media-analyst-skills/) | Running paid media analysis end to end, across ad platforms. |
| [`no-slop-writing/`](no-slop-writing/) | Editing, auditing, and ship-checking writing so it reads like a specific person rather than generic AI output. |

### Healthcare trade media planning

| Skill | What it does |
|---|---|
| [`healthcare-trade-media-planning/`](healthcare-trade-media-planning/) | Healthcare trade publication research and media planning: maps business groups, products, audiences, and regions to trade publishers, associations, media kits, rates, and contacts. Covers Dental, Health IT, Medical Surgical, and Biopharma/Life Sciences. |

### AI governance and adoption

Two skills over one shared framework, split by what you want out of it: `pmi-ai-standard` is advisory (think, argue, prep talking points), `ai-adoption-plan` is a deliverable generator (produces a Word document). Live in [`ai-governance-and-adoption/`](ai-governance-and-adoption/).

| Skill | What it does |
|---|---|
| [`ai-governance-and-adoption/ai-adoption-plan/`](ai-governance-and-adoption/ai-adoption-plan/) | Builds a formal, client- or leadership-ready AI adoption and governance plan as a Word document, grounded in PMI's Standard for Artificial Intelligence in PPPM. |
| [`ai-governance-and-adoption/pmi-ai-standard/`](ai-governance-and-adoption/pmi-ai-standard/) | Reference and coaching skill for grounding any AI-adoption discussion, pitch, or governance argument in PMI's actual published AI standard — not general AI-adoption folklore. |

### Paid media analyst skills

A set of 12 skills for running paid media analysis end to end — from raw platform exports to a client-ready deck. Originally built for one client's account setup, then anonymized (client, product, and account names swapped for generic placeholders like `[Client]` and `[Account: X]`) so they're safe to reuse anywhere. Live in [`paid-media-analyst-skills/`](paid-media-analyst-skills/).

Unlike the other two groups, these skills aren't drag-and-drop on their own — several depend on shared files that sit alongside them in this folder: [`prompts/`](paid-media-analyst-skills/prompts/) (the detailed agent instructions each skill runs), [`scripts/`](paid-media-analyst-skills/scripts/) (helper scripts like the QA linter and the Firecrawl fetch tool), and [`.claude/agents/`](paid-media-analyst-skills/.claude/agents/) (the QA, run-log, and memory-curator subagents `qa-review` calls). To use this set, copy the whole `paid-media-analyst-skills/` folder into your project so those shared paths stay in place, rather than pulling out a single skill folder.

| Skill | What it does |
|---|---|
| [`analyze-bing-campaigns/`](paid-media-analyst-skills/analyze-bing-campaigns/) | Analyzes Microsoft (Bing) Ads exports and flags performance issues and opportunities. |
| [`analyze-meta-campaigns/`](paid-media-analyst-skills/analyze-meta-campaigns/) | Analyzes Meta (Facebook/Instagram) ad exports and flags performance issues and opportunities. |
| [`analyze-dsp-display/`](paid-media-analyst-skills/analyze-dsp-display/) | Analyzes programmatic display (DSP) exports — line items, creative rotation, inventory mix, audience segments, and frequency. |
| [`analyze-search-campaigns/`](paid-media-analyst-skills/analyze-search-campaigns/) | Analyzes Google Search campaign exports — spend, keywords, conversions, and structural issues. |
| [`analyze-search-ad-copy/`](paid-media-analyst-skills/analyze-search-ad-copy/) | Reviews search ad copy for gaps, missed messaging, and branding consistency. |
| [`create-media-plan/`](paid-media-analyst-skills/create-media-plan/) | Builds a media plan from budget and account data. |
| [`firecrawl-scrape/`](paid-media-analyst-skills/firecrawl-scrape/) | Pulls landing page content for use in other skills (ad copy checks, landing page audits) when a site blocks normal fetching. |
| [`landing-page-audit/`](paid-media-analyst-skills/landing-page-audit/) | Checks whether landing pages actually match what the ads promise, and flags coverage gaps. |
| [`qa-review/`](paid-media-analyst-skills/qa-review/) | Reviews a finished report or deck for factual errors, formatting bugs, and unsupported claims before it goes to a client. |
| [`skill-editor/`](paid-media-analyst-skills/skill-editor/) | Helps edit and maintain the other skills in this set. |
| [`update-skill-memory/`](paid-media-analyst-skills/update-skill-memory/) | Records new lessons learned into a skill's `memory.md` so future runs improve over time. |

Each of these skills keeps a `memory.md` file — a running log of past mistakes, client corrections, and lessons learned, so the skill gets smarter the more you use it. Since these were pulled from a real client engagement, the `memory.md` files still describe realistic scenarios (just with names swapped out) — treat them as example patterns to learn from, not literal client history.

### No-slop writing

| Skill | What it does |
|---|---|
| [`no-slop-writing/`](no-slop-writing/) | Edits, audits, or pre-flights a draft (post, email, memo, landing page, deck, doc) to remove the patterns that make writing sound machine-made and the vagueness underneath them. Three modes: edit a draft, detect slop patterns without rewriting, or ship-check a near-final piece. Ships with a blank [`references/voice-profile.md`](no-slop-writing/references/voice-profile.md) you can fill in so edits match your own voice, plus [`references/eval.md`](no-slop-writing/references/eval.md) for testing the skill. |

## Installing a skill

`healthcare-trade-media-planning/` and `no-slop-writing/` are each a single skill folder, and each subfolder of `ai-governance-and-adoption/` is one too: copy the folder into your Claude client's skills directory (or however your Claude product supports custom/loaded skills), following that skill's own `SKILL.md` for setup notes. The two AI governance skills each work alone, but `ai-adoption-plan` will read `pmi-ai-standard`'s reference files for fuller framework detail when both are installed side by side — so install the pair together if you want the richer output. `paid-media-analyst-skills/` is the exception — copy the whole folder together (see that section above) so the shared `prompts/`, `scripts/`, and `.claude/agents/` files it depends on come with it.

## Getting started

1. Pick the skill(s) you want and copy that folder wherever your Claude client loads skills from.
2. Check each skill's `SKILL.md` for any "before you use this" or "adapting this skill" notes — `healthcare-trade-media-planning`, in particular, ships with bracketed placeholders (`[YOUR COMPANY]`, `[YOUR PRODUCT]`) to swap in your own details.
3. Re-verify any time-sensitive data (media kit rates, contacts, standards versions) before relying on it — these are point-in-time snapshots.

## Adding more skills

A standalone skill goes in its own top-level folder with its own `SKILL.md` + `references/`. A related group of skills (like AI governance and adoption, or paid media analyst) lives together in one top-level folder, with each skill as its own subfolder. Add a row to the relevant table above when you do.

Before adding a skill pulled from a real client engagement, anonymize it first — swap out client names, product names, account codenames, and domains for generic placeholders.

## License

MIT — see [LICENSE](LICENSE).
