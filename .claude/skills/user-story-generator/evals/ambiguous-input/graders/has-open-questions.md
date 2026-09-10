---
type: regex
pattern: '## Open questions\s*\n(?:\s*[-*].+\n?){3,}'
match: contains
target: {source: file, path: "output/demo/stories.md"}
---
Because the brief is vague, the Open questions section must carry real weight — at least
three specific unresolved questions.
