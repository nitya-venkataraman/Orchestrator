# ux-pipeline

A human-in-the-loop UX design pipeline. Raw research goes in one end; developer-ready
user stories and microcopy come out the other. Each phase is a Claude Agent SDK **skill**,
orchestrated as a LangGraph state machine. Every stage is machine-vetted by a two-tier
gate before a human ever sees it, so the human spends attention on judgment, not on
catching malformed JSON and bad arithmetic.

**The graph does not run end to end.** Both model calls are stubs that raise
`NotImplementedError` — `claude_skill_client.invoke_skill()` (the stage call) and
`orchestrator._judge_model()` (the Tier-2 judge). Don't try to execute a run from here;
drive a real run through the conversational Superlap skills on claude.ai. Everything
*around* those two calls is real and testable now: the Tier-1 validators, rubric loading
and scoring, the cache, the retry/escalation gate, the direction + platform fork, and the
`output/` + `workspace/` persistence.

The rulebook lives outside this directory, in
[`../rules/CONTRACTS.md`](../rules/CONTRACTS.md) (per-stage schemas + Tier-1 rules) and
[`../rules/rubrics/`](../rules/rubrics/) (Tier-2 scoring, one file per stage). It is the
source of truth: the validators *implement* it, they don't restate it. For the flow
diagram, the layout tree and the dependency list, see [`README.md`](README.md).

## Modules

- **`state.py`** — `UXPipelineState`, the `TypedDict` threaded through every node.
  Artifact fields are typed per `../rules/CONTRACTS.md`; `attempts`, `stage_status`,
  `judge_scores`, `escalated`, `run_slug` carry the gate bookkeeping.
- **`orchestrator.py`** — the LangGraph graph. One node per phase → shared `gate` node →
  shared `human_review` node (`interrupt()` for approval). `select_direction` forks after
  ideation. Compiled with a `SqliteSaver` checkpointer (falls back to `MemorySaver`) so
  HITL interrupts survive a restart.
- **`validators/`** — deterministic Tier-1 checks, one module per stage.
  `run_tier1(stage, artifact, context)` is the entry point; each module is also a CLI
  (`python3 ux-pipeline/validators/wireframe.py file.json`).
- **`rubrics.py`** — loads `../rules/rubrics/<stage>.md` (prose + a machine-readable
  `json` block of weights + `pass_when`). `load_rubric()` builds the judge prompt;
  `evaluate(stage, {dimension: 1..5})` applies the pass rule. Pure, no model call.
- **`cache.py`** — content-addressed artifact cache under `workspace/cache/`. A resumed
  run replays the exact artifact the human approved instead of regenerating it.
- **`claude_skill_client.py`** — `invoke_skill(name, state)`. `build_payload()` assembles
  the SKILL.md, the *contents* of `references/`+`assets/`, the run identity, the prior
  approved artifacts the stage needs as context, and `feedback_loop` — all real; only the
  SDK call itself is missing.
- **`workspace/`** — run bookkeeping (gitignored): `run.json` (run_id, slug,
  `stage_status`, `selected_direction`), `artifacts/<stage>.json` (approved artifacts),
  `cache/`, `events.jsonl` (append-only audit trail), `checkpoints.sqlite`. Never
  hand-edit it, and never commit it.

## Skills (one per phase)

| Skill | Stage | Reads from state | Writes to state | `output/` files |
|---|---|---|---|---|
| `discovery-synthesis` | 1 | `raw_research_data` | `synthesized_insights` | `discovery/discovery-synthesis-<slug>.{json,md}` |
| `strategy-definition` | 2 | `synthesized_insights` | `persona_profile`, `journey_map`, `problem_statement` | `strategy/strategy-<slug>.{json,md}` |
| `ideation-concepting` | 3 | `problem_statement`, `persona_profile` | `feature_matrix`, `concept_proposals` | `ideation/ideation-<slug>.{json,md}` |
| `wireframe-ia` | 4 | `feature_matrix`, `selected_concept`, `selected_direction`, `target_surface`, `mobile_platform`, `design_system_input` | `design_system`, `ux_interpretation`, `user_flow`, `sitemap`, `wireframe_specs` (pages), `responsive_matrix`, `prototype_flows`, `design_system_gaps`, `assumptions`, `validation`, `design_tokens_applied`, `figma_file_url` | `wireframe/wireframe-<slug>.{json,md}` |
| `delivery-handoff` | 5 | `sitemap`, `wireframe_specs`, `persona_profile` | `developer_handoff_stories`, `microcopy` | `delivery/delivery-<slug>.{json,md}` |

## Invariants — don't break these

- **Never invent data.** If an input is missing or thin, flag the gap explicitly rather
  than fabricating personas, quotes, or metrics.
- **Preserve traceability.** Nothing downstream may reference an artifact the upstream
  stage did not produce: persona `grounded_in` names a Stage-1 theme, every feature `hmw`
  matches a Stage-2 HMW, every wireframe screen appears in the sitemap, every story ties
  to a Stage-2 persona and a Stage-4 screen. Tier-1 enforces this whenever the upstream
  artifact is in context — don't weaken those checks to make an artifact pass.
- **Self-check before the gate.** A stage runs its `validators/<stage>.py` Tier-1 rules
  and only surfaces output that passes. A gate failure — Tier-1 violation or a Tier-2
  score below the stage's `pass_when` — re-runs the stage with the concrete reason list as
  `feedback_loop`, capped at 2 retries, then escalates with `escalated = true`.
- **Tier-2 is a 1–5 rubric, not a threshold.** Each dimension is scored 1–5 against
  `../rules/rubrics/<stage>.md`; the pass rule (default "every dim ≥ 4, or every dim ≥ 3
  and weighted mean ≥ 4.0") lives in that file's `json` block, tightened for wireframe
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
- **Persist both formats.** All five stages write `output/<stage>/<stage>-<slug>.{json,md}`,
  reusing one kebab-case `<slug>` per run and overwriting on re-run — never a timestamp
  suffix.
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

There is **no test suite here**, and CI does not cover this directory —
`.github/workflows/harness.yml` runs only the user-story harness. These two commands are
the whole safety net, so run them before you finish:

```bash
python3 ux-pipeline/rubrics.py --check                       # every rubric: weights sum to 1.0, pass_when parses
python3 ux-pipeline/validators/<stage>.py <artifact.json>    # Tier-1 on one artifact
```
