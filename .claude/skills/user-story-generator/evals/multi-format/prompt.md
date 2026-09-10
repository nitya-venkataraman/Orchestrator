---
name: "User stories — multiple input formats, list every source"
tags: [functional, multi-source]
plugins: ["../.."]
runs: 3
max_turns: 14
allowed_tools: [Read, Write, Bash, Glob]
---

Use the user-story-generator skill on the THREE inputs below (an email, a CSV, and a chat
export). Write the backlog to `output/demo/stories.md` using the skill's output template.
The `_Generated: … · Sources: …_` line must name all three inputs.

--- INPUT A: email (email-thread.txt) ---

From: Rosa Imports (Operations) — the warehouse team can't tell why an item came back;
often no paperwork, so they email customer service to find the original order (1–2 day
round trip). A scannable code on the packing slip that pulls up the order + stated return
reason would let them process on the spot. Also: no report of what is returned and why —
finance asks monthly and Rosa builds it by hand.

--- INPUT B: requirements.csv ---

id,area,requirement,priority
R1,intake,Scan a return barcode to open the matching order,High
R2,intake,Show the customer-stated return reason on the return screen,High
R3,processing,Mark each returned item as restock / refurbish / scrap,Medium
R4,reporting,Monthly export of returns by reason and category,Medium
R5,intake,Handle a return with no barcode by manual order lookup,Medium

--- INPUT C: Slack export (slack-dump.md) ---

- return screen should show customer-uploaded photos from the RMA request, if any
- a supervisor must be able to override the restock/refurbish/scrap decision
- every status change must be timestamped and attributed (audit requirement)
- customers keep asking "did you get my return" — a customer-visible status "not sure if
  that's this project or a separate one"
