# Rubric — Stage 6: evaluation-planning

Scores an evaluation plan (`usability_test` + `metric_plan` + `open_baselines`).
Read [`README.md`](README.md) first. Tier-1
(`ux-pipeline/validators/evaluation.py`) already checks that the objective and
consequence are stated, that participants resolve to Stage-2 personas, that every
task names a real journey stage and real pages, that every Stage-3
`success_metric` has exactly one plan entry whose events resolve to Stage-5
analytics events, and that unknown baselines are declared — this rubric judges
whether the plan would actually *produce evidence*, or merely produce a report.

This is the only stage that looks backwards. Everything before it makes claims:
themes claim what users need, HMWs claim what the problem is, RICE claims what
matters, the design claims it will work. This stage plans how those claims get
checked. Score it as the pipeline's honesty mechanism, because that is what it is.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `task_fidelity` | 0.40 | Each task is a real thing this persona does, phrased as a goal in their words, with no clue to the interface built into the wording. Success criteria are observable behaviour someone could score from a recording, not satisfaction or opinion. |
| `risk_coverage` | 0.30 | The plan tests where the design is most likely to be wrong — the high-severity `heuristic_review` findings, the pages the primary journey depends on, and the design decisions that came from an assumption rather than from evidence. Not the easy paths. |
| `metric_integrity` | 0.30 | Every metric's events could genuinely compute it; `read_after` is honest about when a signal will exist; unknown baselines are listed with a real way to establish them rather than parked. |

## Score anchors

### `task_fidelity`
- **5** — Tasks read like the participant's own goal ("You've been assigned this borrower and need to be ready for review by Thursday — get started"), never the interface's ("Click the extract button and commit the terms"). Success criteria are observable: completed without assistance, found the figure's source within N seconds, recovered from the failed feed unaided.
- **3** — Tasks are real but leak the solution in their wording, or one or two success criteria are attitudinal ("user finds it intuitive", "participant is satisfied").
- **1** — Tasks are a feature tour. Criteria are unfalsifiable, or the plan tests whether people can use the UI rather than whether the UI solves their problem.

### `risk_coverage`
- **5** — The tasks concentrate on the risky parts: what the heuristic review flagged as high, what the design does differently from what users do today, the recovery paths the error scenarios describe. `what_would_change_the_design` names a specific change a specific result would trigger.
- **3** — Reasonable coverage of the main journey, but the known-shaky parts get the same attention as the settled ones, or `what_would_change_the_design` is generic ("we would iterate on the findings").
- **1** — Tests the happy path only, or tests the parts already known to work. A plan that cannot fail.

### `metric_integrity`
- **5** — Each metric's named events carry the properties needed to compute it; `read_after` reflects real accrual time rather than "post-launch"; every unknown baseline has a stated way to establish it, and the plan says which metrics simply cannot be read yet.
- **3** — Plan is complete but one or two metrics rely on events that could not actually compute them, or a row names no events where an event plainly could have carried it, or `read_after` is uniformly vague, or open baselines are listed without any route to closing them.
- **1** — The metric plan restates the Stage-3 metrics with no mechanism behind them, or claims baselines the pipeline never established.

## Calibration

`task_fidelity` is where a plan quietly becomes a demo. The tell is the verb: a
task that tells the participant *what to do in the interface* has already given
away the thing being tested. Read each scenario and ask whether someone who had
never seen the design could still attempt it — if not, it is a script, not a task.

`risk_coverage` is graded against the Stage-4 `heuristic_review`. Every
high-severity finding there is a hypothesis about where this design fails; a plan
that tests none of them is not evaluating this design, it is evaluating a
generic one. Cross-check the two lists explicitly before scoring.

`metric_integrity` is not about whether the metrics are good — Stage 3's
`rice_integrity` covers that. It is about whether they can be *read*. A metric
whose events do not carry the identifier or the duration it needs is a metric
nobody will ever compute, and it will be quietly dropped three months in.

## Common failure modes

- Tasks worded as instructions ("Use the search bar to find…") rather than goals.
- Success criteria that are opinions ("participant reports the flow is clear").
- Five participants recruited from one segment when the research named three personas.
- No task touching any high-severity `heuristic_review` finding.
- `what_would_change_the_design` that commits to nothing.
- `read_after: "after launch"` on every metric regardless of how long the signal takes.
- An `open_baselines` list that is a graveyard — no method, no owner, no date.
- An empty `events` list used to dodge instrumentation on a metric the product
  could obviously emit, with `baseline_source` waving at "reporting".
- A metric plan that covers the easy metrics and silently omits the one the
  business case rests on. (Tier-1 catches the omission; this catches the version
  where it is present but hollow.)

```json
{
  "stage": "evaluation-planning",
  "weights": {
    "task_fidelity": 0.40,
    "risk_coverage": 0.30,
    "metric_integrity": 0.30
  },
  "pass_when": "min>=4 or (min>=3 and weighted_mean>=4.0)"
}
```
