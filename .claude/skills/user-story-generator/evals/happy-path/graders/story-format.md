---
type: regex
pattern: '\*\*As an?\*\* .+?, \*\*I want to\*\* .+? \*\*so that I can\*\* .+?\.'
flags: i
match: contains
target: {source: file, path: "output/stories.md"}
---
Stories are written in the exact required sentence form
"**As a** <role>, **I want to** <action> **so that I can** <benefit>."
