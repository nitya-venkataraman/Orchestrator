# AI POC

A lightweight project repo for turning raw project inputs into structured, review-ready user stories.

## Purpose

Product, design, and engineering inputs arrive in many shapes — meeting notes, transcripts,
emails, Slack threads, PRDs, spreadsheets, bullet dumps, screenshots-turned-text. This repo
provides a repeatable way to convert any of that into consistent user stories with acceptance
criteria.

## Skills

### UserStoryGenerator

Analyzes project-level inputs in **any format** and converts them into structured user stories.

- Location: `.claude/skills/user-story-generator/SKILL.md`
- Invoke it whenever the user asks to "generate user stories", "turn this into stories",
  "write acceptance criteria", "break this down into a backlog", or provides raw requirements
  material and wants it structured.

**User story format (required):**

> As a **[user-type]**, I want to **[action]** so that I can **[benefit/gain]**.

Every story must also include **acceptance criteria** (Given/When/Then or a checklist).

## Conventions

- Generated stories are written to `output/` as Markdown, one file per epic or per run.
- Keep the story voice user-centric — describe outcomes, not implementation.
- When inputs are ambiguous or incomplete, list open questions rather than inventing detail.

## Repo layout

```
CLAUDE.md                     # this file
README.md                     # human-facing overview
.claude/skills/
  user-story-generator/
    SKILL.md                  # the UserStoryGenerator skill
    examples/                 # sample input -> output
inputs/                       # drop raw source material here (any format)
output/                       # generated user stories land here
```
