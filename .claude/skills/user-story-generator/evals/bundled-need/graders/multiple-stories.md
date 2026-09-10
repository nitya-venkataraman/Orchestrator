---
type: regex
pattern: '^### US-\d+:'
flags: m
match: count:4
target: {source: file, path: "output/demo/stories.md"}
---
The one bundled sentence (filter by date, filter by owner, sort by column, export CSV,
export PDF) should decompose into at least four distinct stories.
