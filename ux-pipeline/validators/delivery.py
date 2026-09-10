#!/usr/bin/env python3
"""
Stage 5 (delivery-handoff) Tier-1 validator — deterministic, no LLM.

Implements `rules/CONTRACTS.md` § Stage 5:
  - >= 1 story; every story has persona, capability, benefit, and >= 1
    acceptance criterion with non-empty given/when/then
  - unique story ids (when present)
  - every persona matches a Stage-2 persona name (only when the Stage-2 artifact
    is passed as context["persona_profile"])
  - every Stage-4 page is referenced by >= 1 story (only when the Stage-4
    artifact is passed as context["wireframe_specs"]); legacy Stage-4 artifacts
    keyed on `screens` / `screen_name` are still accepted
  - every Stage-4 page is covered by >= 1 story carrying accessibility_criteria,
    so the accessibility Stage 4 designed in becomes a testable requirement
    instead of being dropped at the handoff boundary (same context condition)
  - analytics_events is present on stories whose page writes data, so a Stage-3
    success_metric is observable after ship (same context condition)
  - every microcopy cta_* value is sentence case, not ALL CAPS

Usage:
    python3 validators/delivery.py output/<project-slug>/delivery.json
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import sys
from typing import List, Optional


def _coerce(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = (parts[1] if len(parts) > 1 else raw).lstrip("json").strip()
    return json.loads(raw)


def _load(context: Optional[dict], key: str) -> Optional[dict]:
    if not context:
        return None
    raw = context.get(key)
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return None
    return raw if isinstance(raw, dict) else None


def _persona_names(context: Optional[dict]) -> Optional[set]:
    doc = _load(context, "persona_profile")
    if not doc or not isinstance(doc.get("personas"), list):
        return None
    return {p.get("name") for p in doc["personas"] if isinstance(p, dict) and p.get("name")}


def _screen_names(context: Optional[dict]) -> Optional[set]:
    """Stage-4 page names. Accepts the current `pages`/`page_name` shape and the
    legacy `screens`/`screen_name` one so older artifacts still gate."""
    doc = _load(context, "wireframe_specs")
    if not doc:
        return None
    for collection, key in (("pages", "page_name"), ("screens", "screen_name")):
        entries = doc.get(collection)
        if isinstance(entries, list):
            return {e.get(key) for e in entries if isinstance(e, dict) and e.get(key)}
    return None


# A page whose primary action writes data is one whose story needs
# instrumentation. Read/browse pages are exempt — an event on every page is
# noise, and noise is what makes analytics unusable.
_WRITE_VERBS = (
    "save", "submit", "create", "add", "commit", "confirm", "send", "upload",
    "delete", "remove", "assign", "approve", "sign", "publish", "book", "pay",
    "update", "edit", "apply", "invite", "start", "request", "flag", "record",
)


def _write_screens(context: Optional[dict]) -> Optional[set]:
    """Stage-4 pages whose `primary_action` writes data."""
    doc = _load(context, "wireframe_specs")
    if not doc:
        return None
    for collection, key in (("pages", "page_name"), ("screens", "screen_name")):
        entries = doc.get(collection)
        if not isinstance(entries, list):
            continue
        writes = set()
        for e in entries:
            if not isinstance(e, dict) or not e.get(key):
                continue
            action = (e.get("primary_action") or "").strip().lower()
            first = action.split()[0] if action else ""
            if first in _WRITE_VERBS:
                writes.add(e[key])
        return writes
    return None


def _check_gwt(entries, label: str, field: str, errors: List[str]) -> None:
    """Every Given/When/Then entry in `entries` must have all three parts."""
    for j, c in enumerate(entries, 1):
        for part in ("given", "when", "then"):
            if not (isinstance(c, dict) and c.get(part)):
                errors.append(
                    "Story '{0}' {1} {2} has no '{3}'".format(label, field, j, part)
                )


def _walk_cta(node, path, errors):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and (k == "cta_primary" or k.startswith("cta_")):
                if v and any(c.isalpha() for c in v) and v == v.upper():
                    errors.append(
                        "microcopy {0}.{1} is ALL CAPS — labels are sentence case: {2!r}".format(path, k, v)
                    )
            else:
                _walk_cta(v, "{0}.{1}".format(path, k), errors)


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []

    stories = data.get("stories")
    if not isinstance(stories, list) or not stories:
        return ["Missing or empty 'stories'"]

    persona_names = _persona_names(context)
    screen_names = _screen_names(context)
    write_screens = _write_screens(context)
    covered_screens = set()
    a11y_covered_screens = set()
    seen_ids = set()

    for i, s in enumerate(stories, 1):
        label = s.get("id") or "story {0}".format(i)
        sid = s.get("id")
        if sid:
            if sid in seen_ids:
                errors.append("Duplicate story id {0!r}".format(sid))
            seen_ids.add(sid)

        for key in ("persona", "capability", "benefit"):
            if not s.get(key):
                errors.append("Story '{0}' has no {1}".format(label, key))

        persona = s.get("persona")
        if persona and persona_names is not None and persona not in persona_names:
            errors.append(
                "Story '{0}' persona {1!r} is not a Stage-2 persona".format(label, persona)
            )

        screen = s.get("screen")
        if screen:
            covered_screens.add(screen)
            if screen_names is not None and screen not in screen_names:
                errors.append(
                    "Story '{0}' screen {1!r} is not a Stage-4 page".format(label, screen)
                )

        a11y = s.get("accessibility_criteria")
        if isinstance(a11y, list) and a11y:
            _check_gwt(a11y, label, "accessibility criterion", errors)
            if screen:
                a11y_covered_screens.add(screen)
        elif a11y is not None and not isinstance(a11y, list):
            errors.append("Story '{0}' accessibility_criteria must be a list".format(label))

        events = s.get("analytics_events")
        if events is not None and not isinstance(events, list):
            errors.append("Story '{0}' analytics_events must be a list".format(label))
        elif isinstance(events, list):
            for j, ev in enumerate(events, 1):
                if not isinstance(ev, dict) or not ev.get("event") or not ev.get("trigger"):
                    errors.append(
                        "Story '{0}' analytics_events {1} needs an 'event' and a "
                        "'trigger'".format(label, j)
                    )
        if screen and write_screens is not None and screen in write_screens:
            if not (isinstance(events, list) and events):
                errors.append(
                    "Story '{0}' lands on '{1}', whose primary action writes data, but "
                    "declares no analytics_events — a success_metric nothing emits is "
                    "not measurable".format(label, screen)
                )

        ac = s.get("acceptance_criteria")
        if not isinstance(ac, list) or not ac:
            errors.append("Story '{0}' has no acceptance_criteria".format(label))
            continue
        _check_gwt(ac, label, "criterion", errors)

    if screen_names is not None:
        for missing in sorted(screen_names - covered_screens):
            errors.append("Stage-4 page {0!r} is not covered by any story".format(missing))
        # Stage 4 designs accessibility in per page; if no story turns it into a
        # criterion, none of it is testable and it is dropped at the boundary.
        for missing in sorted(screen_names - a11y_covered_screens):
            errors.append(
                "Stage-4 page {0!r} has no story carrying accessibility_criteria — its "
                "accessibility block never becomes a testable requirement".format(missing)
            )

    microcopy = data.get("microcopy")
    if not isinstance(microcopy, dict):
        errors.append("Missing or non-dict 'microcopy'")
    else:
        _walk_cta(microcopy, "microcopy", errors)

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
    print("PASS — {0} stories, structure clean.".format(len(data.get("stories", []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
