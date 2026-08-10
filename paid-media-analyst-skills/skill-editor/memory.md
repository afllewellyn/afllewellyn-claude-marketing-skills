# Memory: skill-editor

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-06-05: Founding standard for skill editing (user-defined)
This skill enforces the standard the user defined: cut AI slop (filler words like "leverage" and "delve", repeated sentence structures, and em-dashes), keep skills concise and progressively disclosed, and make every instruction clear and actionable for a human. Use specific before/after examples and prioritize clarity above all else. Behavior is propose-first: present before/after rewrites and apply only after the user approves.

### 2026-06-05: The first audit will flag the existing skills heavily
The existing SKILL.md files use em-dashes and some filler heavily, so a first pass surfaces many edits; that is expected, not a sign something is wrong. Preserve meaning, frontmatter, and code blocks; change wording, structure, and clarity only.

## Standing preferences (apply every run)

- **Replace em-dashes** with a comma, period, colon, or parentheses depending on how the clauses relate.
- **Progressive disclosure for this repo** means the top of a SKILL.md states what and when plus the high-level steps, while deep mechanics live in the numbered steps or the referenced `prompts/<platform>/agent_*.md` spec; flag detail re-inlined from an agent spec.
- **Out of scope:** memory.md files and any change to skill behavior; tighten SKILL.md prose and structure only.
