---
name: strategy-definition
description: Use this skill to convert synthesized research insights into personas, a current-state journey map, and HMW-framed problem statements. Triggered as Node 2 of the UX pipeline.
---

# Strategy & Definition

## Steps
1. Read `synthesized_insights` from state.
2. Draft 1 primary + 1 secondary persona (name, goals, frustrations, quote) — grounded only in themes from step 1.
3. Build a current-state journey map (stages, actions, emotions, friction points, drop-off risks).
4. Convert top friction points into 3-5 "How Might We" problem statements.

## Output contract
Return `persona_profile`, `journey_map`, `problem_statement`.
