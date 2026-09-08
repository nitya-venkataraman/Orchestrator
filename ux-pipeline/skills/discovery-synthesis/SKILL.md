---
name: discovery-synthesis
description: Use this skill when raw qualitative UX research (interview transcripts, survey CSVs, support tickets, competitor notes) needs to be synthesized into thematic insights. Triggered as Node 1 of the UX pipeline.
---

# Discovery & Research Synthesis

## Steps
1. Ingest `raw_research_data` from state.
2. Extract recurring pain points and verbatim user quotes.
3. Cluster findings into thematic affinity groups (2–6 themes).
4. Count `frequency` as distinct participants, not mentions. Declare what the corpus
   cannot answer in `gaps`.
5. **Self-check.** Run `python ux-pipeline/validators/synthesis.py <your .json>` and fix every
   violation before returning — quotes must be verbatim substrings of the corpus.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 1 — discovery-synthesis** for the JSON shape,
and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/discovery-synthesis.md`](../../../rules/rubrics/discovery-synthesis.md).
Do not invent data not present in the input.

1. Return `synthesized_insights` (the Stage-1 JSON artifact) to state.
2. Persist `output/discovery-synthesis-<slug>.json` (pretty-printed) and
   `output/discovery-synthesis-<slug>.md` (the Research Synthesis Report: per theme —
   name, severity, one-line behavioral insight, supporting quotes with sources; then a
   Gaps list). Reuse one kebab-case `<slug>` for the whole run; overwrite on re-run,
   never suffix a timestamp.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
