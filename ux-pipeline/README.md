# ux-pipeline

Human-in-the-loop UX design pipeline: raw research → synthesized insights → strategy →
concepts → wireframes/IA → developer handoff. Five Claude Agent SDK skills orchestrated by
a LangGraph state machine, with a human approval gate between every phase.

## Layout

```
ux-pipeline/
├── state.py                  # UXPipelineState TypedDict
├── orchestrator.py           # LangGraph graph + HITL review gate
├── claude_skill_client.py    # invoke_skill() — wire to your Claude Agent SDK client
├── CLAUDE.md                 # architecture + conventions
└── skills/
    ├── discovery-synthesis/SKILL.md
    ├── strategy-definition/SKILL.md
    ├── ideation-concepting/SKILL.md
    ├── wireframe-ia/
    │   ├── SKILL.md
    │   ├── references/superlap-design-tokens.json
    │   └── assets/component-patterns.md
    └── delivery-handoff/SKILL.md
```

## Status

Scaffold. `claude_skill_client.invoke_skill()` raises `NotImplementedError` — replace the
pseudo-call with a real Claude Agent SDK invocation, then plug a persistent checkpointer
into `graph.compile()` in `orchestrator.py` so the HITL interrupts survive restarts.

## Dependencies

- `langgraph`
- Claude Agent SDK (for `claude_skill_client.py`)

## Flow

```
discovery → [approve] → strategy → [approve] → ideation → [approve] → wireframe → [approve] → delivery → [approve] → complete
```

At each gate: approve to advance, or return revision feedback to re-run the same phase.
