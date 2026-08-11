---
name: skill-editor
description: Audit and tighten SKILL.md files. Removes AI-slop wording and em-dashes, enforces conciseness and progressive disclosure, and verifies every instruction is clear and actionable for a human. Use when the user asks to review, clean up, tighten, audit, or edit a skill, or types /skill-editor. Proposes before/after rewrites and applies them only after you approve.
argument-hint: "[optional: skill name or path to audit; defaults to all skills under .claude/skills/]"
allowed-tools: Read, Edit, Grep, Glob, Write
---

# Skill Editor

Audit a SKILL.md and tighten it: cut AI slop, enforce conciseness and progressive
disclosure, and make every instruction clear and actionable. Propose the edits
first, then apply them only after the user approves.

## Check Memory First

Before running, read `memory.md` in this skill's folder for the editing standard and
past feedback. Apply anything relevant, and add a dated entry at the end of the run
if a new preference surfaces.

## What You Receive as Arguments

- `$ARGUMENTS`: a skill name (for example `qa-review`) or a path to a SKILL.md. Empty
  means audit every `SKILL.md` under `.claude/skills/`.

## What good looks like

A SKILL.md passes when it:

- States what it does and when to use it in the first few lines.
- Keeps the high-level flow at the top and pushes deep mechanics into numbered steps
  or the referenced `prompts/<platform>/agent_*.md` spec.
- Gives imperative, specific instructions a human can follow without guessing.
- Has no AI-slop words, no em-dashes, and no repeated sentence shapes.
- Includes the "Check Memory First" pointer to its `memory.md`.

## Step 1: Scope

Resolve the target file(s) with Glob (`.claude/skills/*/SKILL.md`, or the one named
in `$ARGUMENTS`). Read each file in full before judging it.

## Step 2: Audit against three checks

### Check 1: Cut AI slop

Flag filler words (this list is not exhaustive): leverage, delve, utilize, robust,
seamless, holistic, foster, realm, embark, unleash, unlock, elevate, supercharge,
cutting-edge, game-changer, testament, pivotal, crucial, vital, comprehensive (when
it adds nothing), moreover, furthermore, "it's worth noting", "when it comes to".
Flag repeated sentence shapes (every line opening the same way, "Not only X but also
Y", rule-of-three triads). Replace every em-dash (the U+2014 long dash) with a comma,
period, colon, or parentheses, based on how the clauses relate.

- Slop, before: "Leverage this skill to seamlessly delve into a comprehensive analysis."
- Slop, after: "Use this skill to analyze the data."
- Em-dash, before: "Run the pipeline — it builds the report — then commit."
- Em-dash, after: "Run the pipeline. It builds the report, then commit."

### Check 2: Concise and progressively disclosed

The top of the file states what and when plus the high-level steps; deep mechanics
live in the steps or the agent spec. Flag detail re-inlined from a
`prompts/<platform>/agent_*.md` spec, long preambles, and any step that repeats what
another step already covered.

- Before: 25 inline lines of CSV encoding edge cases sitting in the intro.
- After: "Load the file (Step 1 covers UTF-16 LE and quoted-comma parsing)," with the
  detail living in Step 1.

### Check 3: Clear and actionable

Every instruction is imperative and specific. Flag vague hedges ("should probably",
"as needed", "if appropriate") and replace each with a concrete action plus its
condition.

- Before: "Data should probably be validated first."
- After: "Validate the data: confirm the required columns exist. If any are missing,
  stop and tell the user which."

## Step 3: Propose

For each file, present a short findings report grouped by the three checks. Each
finding is one line: the issue, the before text, and the after text. If a file is
already clean, say so and move on.

## Step 4: Apply on approval

After the user approves, apply the edits with Edit. Preserve the frontmatter fields,
the meaning, the behavior, and every code block and command. Re-scan the file and
repeat until it is clean.

## Important Notes

- Change wording, structure, and clarity only. Never change what a skill does.
- Keep all required frontmatter (`name`, `description`, `argument-hint`,
  `allowed-tools`) and all commands and code intact.
- `memory.md` files are out of scope; audit `SKILL.md` only.
- This skill's own SKILL.md follows these rules. Use it as a reference for the target
  style.
