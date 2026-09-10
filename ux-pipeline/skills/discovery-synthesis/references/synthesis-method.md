# Synthesis method

How to get from a corpus to themes without inventing anything. The SKILL.md gives
the steps; this is the craft behind them.

## Clustering: by behaviour, not by wording

Affinity clustering groups observations that share a *cause*, not ones that share
a phrase. Six participants saying "it's slow" may be describing four different
problems — a slow search, a slow page, a slow approval, and a slow colleague.
Grouping them into one "performance" theme destroys the finding.

The test: state the theme as a behaviour and a reason. *"Associates rebuild the
export by hand because they don't trust the totals"* is a theme. *"Users are
frustrated by exports"* is a bucket. If the sentence has no verb the participant
would recognise as their own action, keep clustering.

Six themes that are really three is the more common failure than three that
should be six. Before finalising, ask of each adjacent pair: would a designer
solve these two the same way? If yes, they are one theme.

## Severity: derived, not felt

`severity` is not how bad the quotes sound. Derive it:

| | Blocks the task or risks real loss | Costs meaningful time or trust | Annoyance |
|---|---|---|---|
| **Most participants** | high | high | medium |
| **Several** | high | medium | low |
| **One or two** | medium | low | low |

Frequency alone does not make something high — a universal minor irritation is
still minor. Consequence alone does not either — a catastrophic edge case one
participant hit once is worth recording at medium with the rarity stated. State
the reasoning in the insight where the two pull apart, because that is exactly
where a reader will otherwise assume you got it wrong.

## Frequency counts people

`frequency` is distinct participants, never mentions. One participant who raised
the same complaint nine times is a frequency of 1 — and a signal worth a sentence
in the insight, but not a bigger number. Inflating this is the easiest way to
make a synthesis lie while every individual quote stays true.

## Quotes are evidence, so they must be verbatim

The quote's job is to let a reader check your work. Tier-1 substring-matches
every quote against the corpus, so tidying a filler word or fixing grammar turns
evidence into paraphrase and fails. Trim from the ends, never from the middle,
and never join two utterances into one quote.

Attribute with a participant identifier (`P07`, `Ticket-4412`, `Review-2891`),
never a name, an email, or an employer. Research participants were promised
something; the artifact is where that promise is kept or broken, and it will be
read by more people than the raw corpus ever is. Tier-1 rejects a `source` that
looks like a name or an email address.

## Gaps are a finding, not an admission

`gaps` is where you say what this corpus cannot answer. It is the most-skipped
and most-valuable field in the artifact, because everything downstream treats the
synthesis as the complete picture — a designer will not go looking for what you
did not mention.

Worth recording:

- **Who is missing.** Eleven associates and no reviewers means the reviewer's
  half of the journey is inference, and Stage 2 needs to know that.
- **What the method could not see.** Interviews reveal what people say they do;
  they do not reveal what they actually do, and they systematically under-report
  workarounds people are slightly embarrassed by.
- **When the data is from.** A corpus gathered before a release describes a
  product that no longer exists.
- **What you expected and did not find.** A pain point the team was certain
  existed, that nobody raised unprompted, is a finding about the team.
- **Where the corpus is one-sided.** Support tickets over-represent failure;
  sales calls over-represent enthusiasm; app-store reviews over-represent both
  extremes and nothing in between.

An empty `gaps` array on a thin corpus is almost always a synthesis that was not
looking.

## The invention line

The corpus supports a behaviour and a reason only when a participant gave you
both. If three participants said they rebuild the export by hand, and none said
why, then "because they don't trust the totals" is your hypothesis, not their
insight. Write the behaviour as the theme and put the hypothesis in `gaps` as a
question worth asking next — which is exactly what the Stage-6 evaluation plan is
for.
