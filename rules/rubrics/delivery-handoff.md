# Rubric — Stage 5: delivery-handoff

Scores a delivery artifact (`stories` + `microcopy`). Read [`README.md`](README.md) first.
Tier-1 (`ux-pipeline/validators/delivery.py`) already checks that every story has a
persona / capability / benefit / Given-When-Then, that personas and screens resolve to
upstream artifacts, and that CTA microcopy is sentence case (not ALL CAPS) — this rubric
judges whether the handoff is *buildable and complete*, not whether it is well-formed.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `story_completeness` | 0.40 | Each story names a real capability and a benefit that is an outcome, not a restatement. Acceptance criteria cover the main path plus the key edge cases, and each is a single checkable scenario. Accessibility criteria are derived from the page's own accessibility block, and any story that writes data emits an event that would actually let its metric be computed. |
| `traceability` | 0.30 | The story set collectively covers the Stage-4 IA — every screen's core purpose is exercised by at least one story — and each story ties to the right Stage-2 persona and Stage-4 screen. The accessibility criteria trace to the specific page they cover, not to a generic checklist. |
| `voice_consistency` | 0.30 | Microcopy matches the product voice: CTAs sentence-case, verb-first, ≤ 4 words (not ALL CAPS); error copy states what happened then what to do with no apology; empty states name the condition and offer exactly one action. |

## Score anchors

### `story_completeness`
- **5** — Every story is one capability with a genuine "why"; criteria cover main path + the edge cases that matter for that screen; a developer could build and test from this alone.
- **3** — Stories are sound but one or two bundle two capabilities, or a `benefit` restates the `capability`, or a story has only a happy-path criterion.
- **1** — Stories are vague ("as a user I want the app to work"), criteria are untestable, or major screen behavior has no story.

### `traceability`
- **5** — Every Stage-4 screen's purpose is covered; persona and screen references are all correct and specific.
- **3** — Most screens covered, but one screen's core interaction has no story, or a story is attributed to the wrong persona.
- **1** — Stories cover a subset of the product; several screens absent; persona attribution is generic or wrong.

### `voice_consistency`
- **5** — Every string could drop into the built UI unedited — sentence-case verb-first CTAs (≤ 4 words, not ALL CAPS), blame-free error copy in "what happened, then what to do" order, single-action empty states. Copy is plain language at the reading level the persona actually has, and no string is so tight that a 30% longer translation would break its control.
- **3** — Mostly on-voice, but a few CTAs are ALL CAPS or over-long, strings are apologetic ("Sorry, something went wrong"), or an empty state offers two competing actions.
- **1** — Microcopy is generic product boilerplate with no relationship to the design-system voice.

## Calibration

`traceability` is the dimension that slips. It's easy to write a clean set of stories for
the interesting screens and quietly skip the utilitarian ones (a cost-breakdown drawer, a
confirmation dialog). Before scoring, walk the Stage-4 `screens` list and confirm each has
a story that exercises its stated `purpose` — a screen with no story is a screen that won't
get built to spec.

`voice_consistency` is not decoration. The voice rules of the design system Stage 4
resolved — whichever one that was — are as enforceable as its component set. "Click here",
an ALL-CAPS or trailing-period CTA, or an apology in an error is a real violation, not a
style nit. The canonical statement of the rules is
`ux-pipeline/skills/wireframe-ia/assets/component-patterns.md` § Voice; the handoff
restates them rather than inventing a second dialect.

## Common failure modes

- A story bundling "add", "edit", and "remove" into one capability.
- `benefit` == `capability` reworded.
- Only main-path acceptance criteria; the error and empty states from Stage 4 aren't
  turned into criteria.
- `accessibility_criteria` present on every page but interchangeable between them —
  "the page is keyboard navigable" pasted eight times. Tier-1 only checks that they
  exist; whether they came from *that page's* accessibility block is this rubric's job.
- An `analytics_events` entry whose `properties` could not actually compute the metric
  the feature claims to move (an event with no identifier, no outcome, no duration).
- Stories for the hero screens, nothing for the drawers / dialogs / confirmations.
- Apologetic microcopy, ALL-CAPS or over-long CTAs; empty states with zero or two actions.

```json
{
  "stage": "delivery-handoff",
  "weights": {
    "story_completeness": 0.40,
    "traceability": 0.30,
    "voice_consistency": 0.30
  },
  "pass_when": "min>=4 or (min>=3 and weighted_mean>=4.0)"
}
```
