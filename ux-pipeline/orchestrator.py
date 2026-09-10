"""
LangGraph orchestrator for the ux-pipeline.

Per stage:  run (cache-checked)  ->  gate (Tier-1 + Tier-2)  ->  human review
            \\__________________ retry with feedback (max 2) _________________/

The gate is machine-only: an artifact reaches the human only after it passes the
deterministic Tier-1 checks in `validators/` and the Tier-2 judge scores it
acceptable (1-5 per dimension) against `rules/rubrics/<stage>.md`. Retries
exhausted -> the artifact is escalated to the human anyway, flagged with what
the gate objected to.

After ideation is approved the graph forks to `select_direction`: a human picks
one design direction before wireframing.

State, artifacts, and the audit trail live under `workspace/` so a run survives
the process. `graph` is compiled with a SqliteSaver checkpointer when available.
"""
from __future__ import annotations

import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command

import cache
import rubrics
from claude_skill_client import invoke_skill
from state import UXPipelineState
from validators import run_tier1

WORKSPACE = Path(os.environ.get("UX_PIPELINE_WORKSPACE", "workspace"))
ARTIFACTS_DIR = WORKSPACE / "artifacts"
EVENTS_LOG = WORKSPACE / "events.jsonl"
RUN_JSON = WORKSPACE / "run.json"

# stage order + the skill each node invokes
ORDER = ["discovery", "strategy", "ideation", "wireframe", "delivery", "evaluation"]
SKILL = {
    "discovery": "discovery-synthesis",
    "strategy": "strategy-definition",
    "ideation": "ideation-concepting",
    "wireframe": "wireframe-ia",
    "delivery": "delivery-handoff",
    "evaluation": "evaluation-planning",
}
# Tier-2 scoring is 1-5 per dimension against rules/rubrics/<stage>.md; the pass rule
# for each stage lives in that file's json block (see rules/rubrics/README.md).
MAX_ATTEMPTS = 2  # a 3rd failure escalates instead of retrying


