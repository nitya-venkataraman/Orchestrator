# Persona and journey craft

The SKILL.md gives the steps and the shape. This is what separates a persona that
changes a design decision from one that decorates a slide.

## A persona is a claim, and `grounded_in` is the receipt

Every trait must survive the question *"which theme said that?"* — that is what
`grounded_in` records, and Tier-1 checks the names resolve. But the check only
verifies the theme exists, not that it says what you claim. The honest test is
per trait, not per persona:

- **Context** — where they sit, what constrains them, what else is on their plate.
  From the research, not from the job title.
- **Goals** — what they are trying to achieve, in their terms. "Complete the
  profile" is a task; "not be the reason the committee slips" is a goal.
- **Frustrations** — the friction the themes actually recorded.
- **Quote** — verbatim from the corpus, attributed. It should be the one line that
  makes a reader recognise this person.

Demographics that change no decision (age, marital status, a stock photo's worth
of personality) do not belong. If removing a trait would change nothing about the
design, it was decoration.

## Two or three, and the third has to earn it

The contract allows 1 primary and 1–2 secondary. A third persona is a claim that
the research describes three genuinely distinct people with different goals — not
three job titles doing the same job. Add one when the evidence supports it and
say so in `grounded_in`; an unsupported third scores badly on `persona_grounding`
rather than being blocked, which is the right place for that judgement.

The primary is the person whose failure means the product failed. There is
exactly one.

## Stress cases, not just happy personas

The persona set describes who you designed for. Somewhere in `context` and
`frustrations`, the journey should also account for people the design could
exclude if nobody named them:

- Someone using a screen reader, or a keyboard only, or magnification. Stage 4
  writes per-page accessibility, but it writes it for whoever Stage 2 described —
  if the personas are all sighted mouse users, the accessibility work has no
  person attached to it.
- Someone in the worst realistic conditions the research described: a bad
  connection, a phone in one hand, a noisy floor, the last hour of a long day.
- Someone new. Half of a product's difficulty lands on people in their first
  week, and personas are almost always written as experts.
- Someone doing this under time pressure or after an error, when attention is
  narrowest. The journey's high-`dropoff_risk` stages are where this matters.

These do not need a persona each. They need to appear in the context and friction
of the personas you have, so the downstream stages know they exist.

## The journey is current-state and it must be uncomfortable

The journey map records what happens **today**, including the parts that make the
current process look bad. A journey that reads like the future product's happy
path has skipped its own job.

- **Stages** are what the person experiences, in their language, not the system's
  phases. `Awareness → Consideration → Purchase → Retention` is a marketing
  funnel pasted over a product; it is a 1 on `journey_realism`.
- **Emotion** must *move*. One word per stage, and if the same word appears at
  every stage the journey has no shape and nothing to design against. The shape
  is the finding: where confidence turns to doubt is where the design intervenes.
- **Friction** is specific and traceable to a theme. "Hard to use" is not friction.
  "The org chart takes four to five hours of day one" is.
- **`dropoff_risk`** is where someone abandons, escalates, or falls back to the
  workaround — not merely where they are annoyed.
- **`current_metric`** goes on a stage only when the research or the analytics
  gave you a real figure. It is optional precisely so nobody feels obliged to
  estimate one; a stage with no figure simply has none, and Stage 3 will record
  the resulting baseline as `"unknown"`. That chain is the pipeline's honesty
  about numbers, and an invented figure here corrupts everything downstream of it.

## HMWs frame the problem, not the answer

Each statement opens literally with "How might we", names a friction, and stays
solution-neutral. The failure mode is smuggling a feature in:

- *"How might we add a precedent search?"* — the answer is already chosen.
- *"How might we make a firm's own prior contact with a target visible before an
  associate starts hunting for it?"* — the problem, open to several answers.

Test each one by asking whether at least two genuinely different features could
answer it. If only one could, you wrote a spec, not a question — and Stage 3 will
produce a feature list with no range in it, because you already narrowed the
space here.

Derive them from the highest-consequence frictions, not the most numerous ones,
and record which friction in `derived_from`.
