# Ideation methods

RICE is how the features get *ranked*. It says nothing about how they get
*generated*, and a list of six obvious features scored impeccably is still a list
of six obvious features. This is the generation half.

## Get range before you score anything

The contract asks for 6–12 features and "range within each HMW". Range means the
options differ in *kind*, not in size. For any friction, there are at least four
different kinds of answer:

| Move | What it does | Example against "the org chart takes five hours" |
|---|---|---|
| **Serve the need better** | Same job, less friction | A faster chart editor with better defaults |
| **Remove the need** | The job stops existing | Derive the chart from the agreements |
| **Change who does it** | Someone or something else does it | The agreement provider supplies structured data |
| **Change when it happens** | Move it in the timeline | Build the chart incrementally as documents arrive |

If every feature under one HMW is a "serve the need better" variant, you stopped
at the first idea. The second and third moves are usually where the interesting
options are, and they are what makes Stage 3's design directions genuinely
distinct rather than three flavours of one bet.

## Techniques worth reaching for

- **Crazy 8s** — force eight answers to one HMW in one pass. The point is that
  ideas five through eight are the ones you would not have reached by stopping at
  a good idea. Keep the ones that survive; discard the rest without ceremony.
- **SCAMPER** — substitute, combine, adapt, modify, put to another use, eliminate,
  reverse. Most useful applied to the *current process*: what happens if this step
  is eliminated? reversed? done by someone else?
- **Analogous inspiration** — who else solves this shape of problem well?
  Reconciling a document against a source is a problem that code review, legal
  redlining, and translation memory all solved differently. Borrowing the
  *mechanism* is not copying the product.
- **Inversion** — ask how you would make the problem worse. The answers usually
  describe the current design, and each one inverts into a candidate.
- **Constraint removal** — what would you build if the hardest constraint were
  gone? Sometimes it is not as fixed as assumed; when it is, the exercise still
  tells you what the constraint costs.

## Score honestly, and remember what each input means

- **Reach** — how many, in what period, grounded in a real population: a segment
  size, `source_count`, or a stated assumption. Not a vibe.
- **Impact** — per-person effect on the goal. It is a fixed scale (0.25 / 0.5 / 1
  / 2 / 3) precisely so it cannot be nudged. If everything is a 2, you have not
  discriminated.
- **Confidence** — how sure you are of the other three. `1.0` means the research
  directly supports it; a single comment supports `0.5`, not `1.0`.
- **Effort** — person-months, honestly, including the parts nobody enjoys.

The one thing that makes a prioritisation worthless is adjusting an input to move
a favoured feature up. Tier-1 recomputes the arithmetic, so the only way to cheat
is through the inputs — which is exactly what `rice_integrity` is looking for.

## The success metric is part of the score

Every feature declares a `success_metric`, and writing it is a check on the
`impact` you just gave. If you cannot name something that would move, the impact
score is a guess. If the metric you name measures *usage of the feature* rather
than the *outcome it exists for*, it will show green while the problem persists —
"extraction screen opened" is a vanity metric; "hours to first committed model"
is the thing the associate actually cares about.

Take `baseline` from a Stage-2 `current_metric` or named analytics. Otherwise
write `"unknown"`. An estimated baseline is the same failure as an inflated
`reach`, and it is worse in one way: it survives into the business case and
nobody remembers it was invented.

## Directions are bets, and you never pick one

2–3 directions, each a genuinely different bet about *how* to solve the problem.
Differentiate on an axis that matters:

- **Who does the work** — the system, the user, or a third party.
- **When value lands** — immediately and partially, or later and completely.
- **How much trust is required** — automate and let people verify, or assist and
  let people decide.
- **Fix the workflow or replace it** — make the current process better, or make it
  unnecessary.

A direction described as a visual theme ("clean and minimal") is not a bet. Each
one needs an explicit `tradeoff` that is a genuine cost — "requires good design"
is not a cost, "only pays off once three quarters of the document corpus is
indexed" is.

**Never select a winner.** The pipeline forks on this decision and the fork
belongs to a human. Present the bets and their costs clearly enough that a
reasonable team could disagree about which is right, and stop there.
