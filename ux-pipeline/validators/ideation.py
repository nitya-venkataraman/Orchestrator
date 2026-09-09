#!/usr/bin/env python3
"""
Stage 3 (ideation-concepting) Tier-1 validator — deterministic, no LLM.

Implements `rules/CONTRACTS.md` § Stage 3:
  - 6-12 features
  - impact in {0.25, 0.5, 1, 2, 3}; confidence in {0.5, 0.8, 1.0};
    effort >= 0.5; reach >= 1
  - rice_score within 0.5 (or 1% for large scores) of the recomputed value
  - 2-3 design directions, each with a non-empty tradeoff
  - every feature.hmw matches a Stage-2 HMW (only when the Stage-2 artifact is
    passed as context["problem_statement"])

Usage:
    python3 validators/ideation.py output/ideation/ideation-<slug>.json
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import sys
from typing import List, Optional

IMPACTS = {0.25, 0.5, 1, 2, 3}
CONFIDENCES = {0.5, 0.8, 1.0}
MIN_FEATURES, MAX_FEATURES = 6, 12
MIN_DIR, MAX_DIR = 2, 3


def _coerce(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = (parts[1] if len(parts) > 1 else raw).lstrip("json").strip()
    return json.loads(raw)


def _rice(reach: float, impact: float, confidence: float, effort: float) -> float:
    return round(reach * impact * confidence / max(effort, 0.5), 1)


def _hmw_statements(context: Optional[dict]) -> Optional[set]:
    if not context:
        return None
    raw = context.get("problem_statement")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None
    if not isinstance(raw, dict):
        return None
    hmws = raw.get("hmw_statements")
    if not isinstance(hmws, list):
        return None
    return {h.get("statement") for h in hmws if isinstance(h, dict) and h.get("statement")}


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []

    features = data.get("features")
    if not isinstance(features, list):
        errors.append("Missing or non-list 'features'")
        features = []
    if features and not (MIN_FEATURES <= len(features) <= MAX_FEATURES):
        errors.append(
            "Feature count {0} outside {1}-{2}".format(len(features), MIN_FEATURES, MAX_FEATURES)
        )

    known_hmws = _hmw_statements(context)
    for i, f in enumerate(features, 1):
        label = f.get("name") or "feature {0}".format(i)
        if not f.get("description"):
            errors.append("Feature '{0}' has no description".format(label))
        hmw = f.get("hmw")
        if not hmw:
            errors.append("Feature '{0}' has no hmw".format(label))
        elif known_hmws is not None and hmw not in known_hmws:
            errors.append("Feature '{0}' hmw does not match any Stage-2 HMW".format(label))

        reach, impact = f.get("reach"), f.get("impact")
        confidence, effort = f.get("confidence"), f.get("effort")
        score = f.get("rice_score")

        if not _num(reach) or reach < 1:
            errors.append("Feature '{0}' reach must be a number >= 1".format(label))
        if impact not in IMPACTS:
            errors.append("Feature '{0}' impact {1!r} not in {2}".format(label, impact, sorted(IMPACTS)))
        if confidence not in CONFIDENCES:
            errors.append(
                "Feature '{0}' confidence {1!r} not in {2}".format(label, confidence, sorted(CONFIDENCES))
            )
        if not _num(effort) or effort < 0.5:
            errors.append("Feature '{0}' effort must be a number >= 0.5".format(label))

        if all(_num(v) for v in (reach, impact, confidence, effort)) and _num(score):
            expected = _rice(reach, impact, confidence, effort)
            tol = max(0.5, abs(expected) * 0.01)
            if abs(expected - score) > tol:
                errors.append(
                    "Feature '{0}' rice_score {1} != recomputed {2}".format(label, score, expected)
                )

    directions = data.get("design_directions")
    if not isinstance(directions, list):
        errors.append("Missing or non-list 'design_directions'")
        directions = []
    if directions and not (MIN_DIR <= len(directions) <= MAX_DIR):
        errors.append(
            "Direction count {0} outside {1}-{2}".format(len(directions), MIN_DIR, MAX_DIR)
        )
    for i, d in enumerate(directions, 1):
        label = d.get("name") or "direction {0}".format(i)
        for key in ("summary", "differentiator", "tradeoff"):
            if not d.get(key):
                errors.append("Direction '{0}' has empty or missing '{1}'".format(label, key))
        if not isinstance(d.get("hmws_addressed"), list) or not d.get("hmws_addressed"):
            errors.append("Direction '{0}' has no hmws_addressed".format(label))

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    blob = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    try:
        data = _coerce(blob)
    except (json.JSONDecodeError, IndexError) as exc:
        print("FAIL — invalid JSON: {0}".format(exc))
        return 1
    errors = validate(data)
    if errors:
        print("FAIL — {0} Tier-1 violation(s):\n".format(len(errors)))
        for e in errors:
            print("  - {0}".format(e))
        return 1
    print("PASS — {0} features, {1} directions, RICE arithmetic clean.".format(
        len(data.get("features", [])), len(data.get("design_directions", []))
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
