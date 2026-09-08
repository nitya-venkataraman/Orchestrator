#!/usr/bin/env python3
"""
Stage 1 (discovery-synthesis) Tier-1 validator — deterministic, no LLM.

Implements the Tier-1 rules in `rules/CONTRACTS.md` § Stage 1:
  - valid JSON in the SynthesisOutput shape
  - 2-6 themes; each theme has >= 1 quote
  - 1 <= frequency <= source_count
  - severity in {high, medium, low}
  - quote text appears verbatim in the corpus (only when the corpus is passed
    as context["raw_research_data"])

Usage:
    python validators/synthesis.py output/discovery-synthesis-<slug>.json
    cat artifact.json | python validators/synthesis.py -
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import re
import sys
from typing import List, Optional

SEVERITIES = {"high", "medium", "low"}
MIN_THEMES, MAX_THEMES = 2, 6


def _coerce(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = (parts[1] if len(parts) > 1 else raw).lstrip("json").strip()
    return json.loads(raw)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []
    context = context or {}

    themes = data.get("themes")
    if not isinstance(themes, list):
        return ["Missing or non-list 'themes'"]
    if not (MIN_THEMES <= len(themes) <= MAX_THEMES):
        errors.append(
            "Theme count {0} outside allowed range {1}-{2}".format(
                len(themes), MIN_THEMES, MAX_THEMES
            )
        )

    source_count = data.get("source_count")
    if not isinstance(source_count, int) or source_count < 1:
        errors.append("'source_count' must be an integer >= 1")
        source_count = None

    if "gaps" not in data or not isinstance(data["gaps"], list):
        errors.append("Missing or non-list 'gaps'")

    _raw = context.get("raw_research_data")
    corpus = _norm(str(_raw)) if _raw else None

    for i, theme in enumerate(themes, 1):
        label = theme.get("name") or "theme {0}".format(i)
        if not theme.get("name"):
            errors.append("Theme {0} has no name".format(i))
        if not theme.get("insight"):
            errors.append("Theme '{0}' has no insight".format(label))

        sev = theme.get("severity")
        if sev not in SEVERITIES:
            errors.append(
                "Theme '{0}' severity {1!r} not in {2}".format(label, sev, sorted(SEVERITIES))
            )

        freq = theme.get("frequency")
        if not isinstance(freq, int) or freq < 1:
            errors.append("Theme '{0}' frequency must be an integer >= 1".format(label))
        elif source_count is not None and freq > source_count:
            errors.append(
                "Theme '{0}' frequency {1} exceeds source_count {2}".format(
                    label, freq, source_count
                )
            )

        quotes = theme.get("quotes") or []
        if not quotes:
            errors.append("Theme '{0}' has no quotes".format(label))
        for q in quotes:
            qtext = q.get("text") if isinstance(q, dict) else None
            if not qtext:
                errors.append("Theme '{0}' has a quote with no text".format(label))
                continue
            if corpus is not None and _norm(qtext) not in corpus:
                errors.append(
                    "Theme '{0}' quote not found verbatim in the corpus: {1!r}".format(
                        label, qtext[:60]
                    )
                )

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
    print("PASS — {0} themes, structure clean.".format(len(data.get("themes", []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
