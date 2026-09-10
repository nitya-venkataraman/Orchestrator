---
type: llm
criteria: >-
  The input bundles several capabilities into one sentence. Judge output/demo/stories.md:
  (1) filtering by date range, filtering by owner, sorting by column, exporting to CSV,
  and exporting to PDF are represented as SEPARATE stories (filtering by date and by owner
  may reasonably be one story or two — either is fine — but sort and each export must be
  their own); (2) no single story contains "and" joining two distinct actions;
  (3) the "export reflects current filters and sort" rule appears as an acceptance
  criterion on the export story/stories; (4) PDF export is marked lower priority than CSV;
  (5) personas are specific ("analyst"); every story has 2+ testable criteria.
target: {source: file, path: "output/demo/stories.md"}
---
PASS only if the bundle is properly split and the stated constraints land as criteria.
