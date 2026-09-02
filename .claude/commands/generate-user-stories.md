---
description: Generate structured user stories with acceptance criteria from project inputs
argument-hint: "[path to inputs — file, dir, or glob; defaults to inputs/]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

Invoke the **user-story-generator** skill
(`.claude/skills/user-story-generator/SKILL.md`) and follow its process end to end.

Inputs to analyze: `$ARGUMENTS`
If that is empty, use everything in the `inputs/` directory. If `inputs/` is also empty,
ask me to provide the source material.

Then:

1. Read every input source and list them.
2. Produce the backlog per the skill's output template
   (`.claude/skills/user-story-generator/references/output-template.md`), writing to
   `output/user-stories-<today>.md`.
3. Run the validator and fix every error before showing me the result:

   ```bash
   python3 harness/validate_stories.py --strict output/user-stories-<today>.md
   ```

4. In your reply: the output file path, a one-line summary (epics / story count /
   number of open questions), and confirmation that the validator passed.
