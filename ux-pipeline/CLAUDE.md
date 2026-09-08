# ux-pipeline

A human-in-the-loop UX design pipeline. Raw research goes in one end; developer-ready
user stories and microcopy come out the other. Each phase is a Claude Agent SDK **skill**,
orchestrated as a LangGraph state machine. Every stage is machine-vetted by a two-tier
gate before a human ever sees it, so the human spends attention on judgment, not on
catching malformed JSON and bad arithmetic.

This is the LangGraph code-form of the vendored `.claude/skills/superlap-*` skills — same
contracts, same gate, same cache/resume behaviour. The rulebook lives outside this
directory in [`../rules/CONTRACTS.md`](../rules/CONTRACTS.md) — the single source of truth
shared by this scaffold and the vendored skills.

## Architecture

```
discovery → gate → [HITL] → strategy → gate → [HITL] → ideation → gate → [HITL]
    → SELECT direction + platform → wireframe → gate → [HITL] → delivery → gate → [HITL] → complete

gate:  Tier-1 structural (validators/)  →  Tier-2 rubric score (1–5 per dimension,
                                           ../rules/rubrics/<stage>.md) passes
       fail → retry with concrete feedback (max 2) → then escalate to the human
```

- **`state.py`** — `UXPipelineState`, the `TypedDict` threaded through every node.
  Artifact fields are typed per `../rules/CONTRACTS.md`; `attempts`, `stage_status`,
  `judge_scores`, `escalated`, `run_slug` carry the gate bookkeeping.
- **`orchestrator.py`** — the LangGraph graph. One node per phase → shared `gate` node →
  shared `human_review` node (`interrupt()` for approval). `select_direction` forks after
  ideation. Compiled with a `SqliteSaver` checkpointer (falls back to `MemorySaver`) so
  HITL interrupts survive a restart.
- **`validators/`** — deterministic Tier-1 checks, one module per stage.
  `run_tier1(stage, artifact, context)` is the entry point; each module is also a CLI
  (`python ux-pipeline/validators/wireframe.py file.json`). `validators/wireframe.py` is a port of
  `.claude/skills/superlap-wireframe/scripts/validate_ds.py` — keep `BASE_ROLES` /
  `FORBIDDEN` and every check function byte-identical.
