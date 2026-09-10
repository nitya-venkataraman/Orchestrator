"""
Thin wrapper around the Claude Agent SDK's container.skills mechanism.
Replace `anthropic_client` with your configured SDK client.

`invoke_skill` is still a pseudo-call — it raises `NotImplementedError` — but the
payload it assembles is now the real one: the SKILL.md, the contents (not just
the paths) of the skill's `references/` and `assets/` files, the current run
state, any `feedback_loop` from a prior gate or human revision, and the prior
approved artifacts the stage needs as context for its traceability checks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

SKILLS_DIR = Path(__file__).parent / "skills"

# Which prior-stage state keys each stage reads as grounding context. Mirrors the
# "Reads from state" column in CLAUDE.md and the traceability rules in rules/CONTRACTS.md.
_CONTEXT_KEYS: Dict[str, List[str]] = {
    "discovery-synthesis": ["raw_research_data"],
    "strategy-definition": ["synthesized_insights"],
    "ideation-concepting": ["problem_statement", "persona_profile"],
    "wireframe-ia": [
        "feature_matrix", "concept_proposals", "selected_concept",
        "selected_direction", "target_surface", "mobile_platform",
        "design_system_input",
    ],
    "delivery-handoff": ["sitemap", "wireframe_specs", "persona_profile"],
    "evaluation-planning": [
        "journey_map", "persona_profile", "feature_matrix", "wireframe_specs",
        "heuristic_review", "developer_handoff_stories",
    ],
}


def _load_attachments(skill_name: str) -> Dict[str, str]:
    """Return {filename: file contents} for the skill's references + assets."""
    out: Dict[str, str] = {}
    for sub in ("references", "assets"):
        d = SKILLS_DIR / skill_name / sub
        if not d.exists():
            continue
        for p in sorted(d.glob("*")):
            if p.is_file():
                out[p.name] = p.read_text(encoding="utf-8")
    return out


def build_payload(skill_name: str, state: dict) -> dict:
    """Assemble everything the skill invocation needs. Pure, testable."""
    skill_md = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
    context = {k: state.get(k) for k in _CONTEXT_KEYS.get(skill_name, []) if state.get(k) is not None}
    return {
        "skill": skill_name,
        "skill_md": skill_md,
        "attachments": _load_attachments(skill_name),
        "run": {k: state.get(k) for k in ("run_id", "run_slug", "project_brief")},
        "context": context,
        "feedback_loop": state.get("feedback_loop"),
        "attempt": (state.get("attempts") or {}).get(skill_name, 0),
    }


def invoke_skill(skill_name: str, state: dict) -> dict:
    payload = build_payload(skill_name, state)

    # Pseudo-call — swap for a real Claude Agent SDK invocation:
    # response = anthropic_client.messages.create(
    #     model="claude-...",
    #     container={"skills": [skill_name]},
    #     messages=[{"role": "user", "content": json.dumps(payload)}],
    # )
    # return json.loads(response.content)

    raise NotImplementedError(
        "Wire this to your Claude Agent SDK client. Skill '{0}' payload ready: "
        "{1} attachment(s), context keys {2}, feedback_loop={3!r}.".format(
            skill_name,
            len(payload["attachments"]),
            sorted(payload["context"].keys()),
            payload["feedback_loop"],
        )
    )
