---
name: discovery-synthesis
description: Use this skill when raw qualitative UX research (interview transcripts, survey CSVs, support tickets, competitor notes) needs to be synthesized into thematic insights. Triggered as Node 1 of the UX pipeline.
allowed-tools: Read, Write, Bash
---

# Discovery & Research Synthesis

## Steps
1. Ingest `raw_research_data` from state. Load `references/synthesis-method.md` —
   it carries the clustering test, the severity derivation table, the participant-ID
   rule for `source`, and what belongs in `gaps`.
2. Extract recurring pain points and verbatim user quotes.
3. Cluster findings into thematic affinity groups (2–6 themes).
4. Count `frequency` as distinct participants, not mentions. Derive `severity` from
   frequency × consequence rather than from how bad the quotes sound. Declare what the
   corpus cannot answer in `gaps`.
5. **Describe the corpus, and protect the people in it.** Fill `corpus` — `method`,
   `participant_count`, `segments`, `collection_window`, `known_bias`. A reader
   cannot judge six themes without knowing whether they came from six power users or
   sixty strangers, and every downstream stage treats this artifact as the complete
   picture. Attribute every quote with a participant identifier (`P07`,
   `Ticket-4412`, `Interview 3`), optionally followed by a role — **never a name, an
   employer, or an email**. This artifact travels further than the raw corpus ever
   does, and the same rule applies to the Markdown you render from it.
6. **Self-check.** Run `python3 ux-pipeline/validators/synthesis.py <your .json>` and fix every
   violation before returning — quotes must be verbatim substrings of the corpus.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 1 — discovery-synthesis** for the JSON shape,
and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/discovery-synthesis.md`](../../../rules/rubrics/discovery-synthesis.md).
Do not invent data not present in the input.

1. Return `synthesized_insights` (the Stage-1 JSON artifact) to state.
2. Persist `output/<project-slug>/discovery-synthesis.json` (pretty-printed) and
   `output/<project-slug>/discovery-synthesis.md` (the Research Synthesis Report: per theme —
   name, severity, one-line behavioral insight, supporting quotes with sources; then the
   Corpus block and a Gaps list). One folder per project, named by a kebab-case `<project-slug>` reused for
   the whole run; create it if absent; overwrite on re-run, never suffix a timestamp.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
