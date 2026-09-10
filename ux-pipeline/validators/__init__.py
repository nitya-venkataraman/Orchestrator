"""
Deterministic Tier-1 validators for the ux-pipeline, one module per stage.

Each stage module exposes `validate(data: dict, context: dict | None) -> list[str]`
returning a list of human-readable violation strings (empty == pass). `context`
carries prior approved artifacts for the cross-stage traceability checks; when a
needed upstream artifact is absent, that specific check is skipped rather than
failed.

`run_tier1(stage, artifact, context)` is the single entry point the orchestrator
calls. `stage` accepts either the graph node name (`discovery`, `strategy`,
`ideation`, `wireframe`, `delivery`, `evaluation`) or the skill name
(`discovery-synthesis`, `strategy-definition`, `ideation-concepting`,
`wireframe-ia`, `delivery-handoff`, `evaluation-planning`).
"""
from __future__ import annotations

from typing import List, Optional

from . import synthesis, strategy, ideation, wireframe, delivery, evaluation

# The contract these validators implement — `rules/CONTRACTS.md` § Contract
# versioning. Artifacts stamp the version they were produced under so a run from
# a skill still carrying an older copy of the rulebook is detectable rather than
# silently non-conforming. Validators do NOT soften themselves per version; the
# stamp is for humans and for CI, which reports an older artifact as legacy
# instead of demanding that fields be invented into it.
CONTRACT_VERSION = "2.0"

_BY_STAGE = {
    "discovery": synthesis,
    "discovery-synthesis": synthesis,
    "strategy": strategy,
    "strategy-definition": strategy,
    "ideation": ideation,
    "ideation-concepting": ideation,
    "wireframe": wireframe,
    "wireframe-ia": wireframe,
    "delivery": delivery,
    "delivery-handoff": delivery,
    "evaluation": evaluation,
    "evaluation-planning": evaluation,
}


def run_tier1(stage: str, artifact: dict, context: Optional[dict] = None) -> List[str]:
    """Return the Tier-1 violation list for `stage`'s `artifact` (empty == pass)."""
    key = (stage or "").replace("_review", "")
    try:
        module = _BY_STAGE[key]
    except KeyError:
        raise ValueError("no Tier-1 validator for stage {0!r}".format(stage))
    return module.validate(artifact, context)


def artifact_version(artifact: dict) -> Optional[str]:
    """The contract version an artifact was produced under, or None if unstamped."""
    if not isinstance(artifact, dict):
        return None
    version = artifact.get("contract_version")
    return version if isinstance(version, str) and version else None


def is_current(artifact: dict) -> bool:
    """True when the artifact was produced under the contract in force now."""
    return artifact_version(artifact) == CONTRACT_VERSION


__all__ = [
    "run_tier1", "artifact_version", "is_current", "CONTRACT_VERSION",
    "synthesis", "strategy", "ideation", "wireframe", "delivery", "evaluation",
]
