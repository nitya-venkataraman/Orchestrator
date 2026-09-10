# ux-pipeline

A human-in-the-loop UX design pipeline. Raw research goes in one end; developer-ready
user stories, microcopy, and a plan for finding out whether any of it worked come
out the other. Each phase is a Claude Agent SDK **skill**,
orchestrated as a LangGraph state machine, machine-vetted by a two-tier gate before a
human ever sees it — so the human spends attention on judgment, not on catching malformed
JSON and bad arithmetic.

**The graph does not run end to end.** `claude_skill_client.invoke_skill()` and
`orchestrator._judge_model()` are stubs that raise `NotImplementedError` (details in
[README.md](README.md) § Status). Don't try to execute a run from here — drive real runs
through the conversational Superlap skills on claude.ai. Everything *around* those two
calls is real and testable now.

The rulebook lives outside this directory, in [`../rules/`](../rules/) — it is the source
of truth, and the validators *implement* it rather than restating it. For the flow
diagram, layout tree and dependencies, see [README.md](README.md).

## Stage vocabularies — check which one you need

Four different names exist for the same six stages. Getting this wrong produces a
path that silently doesn't resolve.

| Context | Names |
|---|---|
| Orchestrator keys (`ORDER`, `SKILL`) | `discovery` · `strategy` · `ideation` · `wireframe` · `delivery` · `evaluation` |
| Skill dirs **and** rubric files | `discovery-synthesis` · `strategy-definition` · `ideation-concepting` · `wireframe-ia` · `delivery-handoff` · `evaluation-planning` |
| `output/<project-slug>/` filenames | `discovery-synthesis` · `strategy` · `ideation` · `wireframe` · `delivery` · `evaluation` — a **mix** of the two above |
| `validators/` modules | `synthesis.py` · `strategy.py` · `ideation.py` · `wireframe.py` · `delivery.py` · `evaluation.py` |

So a rubric is `../rules/rubrics/<skill-name>.md` — `wireframe-ia.md`, never
`wireframe.md`. `rubrics.py` accepts either the stage key or the skill name via
`_STAGE_TO_FILE`; nothing else does that normalization for you.

## Modules

[README.md](README.md) has the one-line-per-file layout tree. What it doesn't say:

- **`orchestrator.py`** — one node per phase → shared `gate` → shared `human_review`
  (`interrupt()` for approval); `select_direction` forks after ideation. The `SqliteSaver`
  checkpointer (falling back to `MemorySaver`) is what makes HITL interrupts survive a
  restart.
- **`validators/`** — `run_tier1(stage, artifact, context)` is the entry point; each
  module is also a CLI (`python3 ux-pipeline/validators/wireframe.py file.json`).
- **`rubrics.py`** — `load_rubric()` builds the judge prompt; `evaluate(stage,
  {dimension: 1..5})` applies the pass rule. Pure, no model call.
- **`cache.py`** — a resumed run replays the exact artifact the human approved instead of
  regenerating it.
- **`claude_skill_client.py`** — `build_payload()` already assembles the SKILL.md, the
  *contents* of `references/`+`assets/`, the run identity, the prior approved artifacts
  the stage needs as context, and `feedback_loop`. Only the SDK call itself is missing.
- **`workspace/`** — never hand-edit it, and never commit it.

## Skills (one per phase)

Per-stage inputs and outputs are specified in [`../rules/CONTRACTS.md`](../rules/CONTRACTS.md).

| Skill | Stage | `output/<project-slug>/` file |
|---|---|---|
| `discovery-synthesis` | 1 | `discovery-synthesis.{json,md}` |
| `strategy-definition` | 2 | `strategy.{json,md}` |
| `ideation-concepting` | 3 | `ideation.{json,md}` |
| `wireframe-ia` | 4 | `wireframe.{json,md}` |
| `delivery-handoff` | 5 | `delivery.{json,md}` |
| `evaluation-planning` | 6 | `evaluation.{json,md}` |

## Invariants — don't break these

- **Never invent data.** If an input is missing or thin, flag the gap explicitly rather
  than fabricating personas, quotes, or metrics. This applies to numbers as hard as to
  quotes: a Stage-3 `success_metric.baseline` is `"unknown"` unless a real figure exists,
  and every unknown one is carried into the Stage-6 `open_baselines` so the pipeline knows
  what it doesn't know.
- **Accessibility survives the handoff.** Stage 4 designs it in per page — seven keys,
  WCAG 2.2 AA, with `contrast` and `touch_targets` citing evidence a validator can check
  and no two pages sharing a block. Stage 5 turns it into acceptance criteria for every
  page. Without that second half it is designed and then dropped, which is where it was
  before.
- **Every stage is evaluable.** Stage 4 critiques itself against the ten usability
  heuristics before a human sees it; Stage 6 plans the usability test and the measurement
  that would show whether any of it worked. A pipeline that only generates cannot be
  wrong, which is not the same as being right.
- **Preserve traceability.** Nothing downstream may reference an artifact the upstream
  stage did not produce: persona `grounded_in` names a Stage-1 theme, every feature `hmw`
  matches a Stage-2 HMW, every wireframe screen appears in the sitemap, every story ties
  to a Stage-2 persona and a Stage-4 screen, every Stage-6 task names a real journey stage
  and real pages, and every Stage-3 `success_metric` has exactly one Stage-6 plan entry.
  Tier-1 enforces this whenever the upstream artifact is in context — don't weaken those
  checks to make an artifact pass.
