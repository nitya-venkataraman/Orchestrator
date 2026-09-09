---
name: delivery-handoff
description: Use this skill to translate approved wireframes/IA into developer-ready Jira user stories, acceptance criteria, and UX microcopy. Triggered as Node 5 (final) of the UX pipeline.
---

# Delivery & Handoff

## Steps
1. Read `sitemap`, `wireframe_specs`, and `persona_profile` from state.
2. Write user stories: "As a **[persona]**, I want to **[capability]**, so that I can
   **[benefit]**." Each story names the Stage-2 `persona` it serves and the Stage-4
   `screen` it lands on, and carries ≥ 1 acceptance criterion as explicit
   Given/When/Then. Every screen in `wireframe_specs` is covered by ≥ 1 story.
3. Generate microcopy: CTA labels, empty states, error states, confirmation messages —
   matching the product voice (sentence-case verb-first CTAs ≤ 4 words, not ALL CAPS;
   error copy that states what happened then what to do with no apology; empty states
   that offer exactly one action).
4. **Self-check.** Run `python3 ux-pipeline/validators/delivery.py <your .json>` and fix every
   violation before returning.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 5 — delivery-handoff** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/delivery-handoff.md`](../../../rules/rubrics/delivery-handoff.md).

1. Return `developer_handoff_stories` (the `stories` list) and `microcopy` to state.
2. Persist to the repo `output/delivery/` directory, reusing the run's `<slug>`:
   - `output/delivery/delivery-<slug>.json` — `{ "stories": [...], "microcopy": {...} }`,
     pretty-printed.
   - `output/delivery/delivery-<slug>.md` — human-readable: one block per story (`### US-<n>: …`
     with the As-a/I-want/so-that sentence and a Given/When/Then acceptance-criteria
     list), then microcopy tables grouped by screen.
   Overwrite on re-run; never suffix a timestamp.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
