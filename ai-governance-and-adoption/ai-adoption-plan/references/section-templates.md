# AI Adoption Plan — Section Templates

Six sections, each grounded in a specific part of PMI's *Standard for Artificial Intelligence in PPPM* (June 2026). If the `pmi-ai-standard` skill's reference files are available (typically at `../../pmi-ai-standard/references/`, i.e. a sibling of this skill's own folder), read the relevant one before drafting each section — that's where the fuller framework detail lives. This file is a self-contained fallback with enough summary to draft a reasonable plan even without it.

For every section: write for two audiences at once — a leadership reader who will skim, and a team reader who has to actually execute. That means a plain-language framing sentence or two before any framework terminology, and concrete specifics (names, tiers, cadences, owners) rather than abstractions once the framing is set. Never introduce a PMI term (e.g., "Performance Domain," "HITL tiering") without a one-clause plain-English gloss the first time it appears in the document.

## 1. Business Case
Cover, briefly, all seven components from the standard's business-case framework (Section 6.1): economic benefit/ROI, decision-making improvement, risk management, competitive advantage, stakeholder engagement & change management, ethics/regulatory, and long-term scalability. Most drafts over-index on ROI and under-cover the change-management and ethics components — don't repeat that mistake. Keep this section to what a leadership audience needs to approve or fund the initiative; save execution detail for later sections.

## 2. Use-Case Scope
Name the specific business problem, then categorize it using the Seven Patterns of AI (Recognition, Hyper-Personalization, Patterns and Anomalies, Conversational and Human Interaction, Autonomous Systems, Predictive Analytics and Decision Support, Goal-Driven Systems). Being specific about the pattern here is what makes the governance model in Section 4 non-generic — an Autonomous Systems or Goal-Driven Systems use case needs a materially different HITL tier structure than a Recognition or Predictive Analytics one, and the document should make that connection explicit rather than leaving the reader to infer it.

## 3. Governance Model
Map the initiative onto the 8 principles and 5 performance domains — not as a checklist recitation, but as a short paragraph per principle/domain that says what it means *for this specific initiative*. State clearly who owns each performance domain (a name or role, not "the team"). This is the section most likely to get skimmed by executives and picked apart by the team that has to run it — so lead with a one-paragraph plain-language summary of "how this will be governed" before the principle-by-principle detail.

## 4. HITL Tiering
A concrete, reversibility-based tier table — not a narrative description. Suggested default shape (adjust tier count/definitions to the actual initiative):

| Tier | Definition | Example action | Approval |
|---|---|---|---|
| 0 — Read-only | No system state changes | Reporting, research, diagnostics | None — log only |
| 1 — Reversible | Acts, but effects can be undone | Drafts, edits to paused/inactive items | Human reviews async, logged |
| 2 — External/spend-affecting | Effects reach outside the system or affect budget | Activating live changes | Human approval queue with SLA |
| 3 — Irreversible/high blast radius | Effects can't be easily undone or reach clients/brand | Large budget shifts, client-facing changes | Mandatory pre-approval, consider two-person sign-off |

Ground the framing in the standard's own logic: HITL is described as both a safeguard *and* a distinct source of value (judgment, context, ethics AI can't supply) — not purely a risk control, which is a more persuasive framing to skeptical stakeholders than "we don't trust the tool yet." Note explicitly that AI confidence is not the same as low stakes — reversibility, not confidence, should gate whether an action needs approval.

## 5. Adoption Cadence
This section is about people, not technology — where the People and Culture principle and the Managing Stakeholder Expectations performance domain become an operational rhythm. Include, concretely: a champion/peer-advocate model with a defined ratio (e.g., one champion per ~15-30 people) and bounded time commitment; a standing meeting cadence (what happens weekly vs. biweekly vs. monthly vs. quarterly, and why each falls where it does — tie this back to the life-cycle tailoring logic: predictive phases can run on a slower cadence, adaptive phases need a tighter one); and the specific quick-win use case(s) that will build early trust. If prior research on the initiative already exists (e.g., transcripts, an existing cadence doc), fold its concrete recommendations in here rather than re-deriving them generically.

## 6. Risks and Open Questions
Work from the standard's ethical-challenge areas — bias, accountability, transparency, data security, hallucination, privacy/consent, traceability, overreliance, regulatory exposure — and flag which ones are live risks for *this* initiative specifically, rather than listing all fourteen when only four are relevant. Close with genuinely open questions rather than manufactured ones; a plan that pretends to have no open questions reads as less credible to both a technical team and a skeptical executive. The full fourteen-area list, with framing for each, is in `../../pmi-ai-standard/references/ethics-and-hitl.md` when that skill is installed alongside this one.

## Document-level guidance
- Lead with a half-page executive summary before Section 1 — the single most important thing for a leadership reader, and the thing most drafts skip or bury.
- Use tables for anything tabular (the HITL tiers, the cadence rhythm, an owner list) rather than prose paragraphs — this is what makes a document usable by a team, not just readable by an executive.
- Build the actual file using the `docx` skill's conventions once content is drafted — don't hand-roll document formatting.
