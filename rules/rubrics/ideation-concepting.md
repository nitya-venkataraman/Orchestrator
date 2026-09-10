# Rubric — Stage 3: ideation-concepting

Scores an `IdeationOutput` artifact (RICE-scored features + 2–3 design directions). Read
[`README.md`](README.md) first. Tier-1 (`ux-pipeline/validators/ideation.py`) already
recomputes every RICE score, so this rubric judges *judgment* — whether the inputs are
honest and the directions are real alternatives.

This stage is deliberately the most lenient in the pipeline (`pass_when` below): divergence
should not be punished as hard as fabrication.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `hmw_linkage` | 0.30 | Every feature answers a specific Stage-2 HMW, and across the set every HMW has at least one feature. The `hmw` field is the real driver, not a label attached afterward. |
| `rice_integrity` | 0.30 | `reach` is grounded in `source_count` / segment sizes or a stated assumption; `impact` and `confidence` are defensible from the research; no input was nudged to move a favored feature up the list. Each `success_metric` names something that would actually move if the feature worked, and its `baseline` is a real figure or an honest `"unknown"`. |
| `direction_distinctness` | 0.40 | Each direction is a different *bet about how to solve the problem*. State each one's central bet in a sentence and a reasonable team could disagree about which is right. |

## Score anchors

### `hmw_linkage`
- **5** — Every feature maps cleanly to one HMW; every HMW is addressed; the mapping would survive someone checking it.
- **3** — Mapping is mostly sound but one feature is stretched onto an HMW it only loosely serves, or one HMW has no feature.
- **1** — Features are a generic backlog with HMW labels bolted on, or several HMWs are unaddressed.

### `rice_integrity`
- **5** — Inputs are individually defensible from the synthesis; `reach` figures trace to stated populations; the ranking reflects real priority. Every `success_metric` is one a team could actually compute, and an unknown baseline is declared rather than invented.
- **3** — Arithmetic is right (Tier-1 enforces that) but one or two `reach` or `confidence` values look optimistic for the evidence, `impact` is smoothed (everything a 2), or a `success_metric` restates the feature instead of naming an outcome ("users use the timeline").
- **1** — Inputs are visibly reverse-engineered from a desired ranking; a favored feature carries a `reach` or `confidence` the research can't support, or a baseline was estimated into existence to make a target look reachable.

### `direction_distinctness`
- **5** — 2–3 directions, each a distinct bet with a named `differentiator` and a real `tradeoff`; they are not all compatible.
- **3** — Directions differ in emphasis or surface but share the same underlying bet; you'd be tempted to just build all of them.
- **1** — One idea with three names; the `tradeoff` fields are cosmetic or near-identical.

## Calibration

`direction_distinctness` carries the most weight because the pipeline forks here — a human
picks one direction and it shapes everything downstream. Three directions that are really
one means the choice is fake. Useful axes for telling real directions apart: who does the
work (user vs system), when the value lands (in-the-moment vs after-the-fact), how much the
user has to trust the product, whether it fixes the workflow or replaces it. If you can't
name which axis separates two directions, they're not separate.

`rice_integrity` is not about the arithmetic — Tier-1 already recomputed it. It's about
whether the *inputs* are honest. The one thing that makes a prioritization worthless is
skewing a `reach` or `confidence` to move a score.

## Common failure modes

- Uniform features within an HMW — stopped at the first idea instead of spanning "serve
  the need / remove the need / change who does the work".
- `confidence: 1.0` on a feature whose evidence is one comment.
- A `success_metric` that measures usage of the feature rather than the outcome it was
  built for — "extraction screen opened" instead of "hours to first committed model".
- A fabricated baseline. `"unknown"` is the correct answer far more often than a run
  admits, and Stage 6 exists to plan how to establish it.
- A direction described as a visual theme ("clean and minimal") rather than a bet.
- `tradeoff` that isn't actually a cost ("tradeoff: requires good design").
- The skill recommending a winning direction (it must not — that's the human's call).

```json
{
  "stage": "ideation-concepting",
  "weights": {
    "hmw_linkage": 0.30,
    "rice_integrity": 0.30,
    "direction_distinctness": 0.40
  },
  "pass_when": "min>=3 and weighted_mean>=3.7"
}
```
