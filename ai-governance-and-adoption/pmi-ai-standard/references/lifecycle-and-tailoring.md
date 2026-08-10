# AI Life Cycle and Tailoring

Source: PMI, *The Standard for Artificial Intelligence in Portfolio, Program, and Project Management* (June 2026), Chapter 4.

## The baseline AI life cycle
Initiation and Planning → Data Collection and Preparation → Model Development → Deployment → Monitoring and Evaluation → Optimization and Iteration → End-of-Life and Decommissioning.

This is presented as a *baseline to tailor*, not a rigid sequence — practitioners are explicitly told to adjust it for local context. It's mapped onto the standard portfolio, program, and project life cycles (Initiating/Planning/Executing/Monitoring & Controlling/Closing, etc.) so AI work has clear intersection points with normal PPPM governance rather than running as a shadow process.

## Predictive, adaptive, and hybrid ways of working (Section 4.1)
The standard's core tailoring guidance: match the method to the phase, not to a house style.
- **Predictive/plan-driven** fits phases with extensive up-front planning and low change likelihood — defining objectives, setting up compliance structures.
- **Adaptive** fits phases needing flexibility, iteration, and rapid feedback — model development and optimization especially.
- **Hybrid** is what most consequential AI initiatives actually need: predictive milestones give experimentation and research phases room to work without stalling the wider program, while adaptive short-cycle iteration handles the parts of the work — especially deployment and operation — that need to respond to what's actually being learned.

## What this means in practice
When someone asks "should this be run like a normal quarterly-cadence project or something faster," the honest, PMI-grounded answer is: neither, uniformly — tailor phase by phase. Front-loaded phases (initiation, compliance setup) can stay predictive; anything touching model behavior, deployment, or optimization benefits from adaptive, short-cycle iteration. This is a more defensible position in a conversation than "AI always needs weekly cadence," which overstates what the standard itself says (see the caveat in `../SKILL.md`).

## Practical checklist for tailoring a new AI initiative
- Which life-cycle phase is this actually in right now? (Not "AI project" generically — which of the seven phases.)
- Does this phase have well-defined, low-volatility requirements (→ predictive) or does it need iteration and fast feedback (→ adaptive)?
- Where are the intersection points with the portfolio/program/project's normal governance cadence, and does the AI life cycle phase line up with them or run ahead/behind?
- Has anyone explicitly decided the hybrid split, or did the team default to "adaptive because AI" or "predictive because that's how we run everything else" without checking?
