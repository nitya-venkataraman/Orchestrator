---
name: delivery-handoff
description: Use this skill to translate approved wireframes/IA into developer-ready Jira user stories, acceptance criteria, and UX microcopy. Triggered as Node 5 (final) of the UX pipeline.
---

# Delivery & Handoff

## Steps
1. Read `sitemap` and `wireframe_specs`.
2. Write Jira-style user stories: "As a [persona], I want [capability], so that [benefit]" + explicit Acceptance Criteria (Given/When/Then).
3. Generate microcopy: button labels, empty states, error states, confirmation messages — matching the brand voice (bold, high-contrast, uppercase CTA convention from the design system).

## Output contract
Return `developer_handoff_stories` and `microcopy`.
