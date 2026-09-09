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

### UX pipeline (`ux-pipeline/`)

The `ux-pipeline/` directory holds the LangGraph code-form of a research-to-design
pipeline — research synthesis, strategy, ideation, page building, delivery handoff — with
a two-tier gate (deterministic `validators/` for Tier-1, a 1–5 rubric judge for Tier-2),
retry/escalation, a content-addressed cache for correct resume, and a direction-selection
fork. Stages write `output/<stage>-<slug>.{json,md}` (prefixes:
`discovery-synthesis-`, `strategy-`, `ideation-`, `wireframe-`, `delivery-`; one
kebab-case `<slug>` per run, re-runs overwrite). Its rulebook is `rules/CONTRACTS.md`
(schemas + Tier-1) and `rules/rubrics/` (Tier-2 scoring, one file per stage). See
`ux-pipeline/CLAUDE.md` for details.

## Conventions

- Generated stories are written to `output/` as Markdown, one file per epic or per run.
- UX pipeline stage artifacts also land in `output/`, as
  `<stage>-<slug>.{json,md}` pairs. These are **gitignored** — they are regenerated
  per run and never committed. `output/` allowlists only `user-stories-*`, so any
  new pipeline stage is ignored automatically.
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
rules/                          # THE ux-pipeline rulebook
  CONTRACTS.md                  # per-stage JSON schema + deterministic Tier-1 rules
  rubrics/<stage>.md            # Tier-2 scoring rubric per stage (1–5 dims, weights, pass rule)
ux-pipeline/                    # LangGraph code-form of the UX pipeline (see its CLAUDE.md)
  validators/                   # deterministic Tier-1 checks, one module per stage
  rubrics.py                    # loads rules/rubrics/, scores a 1–5 map against the pass rule
.github/workflows/harness.yml   # CI
inputs/                         # drop raw source material here (any format)
output/                         # generated user stories (tracked) + pipeline artifacts (ignored)
```
