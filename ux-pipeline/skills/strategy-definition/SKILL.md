---
name: strategy-definition
description: Use this skill to convert synthesized research insights into personas, a current-state journey map, and HMW-framed problem statements. Triggered as Node 2 of the UX pipeline.
---

# Strategy & Definition

## Steps
1. Read `synthesized_insights` from state.
2. Draft exactly 1 primary + 1 secondary persona (name, context, goals, frustrations,
   attributed quote) — every trait answerable with "which theme said that?" and named in
   `grounded_in`.
3. Build a current-state journey map: 4–7 stages with actions, a one-word emotion that
   moves across the journey, friction points, and `dropoff_risk`.
4. Convert top friction points into 3–5 "How Might We" statements — each opens literally
   with "How might we", names a friction (not a feature), stays solution-neutral.
5. **Self-check.** Run `python3 ux-pipeline/validators/strategy.py <your .json>` and fix every
   violation before returning.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 2 — strategy-definition** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/strategy-definition.md`](../../../rules/rubrics/strategy-definition.md).

1. Return `persona_profile`, `journey_map`, `problem_statement` to state.
2. Persist `output/strategy/strategy-<slug>.json` and `output/strategy/strategy-<slug>.md` (persona cards,
   the current-state journey table, the numbered HMW list with `derived_from`). Reuse the
   run's `<slug>`; overwrite on re-run.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
