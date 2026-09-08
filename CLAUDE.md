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

### Superlap UX pipeline (vendored)

`.claude/skills/superlap-{synthesis,strategy,ideation,wireframe,pipeline}/` are vendored
copies of the claude.ai-synced Superlap pipeline skills, kept here so they are
git-tracked and editable. The canonical copies still live on claude.ai — re-upload after
editing here.

- Stages 1–4 each produce a validated JSON artifact **and** write two files to `output/`:
  `output/<stage>-<slug>.json` plus a human-readable `output/<stage>-<slug>.md`
  (prefixes: `discovery-synthesis-`, `strategy-`, `ideation-`, `wireframe-`). One
  kebab-case `<slug>` per run; re-runs overwrite.
- The stage's visible reply is the Markdown rendering, not the JSON.
- `superlap-wireframe` (Stage 4) is the **Figma Page Builder**: it takes requirements
  (or a feature list + a chosen design direction), a **target** (`web` / `mobile` /
  `both`, asked if not supplied, plus Android-or-iOS when the target includes mobile),
  and the project's design system if it has one. It produces a UX interpretation, a user
  flow, a sitemap, page-by-page specs with responsive behaviour across the 1440/1280/768/375
  breakpoints, all UI states, WCAG AA accessibility, per-page build `requirements`,
  `prototype_flows`, assumptions and a validation summary — then builds a **high-fidelity,
  prototype-wired Figma file** per run (URL in `figma_file_url`). Validate specs with
  `python3 .claude/skills/superlap-wireframe/scripts/validate_ds.py <file>`.
- The stage is **design-system agnostic** — it reuses whatever design system the project
  has and only falls back to a documented baseline (recorded in `assumptions`) when there
  is none. The enforced vocabulary (the base-role taxonomy, the `NN - Title` / `MNN - Title`
  page naming, the `Component / <Name>` component naming, the breakpoints, and the required
  state and accessibility keys) lives in
  `.claude/skills/superlap-wireframe/references/page-builder-reference.md`. Material 3 is
  now one optional baseline profile in `references/material-design-system.md`, not an
  allowlist.
- The `ux-pipeline/` directory holds the LangGraph code-form of the same pipeline — a
  two-tier gate (deterministic `validators/` for Tier-1, a 1–5 rubric judge for Tier-2),
  retry/escalation, a content-addressed cache for correct resume, a direction-selection
  fork, and all five stages (delivery-handoff included) writing
  `output/<stage>-<slug>.{json,md}`. Its rulebook is `rules/CONTRACTS.md` (schemas +
  Tier-1) and `rules/rubrics/` (Tier-2 scoring, one file per stage); Stages 1–4 mirror
  `.claude/skills/superlap-pipeline/references/contracts.md`.

## Conventions

- Generated stories are written to `output/` as Markdown, one file per epic or per run.
- Superlap pipeline stage artifacts also land in `output/`, as
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
rules/                          # THE ux-pipeline rulebook (shared with the vendored skills)
  CONTRACTS.md                  # per-stage JSON schema + deterministic Tier-1 rules
  rubrics/<stage>.md            # Tier-2 scoring rubric per stage (1–5 dims, weights, pass rule)
ux-pipeline/                    # LangGraph code-form of the Superlap pipeline (see its CLAUDE.md)
  validators/                   # deterministic Tier-1 checks, one module per stage
  rubrics.py                    # loads rules/rubrics/, scores a 1–5 map against the pass rule
.github/workflows/harness.yml   # CI
inputs/                         # drop raw source material here (any format)
output/                         # generated user stories (tracked) + pipeline artifacts (ignored)
```
