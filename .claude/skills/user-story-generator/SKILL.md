---
name: user-story-generator
description: >-
  Analyzes project inputs in any format (notes, transcripts, emails, PRDs, spreadsheets,
  bullet lists, chat logs) and converts them into structured user stories with acceptance
  criteria. Use when the user asks to generate user stories, turn requirements into a
  backlog, write acceptance criteria, or break a feature or project down into stories.
---

# UserStoryGenerator

Convert raw, unstructured project material into a clean set of user stories, each with
acceptance criteria, grouped into epics.

## When to use

- The user pastes or points to requirements material (notes, transcript, email thread,
  PRD, spec, spreadsheet, Slack export, screenshots-turned-text) and wants stories.
- The user says: "generate user stories", "write the backlog", "add acceptance criteria",
  "break this into stories", "convert this to Agile stories".
- Working at a **project level**: scan every provided input, not just one document.

## Inputs

Accept any format. Typical sources:

- `inputs/` directory in this repo (read every file found there)
- Text pasted directly into the conversation
- Linked or attached documents, transcripts, tables

If no input is provided, ask the user to paste the material or drop files in `inputs/`.

## Process

1. **Gather** – Collect all inputs. If `inputs/` exists and is non-empty, read all of it.
   List the sources you are working from.
2. **Extract** – Pull out every distinct capability, need, pain point, constraint, and
   actor mentioned. Keep a running list of the **user types / personas** referenced.
3. **Cluster** – Group related needs into **epics** (themes / feature areas).
4. **Write stories** – For each need, write one user story in the required format.
   Split anything that bundles multiple actions or benefits into separate stories.
5. **Acceptance criteria** – Add 2–6 testable criteria per story (see format below).
6. **Flag gaps** – Where inputs are silent or contradictory, add an "Open questions"
   list instead of guessing. Do not invent scope, personas, or numbers.
7. **Write output** – Save to `output/user-stories-<YYYY-MM-DD>.md` (or per-epic files
   for large sets). Also summarize in the chat response.

## Required user story format

Every story MUST use this sentence:

> **As a** [user-type], **I want to** [action] **so that I can** [benefit/gain].

Rules:
- `[user-type]` is a role/persona, never "user" if a more specific role is known.
- `[action]` is a single, concrete capability from the user's point of view.
- `[benefit/gain]` is the outcome or value — the "why", not a restatement of the action.
- No implementation detail in the story sentence (no table names, endpoints, frameworks).

## Acceptance criteria format

Prefer Gherkin-style:

```
- Given <context>, when <action>, then <expected outcome>.
```

A checklist is acceptable when scenarios don't fit Given/When/Then:

```
- [ ] <observable, testable condition>
```

Criteria must be **testable, specific, and cover the main path plus key edge cases**
(empty state, invalid input, permissions, error handling) when relevant.

## Output template

```markdown
# User Stories — <project / feature name>

_Generated: <date> · Sources: <list of inputs>_

## Personas
- **<user-type>** — <one-line description>

## Epic: <epic name>

### US-<n>: <short title>
**As a** <user-type>, **I want to** <action> **so that I can** <benefit/gain>.

**Acceptance criteria**
- Given <...>, when <...>, then <...>.
- Given <...>, when <...>, then <...>.

**Priority:** <High/Medium/Low>  ·  **Notes:** <optional>

---

## Open questions
- <ambiguity or missing info that blocks a confident story>
```

## Quality checklist before finishing

- [ ] Every input source was reviewed and is listed.
- [ ] Every story follows the `As a / I want to / so that` sentence exactly.
- [ ] No story bundles multiple actions or multiple benefits.
- [ ] Every story has at least 2 testable acceptance criteria.
- [ ] Personas are specific; "user" only used when truly generic.
- [ ] Assumptions and gaps are in "Open questions", not invented into stories.
- [ ] Output file written to `output/`.

See `examples/` for a worked input-to-output sample.
