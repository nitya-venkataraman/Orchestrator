# AI POC

A lightweight project repo for turning raw project inputs into structured, review-ready user stories.

## Purpose

Product, design, and engineering inputs arrive in many shapes — meeting notes, transcripts,
emails, Slack threads, PRDs, spreadsheets, bullet dumps, screenshots-turned-text. This repo
provides a repeatable way to convert any of that into consistent user stories with acceptance
criteria.

## Skills

### UserStoryGenerator

Analyzes project-level inputs in **any format** and converts them into structured user stories.

- Location: `.claude/skills/user-story-generator/SKILL.md`
- Invoke it whenever the user asks to "generate user stories", "turn this into stories",
  "write acceptance criteria", "break this down into a backlog", or provides raw requirements
  material and wants it structured.

**User story format (required):**

> As a **[user-type]**, I want to **[action]** so that I can **[benefit/gain]**.

Every story must also include **acceptance criteria** (Given/When/Then or a checklist).

## Conventions

- Generated stories are written to `output/` as Markdown, one file per epic or per run.
- Keep the story voice user-centric — describe outcomes, not implementation.
- When inputs are ambiguous or incomplete, list open questions rather than inventing detail.
- **Always** finish by running `python3 harness/validate_stories.py --strict <file>` and
  fixing every error. The skill's own process includes this step.

## Testing the skill

The `harness/` directory is a three-layer harness — see [harness/README.md](harness/README.md):

1. `python3 harness/validate_stories.py <file>` — deterministic format check (no LLM).
2. `python3 harness/run.py` — run the skill end to end on `harness/fixtures/*` (needs `claude` CLI).
3. `claude plugin eval ./.claude/skills/user-story-generator` — LLM-graded eval suite
   (early-access; no-ops where not enabled).

`make test` / `make lint` / `make run` / `make eval` wrap these. CI runs layers 1–2 on
every push.

## Repo layout

```
CLAUDE.md · README.md
Makefile                        # make test | lint | validate | run | eval
.claude/
  commands/generate-user-stories.md   # /generate-user-stories slash command
  skills/user-story-generator/
    SKILL.md                    # the UserStoryGenerator skill
    references/                 # output template, criteria guide, quality rubric
    examples/                   # sample input -> output
    evals/                      # `claude plugin eval` cases (prompt.md + graders/)
harness/
  validate_stories.py           # deterministic validator
  run.py                        # local end-to-end runner
  lint_skill.py                 # skill + eval-suite structure lint
  fixtures/                     # input bundles per scenario
  tests/                        # validator self-tests + samples
.github/workflows/harness.yml   # CI
inputs/                         # drop raw source material here (any format)
output/                         # generated user stories land here
```