- **`rubrics.py`** — loads `../rules/rubrics/<stage>.md` (prose + a machine-readable
  ```json block of weights + `pass_when`). `load_rubric()` builds the judge prompt;
  `evaluate(stage, {dimension: 1..5})` applies the pass rule. Pure, no model call.
- **`cache.py`** — content-addressed artifact cache under `workspace/cache/`. A resumed
  run replays the exact artifact the human approved instead of regenerating it.
- **`claude_skill_client.py`** — `invoke_skill(name, state)`. `build_payload()` assembles
  the SKILL.md, the *contents* of `references/`+`assets/`, the run identity, the prior
  approved artifacts the stage needs as context, and `feedback_loop`. Still raises
  `NotImplementedError` — plug in your SDK client. `orchestrator.judge()` is rubric-driven
  now: real prompt assembly + `rubrics.evaluate()`, with only the model call
  (`_judge_model()`) stubbed the same way.
- **`workspace/`** — run bookkeeping (gitignored): `run.json` (run_id, slug,
  `stage_status`, `selected_direction`), `artifacts/<stage>.json` (approved artifacts),
  `cache/`, `events.jsonl` (append-only audit trail), `checkpoints.sqlite`.

## Skills (one per phase)

| Skill | Node | Reads from state | Writes to state | `output/` files |
|---|---|---|---|---|
| `discovery-synthesis` | 1 | `raw_research_data` | `synthesized_insights` | `discovery-synthesis-<slug>.{json,md}` |
| `strategy-definition` | 2 | `synthesized_insights` | `persona_profile`, `journey_map`, `problem_statement` | `strategy-<slug>.{json,md}` |
| `ideation-concepting` | 3 | `problem_statement`, `persona_profile` | `feature_matrix`, `concept_proposals` | `ideation-<slug>.{json,md}` |
| `wireframe-ia` | 4 | `feature_matrix`, `selected_concept`, `selected_direction`, `target_surface`, `mobile_platform`, `design_system_input` | `design_system`, `ux_interpretation`, `user_flow`, `sitemap`, `wireframe_specs` (pages), `responsive_matrix`, `prototype_flows`, `design_system_gaps`, `assumptions`, `validation`, `design_tokens_applied`, `figma_file_url` | `wireframe-<slug>.{json,md}` |
| `delivery-handoff` | 5 | `sitemap`, `wireframe_specs`, `persona_profile` | `developer_handoff_stories`, `microcopy` | `delivery-<slug>.{json,md}` |

## Conventions

- **Skills never invent data.** If an input is missing or thin, the skill flags the gap
  explicitly instead of fabricating personas, quotes, or metrics.
- **Traceability is mandatory.** Nothing downstream may reference an artifact the upstream
  stage did not produce: persona `grounded_in` names a Stage-1 theme, every feature `hmw`
  matches a Stage-2 HMW, every wireframe screen appears in the sitemap, every story ties
  to a Stage-2 persona and a Stage-4 screen. The Tier-1 validators enforce this whenever
  the upstream artifact is in context.
- **Each stage self-checks before the gate.** A stage runs its `validators/<stage>.py`
  Tier-1 rules and only surfaces output that passes. A gate failure — Tier-1 violation or
  a Tier-2 rubric score below the stage's `pass_when` — re-runs the stage with the
  concrete reason list as `feedback_loop`, capped at 2 retries, then escalates to the
  human with `escalated = true`.
- **Tier-2 is a 1–5 rubric, not a threshold.** Each dimension is scored 1–5 against
  `../rules/rubrics/<stage>.md`; the pass rule (default "every dim ≥ 4, or every dim ≥ 3
  and weighted mean ≥ 4.0") lives in that file's ```json block, tightened for wireframe
  (`ds_compliance` = 5) and loosened for ideation. `judge_scores[stage]` stores the
  weighted mean.
- **Humans make the choices.** Ideation proposes 2–3 directions but never picks a winner;
  `selected_direction`, `target_surface` (web / mobile / both), `mobile_platform`
  (android / ios, when the surface includes mobile) and `design_system_input` are set by a
  person at the `select_direction` fork, and all become part of the wireframe cache key.
- **Revision feedback is an input.** On a revise decision the same stage re-runs with
  `feedback_loop` in its payload; a human revision resets that stage's attempt counter and
  invalidates its cache so the rerun genuinely regenerates.
- **Approved stages don't silently re-run.** On entry the orchestrator reads
  `workspace/run.json` and resumes at the first stage not `APPROVED`.
- **The design system is the project's, not ours.** `wireframe-ia` is **design-system
  agnostic**: it reuses whatever system the project supplies (or is linkable in Figma) and
  falls back to a documented baseline only when there is none, recording that in
  `assumptions`. What is fixed is the **base-role taxonomy** (`BASE_ROLES` in
  `validators/wireframe.py`), the page/component naming patterns, and the required state,
  responsive and accessibility keys — all in `../rules/CONTRACTS.md` § Stage 4. Colour is
  always a token, never a raw hex or `rgb()`; `px` is allowed because the breakpoints and
  the 44×44px touch minimum are px by definition. Reuse before you create — a `new`
  component needs a `why_new` — and a need outside the taxonomy is a "Design System Gap",
  never an invented role.
- **Human-readable output by default.** Each stage renders its result as Markdown and
  shows that at the HITL gate — never a raw JSON dump.
- **Every stage persists both formats.** All five stages write
  `output/<stage>-<slug>.{json,md}`, reusing one kebab-case `<slug>` per run and
  overwriting on re-run — never a timestamp suffix.
- **`wireframe-ia` also renders to Figma.** It creates a new **high-fidelity** Figma
  design file per run from the spec — real components, Auto Layout, variables bound to the
  resolved design system's tokens, variants for meaningful states, and **prototype
  connections** for every `prototype_flows` entry — and records the URL in
  `figma_file_url`.
- **Status vocabulary** (`stage_status`, `run.json`): `PENDING`, `RUNNING`,
  `AWAITING_APPROVAL`, `APPROVED`, `ESCALATED`.

## Working on this repo

- Add a phase → new `skills/<name>/SKILL.md`, new `validators/<name>.py`, new
  `../rules/rubrics/<name>.md` + a `../rules/CONTRACTS.md` section, new node in
  `orchestrator.py`, extend `ORDER` / `SKILL` there, the `_STAGE_TO_FILE` map in
  `rubrics.py`, and the `Phase` literal in `state.py`.
- Keep `../rules/CONTRACTS.md` Stages 1–4 in sync with
  `.claude/skills/superlap-pipeline/references/contracts.md`, the `BASE_ROLES` /
  `FORBIDDEN` constants and check functions in sync with the vendored `validate_ds.py`,
  the page-builder reference in sync with its `.claude/skills/superlap-*` copies, and each
  `../rules/rubrics/<stage>.md` in sync with the vendored skill's *Quality bar* section.
- Wiring left to do: a real Claude Agent SDK call in `invoke_skill()`, and the model call
  in `orchestrator._judge_model()`. Both are stubbed (the rubric scoring around the judge
  model is real); `python ux-pipeline/rubrics.py --check` validates the rubric files.
- Deps beyond `langgraph`: `langgraph-checkpoint-sqlite` for durable resume.
- `skills/wireframe-ia/references/material-design-tokens.json` is the **baseline** token
  set used only when the project supplies no design system of its own — colour roles,
  typescale, shape-corner scale, elevation levels, the 4dp spacing grid, and per-platform
  insets. Specs reference tokens by name; the values exist so the Figma step can create
  matching Figma variables. Page, component, responsive, state and accessibility narrative
  lives in `assets/component-patterns.md`.
