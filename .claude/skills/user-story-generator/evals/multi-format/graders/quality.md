---
type: llm
criteria: >-
  Check output/stories.md against .claude/skills/user-story-generator/references/rubric.md.
  Specifically: (1) the Sources line names all three inputs (email, CSV, Slack export);
  (2) needs from every input are represented — barcode scan, show return reason, manual
  lookup fallback, restock/refurbish/scrap disposition, supervisor override, timestamped
  and attributed status changes, show customer RMA photos, monthly returns report;
  (3) stories are single-action and use specific personas (warehouse operator, supervisor,
  finance/analyst); (4) each story has 2+ testable acceptance criteria; (5) the
  customer-visible "did you get my return" status, which the source itself flags as maybe
  out of scope, is placed under Open questions rather than committed as a story.
target: {source: file, path: "output/stories.md"}
---
PASS only if all three sources are covered and the ambiguous item is deferred, not assumed.
