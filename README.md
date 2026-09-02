# AI POC

Turn raw project inputs into structured user stories with acceptance criteria.

## What's here

- **`.claude/skills/user-story-generator/`** — the `UserStoryGenerator` skill. It reads
  project inputs in any format and produces user stories in the form:

  > As a **[user-type]**, I want to **[action]** so that I can **[benefit/gain]**.

  Each story ships with testable acceptance criteria.

- **`inputs/`** — drop source material here (notes, transcripts, PRDs, exports, etc.).
- **`output/`** — generated user stories are written here.

## Usage

In Claude Code, from this repo:

```
/user-story-generator
```

or just ask: *"Generate user stories from the notes in inputs/."*

The skill activates automatically when you provide requirements material and ask for
stories, a backlog, or acceptance criteria.

## Example

See `.claude/skills/user-story-generator/examples/` for a sample input and the stories
generated from it.
