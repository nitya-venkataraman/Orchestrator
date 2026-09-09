---
type: llm
criteria: >-
  Judge the generated backlog in output/delivery/stories.md against the project rubric
  (.claude/skills/user-story-generator/references/rubric.md). It should score 4+ on every
  dimension. Specifically check: (1) every story is one action, not a bundle — "save",
  "run", "rename", "delete", "opt in to alerts", "unsubscribe from alerts" are separate
  stories; (2) the "so that" clause is a real benefit, not a restatement; (3) personas are
  specific (job seeker / seeker), not a blank "user"; (4) each story has 2+ testable
  acceptance criteria; (5) the 20-saved-search cap and the daily/weekly choice appear as
  criteria, not dropped; (6) out-of-scope items (push, instant alerts, shared searches,
  recruiters) are NOT turned into stories — at most noted under Open questions.
target: {source: file, path: "output/delivery/stories.md"}
---
Score PASS only if the backlog is faithful to the inputs, correctly decomposed, and
free of invented scope.
