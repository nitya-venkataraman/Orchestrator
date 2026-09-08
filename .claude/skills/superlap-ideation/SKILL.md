---
name: superlap-ideation
description: Stage 3 of the Superlap UX pipeline. Turns How-Might-We statements and personas into RICE-prioritized features plus 2-3 genuinely distinct design directions, as validated JSON with arithmetically correct RICE scores. Use whenever someone needs feature ideation, RICE or impact/effort prioritization, a prioritized backlog from problem statements, or competing concept directions to choose between — and whenever they mention ideation, concepting, RICE scoring, feature prioritization, design directions, or the Superlap pipeline. Also use it as stage 3 when running the full pipeline. Never pick the winning direction; that is the human's call.
---

# Ideation & Concepting — Stage 3

HMWs in, `IdeationOutput` JSON out. Two things get checked mechanically here:
**the RICE arithmetic** (recomputed, not trusted) and **direction
distinctness** (three names on one idea is the most common failure in this
stage).

You do not select a winner. The pipeline halts after this stage and a human
picks the direction to carry into wireframing — that fork is the point.

## Inputs

- `strategy` (required) — Stage 2 `StrategyOutput` JSON.
- `synthesis` (optional) — Stage 1 output, for grounding checks.
- `revision_feedback` (optional).

## Method

**Features — 6 to 12.** Generate against each HMW; every feature declares the
`hmw` it answers. Aim for range within each HMW: one obvious answer, one that
removes the need rather than serving it, one that changes who does the work.
Uniform features across an HMW usually means you stopped at the first idea.

**RICE, computed honestly.**

```
rice_score = (reach × impact × confidence) / effort
```

- `reach` — users affected per quarter. A count, not a rating. Ground it in
  `source_count` and segment sizes from the research where you can; where you
  can't, use a stated assumption and drop `confidence`.
- `impact` — one of `0.25, 0.5, 1, 2, 3` (minimal → massive). These five values
  only; a 1.5 signals you're smoothing rather than deciding.
- `confidence` — `0.5`, `0.8`, or `1.0` (low / medium / high). High confidence
  needs evidence in the synthesis, not conviction.
- `effort` — person-months, minimum 0.5.

Compute the score and round to one decimal. The validator recomputes it and
fails a mismatch greater than 0.5, so a stated score that "feels right" but
doesn't divide out will bounce back to you. Do the arithmetic.

Resist inflating `reach` on the features you like. Skewing an input to move a
score is the one thing that makes the whole prioritization worthless.

**Design directions — 2 to 3, genuinely different.** A direction is a *bet
about how to solve the problem*, not a visual theme. Each names its
`differentiator`, the `hmws_addressed`, and — importantly — its `tradeoff`.

The distinctness test: state each direction's central bet in one sentence and
check that a reasonable team could disagree about which is right. If all three
bets are compatible and you'd just build all of them, you have one direction
with three feature sets.

Useful axes for pulling directions apart: who does the work (user vs system),
when the value lands (in-the-moment vs after-the-fact), how much the user has
to trust the product, and whether it fixes the workflow or replaces it.

## Output contract

Every run produces three things:

1. **The validated JSON artifact** — the schema below, unchanged. It stays the machine
   contract: the Tier-1 validator recomputes the RICE arithmetic against it and Stage 4
   parses it literally. Do not rename fields, add prose inside it, or drop required keys.
2. **Two files written to the repo's `output/` directory:**
   - `output/ideation-<slug>.json` — the JSON artifact, pretty-printed
   - `output/ideation-<slug>.md` — the human-readable rendering (see **Rendering** below)

   Use the **same `<slug>`** as the earlier stages so a run's files line up. Overwrite on
   re-run — never suffix a timestamp.
3. **Your visible reply is the Markdown rendering** — the exact contents of the `.md`
   file, and nothing else. Do not paste the raw JSON into the reply; it lives in the
   `.json` file. Show the JSON only if asked.

```json
{
  "features": [
    {
      "name": "string",
      "description": "string — one sentence",
      "hmw": "the HMW statement this answers",
      "reach": 0,
      "impact": 0.25,
      "confidence": 0.8,
      "effort": 1.0,
      "rice_score": 0.0
    }
  ],
  "design_directions": [
    {
      "name": "string — memorable, 2-4 words",
      "summary": "string — the central bet, one or two sentences",
      "differentiator": "string — what only this direction does",
      "hmws_addressed": ["How might we ..."],
      "tradeoff": "string — what this direction gives up"
    }
  ]
}
```

Validator constraints:

- 6–12 features; every `hmw` matches an HMW statement from the input strategy.
- `impact` ∈ {0.25, 0.5, 1, 2, 3}; `confidence` ∈ {0.5, 0.8, 1.0};
  `effort` ≥ 0.5; `reach` ≥ 1.
- `rice_score` within 0.5 of the recomputed value.
- 2–3 design directions, each with a non-empty `tradeoff`.

## Rendering

The `.md` file — and your visible reply — follows the format already established in
`output/ideation-flight-booking.md`. Required sections:

- `# Ideation & Concepting — <Project>` title + one-line summary.
- `## Feature Backlog (RICE)` — a Markdown table sorted by `rice_score` descending,
  columns: Feature, HMW, Reach, Impact, Confidence, Effort, RICE. One row per feature.
- `## Design Directions` — one block per direction (`### <name>`) with the central bet,
  the differentiator, the HMWs it addresses, and the tradeoff called out explicitly.
- A closing line stating the human picks the direction; the skill never recommends one.

Keep it scannable: a designer reads this, not the JSON.

## Quality bar

Judge threshold **0.70** — lower than its neighbours, because divergence
should not be punished as hard as fabrication.

| Criterion | Weight | What it checks |
|---|---|---|
| `hmw_linkage` | 0.30 | Every feature maps to a specific HMW |
| `rice_integrity` | 0.30 | Scores internally consistent and inputs not inflated |
| `direction_distinctness` | 0.40 | Directions are genuinely different approaches |

## Revision handling

`revision_feedback` is direction on the previous artifact. If the note is
"directions are too similar", the fix is to change one direction's underlying
bet — not to rename it or restate its summary more emphatically. If the note is
a RICE mismatch, recompute rather than adjusting the stated score to match.
