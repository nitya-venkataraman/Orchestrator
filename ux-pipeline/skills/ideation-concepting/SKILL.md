---
name: ideation-concepting
description: Use this skill to brainstorm and prioritize features and propose UX design directions from problem statements and personas. Triggered as Node 3 of the UX pipeline.
---

# Ideation & Concepting

## Steps
1. Read `problem_statement` and `persona_profile`.
2. Brainstorm 6–12 features; every feature declares the `hmw` it answers (matching a
   Stage-2 HMW verbatim). Aim for range within each HMW.
3. Score each feature with RICE — `impact` ∈ {0.25, 0.5, 1, 2, 3},
   `confidence` ∈ {0.5, 0.8, 1.0}, `effort` ≥ 0.5, `reach` ≥ 1. Compute
   `(reach × impact × confidence) / effort`, round to one decimal. Do not inflate inputs.
4. Propose 2–3 genuinely distinct design directions — each a different bet, with a
   named `differentiator` and an explicit `tradeoff`. Never select a winner.
5. **Self-check.** Run `python3 ux-pipeline/validators/ideation.py <your .json>` — it recomputes every
   RICE score — and fix every violation before returning.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 3 — ideation-concepting** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/ideation-concepting.md`](../../../rules/rubrics/ideation-concepting.md).

1. Return `feature_matrix` (the `features` list) and `concept_proposals` (the
   `design_directions` list) to state. The winner is a human decision at the selection
   fork.
2. Persist `output/ideation/ideation-<slug>.json` and `output/ideation/ideation-<slug>.md` (the RICE table
   sorted by score descending, then the directions with differentiator and tradeoff, then
   a closing line that the human picks). Reuse the run's `<slug>`; overwrite on re-run.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
