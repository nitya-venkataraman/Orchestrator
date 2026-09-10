# Rubric — Stage 1: discovery-synthesis

Scores a `SynthesisOutput` artifact (themes + gaps + source_count). Read
[`README.md`](README.md) first — scale, stance, evidence, and output shape are defined
there. Tier-1 (`ux-pipeline/validators/synthesis.py`) must already pass; this rubric judges
whether the synthesis is *true to the corpus*, not whether it is well-formed.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `evidence_grounding` | 0.40 | Every theme's insight is a direct read of its quotes. No claim goes beyond what a participant actually said. `frequency` matches the distinct participants in the quotes. |
| `theme_distinctness` | 0.25 | The themes are genuinely different behaviors, not one behavior described in five vocabularies. Merging any two would lose information. |
| `signal_coverage` | 0.35 | Every signal raised by 3+ participants (or flagged as high-severity in the source) lands in a theme. Nothing common was dropped for being inconvenient. |

## Score anchors

### `evidence_grounding`
- **5** — Each `insight` is defensible line-by-line against its `quotes`; nothing invented; severity and frequency track the evidence.
- **3** — Themes are quote-backed, but one or two insights editorialize past the quote ("users are furious" where the quote is mild), or a `frequency` is inflated.
- **1** — A theme has no usable quote, quotes are paraphrased/stitched, or an insight introduces a cause, segment, or metric that appears nowhere in the corpus.

### `theme_distinctness`
- **5** — 2–6 themes, each a distinct behavior + driving belief; no overlap.
- **3** — Mostly distinct, but two themes share a root cause and should be merged, or one theme is really two.
- **1** — Themes are vocabulary clusters ("slow", "confusing", "frustrating") over the same underlying issue.

### `signal_coverage`
- **5** — Re-scanning the corpus surfaces no high-frequency complaint that is missing from the themes.
- **3** — One notable recurring signal is under-weighted (buried in a theme's third quote instead of named) or a mid-frequency signal is missing.
- **1** — A complaint raised by many participants — or the single most severe issue in the source — is absent entirely.

## Calibration

`signal_coverage` is the dimension people lose. A tidy, distinct, well-quoted synthesis
that quietly dropped the most common complaint still fails — a designer will trust this
list *as the complete picture*. Before scoring, list every issue mentioned by 3+
participants in the raw corpus and check each one appears in a theme.

`evidence_grounding` fails quietly the other direction: an insight that sounds sharp
("users rebuild the export by hand because they don't trust the totals") is only a 5 if a
participant actually described both the behavior and the reason. If they only described the
behavior, the "because" is invention — score 3 and flag it.

## Common failure modes

- Insight restates sentiment instead of naming behavior ("users are frustrated by X").
- `frequency` counts mentions, not distinct participants.
- Six themes that are really three (clustered by wording).
- Empty `gaps` array on a thin or single-source corpus — usually means the synthesis
  wasn't looking for what's missing.
- A `corpus.known_bias` that lists no bias. Every corpus has one: support tickets
  over-represent failure, sales calls over-represent enthusiasm, interviews record what
  people say they do rather than what they do, and three participants cannot size
  anything. Naming it is a finding, not a disclaimer.
- `severity` that tracks how strongly the quotes are worded rather than frequency ×
  consequence — a universally-mentioned minor irritation scored high, or a rare
  catastrophic case scored low.
- The highest-severity issue in the source appears only as a supporting quote under an
  unrelated theme.

```json
{
  "stage": "discovery-synthesis",
  "weights": {
    "evidence_grounding": 0.40,
    "theme_distinctness": 0.25,
    "signal_coverage": 0.35
  },
  "pass_when": "min>=4 or (min>=3 and weighted_mean>=4.0)"
}
```
