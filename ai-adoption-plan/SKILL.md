---
name: ai-adoption-plan
description: Builds a formal, client- or leadership-ready AI adoption and governance plan as a Word document (.docx) from whatever context exists about a real or prospective AI initiative — call transcripts, notes, existing research, a described business problem. Grounded in PMI's Standard for Artificial Intelligence in PPPM (8 principles, 5 performance domains, business-case framework, Human-in-the-Loop tiering). Use this whenever the user asks to "build an AI adoption plan," "write up a governance model," "turn this research into a proposal/plan doc," "create a rollout plan for [an AI tool/initiative]," or uploads transcripts/notes about an AI initiative and wants a structured plan or proposal produced from them — as opposed to just talking through the ideas (for that, use the pmi-ai-standard skill instead).
---

# AI Adoption Plan Generator

Produces a structured AI adoption/governance plan document, grounded in PMI's AI standard, for a specific real or prospective initiative. This is a *deliverable* skill — the output is a file, not a conversation. If the user just wants to think through an approach or prep talking points rather than get a document, that's the `pmi-ai-standard` skill's job instead; the two share the same underlying framework so there's no conflict in switching between them.

## Workflow

1. **Gather the actual inputs.** Before drafting anything, make sure you have: what the initiative is (a tool, a capability, a rollout), who it's for for (a client, an internal team), and whatever existing material describes it — transcripts, prior research docs, notes on current AI usage, stated goals or constraints. If a project or session already contains relevant material (prior research, an existing cadence doc, interview notes), use it — don't re-derive from scratch what's already been worked out. If the inputs are thin, ask the user directly rather than inventing specifics; a plan with honestly-flagged gaps is more useful than one with confident placeholders.

2. **Read `references/section-templates.md`** for the six-section structure and what each section needs to cover. If the `pmi-ai-standard` skill is also installed (check for a sibling directory, typically `../pmi-ai-standard/`), read its reference files for the fuller framework detail — `principles.md`, `performance-domains.md`, `lifecycle-and-tailoring.md`, `business-case-framework.md`, and `ethics-and-hitl.md` — rather than relying only on the condensed version in `section-templates.md`.

3. **Draft the six sections** as markdown first: Business Case, Use-Case Scope, Governance Model, HITL Tiering, Adoption Cadence, Risks and Open Questions — plus a half-page executive summary at the top. Write every section for two readers at once: a leadership audience that will skim for the decision, and a team audience that has to execute the specifics. Concretely, that means:
   - No PMI/framework term appears without a plain-language gloss the first time it's used — **including inside the executive summary itself.** It's easy to gloss terms in the body sections and forget the summary is often the only part a leadership reader actually reads; if "HITL" or "performance domain" shows up in the summary before it's explained, add the gloss right there rather than assuming the reader will get to the later section that defines it.
   - Every recommendation has an owner, a cadence, or a concrete next step attached — not just a description.
   - Tables for anything tabular (HITL tiers, meeting cadence, RACI-style ownership) — tables read faster for both audiences than prose.
   - The executive summary stands alone: someone who reads only that page should understand the recommendation, the governance approach, and what's being asked of them.

4. **Build the actual .docx file using the `docx` skill's conventions.** Don't hand-roll Word formatting — read that skill's SKILL.md for the mechanics once content is ready. Structure: title page or header, executive summary, then the six sections in order, with a table of contents if the document runs long.

5. **Name the file and deliver it** clearly tied to the initiative (e.g., `[Client/Initiative]-AI-Adoption-Plan.docx`), and briefly tell the user what's in it and where any gaps or assumptions are — don't let a confidently-formatted document imply more certainty than the inputs actually support.

## What "good" looks like
A leadership reader should be able to approve or push back after reading the executive summary alone. A team member should be able to open the HITL tiering table and the adoption cadence section and know exactly what they're responsible for and when. If either of those isn't true, the draft isn't done — go back and cut abstraction, add specifics, or restructure before delivering.
