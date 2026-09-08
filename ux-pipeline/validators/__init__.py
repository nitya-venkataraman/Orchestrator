"""
Deterministic Tier-1 validators for the ux-pipeline, one module per stage.

Each stage module exposes `validate(data: dict, context: dict | None) -> list[str]`
returning a list of human-readable violation strings (empty == pass). `context`
carries prior approved artifacts for the cross-stage traceability checks; when a
needed upstream artifact is absent, that specific check is skipped rather than
failed.

`run_tier1(stage, artifact, context)` is the single entry point the orchestrator
calls. `stage` accepts either the graph node name (`discovery`, `strategy`,
`ideation`, `wireframe`, `delivery`) or the skill name
(`discovery-synthesis`, `strategy-definition`, `ideation-concepting`,
`wireframe-ia`, `delivery-handoff`).
"""
from __future__ import annotations

from typing import List, Optional

from . import synthesis, strategy, ideation, wireframe, delivery

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
}


def run_tier1(stage: str, artifact: dict, context: Optional[dict] = None) -> List[str]:
    """Return the Tier-1 violation list for `stage`'s `artifact` (empty == pass)."""
    key = (stage or "").replace("_review", "")
    try:
        module = _BY_STAGE[key]
    except KeyError:
        raise ValueError("no Tier-1 validator for stage {0!r}".format(stage))
    return module.validate(artifact, context)


__all__ = ["run_tier1", "synthesis", "strategy", "ideation", "wireframe", "delivery"]
