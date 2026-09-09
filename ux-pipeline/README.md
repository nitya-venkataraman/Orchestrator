# ux-pipeline

Human-in-the-loop UX design pipeline: raw research → synthesized insights → strategy →
concepts → wireframes/IA → developer handoff. Five Claude Agent SDK skills orchestrated by
a LangGraph state machine, with a two-tier machine gate and a human approval gate between
every phase.

The rulebook lives in a repo-level [`../rules/`](../rules/) folder:
[`../rules/CONTRACTS.md`](../rules/CONTRACTS.md) (per-stage schemas + Tier-1 rules)
and [`../rules/rubrics/`](../rules/rubrics/) (the Tier-2 scoring rubrics, one per stage).

## Layout

```
rules/
├── CONTRACTS.md              # per-stage JSON schema + deterministic Tier-1 rules
└── rubrics/<stage>.md        # Tier-2 rubric: dimensions, weights, anchors, pass rule

ux-pipeline/
├── state.py                  # UXPipelineState TypedDict (typed per ../rules/CONTRACTS.md)
├── orchestrator.py           # LangGraph graph: stage → gate → human_review, + fork
├── claude_skill_client.py    # invoke_skill() / build_payload() — wire to your SDK
├── rubrics.py                # loads ../rules/rubrics/, scores a 1–5 map against pass_when
├── cache.py                  # content-addressed artifact cache (workspace/cache/)
├── CLAUDE.md                 # architecture + conventions
├── validators/               # deterministic Tier-1, one module per stage + run_tier1()
└── skills/
    ├── discovery-synthesis/SKILL.md
    ├── strategy-definition/SKILL.md
    ├── ideation-concepting/SKILL.md
    ├── wireframe-ia/{SKILL.md, references/, assets/}
    └── delivery-handoff/SKILL.md
```

`workspace/` (gitignored) holds per-run state: `run.json`, `artifacts/<stage>.json`,
`cache/`, `events.jsonl`, `checkpoints.sqlite`.

## Status

Scaffold, contract-complete. Two model calls remain stubbed so the graph runs:

- `claude_skill_client.invoke_skill()` raises `NotImplementedError` — replace the
  pseudo-call with a real Claude Agent SDK invocation. `build_payload()` already assembles
  the real payload (SKILL.md, reference/asset contents, prior artifacts, `feedback_loop`).
- `orchestrator._judge_model()` raises `NotImplementedError` — replace with a Claude call
  that returns a 1–5 score + rationale + evidence per rubric dimension. Everything around
  it — prompt assembly (`_judge_prompt`), rubric loading (`rubrics.load_rubric`), the
  weighted mean and `pass_when` evaluation (`rubrics.evaluate`) — is real.

The Tier-1 validators (including the design-system-agnostic wireframe checks), the rubric scoring, the
cache, the retry/escalation gate, the direction + platform selection fork, and the
`output/` + `workspace/` persistence are all real and testable now.
Run `python3 ux-pipeline/rubrics.py --check` to validate the rubric files.

## Dependencies

- `langgraph`
- `langgraph-checkpoint-sqlite` — durable HITL resume
- Claude Agent SDK — for `claude_skill_client.py`

## Flow

```
discovery → gate → [approve] → strategy → gate → [approve] → ideation → gate → [approve]
   → PICK direction + platform → wireframe → gate → [approve] → delivery → gate → [approve] → complete
```

At the machine gate: Tier-1 structural, then Tier-2 rubric (1–5 per dimension against
`../rules/rubrics/<stage>.md`, pass rule in that file), else retry with feedback (max 2)
then escalate. At the human gate: approve to advance, or return revision feedback to re-run
the same phase (counter resets, cache invalidated).
