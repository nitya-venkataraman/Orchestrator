---
name: superlap-synthesis
description: Stage 1 of the Superlap UX pipeline. Turns raw qualitative research — interview transcripts, survey exports, support tickets, sales-call notes, app-store reviews, competitor teardowns — into evidence-backed themes as validated JSON, where every theme carries verbatim quotes and nothing is invented. Use this whenever someone has a pile of user research and needs it synthesized, coded, clustered, or turned into themes/insights/affinity groups, and whenever they mention discovery synthesis, thematic analysis, research readout, or the Superlap pipeline. Also use it as the first stage when running the full pipeline.
---

# Discovery Synthesis — Stage 1

Raw research in, `SynthesisOutput` JSON out. The hard constraint is
**evidence grounding**: a theme that cannot point at a real quote from the
supplied sources does not exist. This is the stage where fabrication does the
most damage, because every downstream stage — personas, HMWs, features,
screens — inherits it and the invention becomes invisible.

## Inputs

- `raw_inputs` (required) — the research corpus. Any mix of transcripts, CSV
  exports, ticket dumps, notes, pasted text, or file paths.
- `revision_feedback` (optional) — reviewer direction on your previous output.

Read every source before clustering. If a source is a file path, open it. If
something is unreadable or truncated, say so in `gaps` rather than working
around it silently.

## Method

1. **Code before you cluster.** Pass through the corpus and pull discrete
   observations — a pain, a workaround, a stated goal, an emotional beat —
   each with its verbatim quote and its source. Resist naming themes yet;
   naming early makes you sort evidence into the names instead of the reverse.
2. **Cluster by shared cause, not shared vocabulary.** Two people saying
   "it's slow" about different things are two themes. Two people describing
   the same broken handoff in different words are one.
3. **Cap at 6 themes.** More than six means you clustered by vocabulary. Merge
   the weakest until the set is genuinely distinct.
4. **Count honestly.** `frequency` is how many distinct participants raised it,
   not how many times it was said. One loud participant is `frequency: 1`.
5. **Write the insight as behavior, not sentiment.** "Users are frustrated by
   exports" is a restatement. "Users rebuild the export by hand in Sheets
   because they don't trust the totals" is an insight — it names the behavior
   and the belief driving it.
6. **Declare what's missing.** `gaps` is where you record signals you'd expect
   but don't see, segments absent from the corpus, and questions the data
   can't answer. A synthesis with an empty `gaps` array is usually a synthesis
   that wasn't looking.

## Output contract

Every run produces three things:

1. **The validated JSON artifact** — the schema below, unchanged. It stays the machine
   contract: the Tier-1 validator and every downstream stage parse it literally. Do not
   rename fields, add prose inside it, or drop required keys.
2. **Two files written to the repo's `output/` directory:**
   - `output/discovery-synthesis-<slug>.json` — the JSON artifact, pretty-printed
   - `output/discovery-synthesis-<slug>.md` — the human-readable rendering (see
     **Rendering** below)

   Derive `<slug>` as a kebab-case project name: an explicit `slug` input if given, else
   the project / brief name, else inferred from the raw inputs (a NYC→ATL booking
   teardown → `flight-booking`). Reuse the same slug for every stage of one run so the
   files line up. Overwrite on re-run — never suffix a timestamp.
3. **Your visible reply is the Markdown rendering** — the exact contents of the `.md`
   file, and nothing else. Do not paste the raw JSON into the reply; it lives in the
   `.json` file. Show the JSON only if asked.

```json
{
  "themes": [
    {
      "name": "string — 2-5 words, names the behavior",
      "insight": "string — one sentence: what people do and why",
      "frequency": 0,
      "quotes": [
        {"text": "verbatim, unedited", "source": "P07 / ticket-4412 / survey row 88"}
      ],
      "severity": "high | medium | low"
    }
  ],
  "gaps": ["string — what the corpus cannot tell us"],
  "source_count": 0
}
```

Constraints the validator enforces:

- 2–6 themes; each theme has ≥ 1 quote; quotes are verbatim substrings of the
  supplied sources — do not clean up grammar, trim filler, or merge two
  utterances into one quote.
- `frequency` ≥ 1 and ≤ `source_count`.
- `severity` is exactly one of `high`, `medium`, `low`.

## Rendering

The `.md` file — and your visible reply — follows the format already established in
`output/discovery-synthesis-flight-booking.md`. Required sections:

- `# Discovery Synthesis — <Project>` title, then a one-line corpus summary: how many
  sources, what they are, and any caveat (e.g. every theme `frequency: 1` because one
  person produced the teardown).
- `## Themes` — one `### <n>. <name> — severity: <sev>` per theme, each with the
  behavioral insight as a short paragraph, then the supporting quotes as a bullet list
  with their source in parentheses.
- `## Gaps` — the `gaps` array as a bullet list.

Keep it scannable: a designer reads this, not the JSON.

## Quality bar (how this is scored)

A judge scores the artifact before any human sees it. Threshold **0.75**.

| Criterion | Weight | What it checks |
|---|---|---|
| `evidence_grounding` | 0.40 | Every theme traces to real quotes; no invented insight |
| `theme_distinctness` | 0.25 | Themes don't overlap or restate each other |
| `signal_coverage` | 0.35 | High-frequency signals in the raw data are all captured |

`signal_coverage` is the one people lose. Before emitting, re-scan the corpus
for anything mentioned by three or more participants and confirm it landed in
a theme. A tidy, distinct, well-quoted synthesis that dropped the most common
complaint still fails.

## Revision handling

When `revision_feedback` is present, it is direction on your previous output,
not a fresh brief. Address the specific objection, keep the parts that weren't
challenged intact, and don't take the opportunity to rewrite themes the
reviewer accepted — the reviewer is comparing against what they saw.

If the feedback is a structural error list from the validator, fix exactly
those fields. If it's a judge's weak-criteria note, the fix is usually
returning to the corpus, not rewording the artifact.
