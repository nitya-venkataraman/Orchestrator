# Handoff checklist

A handoff is complete when a developer could build the thing without asking you a
question, and a tester could tell whether they got it right. The SKILL.md gives
the steps; this is what "complete" includes.

## The story

- **One capability per story.** "Add, edit and remove" is three stories. The tell
  is an "and" in the capability that joins two different verbs.
- **The benefit is an outcome, not the capability reworded.** "so that I can see
  the list" after "I want to see the list" is a story that says nothing about why
  anyone wanted it.
- **The persona is the one who actually does this**, named from Stage 2 — not
  "a user".
- **The screen is where it lands**, named from Stage 4.

## Acceptance criteria

Given/When/Then, one checkable scenario each. The main path is the floor, not the
job:

- The **main path**, obviously.
- The **error and empty states** Stage 4 specified for that page. Those are design
  decisions, and untested design decisions get built as whatever was easiest.
- The **edge cases** from `requirements.edge_cases` that matter for this story.
- The **permission cases** where the page's `permissions` differ by role.

A criterion that cannot fail is not a criterion. "Then the page works correctly"
tests nothing.

## Accessibility criteria are not optional

Every Stage-4 page needs at least one story carrying `accessibility_criteria`,
and Tier-1 enforces it. Derive them from *that page's* `accessibility` block, not
from a generic checklist — the block already says what this page's keyboard path
is, what its labels must identify, and what it announces:

- **Keyboard** — the tab order the page declared, focus visible throughout, focus
  moving into and back out of anything that opens, Escape closing it.
- **Labels and errors** — every control labelled visibly, every error identifying
  which field and why, in text.
- **Announcements** — the page's `status_messages`: what a screen-reader user is
  told when an async result lands, and whether it interrupts.
- **Never colour alone** — any state signalled by colour also signalled in text or
  shape.

Eight identical "the page is keyboard navigable" criteria satisfy Tier-1 and fail
the rubric, which is the correct outcome: the structure is checkable, the honesty
is judged.

## Instrumentation

Any story landing on a page whose `primary_action` writes data carries
`analytics_events`. Each names the `event`, the `trigger` that fires it, and the
`properties` that make it computable.

The test is not "does an event exist" but "could this event compute the metric it
exists for". An event with no identifier cannot be joined; one with no outcome
cannot be split into success and failure; one with no duration cannot answer a
question about time. Read the Stage-3 `success_metric` the feature declared and
work backwards to the properties it needs.

Write pages are the floor, not the ceiling. If a metric needs an event on a read
page, specify it — Stage 6 will otherwise record that metric as unreadable, which
is honest but avoidable.

## Microcopy

Voice rules are in
`ux-pipeline/skills/wireframe-ia/assets/component-patterns.md` § Voice — the
handoff restates them rather than inventing a second dialect. Sentence case,
verb-first, ≤ 4 words, no ALL CAPS, no trailing period, never "Click here".

Beyond voice:

- **Errors:** what happened, then what to do. No apology — "Sorry, something went
  wrong" tells the reader nothing and asks them to accept a feeling instead of a
  fact. Say what is preserved, too; the fear behind most error messages is that
  the work is gone.
- **Empty states:** why it is empty, and exactly one action. Two competing actions
  in an empty state is a decision handed to someone with no information.
- **Plain language** at the reading level the persona actually has. Domain terms
  the persona uses daily are plain language *for them*; system vocabulary is not.
- **Localization headroom.** Assume a translation runs ~30% longer. A label that
  only fits its control in English is a defect in every other language, and it is
  cheaper to catch here than in a QA pass against a German build.

## What is out of scope here

The pipeline does not produce redlines, spacing annotations, or asset exports —
Stage 4's Figma file carries the layout, its variables carry the tokens, and its
component names carry the system. Do not restate measurements in prose; they will
drift from the file and be believed.
