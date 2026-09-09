---
name: "User stories — happy path (well-specified feature)"
tags: [functional, happy-path]
plugins: ["../.."]
runs: 3
max_turns: 12
allowed_tools: [Read, Write, Bash, Glob]
---

Use the user-story-generator skill to turn the inputs below into a backlog.
Write the result to `output/delivery/stories.md` using the skill's output template.

--- INPUT 1: kickoff meeting notes ---

Attendees: Priya (PM), Dan (eng), Mel (support lead)

- Job seekers run the same search (keywords + location + remote toggle) again and again.
  They want to save a search and get back to it in one tap.
- Mel: top support request this quarter is "how do I get notified when new jobs match".
  People want an email when fresh matches appear.
- Should be able to name a saved search ("Remote React roles").
- Manage the list: rename, delete. Cap at 20 saved searches per account.
- Recruiters are a different persona and are out of scope for this piece.
- Email digest frequency: daily or weekly, seeker chooses. Instant was rejected for v1.

--- INPUT 2: PRD excerpt ---

Goal: reduce repeat-search effort and grow return visits via match notifications.
In scope for v1: create a saved search from current filters; view saved searches newest
first; run a saved search; opt in to email match alerts per saved search (daily or
weekly); unsubscribe from a saved search's alerts without deleting the search.
Not in scope for v1: push notifications, shared/team searches, instant alerts.
