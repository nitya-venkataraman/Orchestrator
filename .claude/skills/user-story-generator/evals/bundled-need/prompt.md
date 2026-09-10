---
name: "User stories — split a bundled requirement"
tags: [functional, decomposition]
plugins: ["../.."]
runs: 3
max_turns: 10
allowed_tools: [Read, Write, Bash, Glob]
---

Use the user-story-generator skill on this input. Write the result to `output/demo/stories.md`
using the skill's output template.

--- INPUT: stakeholder review note ---

"On the reports page, analysts need to be able to filter the results table by date range
and owner, sort it by any column, and export the filtered view to CSV and PDF so they can
share it in the weekly business review."

Extra context:
- The export must reflect the current filters and sort, not the raw table.
- PDF export is lower priority than CSV.
- 'Owner' is a person field already on each row.
