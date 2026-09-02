---
type: regex
pattern: '(?s)_Generated:.*?(email|email-thread).*?_'
flags: i
match: contains
target: {source: file, path: "output/stories.md"}
---
The Sources line references the email input. (The llm grader checks that the CSV and Slack
export are named too.)