- **Self-check before the gate.** A stage runs its `validators/<stage>.py` Tier-1 rules
  and only surfaces output that passes. A gate failure — Tier-1 violation or a Tier-2
  score below the stage's `pass_when` — re-runs the stage with the concrete reason list as
  `feedback_loop`, capped at 2 retries, then escalates with `escalated = true`.
- **Tier-2 is a 1–5 rubric, not a threshold.** Each dimension is scored 1–5 against the
  stage's rubric file; the pass rule (default "every dim ≥ 4, or every dim ≥ 3 and
  weighted mean ≥ 4.0") lives in that file's `json` block, tightened for wireframe
  (`ds_compliance` = 5) and loosened for ideation. `judge_scores[stage]` stores the
  weighted mean. Change a rule in the rubric file, never in code.
- **Humans make the choices.** Ideation proposes 2–3 directions but never picks a winner.
  `selected_direction`, `target_surface` (web / mobile / both), `mobile_platform`
  (android / ios, when the surface includes mobile) and `design_system_input` are set by a
  person at the `select_direction` fork, and all become part of the wireframe cache key.
- **Treat revision feedback as an input.** On a revise decision the same stage re-runs
  with `feedback_loop` in its payload; a human revision resets that stage's attempt
  counter and invalidates its cache so the rerun genuinely regenerates.
- **Don't silently re-run an approved stage.** On entry the orchestrator reads
  `workspace/run.json` and resumes at the first stage not `APPROVED`.
- **The design system is the project's, not ours.** `wireframe-ia` reuses whatever system
  the project supplies (or is linkable in Figma) and falls back to the baseline only when
  there is none, recording that in `assumptions`. Fixed regardless: the base-role taxonomy
  (`BASE_ROLES` in `validators/wireframe.py`), the page/component naming patterns, and the
  required state, responsive and accessibility keys — all in `../rules/CONTRACTS.md`
  § Stage 4. Colour is always a token, never a raw hex or `rgb()`; `px` is allowed,
  because the breakpoints and the 44×44px touch minimum are px by definition. Reuse before
  you create — a `new` component needs a `why_new` — and a need outside the taxonomy is a
  `design_system_gaps` entry, never an invented role.
- **Show Markdown at the gate, never a raw JSON dump.** Each stage renders its result as
  Markdown and shows that to the human.
- **Persist both formats.** All six stages write into one folder per project —
  `output/<project-slug>/<stage>.{json,md}` — reusing the run's kebab-case
  `<project-slug>` and overwriting on re-run, never a timestamp suffix. The run index
  goes beside them as `output/<project-slug>/RUN-SUMMARY.md`, linking its siblings by
  bare filename.
- **`wireframe-ia` also renders to Figma.** One new **high-fidelity** file per run: real
  components, Auto Layout, variables bound to the resolved system's tokens, variants for
  meaningful states, and **prototype connections** for every `prototype_flows` entry. The
  URL goes in `figma_file_url`.
- **Status vocabulary** (`stage_status`, `run.json`): `PENDING`, `RUNNING`,
  `AWAITING_APPROVAL`, `APPROVED`, `ESCALATED`.

## Working on this repo

- Add a phase → new `skills/<name>/SKILL.md`, new `validators/<name>.py`, new
  `../rules/rubrics/<name>.md` + a `../rules/CONTRACTS.md` section, new node in
  `orchestrator.py`, extend `ORDER` / `SKILL` there, the `_STAGE_TO_FILE` map in
  `rubrics.py`, and the `Phase` literal in `state.py`.
- `skills/wireframe-ia/references/material-design-tokens.json` is the **baseline** token
  set, used only when the project supplies no design system of its own — colour roles,
  typescale, shape-corner scale, elevation levels, the 4dp spacing grid, and per-platform
  insets. Specs reference tokens by name; the values exist so the Figma step can create
  matching Figma variables. Page, component, responsive, state and accessibility narrative
  lives in `assets/component-patterns.md`.

## Verify

`make ux-test` is the safety net, and CI runs it on every push and PR
(`.github/workflows/harness.yml`, job `ux-pipeline`). Run it before you finish:

```bash
make ux-test
```

That is three checks:

```bash
python3 ux-pipeline/rubrics.py --check          # every rubric: weights sum to 1.0, pass_when parses
python3 ux-pipeline/tests/run_tests.py          # Tier-1 fixtures: good-* pass, bad-* fail with the registered diagnostic
python3 ux-pipeline/tests/check_artifacts.py    # every committed output/ artifact still conforms
```

`python3 ux-pipeline/validators/<stage>.py <artifact.json>` still checks one artifact by
hand — but note it runs **without upstream context**, so every cross-stage traceability
check is skipped. It is a weaker check than the gate's; `check_artifacts.py` supplies the
sibling stages and is the one that catches a broken reference.

**Changing a rule?** Change `../rules/` first, then the validator, then add a fixture
under `tests/fixtures/<skill-name>/` — a `good-*` if the rule admits something new, a
`bad-*` plus its entry in `EXPECTED_BAD` if it rejects something. A rule with no fixture
is a rule that will be silently reverted.
