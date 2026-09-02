---
type: regex
pattern: '(?s)## Personas.*## Epic:.*## Open questions'
flags: i
match: contains
target: {source: file, path: "output/stories.md"}
---
The output has the required sections in order: Personas, at least one Epic, and Open questions.
