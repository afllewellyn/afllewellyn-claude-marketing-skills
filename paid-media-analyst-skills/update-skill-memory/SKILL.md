---
name: update-skill-memory
description: Sync durable lessons and user feedback from this session into the per-skill memory.md files. Invokes the memory-curator subagent, then refreshes the memory sentinel so the memory-gate Stop hook stays quiet. Use when the memory-gate hook asks for it, when the user asks to update or refresh skill memory, or when you want a full resync from CLAUDE.md. Pass --full to backfill every skill from the entire CLAUDE.md history.
argument-hint: "[--full to resync all skills from CLAUDE.md; empty for this session's changes]"
allowed-tools: Read, Bash, Grep, Glob, Task
---

# Update Skill Memory

Capture this session's durable, skill-specific lessons into each skill's `memory.md`,
then refresh the sentinel the Stop hook checks.

## Check Memory First

Before running, read `memory.md` in this skill's folder for past feedback and the
editing standard. Apply anything relevant, and add a dated entry at the end of the run
if a new preference surfaces.

## What You Receive as Arguments

- `$ARGUMENTS`: empty syncs this session's changes (incremental). `--full` resyncs every
  skill from the entire `CLAUDE.md` Session Learnings and Run Log (the re-runnable
  historical backfill).

## Step 1: Collect this session's feedback

Write down the user's corrections and stated preferences from this session in a few
bullets. Subagents do not see the conversation, so you have to pass these to the curator
yourself.

## Step 2: Run the memory-curator

Invoke the **`memory-curator`** subagent (via the Task tool). Pass it the mode
(`incremental` or `full`) and the session-feedback bullets from Step 1. It routes each
lesson to the right skill, dedupes, and auto-writes dated entries to
`.claude/skills/<skill>/memory.md`. Relay its per-skill summary to the user.

## Step 3: Refresh the sentinel

```bash
mkdir -p .claude && date +%s > .claude/.memory-last-run
```

This tells the `memory-gate.sh` Stop hook the sync happened this session.

## Important Notes

- The curator auto-writes `memory.md` (low-stakes, reversible via git). Review the diff
  and commit in your normal flow; the curator does not commit.
- It never edits `CLAUDE.md` (the run-log-curator owns that) or changes skill behavior.
