---
name: evaluation-planning
description: Use this skill to turn an approved design and handoff into a usability test plan and a measurement plan — the tasks that would show whether the design works, and the instrumentation that would show whether it worked. Triggered as Node 6 (final) of the UX pipeline.
allowed-tools: Read, Write, Bash
---

# Evaluation Planning

Stages 1–5 are generative: they research, frame, ideate, design and hand off, and
every one of them makes a claim. Themes claim what users need. HMWs claim what the
problem is. RICE claims what matters. The design claims it will work. **This stage
plans how those claims get checked** — it is the only place the pipeline looks
back at itself.

It plans evaluation; it does not run it. The output is a plan a team executes
after the build.

## Steps

1. Read `journey_map`, `feature_matrix` (for the `success_metric` on each
   feature), `wireframe_specs`, the Stage-4 `heuristic_review`, and
   `developer_handoff_stories` (for the `analytics_events`).
2. **State the objective and the consequence.** What decision is this test meant
   to inform, and — in `what_would_change_the_design` — what specific result
   would cause what specific change. A test whose outcome would change nothing is
   theatre; naming the consequence first is what stops it being run for
   reassurance.
3. **Recruit from the research.** `participants.segments` names Stage-2 personas,
   `count` ≥ 5, and `recruit_from` says where they actually come from. Testing
   with people the research never described tells you about a different product.
4. **Write 3–8 tasks.** Each is a real thing that persona does, phrased as *their
   goal in their words* — never as interface instructions. "You've been assigned
   this borrower and need to be ready for review by Thursday" is a task; "click
   Extract and commit the terms" is a script that has already given away what you
   were testing. Each task names the Stage-2 `journey_stage` it exercises and the
   Stage-4 `pages` it touches.
5. **Make success observable.** `success_criteria` is behaviour someone could
   score from a recording — completed unaided, found the source within a stated
   time, recovered from the failed feed without help. Not "found it intuitive".
6. **Aim at the risk.** Use `probes` to tie tasks to the Stage-4
   `heuristic_review` findings. Every high-severity finding there is a hypothesis
   about where *this* design fails; a plan that tests none of them is evaluating
   a generic design. Test what is most likely wrong, not what is known to work.
7. **Plan the measurement.** Every Stage-3 `success_metric` gets exactly one
   `metric_plan` row: the Stage-5 `analytics_events` that compute it, where the
   `baseline_source` comes from, and `read_after` — the honest point at which
   enough signal exists, not "after launch" on everything.
8. **Declare what you still don't know.** Every metric whose Stage-3 `baseline`
   is `"unknown"` goes in `open_baselines`, with how it would be established.
   Not knowing a baseline is allowed; losing track of which ones you don't know
   is not.
9. **Self-check.** Run `python3 ux-pipeline/validators/evaluation.py <your .json>`
   and fix every violation before returning.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 6 — evaluation-planning** for
the JSON shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/evaluation-planning.md`](../../../rules/rubrics/evaluation-planning.md).

1. Return `evaluation_plan` (the whole artifact) to state.
2. Persist `output/<project-slug>/evaluation.json` and
   `output/<project-slug>/evaluation.md` — the Markdown being the test plan as a
   team would run it: objective and what would change the design, participants,
   one block per task (scenario, what it probes, success criteria, pages), then
   the metric plan as a table, then open baselines. Reuse the run's
   `<project-slug>` folder; overwrite on re-run, never suffix a timestamp.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
