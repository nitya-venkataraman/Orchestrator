# Quality rubric — generated user stories

Single source of truth for judging a backlog produced by this skill. Used by the skill's
own final self-check, by human reviewers, and by the `llm` graders in
`.claude/skills/user-story-generator/evals/*/graders/`.

Score each dimension 1–5 (5 = fully met). A backlog is acceptable at **4+ on every
dimension** and **no dimension below 3**.

| # | Dimension | What "5" looks like |
|---|-----------|---------------------|
| 1 | **Format compliance** | Every story is exactly `As a <role>, I want to <action> so that I can <benefit>.` Personas, epics, Open questions sections all present. Passes `harness/validate_stories.py --strict`. |
| 2 | **One action per story** | No story bundles multiple capabilities. "Filter, sort, and export" becomes three stories. |
| 3 | **Benefit is a real "why"** | The `so that` clause states an outcome or value, not a restatement of the action. |
| 4 | **Specific personas** | Roles come from the source material (e.g. "finance approver"), not a blanket "user", unless the input truly names no role. |
| 5 | **Testable criteria** | 2–6 per story, each a single checkable scenario; main path + key edge cases covered. |
| 6 | **Source fidelity** | Every distinct need in the inputs is represented. The `Sources:` line lists every input file/section reviewed. |
| 7 | **No invented scope** | Nothing is added that the inputs don't support. Ambiguities and unmade decisions appear under **Open questions**, not as stories or criteria. |
| 8 | **User-centric voice** | Stories and criteria avoid implementation detail (APIs, tables, frameworks, services). |

## Common failure modes

- Turning a vague one-line brief into a large confident backlog (violates 7).
- Copying a compound requirement into one story (violates 2).
- `so that I can do X` where X == the action (violates 3).
- Dropping the Open questions section when inputs were incomplete (violates 7).
- Only a main-path criterion, no edge cases (violates 5).
