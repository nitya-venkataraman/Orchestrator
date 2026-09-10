# Output template

Write generated stories to `output/<project-slug>/user-stories-<YYYY-MM-DD>.md` (or one file per epic for
large sets). Use this exact structure — the harness validator
(`harness/validate_stories.py`) checks against it.

```markdown
# User Stories — <project / feature name>

_Generated: <date> · Sources: <comma-separated list of every input reviewed>_

## Personas
- **<user-type>** — <one-line description>
- **<user-type>** — <one-line description>

## Epic: <epic name>

### US-1: <short title>
**As a** <user-type>, **I want to** <single concrete action> **so that I can** <benefit/gain>.

**Acceptance criteria**
- Given <context>, when <action>, then <expected outcome>.
- Given <context>, when <action>, then <expected outcome>.

**Priority:** <High/Medium/Low>  ·  **Notes:** <optional>

### US-2: <short title>
**As a** <user-type>, **I want to** <action> **so that I can** <benefit/gain>.

**Acceptance criteria**
- Given <...>, when <...>, then <...>.
- Given <...>, when <...>, then <...>.

**Priority:** <High/Medium/Low>

---

## Epic: <next epic name>

### US-3: <short title>
...

---

## Open questions
- <ambiguity, contradiction, or missing information that blocks a confident story>
- <decision the stakeholders still need to make>
```

Rules the validator enforces:

- The title line starts with `# User Stories`.
- A `_Generated: … · Sources: …_` line is present and lists every input.
- `## Personas` exists with at least one `- **Name** — description` bullet.
- At least one `## Epic:` heading.
- Every `### US-<n>:` block has the story sentence and **≥ 2** acceptance criteria.
- `## Open questions` section is present (use "- None" only if truly nothing is open).
- No `<...>` or `[user-type]` placeholders remain.
