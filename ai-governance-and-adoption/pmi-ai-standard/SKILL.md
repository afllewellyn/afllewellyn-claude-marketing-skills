---
name: pmi-ai-standard
description: Grounds any discussion, pitch, plan, or piece of writing about AI adoption, AI governance, or an AI-enabled initiative in PMI's official Standard for Artificial Intelligence in Portfolio, Program, and Project Management (June 2026) — its 8 principles, 5 performance domains, life-cycle tailoring guidance, business-case framework, and Human-in-the-Loop/ethics model. Use this whenever the user is preparing for a conversation about rolling out AI, defending an AI governance or approval model, building an AI business case, prepping for an interview or leadership call about AI strategy, or checking whether an AI plan or argument actually holds up against a real standard rather than general intuition — even if the user doesn't mention PMI or "the standard" by name. Also use it to catch claims that get attributed to PMI but aren't actually supported by the standard's primary text.
---

# PMI AI Standard — Coaching and Reference Skill

This skill exists so that AI-adoption conversations are grounded in PMI's actual published standard instead of reconstructed from memory or general AI-adoption folklore each time. It is a *reference and coaching* skill, not a document generator — the default mode is advisory: help the user think, argue, or write more precisely using the standard's own framework. (For producing an actual formal plan document, see the separate `ai-adoption-plan` skill, which reuses these same reference files.)

## How to use this skill

1. **Figure out what the user actually needs.** Common shapes: "does my plan/argument hold up," "how do I defend X to a skeptical audience," "what would this standard say about Y," "help me prep talking points," "write this up." Don't default to dumping the whole framework — pull only the reference file(s) relevant to what's being discussed.

2. **Load the relevant reference file(s).** Don't load all of them by default — that defeats the point of keeping this skill lightweight. Pick based on the topic:
   - `references/principles.md` — the 8 principles (Strategic Value, Risk, Governance and Compliance, People and Culture, Ethics and Professional Responsibility, Stakeholder Engagement, Optimization and Innovation, Data Quality). Use for "does this plan cover the bases" or "what's the PMI-correct name for this concern."
   - `references/performance-domains.md` — the 5 performance domains (Managing Stakeholder Expectations, Defining Scope, Designing Architecture, Executing Strategic Goals, Managing Risk). Use for "who owns what" or diagnosing why an initiative is struggling.
   - `references/lifecycle-and-tailoring.md` — the AI life cycle and predictive/adaptive/hybrid tailoring guidance. Use for cadence questions — how fast should this move, should this phase be agile or plan-driven.
   - `references/business-case-framework.md` — the seven-component business case model and the Seven Patterns of AI use-case categorization. Use for "how do I pitch this" or "what kind of AI problem is this actually."
   - `references/ethics-and-hitl.md` — Human-in-the-Loop as both safeguard and value source, plus the standard's ethical challenge areas. Use for governance/approval-model questions and ethics objections.

3. **Answer using the standard's actual framing**, citing the specific principle, domain, or section by name (e.g., "this is a Governance and Compliance gap" or "Section 6.1's stakeholder engagement component"). Precision here is the whole value proposition of this skill over generic advice — vague appeals to "AI best practices" are exactly what this skill is meant to replace.

4. **Flag scope carefully.** The standard supports "continuous," "iterative," and hybrid predictive/adaptive tailoring — but it does **not** explicitly prescribe a weekly/biweekly cadence or say AI governance must beat quarterly/annual review cycles. If the user (or a source they're drawing from) attributes that sharper cadence claim to PMI, correct it: that argument is better sourced to change-management research (e.g., Prosci, MIT CISR) layered on top of PMI's iterative framing, not to PMI's primary text directly. Getting this distinction right is part of what makes this skill trustworthy — don't let enthusiasm for a good argument outrun what the source actually says.

5. **When the user wants something written** (talking points, a short brief, a response to a stakeholder), write it directly, keep it concise, and make sure it would hold up if someone who has actually read the standard pushed back on it.

6. **For "defend this to a skeptical audience" requests specifically, prefer a rehearsed-exchange format over a single narrative answer.** Structure it as a short set of "If they say X, respond Y" pairs covering the pushback most likely to actually come up, each answer kept to a few sentences. This has consistently tested as more usable prep than one long persuasive essay — it's what someone can actually rehearse and recall in the room, and it forces each individual answer to stay sharp rather than let a good opening argument coast through the rest. Lead with whichever single sentence is the most load-bearing one to remember, stated plainly, before the exchange pairs.

## Style
Match the register of what's being prepared. Interview or leadership-call prep should sound like something a confident, well-read practitioner would say out loud — not like a citation list. A written brief can be more structured. Either way, avoid stacking every principle and domain into one answer just because they're all technically relevant; pick the two or three that actually resolve the question in front of you.
