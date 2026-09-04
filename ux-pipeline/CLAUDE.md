# ux-pipeline

A human-in-the-loop UX design pipeline. Raw research goes in one end; developer-ready
user stories and microcopy come out the other. Each phase is a Claude Agent SDK **skill**,
orchestrated as a LangGraph state machine with an approval gate between every phase.

## Architecture

```
discovery → [HITL] → strategy → [HITL] → ideation → [HITL] → wireframe → [HITL] → delivery → [HITL] → complete
```

- **`state.py`** — `UXPipelineState`, the `TypedDict` threaded through every node.
- **`orchestrator.py`** — LangGraph graph. One node per phase, all routed through a shared
  `human_review_gate` that uses `interrupt()` to pause for approval. Approve → advance;
  request revision → re-run the same phase with `feedback_loop` set.
- **`claude_skill_client.py`** — `invoke_skill(name, state)`. Loads `skills/<name>/SKILL.md`
  plus any `references/` and `assets/` files, and (once wired) calls the Claude Agent SDK
  with that skill mounted. Currently raises `NotImplementedError` — plug in your SDK client.

## Skills (one per phase)

| Skill | Node | Reads from state | Writes to state |
|---|---|---|---|
| `discovery-synthesis` | 1 | `raw_research_data` | `synthesized_insights` |
| `strategy-definition` | 2 | `synthesized_insights` | `persona_profile`, `journey_map`, `problem_statement` |
| `ideation-concepting` | 3 | `problem_statement`, `persona_profile` | `feature_matrix`, `concept_proposals` |
| `wireframe-ia` | 4 | `selected_concept` | `sitemap`, `wireframe_specs`, `design_tokens_applied` |
| `delivery-handoff` | 5 | `sitemap`, `wireframe_specs` | `developer_handoff_stories`, `microcopy` |

## Conventions

- **Skills never invent data.** If an input is missing or thin, the skill flags the gap
  explicitly instead of fabricating personas, quotes, or metrics.
- **Humans make the choices.** Ideation proposes 2-3 concepts but never picks a winner;
  the `selected_concept` is set by a person at the HITL gate.
- **The design system is law.** `wireframe-ia` maps every color, size, space, and radius to
  `skills/wireframe-ia/references/superlap-design-tokens.json`. A need outside the token set
  is reported as a "Design System Gap", never solved with a new hex value.
- Skill I/O is a JSON-serializable dict matching the "Output contract" in each `SKILL.md`.

## Working on this repo

- Add a phase → new `skills/<name>/SKILL.md`, new node in `orchestrator.py`, extend the
  `order` list in `next_phase()` and the `current_phase` literal in `state.py`.
- `graph.compile(checkpointer=...)` is currently `None`. For HITL pause/resume that survives
  a process restart, pass a persistent checkpointer (e.g. `SqliteSaver`).
- The Superlap design tokens were extracted verbatim from the source brand analysis. Scope
  is color / typography / space / radius / shadow; motion and drawer-shorthand rules live in
  `assets/component-patterns.md` as narrative, not tokens.
