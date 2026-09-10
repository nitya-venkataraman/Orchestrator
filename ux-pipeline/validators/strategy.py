#!/usr/bin/env python3
"""
Stage 2 (strategy-definition) Tier-1 validator — deterministic, no LLM.

Implements `rules/CONTRACTS.md` § Stage 2:
  - 2-3 personas: exactly one primary, one or two secondary
  - every hmw_statements[*].statement starts with "how might we"
  - 4-7 journey stages; 3-5 HMW statements
  - dropoff_risk in {high, medium, low}
  - every persona grounded_in entry matches a Stage-1 theme name (only when the
    Stage-1 artifact is passed as context["synthesized_insights"])

Usage:
    python3 validators/strategy.py output/<project-slug>/strategy.json
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import sys
from typing import List, Optional

RISKS = {"high", "medium", "low"}
MIN_STAGES, MAX_STAGES = 4, 7
MIN_HMW, MAX_HMW = 3, 5
MIN_PERSONAS, MAX_PERSONAS = 2, 3


def _coerce(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = (parts[1] if len(parts) > 1 else raw).lstrip("json").strip()
    return json.loads(raw)


def _theme_names(context: Optional[dict]) -> Optional[set]:
    if not context:
        return None
    raw = context.get("synthesized_insights")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None
    if not isinstance(raw, dict):
        return None
    themes = raw.get("themes")
    if not isinstance(themes, list):
        return None
    return {t.get("name") for t in themes if isinstance(t, dict) and t.get("name")}


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []

    personas = data.get("personas")
    if not isinstance(personas, list):
        errors.append("Missing or non-list 'personas'")
        personas = []
    if personas and not MIN_PERSONAS <= len(personas) <= MAX_PERSONAS:
        errors.append(
            "Expected {0}-{1} personas, found {2}".format(
                MIN_PERSONAS, MAX_PERSONAS, len(personas)
            )
        )
    types = [p.get("type") for p in personas if isinstance(p, dict)]
    if personas:
        primaries = types.count("primary")
        secondaries = types.count("secondary")
        if primaries != 1:
            errors.append(
                "Expected exactly 1 'primary' persona, found {0}".format(primaries)
            )
        if secondaries != len(personas) - primaries or secondaries < 1:
            errors.append(
                "Every persona besides the primary must be 'secondary' "
                "(found {0} secondary of {1} personas)".format(secondaries, len(personas))
            )

    known_themes = _theme_names(context)
    for p in personas:
        label = p.get("name") or "<unnamed persona>"
        for key in ("context", "quote"):
            if not p.get(key):
                errors.append("Persona '{0}' has no {1}".format(label, key))
        for key in ("goals", "frustrations", "grounded_in"):
            if not isinstance(p.get(key), list) or not p.get(key):
                errors.append("Persona '{0}' has empty or missing '{1}'".format(label, key))
        if known_themes is not None:
            for g in p.get("grounded_in") or []:
                if g not in known_themes:
                    errors.append(
                        "Persona '{0}' grounded_in '{1}' is not a Stage-1 theme".format(label, g)
                    )

    journey = data.get("journey")
    if not isinstance(journey, list):
        errors.append("Missing or non-list 'journey'")
        journey = []
    if journey and not (MIN_STAGES <= len(journey) <= MAX_STAGES):
        errors.append(
            "Journey stage count {0} outside {1}-{2}".format(len(journey), MIN_STAGES, MAX_STAGES)
        )
    for s in journey:
        label = s.get("stage") or "<unnamed stage>"
        if s.get("dropoff_risk") not in RISKS:
            errors.append(
                "Journey stage '{0}' dropoff_risk {1!r} not in {2}".format(
                    label, s.get("dropoff_risk"), sorted(RISKS)
                )
            )
        if not s.get("emotion"):
            errors.append("Journey stage '{0}' has no emotion".format(label))
        if not isinstance(s.get("actions"), list) or not s.get("actions"):
            errors.append("Journey stage '{0}' has no actions".format(label))

    hmws = data.get("hmw_statements")
    if not isinstance(hmws, list):
        errors.append("Missing or non-list 'hmw_statements'")
        hmws = []
    if hmws and not (MIN_HMW <= len(hmws) <= MAX_HMW):
        errors.append("HMW count {0} outside {1}-{2}".format(len(hmws), MIN_HMW, MAX_HMW))
    for h in hmws:
        stmt = (h.get("statement") if isinstance(h, dict) else "") or ""
        if not stmt.strip().lower().startswith("how might we"):
            errors.append("HMW does not start with 'How might we': {0!r}".format(stmt[:60]))
        if not (h.get("derived_from") if isinstance(h, dict) else None):
            errors.append("HMW {0!r} has no derived_from".format(stmt[:40]))

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
    print("PASS — 2 personas, {0} journey stages, {1} HMWs.".format(
        len(data.get("journey", [])), len(data.get("hmw_statements", []))
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
