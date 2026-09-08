---
name: superlap-pipeline
description: Runs the full Superlap UX pipeline end to end — research synthesis, strategy, ideation, page building — with a two-tier quality gate and a human approval checkpoint at every stage, artifact caching so approved stages never re-run, and a direction-, surface- and design-system-selection fork before wireframing (web, mobile, or both). Use whenever someone wants to take raw user research all the way through to responsive, accessible page specs and a Figma prototype, run the UX pipeline, resume a paused run, approve or revise a stage, or pick a design direction or target surface — and whenever they mention the Superlap pipeline, HITL gates, the research-to-design pipeline, or ask to chain the discovery/strategy/ideation/wireframe stages together.
---

# Superlap UX Pipeline — Orchestrator

Drives four stages from raw research to responsive, accessible page specs and a
wired Figma prototype — web, mobile, or both. Each stage is machine-vetted
before a human ever looks at it, so the human spends their attention on
judgment rather than on catching malformed JSON and bad arithmetic.

```
raw research
   │
   ▼ synthesis ─► [tier-1 + tier-2 gate] ─► HITL approve ─┐
   ▼ strategy  ─► [gate] ─► HITL approve ─────────────────┤
   ▼ ideation  ─► [gate] ─► HITL approve ─► SELECT direction + surface + DS
   ▼ wireframe ─► [gate] ─► HITL approve ─► done
```

## The four stages

Each stage is its own skill. Invoke it, or follow its SKILL.md directly if it
is not installed:

| # | Stage | Skill | Threshold |
|---|---|---|---|
| 1 | Discovery synthesis | `superlap-synthesis` | 0.75 |
| 2 | Strategy definition | `superlap-strategy` | 0.75 |
| 3 | Ideation & concepting | `superlap-ideation` | 0.70 |
| 4 | Wireframing & IA (web/mobile pages, responsive, accessible, + build requirements + prototype) | `superlap-wireframe` | 0.80 |

Full contracts, rubrics, and per-stage constraints: `references/contracts.md`.

## Run state

Everything lives under `workspace/` in the working directory, so a run
survives the conversation:

```
workspace/
├── run.json                 # run_id, raw_inputs, stage statuses, selected_direction
├── artifacts/<stage>.json   # the approved artifact per stage
├── cache/<key>.json         # content-addressed stage outputs
└── events.jsonl             # append-only audit trail
```

`workspace/` is orchestration bookkeeping. The **reviewer-facing** artifacts are what
each stage skill writes to the repo's `output/` directory — `discovery-synthesis-<slug>`,
`strategy-<slug>`, `ideation-<slug>`, `wireframe-<slug>`, each as a `.json` (machine
contract) and a `.md` (human rendering). Use one `<slug>` for the whole run.

Before doing anything, check whether `workspace/run.json` exists. If it does,
this is a **resume** — read it and pick up at the first stage that is not
`APPROVED`. Starting a fresh run over an existing one silently discards
approved work, so if the intent is ambiguous, ask.

## Per-stage loop

For each stage in order:

**1. Cache check.** Compute the input hash — `raw_inputs`, prior approved
artifacts, `selected_direction`, `target_surface`, `mobile_platform`,
`design_system_input`, the stage's `revision_feedback`, and its attempt number. Run:

```bash
python scripts/cache.py get <run_id> <stage> <attempt> <input_hash>
```

A hit returns the exact artifact that was produced before. Use it and skip to
step 3. This is what makes resume both free and *correct*: the human sees
byte-for-byte the artifact they approved, not a fresh generation that drifted.

**2. Run the stage** on a miss. Pass the stage its inputs, any prior approved
artifacts as context, and `revision_feedback` if present. Store the result with
`python scripts/cache.py put <run_id> <stage> <attempt> <input_hash> <file>`.

**3. Tier 1 — structural.** Read the stage's `output/<stage>-<slug>.json` and check
its hard rules: schema shape, HMW prefixes, RICE arithmetic recomputed, the
wireframe base-role taxonomy, page and component naming, raw-colour discipline,
the required state / accessibility / responsive keys, and prototype
reachability. These are mechanical and cheap. On failure, increment
the attempt, set `revision_feedback` to the concrete error list, invalidate the
stage's cache, and go back to step 1. Give it at most **2 retries** — a third
identical failure means the brief is wrong, not the generation.

**4. Tier 2 — judge.** Score the artifact against the stage's rubric
(`references/contracts.md`), weighting each criterion and comparing the total
to the threshold. Be strict; an inflated score defeats the purpose of the gate,
and the human downstream is relying on it having been honest. Score below
threshold behaves like a Tier-1 failure, with the weak criteria and their
reasons as the feedback.

Judging your own output has an obvious bias problem. Read the artifact against
the source material as if someone else wrote it and you were asked to find the
weakest claim in it.

**5. HITL checkpoint.** Only artifacts that passed both tiers reach the human.
Present:

- the stage name and the judge's weighted score with the per-criterion breakdown
- the artifact itself, readably — present the stage's `output/<stage>-<slug>.md`
  rendering (for the wireframe stage that includes its `figma_file_url`), not the raw
  JSON
- the ask: **approve**, or **revise with feedback**

Use `AskUserQuestion` where available so approve/revise is one click. Record
the checkpoint in `events.jsonl` before waiting.

On approve: write `workspace/artifacts/<stage>.json`, mark the stage
`APPROVED` in `run.json`, reset its attempt counter, clear its feedback, move
on.

On revise: store the human's feedback, **invalidate that stage's cache**
(`python scripts/cache.py invalidate <run_id> <stage>`) so the rerun genuinely
regenerates instead of returning the artifact they just rejected, and loop.
Human feedback resets the retry counter — a human asking for a change is not a
failed attempt.

## The selection fork

After ideation is approved, the human makes two choices before wireframing:

1. **One design direction.** Present the 2–3 directions with their
   differentiators and tradeoffs and ask for one. Do not recommend a winner
   unless asked — the fork exists precisely because this is a judgment call
   about product strategy, and a nudge here quietly decides the rest of the
   pipeline.
2. **The target surface** — **web, mobile, or both**. It decides breakpoints
   versus safe areas and the page-naming family. If the surface includes mobile,
   also ask **Android or iOS** for the platform conventions (nav pattern,
   safe-area insets, touch-target minimum, system font).
3. **The design system** — ask whether the project has one (a component library,
   token file, Figma library, styleguide, or existing code) and take whatever
   they have. Stage 4 is design-system agnostic and reuses it. If they have
   none, it falls back to a documented baseline and records that as an
   assumption.

Write `selected_direction`, `target_surface`, `mobile_platform`, and
`design_system_input` to `run.json`. All become part of the cache key for
wireframing, so changing any of them later correctly invalidates the wireframe
and nothing upstream.

## Finishing

When wireframe is approved, write a run summary: the four artifacts (link each stage's
`output/<stage>-<slug>.json` and `.md`), the score per stage, the number of revisions
each took, the selected direction, the target surface (and mobile platform), the
resolved design system, and the wireframe's `figma_file_url`. If the wireframe
declared `design_system_gaps` or `assumptions`, surface them — they are findings
the design system owner and the product owner need, and they get lost if they
stay inside the JSON.

## If the user asks for the code

This skill runs the pipeline conversationally. The deployable CrewAI +
FastAPI + Streamlit implementation of the same design is a separate skill,
`superlap-scaffold`.
