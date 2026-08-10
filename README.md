# afllewellyn-claude-marketing-skills

A collection of [Claude skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for marketing, media planning, and AI adoption/governance work. Each skill lives in its own folder and can be installed independently — you don't need all of them.

These are generic templates, not tied to any one company. Where a skill has a company-specific "quick-start" layer (real spend, verified reps, past decisions), it ships blank so you can fill in your own — see each skill's folder for details.

## Skills in this repo

| Skill | What it does |
|---|---|
| [`healthcare-trade-media-planning/`](healthcare-trade-media-planning/) | Healthcare trade publication research and media planning: maps business groups, products, audiences, and regions to trade publishers, associations, media kits, rates, and contacts. Covers Dental, Health IT, Medical Surgical, and Biopharma/Life Sciences. |
| [`ai-adoption-plan/`](ai-adoption-plan/) | Builds a formal, client- or leadership-ready AI adoption and governance plan as a Word document, grounded in PMI's Standard for Artificial Intelligence in PPPM. |
| [`pmi-ai-standard/`](pmi-ai-standard/) | Reference and coaching skill for grounding any AI-adoption discussion, pitch, or governance argument in PMI's actual published AI standard — not general AI-adoption folklore. |

## Installing a skill

Each folder is a self-contained skill: copy it into your Claude client's skills directory (or however your Claude product supports custom/loaded skills), following that skill's own `SKILL.md` for setup notes.

## Getting started

1. Pick the skill(s) you want and copy that folder wherever your Claude client loads skills from.
2. Check each skill's `SKILL.md` for any "before you use this" or "adapting this skill" notes — `healthcare-trade-media-planning`, in particular, ships with bracketed placeholders (`[YOUR COMPANY]`, `[YOUR PRODUCT]`) to swap in your own details.
3. Re-verify any time-sensitive data (media kit rates, contacts, standards versions) before relying on it — these are point-in-time snapshots.

## Adding more skills

New skills go in their own top-level folder with their own `SKILL.md` + `references/`. Add a row to the table above when you do.

## License

MIT — see [LICENSE](LICENSE).
