# Rubric — Stage 2: strategy-definition

Scores a `StrategyOutput` artifact (2 personas + current-state journey + HMW statements).
Read [`README.md`](README.md) first. Tier-1 (`ux-pipeline/validators/strategy.py`) must
already pass; this rubric judges whether the strategy is a faithful point of view on the
research, not whether it is well-formed.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `persona_grounding` | 0.30 | Every persona trait — context, goal, frustration — traces to a named Stage-1 theme. No demographic, tool, or habit that the research never established. |
| `hmw_quality` | 0.35 | Each HMW opens a design space: names a journey friction, stays solution-neutral, and admits three genuinely different answers. |
| `journey_realism` | 0.35 | Stages are named in the user's own terms and the emotion moves across them. The map is recognizably *this* product's flow, not a generic funnel. |

## Score anchors

### `persona_grounding`
- **5** — Ask "which theme said that?" of any trait and there's an answer; `grounded_in` is complete and accurate; the `quote` is lifted verbatim from the synthesis.
- **3** — Personas are broadly research-backed, but one or two traits are plausible extrapolation (a commute, a job title, a "prefers mobile") the corpus never mentions.
- **1** — A persona has a fabricated life — demographics, tools, or motivations with no basis — or `grounded_in` cites themes that don't support the trait.

### `hmw_quality`
- **5** — Every HMW is friction-framed, solution-neutral, and scoped so three distinct concepts could answer it.
- **3** — HMWs are correctly formed but one is a feature in disguise ("how might we add a bulk-export button") or one is so broad it gives ideation nothing to push against.
- **1** — Multiple HMWs are solutioned, or they restate the friction without opening any design space.

### `journey_realism`
- **5** — Stages use the participants' language ("waits for the nightly export", "rebuilds the total by hand"); emotion varies stage to stage and matches described affect; friction points are specific.
- **3** — The journey is real but partly generic — a stage or two reads like a template step, or the emotion column is flat in places.
- **1** — "Awareness → Consideration → Purchase → Retention" or similar: a marketing funnel, not this product's journey.

## Calibration

`journey_realism` is where generic output gets caught. If the stage names would fit any
product in the category, the map wasn't observed — score it 2–3 even if the structure is
tidy. The tell of a 5 is that someone who read the research would recognize the journey
without being told which product it's for.

`persona_grounding` and fabrication: the pipeline's whole failure mode is a fictional
person the team then designs for. Be strict — a single unsupported motivating trait
("she's time-poor and impatient") that shapes downstream features is a 2 on this
dimension, not a rounding error.

## Common failure modes

- A persona `quote` written in the user's voice rather than quoted from the synthesis.
- Age / income / job title stated where the corpus never established them.
- Every journey stage tagged "frustrated" — emotion that doesn't move.
- HMW count is in range but two of them are the same problem.
- `derived_from` points at a theme that doesn't actually contain that friction.

```json
{
  "stage": "strategy-definition",
  "weights": {
    "persona_grounding": 0.30,
    "hmw_quality": 0.35,
    "journey_realism": 0.35
  },
  "pass_when": "min>=4 or (min>=3 and weighted_mean>=4.0)"
}
```
