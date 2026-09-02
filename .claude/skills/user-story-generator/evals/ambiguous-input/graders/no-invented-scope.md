---
type: llm
criteria: >-
  The only input is a one-line founder DM saying onboarding is bad and asking for a
  backlog. Judge output/stories.md for restraint: (1) it must NOT invent a detailed
  onboarding redesign — no specific stories about tooltips, checklists, progress bars,
  welcome emails, tutorial videos, etc. unless clearly framed as options/hypotheses to
  validate; (2) any concrete stories should be about the discovery work the DM actually
  authorises (e.g. "As a PM, I want to interview churned users so that I can find why they
  don't return", "instrument the signup funnel"); (3) the Open questions section should
  capture what "better" means, target metric, timeline, which segment, research scope;
  (4) format rules still hold (story sentence, 2+ criteria each, sections present).
  FAIL if the model fabricated a confident feature backlog from this single sentence.
target: {source: file, path: "output/stories.md"}
---
PASS only if the response distinguishes what the input supports from what it does not.
