#!/usr/bin/env python3
"""
Tier-2 rubric loader + scoring for the ux-pipeline.

The rubric prose, dimension weights, and pass rule for each stage live in
`rules/rubrics/<skill-name>.md` (see `rules/rubrics/README.md`). This module reads
them, assembles the judge prompt, and turns a per-dimension 1-5 score map into a
pass/fail decision. It contains no model call — `orchestrator.judge()` owns that.

CLI:
    python ux-pipeline/rubrics.py <stage>          # print the assembled rubric
    python ux-pipeline/rubrics.py --check          # validate every rubric file
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_DIR = REPO_ROOT / "rules" / "rubrics"

# graph-node name / skill name -> rubric filename stem
_STAGE_TO_FILE = {
    "discovery": "discovery-synthesis",
    "discovery-synthesis": "discovery-synthesis",
    "strategy": "strategy-definition",
    "strategy-definition": "strategy-definition",
    "ideation": "ideation-concepting",
    "ideation-concepting": "ideation-concepting",
    "wireframe": "wireframe-ia",
    "wireframe-ia": "wireframe-ia",
    "delivery": "delivery-handoff",
    "delivery-handoff": "delivery-handoff",
}

_JSON_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def _stem(stage: str) -> str:
    key = (stage or "").replace("_review", "")
    try:
        return _STAGE_TO_FILE[key]
    except KeyError:
        raise ValueError("no rubric for stage {0!r}".format(stage))


def rubric_path(stage: str) -> Path:
    return RUBRIC_DIR / (_stem(stage) + ".md")


def load_rubric(stage: str) -> str:
    """The shared scoring contract + the stage rubric, concatenated for the judge prompt."""
    shared = (RUBRIC_DIR / "README.md").read_text(encoding="utf-8")
    stage_md = rubric_path(stage).read_text(encoding="utf-8")
    return "{0}\n\n---\n\n{1}".format(shared, stage_md)


def rubric_spec(stage: str) -> Dict:
    """Parse the machine-readable ```json block: {weights, pass_when}."""
    text = rubric_path(stage).read_text(encoding="utf-8")
    m = _JSON_FENCE.search(text)
    if not m:
        raise ValueError("no ```json block in {0}".format(rubric_path(stage).name))
    spec = json.loads(m.group(1))
    weights = spec.get("weights") or {}
    total = round(sum(weights.values()), 6)
    if total != 1.0:
        raise ValueError(
            "{0}: weights sum to {1}, expected 1.0".format(rubric_path(stage).name, total)
        )
    if "pass_when" not in spec:
        raise ValueError("{0}: missing pass_when".format(rubric_path(stage).name))
    return spec


def weighted_mean(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    return round(sum(scores[k] * w for k, w in weights.items()), 4)


def _pass(expr: str, scores: Dict[str, float], mean: float) -> bool:
    """Evaluate a rubric pass_when expression in a locked-down namespace."""
    env = {
        "__builtins__": {},
        "min": min(scores.values()) if scores else 0,
        "max": max(scores.values()) if scores else 0,
        "weighted_mean": mean,
        "scores": dict(scores),
    }
    return bool(eval(expr, env))  # noqa: S307 - expr is repo-controlled, env has no builtins


def evaluate(stage: str, scores: Dict[str, float]) -> Dict:
    """
    Apply the stage rubric to a per-dimension 1-5 score map.

    Returns {"scores", "weighted_mean", "pass", "weak": [dims scoring < 4]}.
    Raises if a required dimension is missing or out of the 1-5 range.
    """
    spec = rubric_spec(stage)
    weights = spec["weights"]
    missing = [k for k in weights if k not in scores]
    if missing:
        raise ValueError("stage {0}: missing scores for {1}".format(stage, missing))
    for k, v in scores.items():
        if not (1 <= v <= 5):
            raise ValueError("stage {0}: {1}={2} outside 1-5".format(stage, k, v))
    mean = weighted_mean(scores, weights)
    return {
        "scores": dict(scores),
        "weighted_mean": mean,
        "pass": _pass(spec["pass_when"], scores, mean),
        "weak": sorted(k for k, v in scores.items() if v < 4),
    }


def _check() -> int:
    bad = 0
    for stem in sorted(set(_STAGE_TO_FILE.values())):
        try:
            spec = rubric_spec(stem)
            print("ok   {0:22} weights sum 1.0, pass_when={1!r}".format(stem, spec["pass_when"]))
        except ValueError as exc:
            bad += 1
            print("FAIL {0:22} {1}".format(stem, exc))
    return 1 if bad else 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    if sys.argv[1] == "--check":
        return _check()
    print(load_rubric(sys.argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
