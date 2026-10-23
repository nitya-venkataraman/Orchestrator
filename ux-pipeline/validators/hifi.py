#!/usr/bin/env python3
"""
Stage 4b (hifi-design) Tier-1 validator — deterministic, no LLM.

Implements `rules/CONTRACTS.md` § Stage 4b:
  - a blocked run (`blocking_gaps` non-empty) carries no screens and no page URL;
    it is a legitimate output, surfaced to the human so they can supply the missing
    Figma URL
  - otherwise: both Figma URLs and `hifi_figma_page_url` are Figma links, and
    `hifi_screens` is non-empty
  - every screen has a name, `wireframe_node_id` and `figma_node_id` in Figma's
    `123:456` form (a `-` left over from a URL is a bug), a `figma_url`, a known
    breakpoint, >= 1 known state, and >= 1 `components_used`
  - `figma_node_id` values are unique
  - no `components_used` entry is a raw colour value
  - every gap names its screen, its need and its reason
  - every Stage-4 page is covered by a screen whose name starts with the page name
    (only when the Stage-4 artifact is passed as context["wireframe_specs"])

Usage:
    python3 validators/hifi.py output/<project-slug>/hifi.json
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import re
import sys
from typing import List, Optional

BREAKPOINTS = {"desktop", "laptop", "tablet", "mobile"}
STATES = {"default", "loading", "empty", "error", "success", "disabled"}
_NODE_ID = re.compile(r"^\d+:\d+$")
_RAW_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")


def _coerce(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = (parts[1] if len(parts) > 1 else raw).lstrip("json").strip()
    return json.loads(raw)


def _is_figma(url) -> bool:
    return isinstance(url, str) and "figma.com/" in url


def _page_names(context: Optional[dict]) -> Optional[set]:
    if not context:
        return None
    doc = context.get("wireframe_specs")
    if isinstance(doc, str):
        try:
            doc = json.loads(doc)
        except json.JSONDecodeError:
            return None
    if not isinstance(doc, dict) or not isinstance(doc.get("pages"), list):
        return None
    return {p.get("page_name") for p in doc["pages"] if isinstance(p, dict) and p.get("page_name")}


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []

    screens = data.get("hifi_screens")
    blocking = data.get("blocking_gaps") or []

    if blocking:
        if screens:
            errors.append("blocking_gaps is set but hifi_screens is not empty — a blocked run builds nothing")
        if data.get("hifi_figma_page_url"):
            errors.append("blocking_gaps is set but hifi_figma_page_url is not null")
        return errors

    for key in ("figma_wireframe_url", "figma_design_system_url", "hifi_figma_page_url"):
        if not _is_figma(data.get(key)):
            errors.append("{0} is missing or not a Figma URL".format(key))

    if not isinstance(screens, list) or not screens:
        return errors + ["Missing or empty 'hifi_screens'"]

    seen = set()
    for i, s in enumerate(screens, 1):
        label = (s.get("name") if isinstance(s, dict) else None) or "screen {0}".format(i)
        if not isinstance(s, dict):
            errors.append("{0} is not an object".format(label))
            continue
        if not s.get("name"):
            errors.append("screen {0} has no name".format(i))
        for key in ("wireframe_node_id", "figma_node_id"):
            value = s.get(key)
            if not (isinstance(value, str) and _NODE_ID.match(value)):
                errors.append(
                    "Screen '{0}' {1} {2!r} is not a Figma node id (expected 123:456, not 123-456)".format(
                        label, key, value))
        node = s.get("figma_node_id")
        if node in seen:
            errors.append("Screen '{0}' repeats figma_node_id {1!r}".format(label, node))
        seen.add(node)
        if not _is_figma(s.get("figma_url")):
            errors.append("Screen '{0}' figma_url is missing or not a Figma URL".format(label))
        if s.get("breakpoint") not in BREAKPOINTS:
            errors.append("Screen '{0}' breakpoint {1!r} not in {2}".format(
                label, s.get("breakpoint"), sorted(BREAKPOINTS)))
        states = s.get("states")
        if not isinstance(states, list) or not states:
            errors.append("Screen '{0}' has no states".format(label))
        else:
            for st in states:
                if st not in STATES:
                    errors.append("Screen '{0}' state {1!r} not in {2}".format(label, st, sorted(STATES)))
        comps = s.get("components_used")
        if not isinstance(comps, list) or not comps:
            errors.append("Screen '{0}' has no components_used".format(label))
        else:
            for c in comps:
                if not isinstance(c, str) or _RAW_COLOUR.search(c):
                    errors.append(
                        "Screen '{0}' components_used entry {1!r} is a raw colour value, "
                        "not a design-system component".format(label, c))

    for j, g in enumerate(data.get("design_system_gaps") or [], 1):
        for key in ("screen", "need", "reason"):
            if not (isinstance(g, dict) and g.get(key)):
                errors.append("design_system_gaps entry {0} has no '{1}'".format(j, key))

    pages = _page_names(context)
    if pages:
        names = [s.get("name") or "" for s in screens if isinstance(s, dict)]
        for page in sorted(pages):
            if not any(n.startswith(page) for n in names):
                errors.append(
                    "Stage-4 page {0!r} has no hi-fi screen — the wireframe is not fully covered".format(page))

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
    print("PASS — {0} hi-fi screen(s), structure clean.".format(len(data.get("hifi_screens") or [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
