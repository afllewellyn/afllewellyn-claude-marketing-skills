# Memory: update-skill-memory

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-06-05: Founding entry (the agentic memory loop)
This skill is the standalone entry point for the agentic memory loop: it runs the memory-curator subagent and refreshes the `.claude/.memory-last-run` sentinel. The memory-gate Stop hook forces it at session end when learnings changed but memory was not synced, and `/qa-review` runs the same curator on analysis runs.

## Standing preferences (apply every run)

- **Pass the session feedback to the curator yourself.** Subagents do not see the parent conversation, so collect the user's corrections and preferences into bullets before invoking the memory-curator.
- **Auto-write, you commit.** The curator edits memory.md directly; review via git diff and commit in the normal flow. It does not commit and never edits CLAUDE.md.
- **`--full` is the re-runnable historical backfill** that resyncs every skill from the entire CLAUDE.md history.
