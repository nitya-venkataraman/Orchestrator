---
name: delivery-handoff
description: Use this skill to translate approved wireframes/IA into developer-ready Jira user stories, acceptance criteria, and UX microcopy. Triggered as Node 5 of the UX pipeline; Node 6 then plans how the design gets evaluated.
allowed-tools: Read, Write, Bash
---

# Delivery & Handoff

## Steps
1. Read `sitemap`, `wireframe_specs`, and `persona_profile` from state, and load
   `references/handoff-checklist.md` — what "buildable" includes, how to derive
   accessibility criteria from a page's own block, what makes an analytics event
   computable, and the content-design rules beyond voice.
2. Write user stories: "As a **[persona]**, I want to **[capability]**, so that I can
   **[benefit]**." Each story names the Stage-2 `persona` it serves and the Stage-4
   `screen` it lands on, and carries ≥ 1 acceptance criterion as explicit
   Given/When/Then. Every screen in `wireframe_specs` is covered by ≥ 1 story.
3. **Carry the accessibility across.** Stage 4 designed accessibility in per page;
   if you don't turn it into criteria, none of it is testable and all of it is lost
   here. Every Stage-4 page needs ≥ 1 story with a non-empty
   `accessibility_criteria`, each a full Given/When/Then derived from *that page's*
   `accessibility` block — its keyboard path, its labels and error identification,
   or what its `status_messages` says gets announced. Not a generic a11y checklist.
4. **Instrument what writes.** Any story landing on a page whose `primary_action`
   writes data carries `analytics_events` — `{event, trigger, properties}` — naming
   the instrumentation that makes the feature's Stage-3 `success_metric` observable
   after ship. A metric nothing emits is not a metric. Read pages need no events;
   an event on every page is noise.
5. Generate microcopy: CTA labels, empty states, error states, confirmation messages —
   matching the product voice (sentence-case verb-first CTAs ≤ 4 words, not ALL CAPS;
   error copy that states what happened then what to do with no apology; empty states
   that offer exactly one action). Plain language at the persona's reading level, and
   no string so tight that a 30% longer translation breaks its control.
6. **Self-check.** Run `python3 ux-pipeline/validators/delivery.py <your .json>` and fix every
   violation before returning.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 5 — delivery-handoff** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/delivery-handoff.md`](../../../rules/rubrics/delivery-handoff.md).

1. Return `developer_handoff_stories` (the `stories` list) and `microcopy` to state.
2. Persist to the run's project folder, `output/<project-slug>/`:
   - `output/<project-slug>/delivery.json` — `{ "stories": [...], "microcopy": {...} }`,
     pretty-printed.
   - `output/<project-slug>/delivery.md` — human-readable: one block per story (`### US-<n>: …`
     with the As-a/I-want/so-that sentence, a Given/When/Then acceptance-criteria
     list, then its accessibility criteria and analytics events where it has them),
     then microcopy tables grouped by screen.
   Overwrite on re-run; never suffix a timestamp.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
