---
name: qa-review
description: Quality-check generated paid-media deliverables before commit and capture the run into CLAUDE.md. Runs the qa-reviewer subagent (forbidden colors/words, currency blending, fabricated campaign labels, total reconciliation, deck geometry) then the run-log-curator subagent (drafts the Analysis Run Log row + deduped Session Learnings). Use this whenever an analysis run has produced files in outputs/, when the user asks to QA / proofread / sanity-check outputs, or when /qa-review is typed.
argument-hint: "[optional path(s) to specific deliverables; defaults to files changed this session]"
allowed-tools: Read, Bash, Grep, Glob, Task
---

# QA Review & Run-Log Curation

Post-analysis quality gate. Advisory — it reports findings and proposes CLAUDE.md
updates; it does not block writes or auto-edit CLAUDE.md.

## Check Memory First

Before running this skill, read `memory.md` in this skill's folder. It holds past
user feedback, stylistic preferences, and campaign-analysis insights specific to
this skill. Apply anything relevant to the current task. If the run surfaces a new
skill-specific lesson, add a dated entry to `memory.md` at the end.

## Step 1: Scope the review

- If `$ARGUMENTS` names files, review those.
- Otherwise default to deliverables changed this session:

```bash
git status --porcelain outputs/ ; git diff --name-only HEAD -- outputs/
```

If nothing changed under `outputs/`, say so and stop.

## Step 2: Run the QA reviewer

Invoke the **`qa-reviewer`** subagent (via the Task tool) on the scoped files.
It runs `scripts/qa_lint.py` for the mechanical checks, then applies judgment
(fabricated labels vs. the source export, currency-footnote adequacy, total
reconciliation incl. the Bing Total-row bug, deck structure, narrative-vs-numbers).
Relay its prioritized findings to the user.

## Step 3: Run the Run-Log curator

Invoke the **`run-log-curator`** subagent (via the Task tool). It drafts the new
**Analysis Run Log** top row and proposes deduped **Session Learnings** entries
for CLAUDE.md. Present the draft for the user to confirm before applying.

## Step 3.5: Sync per-skill memory

Invoke the **`memory-curator`** subagent (via the Task tool). Pass it `incremental`
mode plus this session's user feedback and the new CLAUDE.md learnings from Step 3. It
routes each durable, skill-specific lesson to the matching
`.claude/skills/<skill>/memory.md` and auto-writes deduped dated entries. Relay its
per-skill summary.

## Step 4: Apply confirmed CLAUDE.md edits

If the user confirms the Step 3 draft this turn, apply the Run Log row and Session
Learnings to `CLAUDE.md` now, before the Step 5 sentinel write, so the sentinel
post-dates the edit. If confirmation is still pending, leave `CLAUDE.md` untouched and
apply the edits in a later turn (see the Step 5 note).

## Step 5: Record that QA and memory ran

Write the session sentinels as the last action, after any `CLAUDE.md` edits applied in
Step 4, so the Stop hooks (`qa-gate.sh` and `memory-gate.sh`) know the review and memory
sync happened this session and will allow the session to end:

```bash
mkdir -p .claude && date +%s | tee .claude/.qa-last-run > .claude/.memory-last-run
```

If you apply the confirmed `CLAUDE.md` edits in a later turn instead, re-run this command
at the end of that turn. Otherwise the edited `CLAUDE.md` is newer than `.memory-last-run`
and `memory-gate.sh` blocks the session again over learnings the curator already
processed.

## Step 6: Summarize

```
## QA Review Complete

### qa-reviewer findings
[blocking / nits / verified clean / reconciliation]

### Proposed CLAUDE.md updates
[Run Log row + Session Learnings additions — apply after user confirms]

### Per-skill memory
[memory-curator summary: entries written / updated / skipped per skill]

### Next
[Apply any still-pending CLAUDE.md edits, re-stamp the Step 5 sentinels, then commit.]
```

## Important Notes
- **Advisory, not blocking** — surface findings; the user decides what to fix.
- **The curator proposes; it does not write CLAUDE.md.** Apply its draft only
  after the user confirms (CLAUDE.md is the system-of-record).
- **Never blend CAD and USD** in any total — always a per-table conversion footnote.
- **Never use "waste" or "consider"** in deliverables (reframe as efficiency / a
  directive verb) — the linter flags both.
