---
name: superlap-strategy
description: Stage 2 of the Superlap UX pipeline. Converts synthesized research themes into personas, a current-state journey map, and How-Might-We problem statements as validated JSON, with every persona trait traceable to a theme. Use whenever someone needs personas built from research, a journey map with emotions and friction points, HMW statements framed from findings, or a strategy/definition phase deliverable — and whenever they mention personas, journey mapping, HMW, problem framing, or the Superlap pipeline. Also use it as stage 2 when running the full pipeline.
---

# Strategy Definition — Stage 2

Themes in, `StrategyOutput` JSON out. This stage is where research becomes a
point of view, and where the classic failure is **quiet fabrication**: a
persona gets a commute, a job title, and a favorite app that no participant
ever mentioned, and from then on the team designs for a fictional person.

Every trait you write should be answerable with "which theme said that?"

## Inputs

- `synthesis` (required) — Stage 1 `SynthesisOutput` JSON.
- `raw_inputs` (optional but preferred) — the original corpus, for quote checks.
- `revision_feedback` (optional).

## Method

**Personas — exactly 2.** One primary (the user whose problem the product is
being built to solve) and one secondary (a user whose needs constrain the
solution). Two is the cap because a third almost always dilutes rather than
informs.

For each persona, derive `goals`, `frustrations`, and `context` from named
themes and carry the theme names in `grounded_in`. The `quote` field is a real
quote lifted from the synthesis, attributed — not a composite you wrote in a
user's voice. Demographics get one line at most, and only where the research
actually establishes them. If the corpus never mentions age, the persona has
no age.

**Journey map — current state.** Map what happens today, not the future you'd
like. 4–7 stages. Each stage carries the user's `actions`, an `emotion` (one
word, drawn from how participants actually described it), `friction` points,
and a `dropoff_risk` of high/medium/low. Emotion should move across the
journey — a map where every stage reads "frustrated" is a map that wasn't
observed closely.

**HMW statements — 3 to 5.** Each one:

- opens literally with "How might we"
- names a friction point from the journey, not a feature
- stays solution-neutral

The test: if the HMW admits exactly one answer, it's a spec in disguise.
"How might we add a bulk-export button" is solutioning. "How might we let
someone trust a number they didn't calculate themselves" opens a design space.

Pitch the scope so that three genuinely different concepts could answer it. Too
broad ("how might we make finance easier") gives ideation nothing to push
against; too narrow gives it nowhere to go.

## Output contract

Every run produces three things:

1. **The validated JSON artifact** — the schema below, unchanged. It stays the machine
   contract: the Tier-1 validator and every downstream stage parse it literally. Do not
   rename fields, add prose inside it, or drop required keys.
2. **Two files written to the repo's `output/` directory:**
   - `output/strategy-<slug>.json` — the JSON artifact, pretty-printed
   - `output/strategy-<slug>.md` — the human-readable rendering (see **Rendering** below)

   Use the **same `<slug>`** as Stage 1 (`output/discovery-synthesis-<slug>.*`) so a
   run's files line up. Overwrite on re-run — never suffix a timestamp.
3. **Your visible reply is the Markdown rendering** — the exact contents of the `.md`
   file, and nothing else. Do not paste the raw JSON into the reply; it lives in the
   `.json` file. Show the JSON only if asked.

```json
{
  "personas": [
    {
      "name": "string",
      "type": "primary | secondary",
      "context": "string — role and situation, research-backed only",
      "goals": ["string"],
      "frustrations": ["string"],
      "quote": "verbatim quote from the synthesis",
      "grounded_in": ["theme name", "theme name"]
    }
  ],
  "journey": [
    {
      "stage": "string",
      "actions": ["string"],
      "emotion": "one word",
      "friction": ["string"],
      "dropoff_risk": "high | medium | low"
    }
  ],
  "hmw_statements": [
    {
      "statement": "How might we ...",
      "derived_from": "journey stage or theme name"
    }
  ]
}
```

Validator constraints:

- Exactly 2 personas, one `primary` and one `secondary`.
- Every `statement` starts with "How might we" (case-insensitive) — this is a
  hard structural check, not a stylistic preference.
- 4–7 journey stages; 3–5 HMW statements.
- Every `grounded_in` entry matches a theme name from the input synthesis.

## Rendering

The `.md` file — and your visible reply — follows the format already established in
`output/strategy-flight-booking.md`. Required sections:

- `# Strategy & Definition — <Project>` title + one-line summary.
- `## Personas` — one card per persona (`### <name> — <primary|secondary>`) with
  context, goals, frustrations, the attributed quote, and a "grounded in:" line naming
  the themes.
- `## Current-State Journey` — a table or ordered list of stages with actions, emotion,
  friction, and drop-off risk.
- `## How Might We` — the HMW statements as a numbered list, each with its
  `derived_from` in parentheses.

Keep it scannable: a designer reads this, not the JSON.

## Quality bar

Judge threshold **0.75**.

| Criterion | Weight | What it checks |
|---|---|---|
| `persona_grounding` | 0.30 | Personas trace to themes; no fabricated traits |
| `hmw_quality` | 0.35 | HMWs are open, non-solutioning, correctly formed |
| `journey_realism` | 0.35 | Stages reflect described behavior and emotion, not a generic funnel |

`journey_realism` is where generic output gets caught. "Awareness → Consideration
→ Purchase → Retention" is a marketing funnel, not this product's journey. Name
the stages in the user's own terms — "waits for the nightly export", "rebuilds
the total by hand" — and the map becomes usable.

## Revision handling

`revision_feedback` is direction on the previous artifact. Address the specific
objection and leave accepted material alone. When feedback targets a persona,
resist the urge to re-derive the journey too — the reviewer is diffing against
what they approved.