# --- helpers ---------------------------------------------------------------------


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log_event(run_id: str, kind: str, **fields) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    rec = {"ts": _now(), "run_id": run_id, "event": kind}
    rec.update(fields)
    with open(EVENTS_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s or "run"


def stage_of(state: UXPipelineState) -> str:
    return state["current_phase"].replace("_review", "")


def next_stage(stage: str) -> str:
    idx = ORDER.index(stage)
    return ORDER[idx + 1] if idx + 1 < len(ORDER) else "complete"


def _artifact_key(stage: str) -> str:
    """State key holding the stage's primary artifact."""
    return {
        "discovery": "synthesized_insights",
        "strategy": "persona_profile",  # strategy writes 3 keys; this is the anchor
        "ideation": "feature_matrix",
        "wireframe": "wireframe_specs",
        "delivery": "developer_handoff_stories",
        "evaluation": "evaluation_plan",
    }[stage]


def _collect_artifact(stage: str, state: UXPipelineState) -> dict:
    """Reassemble the rules/CONTRACTS.md JSON shape from the stage's state keys."""
    if stage == "discovery":
        return state.get("synthesized_insights") or {}
    if stage == "strategy":
        return {
            "personas": state.get("persona_profile") or [],
            "journey": state.get("journey_map") or [],
            "hmw_statements": state.get("problem_statement") or [],
        }
    if stage == "ideation":
        return {
            "features": state.get("feature_matrix") or [],
            "design_directions": state.get("concept_proposals") or [],
        }
    if stage == "wireframe":
        return {
            "target": state.get("target_surface"),
            "mobile_platform": state.get("mobile_platform"),
            "design_system": state.get("design_system") or {},
            "ux_interpretation": state.get("ux_interpretation") or {},
            "user_flow": state.get("user_flow") or {},
            "sitemap": state.get("sitemap") or [],
            "pages": state.get("wireframe_specs") or [],
            "responsive_matrix": state.get("responsive_matrix") or [],
            "prototype_flows": state.get("prototype_flows") or [],
            "design_system_gaps": state.get("design_system_gaps") or [],
            "heuristic_review": state.get("heuristic_review") or [],
            "assumptions": state.get("assumptions") or [],
            "validation": state.get("validation") or {},
            "design_tokens_applied": state.get("design_tokens_applied"),
            "figma_file_url": state.get("figma_file_url"),
        }
    if stage == "delivery":
        return {
            "stories": state.get("developer_handoff_stories") or [],
            "microcopy": state.get("microcopy") or {},
        }
    if stage == "evaluation":
        # Stage 6 writes one whole artifact rather than a set of state keys.
        return state.get("evaluation_plan") or {}
    return {}


def _tier1_context(stage: str, state: UXPipelineState) -> dict:
    return {
        "raw_research_data": state.get("raw_research_data"),
        "synthesized_insights": state.get("synthesized_insights"),
        "problem_statement": {"hmw_statements": state.get("problem_statement") or []},
        "persona_profile": {"personas": state.get("persona_profile") or []},
        "feature_matrix": {"features": state.get("feature_matrix") or []},
        "selected_direction": state.get("selected_direction"),
        "target_surface": state.get("target_surface"),
        "mobile_platform": state.get("mobile_platform"),
        "design_system_input": state.get("design_system_input"),
        "wireframe_specs": {"pages": state.get("wireframe_specs") or []},
        "journey_map": {"journey": state.get("journey_map") or []},
        "developer_handoff_stories": {
            "stories": state.get("developer_handoff_stories") or []
        },
    }


def _tier2_reasons(scores: Dict) -> List[str]:
    """Turn a failing judge result into a concrete revision-feedback list."""
    rationale = scores.get("rationale") or {}
    per_dim = scores.get("scores") or {}
    weak = scores.get("weak") or []
    if weak:
        return ["{0} scored {1}/5 — {2}".format(
            k, per_dim.get(k, "?"), rationale.get(k) or "see rules/rubrics") for k in weak]
    # every dimension >= 4 but the stage's pass_when still rejected it
    return [
        "Tier-2 rubric not met (weighted mean {0:.2f}). Dimension scores: {1}. "
        "Raise the ones the stage rubric floors hardest.".format(
            scores.get("score", 0.0),
            ", ".join("{0}={1}".format(k, v) for k, v in sorted(per_dim.items())),
        )
    ]


def _judge_prompt(stage: str, artifact: dict, state: UXPipelineState) -> str:
    """Assemble the Tier-2 judge prompt: the rubric + the artifact + its source material."""
    context = _tier1_context(stage, state)
    return (
        rubrics.load_rubric(stage)
        + "\n\n---\n\n## Artifact under review\n\n"
        + json.dumps(artifact, indent=2)
        + "\n\n## Source material (score against this)\n\n"
        + json.dumps({k: v for k, v in context.items() if v}, indent=2)
        + "\n\nReturn the JSON object described in the scoring contract."
    )


def _judge_model(prompt: str) -> Dict[str, dict]:
    """
    The model call. Wire this to a Claude request that returns, per rubric dimension,
    {"score": 1-5, "rationale": "...", "evidence": "..."}.

    Stubbed like `claude_skill_client.invoke_skill` — the scoring logic around it
    (`judge`, `rubrics.evaluate`) is real and tested.
    """
    raise NotImplementedError(
        "Wire _judge_model() to a Claude call. It receives the assembled rubric + "
        "artifact + source material and must return a per-dimension 1-5 score map."
    )


def judge(stage: str, artifact: dict, state: UXPipelineState) -> Dict[str, float]:
    """
    Tier-2 judge. Scores the artifact 1-5 per dimension against
    rules/rubrics/<stage>.md and applies that rubric's pass rule.

    Returns {"score": <weighted mean>, "pass": bool, "weighted_mean": float,
             "weak": [dims < 4], "rationale": {dim: str}}.
    """
    raw = _judge_model(_judge_prompt(stage, artifact, state))
    weights = rubrics.rubric_spec(stage)["weights"]
    dim_scores = {k: raw[k]["score"] for k in weights if k in raw}
    result = rubrics.evaluate(stage, dim_scores)
    result["score"] = result["weighted_mean"]
    result["rationale"] = {k: raw[k].get("rationale", "") for k in dim_scores}
    return result


def _input_hash(stage: str, state: UXPipelineState, attempt: int) -> str:
    return cache.input_hash(
        state.get("raw_research_data"),
        json.dumps(_collect_artifact(_prior(stage), state), sort_keys=True) if _prior(stage) else "",
        state.get("feedback_loop"),
        state.get("selected_direction"),
        # only these shape the wireframe stage, so they only enter its key
        state.get("target_surface") if stage == "wireframe" else None,
        state.get("mobile_platform") if stage == "wireframe" else None,
        state.get("design_system_input") if stage == "wireframe" else None,
        attempt,
    )


def _prior(stage: str) -> Optional[str]:
    idx = ORDER.index(stage)
    return ORDER[idx - 1] if idx > 0 else None


# --- run lifecycle -------------------------------------------------------------


def load_or_init_run(state: UXPipelineState) -> dict:
    """Resume from workspace/run.json if present, else start a fresh run record."""
    if RUN_JSON.exists():
        record = json.loads(RUN_JSON.read_text(encoding="utf-8"))
        return record
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    record = {
        "run_id": state.get("run_id") or uuid.uuid4().hex[:12],
        "run_slug": state.get("run_slug") or slugify(state.get("project_brief", "")),
        "stage_status": {s: "PENDING" for s in ORDER},
        "selected_direction": None,
        "target_surface": None,
        "mobile_platform": None,
        "design_system_input": None,
    }
    RUN_JSON.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def _save_run(record: dict) -> None:
    RUN_JSON.write_text(json.dumps(record, indent=2), encoding="utf-8")


# --- nodes -------------------------------------------------------------------


def _run_stage(stage: str, state: UXPipelineState) -> dict:
    record = load_or_init_run(state)
    run_id, slug = record["run_id"], record["run_slug"]
    attempts = dict(state.get("attempts") or {})
    attempt = attempts.get(stage, 0)

    ihash = _input_hash(stage, state, attempt)
    cached = cache.get(run_id, stage, attempt, ihash)
    if cached is not None:
        log_event(run_id, "cache_hit", stage=stage, attempt=attempt)
        result = cached if isinstance(cached, dict) else json.loads(cached)
    else:
        log_event(run_id, "stage_run", stage=stage, attempt=attempt)
        result = invoke_skill(SKILL[stage], state)
        cache.put(run_id, stage, attempt, ihash, result)

    status = dict(state.get("stage_status") or record["stage_status"])
    status[stage] = "RUNNING"
    return {
        **result,
        "run_id": run_id,
        "run_slug": slug,
        "attempts": attempts,
        "stage_status": status,
        "current_phase": stage + "_review",
    }


def discovery_node(state: UXPipelineState) -> dict:
    return _run_stage("discovery", state)


def strategy_node(state: UXPipelineState) -> dict:
    return _run_stage("strategy", state)


def ideation_node(state: UXPipelineState) -> dict:
    return _run_stage("ideation", state)


def wireframe_node(state: UXPipelineState) -> dict:
    return _run_stage("wireframe", state)


def delivery_node(state: UXPipelineState) -> dict:
    return _run_stage("delivery", state)


def evaluation_node(state: UXPipelineState) -> dict:
    return _run_stage("evaluation", state)


def gate_node(state: UXPipelineState) -> Command:
    """Tier-1 structural + Tier-2 judge. Pass -> human; fail -> retry or escalate."""
    stage = stage_of(state)
    record = load_or_init_run(state)
    run_id = record["run_id"]
    artifact = _collect_artifact(stage, state)

    tier1 = run_tier1(stage, artifact, _tier1_context(stage, state))
    scores = {} if tier1 else judge(stage, artifact, state)
    score = float(scores.get("score", 0.0))
    tier2_fail = (not tier1) and not scores.get("pass", False)

    attempts = dict(state.get("attempts") or {})
    status = dict(state.get("stage_status") or record["stage_status"])
    judge_scores = dict(state.get("judge_scores") or {})
    # `judge_scores[stage]` is the Tier-2 weighted mean on the rubric's 1-5
    # scale, and nothing else — never a 0-1 fraction, never a placeholder. A
    # Tier-1 failure means the judge never ran, so record None rather than 0.0,
    # which would otherwise read as a real (impossibly low) score.
    judge_scores[stage] = None if tier1 else score

    if tier1 or tier2_fail:
        reason = tier1 or _tier2_reasons(scores)
        attempts[stage] = attempts.get(stage, 0) + 1
        cache.invalidate(run_id, stage)
        log_event(run_id, "gate_fail", stage=stage, attempt=attempts[stage],
                  tier="1" if tier1 else "2", reasons=reason)

        if attempts[stage] > MAX_ATTEMPTS:
            status[stage] = "ESCALATED"
            _save_status(record, status)
            return Command(
                update={
                    "attempts": attempts, "stage_status": status,
                    "judge_scores": judge_scores, "escalated": True,
                    "feedback_loop": "GATE ESCALATION — unresolved after {0} attempts:\n- {1}".format(
                        MAX_ATTEMPTS, "\n- ".join(reason)
                    ),
                },
                goto="human_review",
            )
        return Command(
            update={
                "attempts": attempts, "stage_status": status, "judge_scores": judge_scores,
                "feedback_loop": "Gate rejected this artifact. Fix exactly these:\n- "
                + "\n- ".join(reason),
            },
            goto=stage,
        )

    status[stage] = "AWAITING_APPROVAL"
    _save_status(record, status)
    log_event(run_id, "gate_pass", stage=stage, score=score)
    return Command(
        update={
            "attempts": attempts, "stage_status": status, "judge_scores": judge_scores,
            "escalated": False, "feedback_loop": None,
        },
        goto="human_review",
    )


def _save_status(record: dict, status: dict) -> None:
    record["stage_status"] = status
    _save_run(record)


def _persist_approved(stage: str, state: UXPipelineState, record: dict) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    artifact = _collect_artifact(stage, state)
    (ARTIFACTS_DIR / (stage + ".json")).write_text(
        json.dumps(artifact, indent=2), encoding="utf-8"
    )


def human_review_gate(state: UXPipelineState) -> Command:
    stage = stage_of(state)
    record = load_or_init_run(state)
    run_id = record["run_id"]

    decision = interrupt({
        "phase": state["current_phase"],
        "stage": stage,
        "escalated": bool(state.get("escalated")),
        "judge_score": (state.get("judge_scores") or {}).get(stage),
        "gate_notes": state.get("feedback_loop"),
        "message": "Review '{0}'. Approve, or revise with feedback.".format(stage),
    })

    attempts = dict(state.get("attempts") or {})
    status = dict(state.get("stage_status") or record["stage_status"])

    if decision.get("approved"):
        _persist_approved(stage, state, record)
        attempts[stage] = 0
        status[stage] = "APPROVED"
        _save_status(record, status)
        log_event(run_id, "approved", stage=stage)
        nxt = next_stage(stage)
        if stage == "ideation":
            nxt = "select_direction"
        return Command(
            update={
                "approved": True, "escalated": False, "feedback_loop": None,
                "attempts": attempts, "stage_status": status,
                "current_phase": nxt if nxt != "complete" else "complete",
            },
            goto=END if nxt == "complete" else nxt,
        )

    # revise: human feedback resets the retry counter and invalidates the cache
    attempts[stage] = 0
    status[stage] = "PENDING"
    cache.invalidate(run_id, stage)
    _save_status(record, status)
    log_event(run_id, "revision_requested", stage=stage, feedback=decision.get("feedback"))
    return Command(
        update={
            "approved": False, "escalated": False,
            "feedback_loop": decision.get("feedback"),
            "attempts": attempts, "stage_status": status,
            "current_phase": stage,
        },
        goto=stage,
    )


def select_direction_node(state: UXPipelineState) -> Command:
    """Fork: a human picks the direction, the target surface, and the design system.

    Stage 4 is design-system agnostic, so `design_system_input` is whatever the
    project already has (a library name, a token file, a Figma library URL, a
    styleguide). Left empty, the stage falls back to a documented baseline and
    records that as an assumption.
    """
    record = load_or_init_run(state)
    directions = state.get("concept_proposals") or []
    choice = interrupt({
        "phase": "select_direction",
        "message": (
            "Pick one design direction to carry into wireframing, the target surface "
            "(web, mobile, or both), the mobile platform if the surface includes "
            "mobile, and the design system to reuse (if the project has one)."
        ),
        "directions": [
            {"name": d.get("name"), "summary": d.get("summary"),
             "differentiator": d.get("differentiator"), "tradeoff": d.get("tradeoff")}
            for d in directions
        ],
        "surfaces": ["web", "mobile", "both"],
        "mobile_platforms": ["android", "ios"],
    })
    picked = choice.get("selected_direction") or choice.get("name")
    surface = (choice.get("target_surface") or choice.get("surface") or "").lower() or None
    platform = (choice.get("mobile_platform") or choice.get("platform") or "").lower() or None
    if surface == "web":
        platform = None
    design_system_input = choice.get("design_system_input") or choice.get("design_system") or None
    record["selected_direction"] = picked
    record["target_surface"] = surface
    record["mobile_platform"] = platform
    record["design_system_input"] = design_system_input
    _save_run(record)
    log_event(
        record["run_id"], "direction_selected", direction=picked,
        surface=surface, platform=platform,
        design_system=design_system_input or "(baseline)",
    )
    return Command(
        update={
            "selected_direction": picked,
            "selected_concept": picked,
            "target_surface": surface,
            "mobile_platform": platform,
            "design_system_input": design_system_input,
            "current_phase": "wireframe",
        },
        goto="wireframe",
    )


# --- graph ------------------------------------------------------------------

builder = StateGraph(UXPipelineState)
builder.add_node("discovery", discovery_node)
builder.add_node("strategy", strategy_node)
builder.add_node("ideation", ideation_node)
builder.add_node("wireframe", wireframe_node)
builder.add_node("delivery", delivery_node)
builder.add_node("evaluation", evaluation_node)
builder.add_node("gate", gate_node)
builder.add_node("human_review", human_review_gate)
builder.add_node("select_direction", select_direction_node)

for node in ORDER:
    builder.add_edge(node, "gate")

builder.set_entry_point("discovery")


def _checkpointer():
    """Prefer a durable SqliteSaver so HITL interrupts survive a restart."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver

        return SqliteSaver.from_conn_string(str(WORKSPACE / "checkpoints.sqlite"))
    except Exception:  # pragma: no cover - optional dependency
        try:
            from langgraph.checkpoint.memory import MemorySaver

            return MemorySaver()
        except Exception:
            return None


graph = builder.compile(checkpointer=_checkpointer())
