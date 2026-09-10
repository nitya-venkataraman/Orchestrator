---
name: "User stories — vague brief, must not invent scope"
tags: [functional, ambiguity, guardrail]
plugins: ["../.."]
runs: 3
max_turns: 10
allowed_tools: [Read, Write, Bash, Glob]
---

Use the user-story-generator skill on this single input. Write the result to
`output/demo/stories.md` using the skill's output template.

--- INPUT: Slack DM from the founder ---

"onboarding is bad, people sign up and never come back. can we make onboarding better this
quarter? talk to a few users maybe. want something in the backlog by friday"
