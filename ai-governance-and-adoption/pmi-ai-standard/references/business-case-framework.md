# Business Case Framework and the Seven Patterns of AI

Source: PMI, *The Standard for Artificial Intelligence in Portfolio, Program, and Project Management* (June 2026), Sections 6.1–6.2.

## The seven components of an AI business case (Section 6.1)
A business case for AI in PPPM should address all seven — most people writing one only cover the first two or three:

1. **Economic benefits and ROI** — revenue, cost reduction, or productivity gains weighed against real implementation costs (training, data infrastructure, ongoing data processing) — not just license/tool cost.
2. **Decision-making improvement** — how AI will actually change what decisions get made or how fast, not just "we'll have more data."
3. **Risk management and uncertainty handling** — how AI-specific risk (see `ethics-and-hitl.md`) gets identified and mitigated, tied back to the Managing AI Risks and Uncertainties performance domain.
4. **Competitive advantage and innovation potential** — the strategic case, not just the operational one.
5. **Stakeholder engagement and change management** — the standard explicitly frames this in an ADKAR-like shape: build **a**wareness, **d**esire, **k**nowledge, **a**bility, and **r**einforcement, and pair it with realistic performance metrics and support mechanisms (training, communication plans, governance) — not just a training deck at launch.
6. **Ethics and regulatory requirements** — how the initiative meets legal/ethical standards, what the explainability (XAI) strategy is, and how resulting risks get minimized.
7. **Long-term scalability and sustainability** — including tracking sustainability KPIs (energy usage, carbon, etc.) where relevant, and treating them as continuously monitored rather than an end-of-project report.

A business case missing components 5–7 will read as technically sound but organizationally naive — those are usually the components that determine whether a leadership audience actually buys in.

## The Seven Patterns of AI (Section 6.2)
A categorization scheme for scoping *what kind of AI problem this actually is* before jumping to a solution:

- **Recognition** — identifying entities, patterns, or content in data (images, speech, documents).
- **Hyper-Personalization** — tailoring outputs/experiences to an individual.
- **Patterns and Anomalies** — detecting the normal vs. the unusual (fraud, defects, drift).
- **Conversational and Human Interaction** — chat, voice, natural-language interfaces.
- **Autonomous Systems** — agents/systems acting with some degree of independence.
- **Predictive Analytics and Decision Support** — forecasting and recommending, human decides.
- **Goal-Driven Systems** — systems oriented around achieving a defined objective, potentially adjusting their own approach to get there.

Use this to sharpen a vague "we want to use AI for X" into a specific pattern, which in turn clarifies what kind of governance and HITL tier applies (an Autonomous Systems or Goal-Driven Systems use case needs materially more oversight than a Recognition or Predictive Analytics one — see `ethics-and-hitl.md`).

## How to use this in a conversation or plan
When someone pitches an AI initiative without a business case, walk them through the seven components as questions, not a lecture: "what's the ROI case," "how does this change a decision," "what could go wrong," "why is this a competitive edge," "how do people actually adopt it," "what's the compliance story," "does this scale." When someone pitches a specific tool or capability, ask which of the Seven Patterns it actually is — it's a fast way to surface when someone is over-scoping (calling a Recognition tool an Autonomous System) or under-scoping (treating a Goal-Driven System like a simple automation).
