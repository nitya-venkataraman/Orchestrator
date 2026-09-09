#!/usr/bin/env python3
"""
Stage 4 (wireframe-ia) Tier-1 validator — deterministic, no LLM.

Checks a page-builder artifact against the rulebook — `rules/CONTRACTS.md`
§ Stage 4, the source of truth for the base-role taxonomy, the page and
component naming conventions, the required UI states, the accessibility keys,
the responsive coverage, and prototype reachability. This module implements
those rules; it does not redefine them. Narrative guidance lives in
`ux-pipeline/skills/wireframe-ia/assets/component-patterns.md`.

This stage is DESIGN-SYSTEM AGNOSTIC. There is no component allowlist — a
component's `name` is whatever the resolved design system calls it. What IS
fixed is the `base` ROLE taxonomy, so the spec stays checkable across any design
system.

Usage:
    python3 validators/wireframe.py wireframe.json
    cat wireframe.json | python3 validators/wireframe.py -

Exit code 0 = pass, 1 = violations found (printed to stdout).
"""
from __future__ import annotations

import json
import re
import sys
from typing import Dict, List, Optional, Set

# --- Base component ROLES (fixed taxonomy; component names stay free text) -----
BASE_ROLES = {
    # structure
    "Header", "Footer", "Navigation", "Sidebar", "Breadcrumb", "Tabs", "Layout",
    "Section", "Divider",
    # content
    "Card", "List", "Table", "Avatar", "Badge", "Chip", "Icon", "Link",
    "Accordion", "Carousel", "Chart", "Stepper",
    # input
    "Button", "Input", "Textarea", "Select", "Checkbox", "Radio", "Switch",
    "Slider", "DatePicker", "TimePicker", "Search", "Filter", "Upload", "Form",
    # navigation & overflow
    "Pagination", "Menu", "Tooltip", "Modal", "Drawer", "BottomSheet", "Popover",
    "FAB",
    # feedback
    "Toast", "Alert", "Banner", "Confirmation", "ProgressIndicator", "Skeleton",
    "EmptyState", "LoadingState", "ErrorState",
}

# Left-over vocabulary from the retired Superlap brutalist design system — a
# spec carrying these was copied forward and never re-based.
FORBIDDEN = [
    "--sl-", "sl-button", "sl-input", "sl-card", "sl-nav", "sl-table",
    "sl-tag", "sl-modal", "sl-banner", "brutalist",
]

# Colour must always be a token. `px` is allowed — the web breakpoints and the
# touch-target minimum are defined in px.
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RGB_RE = re.compile(r"\brgba?\(")

WEB_PAGE_RE = re.compile(r"^(\d{2}) - \S.*$")
MOBILE_PAGE_RE = re.compile(r"^M(\d{2}) - \S.*$")
COMPONENT_NAME_RE = re.compile(r"^(Page|Section|Component) / \S.*$")

TARGETS = {"web", "mobile", "both"}
MOBILE_PLATFORMS = {"android", "ios"}
DS_SOURCES = {"existing", "baseline"}
COMPONENT_SOURCES = {"reused", "new"}

REQUIRED_STATES = ("default", "loading", "empty", "error")
OPTIONAL_STATES = ("success", "disabled")
REQUIRED_A11Y = ("contrast", "keyboard_focus", "labels", "touch_targets", "reading_order")
WEB_BREAKPOINTS = ("desktop", "laptop", "tablet", "mobile")
REQUIRED_UX_KEYS = (
    "primary_user", "user_goal", "business_goal", "main_task", "context",
    "entry_point", "expected_outcome",
)
REQUIRED_PAGE_STRINGS = ("purpose", "primary_user", "primary_action", "navigation")
REQUIRED_PAGE_LISTS = ("content_structure", "data", "interactions")
REQUIRED_REQ_LISTS = ("data_dependencies", "edge_cases")
OPTIONAL_REQ_LISTS = ("permissions", "open_questions")
VALIDATION_KEYS = ("ux", "ui", "responsive", "accessibility", "prototype")

MIN_PAGES, MAX_PAGES = 3, 12
CTA_MAX_WORDS = 4


def coerce_json(raw: str) -> dict:
    """Extract JSON from an LLM string, tolerating code fences."""
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        raw = raw.lstrip("json").strip()
    return json.loads(raw)


def _is_str(val) -> bool:
    return isinstance(val, str) and bool(val.strip())


def _is_list(val) -> bool:
    return isinstance(val, list) and bool(val)


def _check_target(data: dict, errors: List[str]) -> str:
    target = str(data.get("target", "")).lower()
    if target not in TARGETS:
        errors.append(
            "target must be one of {0} (got {1!r})".format(
                ", ".join(sorted(TARGETS)), data.get("target")
            )
        )
    platform = data.get("mobile_platform")
    if target in ("mobile", "both"):
        if str(platform or "").lower() not in MOBILE_PLATFORMS:
            errors.append(
                "target {0!r} requires mobile_platform 'android' or 'ios' "
                "(got {1!r})".format(target, platform)
            )
    elif target == "web" and platform not in (None, "", "null"):
        errors.append(
            "target 'web' must not set mobile_platform (got {0!r})".format(platform)
        )
    return target


def _check_design_system(data: dict, errors: List[str]) -> None:
    ds = data.get("design_system")
    if not isinstance(ds, dict):
        errors.append("design_system must be an object {name, source, tokens}")
        return
    if not _is_str(ds.get("name")):
        errors.append("design_system.name is missing — name the system you designed against")
    source = str(ds.get("source", "")).lower()
    if source not in DS_SOURCES:
        errors.append(
            "design_system.source must be 'existing' or 'baseline' (got {0!r})".format(
                ds.get("source")
            )
        )
    if source == "baseline" and not _is_list(data.get("assumptions")):
        errors.append(
            "design_system.source is 'baseline' but assumptions is empty — record "
            "which system you chose and why"
        )
    tokens = ds.get("tokens")
    if not isinstance(tokens, dict):
        errors.append("design_system.tokens must be an object of referenced token names")
    else:
        for kind in ("color", "typography", "spacing"):
            if not _is_list(tokens.get(kind)):
                errors.append("design_system.tokens.{0} is missing or empty".format(kind))


def _check_ux_interpretation(data: dict, errors: List[str]) -> None:
    ux = data.get("ux_interpretation")
    if not isinstance(ux, dict):
        errors.append("ux_interpretation is missing — Stage 1 of the process is mandatory")
        return
    for key in REQUIRED_UX_KEYS:
        if not _is_str(ux.get(key)):
            errors.append("ux_interpretation.{0} is missing or empty".format(key))
    for key in ("required_data", "business_rules", "constraints", "dependencies"):
        if key in ux and not isinstance(ux[key], list):
            errors.append("ux_interpretation.{0} must be a list".format(key))


def _check_user_flow(data: dict, errors: List[str]) -> None:
    flow = data.get("user_flow")
    if not isinstance(flow, dict):
        errors.append("user_flow is missing")
        return
    if not _is_list(flow.get("primary_journey")):
        errors.append("user_flow.primary_journey is missing or empty")
    for key in ("supporting_tasks", "error_scenarios"):
        if key in flow and not isinstance(flow[key], list):
            errors.append("user_flow.{0} must be a list".format(key))


def _check_components(page_name: str, page: dict, errors: List[str]) -> None:
    comps = page.get("components")
    if not _is_list(comps):
        errors.append("Page '{0}' declares no components".format(page_name))
        return
    for comp in comps:
        if not isinstance(comp, dict):
            errors.append(
                "Page '{0}' component entries must be objects "
                "{{name, base, source}} (got {1!r})".format(page_name, comp)
            )
            continue
        name = comp.get("name")
        if not _is_str(name) or not COMPONENT_NAME_RE.match(name):
            errors.append(
                "Page '{0}' component name {1!r} must be "
                "'Page|Section|Component / <Name>'".format(page_name, name)
            )
        base = comp.get("base")
        if base not in BASE_ROLES:
            errors.append(
                "Page '{0}' component {1!r} has base role {2!r}, which is not in the "
                "role taxonomy — if nothing fits, file a design_system_gaps "
                "entry".format(page_name, name, base)
            )
        source = str(comp.get("source", "")).lower()
        if source not in COMPONENT_SOURCES:
            errors.append(
                "Page '{0}' component {1!r} source must be 'reused' or 'new' "
                "(got {2!r})".format(page_name, name, comp.get("source"))
            )
        if source == "new" and not _is_str(comp.get("why_new")):
            errors.append(
                "Page '{0}' component {1!r} is new but has no why_new — reuse before "
                "you create".format(page_name, name)
            )
        if "variants" in comp and not isinstance(comp["variants"], list):
            errors.append(
                "Page '{0}' component {1!r} variants must be a list".format(page_name, name)
            )


def _check_states(page_name: str, page: dict, errors: List[str]) -> None:
    states = page.get("states")
    if not isinstance(states, dict):
        errors.append("Page '{0}' has no states object".format(page_name))
        return
    for state in REQUIRED_STATES:
        if not _is_str(states.get(state)):
            errors.append("Page '{0}' states.{1} is missing or empty".format(page_name, state))
    for state in OPTIONAL_STATES:
        if state in states and not _is_str(states[state]):
            errors.append(
                "Page '{0}' states.{1} is present but empty".format(page_name, state)
            )


def _check_responsive(page_name: str, page: dict, is_mobile: bool, errors: List[str]) -> None:
    resp = page.get("responsive")
    if not isinstance(resp, dict):
        errors.append("Page '{0}' has no responsive object".format(page_name))
        return
    required = ("mobile",) if is_mobile else WEB_BREAKPOINTS
    for bp in required:
        if not _is_str(resp.get(bp)):
            errors.append(
                "Page '{0}' responsive.{1} is missing or empty".format(page_name, bp)
            )


def _check_accessibility(page_name: str, page: dict, errors: List[str]) -> None:
    a11y = page.get("accessibility")
    if not isinstance(a11y, dict):
        errors.append(
            "Page '{0}' has no accessibility object — accessibility is designed in, "
            "not added at the end".format(page_name)
        )
        return
    for key in REQUIRED_A11Y:
        if not _is_str(a11y.get(key)):
            errors.append("Page '{0}' accessibility.{1} is missing or empty".format(page_name, key))


def _check_requirements(page_name: str, page: dict, errors: List[str]) -> None:
    req = page.get("requirements")
    if not isinstance(req, dict):
        errors.append("Page '{0}' has no requirements block".format(page_name))
        return
    for field in REQUIRED_REQ_LISTS:
        if not _is_list(req.get(field)):
            errors.append(
                "Page '{0}' requirements.{1} is missing or empty".format(page_name, field)
            )
    for field in OPTIONAL_REQ_LISTS:
        if field in req and not isinstance(req[field], list):
            errors.append("Page '{0}' requirements.{1} must be a list".format(page_name, field))


def _check_page_names(pages: List[dict], target: str, errors: List[str]) -> Dict[str, List[str]]:
    """Validate the NN / MNN naming convention; return {family: [names in order]}."""
    families: Dict[str, List[tuple]] = {"web": [], "mobile": []}
    for page in pages:
        name = page.get("page_name")
        if not _is_str(name):
            errors.append("A page has no page_name")
            continue
        web, mob = WEB_PAGE_RE.match(name), MOBILE_PAGE_RE.match(name)
        if mob:
            families["mobile"].append((int(mob.group(1)), name))
        elif web:
            families["web"].append((int(web.group(1)), name))
        else:
            errors.append(
                "Page name {0!r} must be 'NN - Title' (web) or 'MNN - Title' "
                "(mobile)".format(name)
            )

    for family, entries in families.items():
        numbers = [n for n, _ in entries]
        for dupe in sorted({n for n in numbers if numbers.count(n) > 1}):
            errors.append(
                "Duplicate {0} page number {1:02d} — numbers are unique within a "
                "family".format(family, dupe)
            )

    if target == "web" and families["mobile"]:
        errors.append("target 'web' but mobile-named (MNN) pages are present")
    if target == "mobile" and families["web"]:
        errors.append("target 'mobile' but web-named (NN) pages are present")
    if target == "both":
        for family in ("web", "mobile"):
            if not families[family]:
                errors.append("target 'both' but no {0} pages were specced".format(family))

    return {
        family: [name for _, name in sorted(entries)]
        for family, entries in families.items()
    }


def _check_prototype(
    data: dict, page_names: Set[str], families: Dict[str, List[str]], errors: List[str]
) -> None:
    flows = data.get("prototype_flows")
    if not _is_list(flows):
        errors.append("prototype_flows is missing or empty — wire the primary journey")
        return

    edges: Dict[str, Set[str]] = {}
    for i, flow in enumerate(flows):
        if not isinstance(flow, dict):
            errors.append("prototype_flows[{0}] must be an object".format(i))
            continue
        src, dst = flow.get("from"), flow.get("to")
        for role, val in (("from", src), ("to", dst)):
            if not _is_str(val):
                errors.append("prototype_flows[{0}].{1} is missing".format(i, role))
            elif val not in page_names:
                errors.append(
                    "prototype_flows[{0}].{1} {2!r} is not a specced page".format(i, role, val)
                )
        for key in ("trigger", "interaction"):
            if not _is_str(flow.get(key)):
                errors.append("prototype_flows[{0}].{1} is missing".format(i, key))
        if _is_str(src) and _is_str(dst):
            edges.setdefault(src, set()).add(dst)

    # Every page must be reachable from its family's entry page — a page nobody
    # can navigate to cannot be part of a completable journey.
    for family, ordered in families.items():
        if not ordered:
            continue
        entry = ordered[0]
        seen, queue = {entry}, [entry]
        while queue:
            node = queue.pop()
            for nxt in edges.get(node, ()):  # noqa: B007
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        for orphan in sorted(set(ordered) - seen):
            errors.append(
                "Page '{0}' is unreachable from the {1} entry page '{2}' via "
                "prototype_flows".format(orphan, family, entry)
            )


def _check_responsive_matrix(data: dict, target: str, errors: List[str]) -> None:
    matrix = data.get("responsive_matrix")
    if target == "mobile":
        if matrix is not None and not isinstance(matrix, list):
            errors.append("responsive_matrix must be a list")
        return
    if not _is_list(matrix):
        errors.append(
            "responsive_matrix is missing or empty — every major component needs its "
            "behaviour across breakpoints"
        )
        return
    for i, row in enumerate(matrix):
        if not isinstance(row, dict):
            errors.append("responsive_matrix[{0}] must be an object".format(i))
            continue
        for key in ("component", "desktop", "tablet", "mobile"):
            if not _is_str(row.get(key)):
                errors.append("responsive_matrix[{0}].{1} is missing or empty".format(i, key))


def _check_validation(data: dict, errors: List[str]) -> None:
    val = data.get("validation")
    if not isinstance(val, dict):
        errors.append("validation is missing — Stage 14 of the process is mandatory")
        return
    for key in VALIDATION_KEYS:
        if not _is_list(val.get(key)):
            errors.append("validation.{0} is missing or empty".format(key))


def _check_gaps(data: dict, errors: List[str]) -> None:
    gaps = data.get("design_system_gaps")
    if gaps is None:
        errors.append("design_system_gaps is missing — use [] if there are genuinely none")
        return
    if not isinstance(gaps, list):
        errors.append("design_system_gaps must be a list")
        return
    for i, gap in enumerate(gaps):
        if not isinstance(gap, dict):
            errors.append("design_system_gaps[{0}] must be an object".format(i))
            continue
        for key in ("need", "why_insufficient"):
            if not _is_str(gap.get(key)):
                errors.append("design_system_gaps[{0}].{1} is missing".format(i, key))
        nearest = gap.get("nearest_role")
        if nearest not in BASE_ROLES:
            errors.append(
                "design_system_gaps[{0}].nearest_role {1!r} is not a base role".format(i, nearest)
            )


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    # `figma_file_url` is produced by the Figma render step, not a spec value —
    # exempt it from the hex / forbidden-term scan.
    blob = json.dumps({k: v for k, v in data.items() if k != "figma_file_url"})
    errors: List[str] = []
    low = blob.lower()

    for term in FORBIDDEN:
        if term in low:
            errors.append("Left-over Superlap DS term present: '{0}'".format(term))

    for hexval in sorted(set(HEX_RE.findall(blob))):
        errors.append("Raw hex '{0}' — colour must be a design-system token".format(hexval))
    if RGB_RE.search(blob):
        errors.append("Raw rgb()/rgba() colour — colour must be a design-system token")

    for key in ("target", "design_system", "sitemap", "pages", "design_tokens_applied"):
        if key not in data:
            errors.append("Missing required key: '{0}'".format(key))

    target = _check_target(data, errors)
    _check_design_system(data, errors)
    _check_ux_interpretation(data, errors)
    _check_user_flow(data, errors)

    if data.get("design_tokens_applied") is not True:
        errors.append("design_tokens_applied must be true")

    pages = data.get("pages") or []
    sitemap = data.get("sitemap") or []

    if not (MIN_PAGES <= len(pages) <= MAX_PAGES):
        errors.append(
            "Page count {0} outside allowed range {1}-{2}".format(
                len(pages), MIN_PAGES, MAX_PAGES
            )
        )

    families = _check_page_names(pages, target, errors)
    mobile_names = set(families.get("mobile") or [])

    for page in pages:
        name = page.get("page_name", "<unnamed>")

        for field in REQUIRED_PAGE_STRINGS:
            if not _is_str(page.get(field)):
                errors.append("Page '{0}' {1} is missing or empty".format(name, field))
        for field in REQUIRED_PAGE_LISTS:
            if not _is_list(page.get(field)):
                errors.append("Page '{0}' {1} is missing or empty".format(name, field))
        if "secondary_actions" in page and not isinstance(page["secondary_actions"], list):
            errors.append("Page '{0}' secondary_actions must be a list".format(name))

        action = page.get("primary_action")
        if _is_str(action):
            if any(c.isalpha() for c in action) and action == action.upper():
                errors.append(
                    "Page '{0}' primary_action {1!r} is ALL CAPS — labels are sentence "
                    "case".format(name, action)
                )
            if len(action.split()) > CTA_MAX_WORDS:
                errors.append(
                    "Page '{0}' primary_action {1!r} is over {2} words".format(
                        name, action, CTA_MAX_WORDS
                    )
                )

        _check_components(name, page, errors)
        _check_states(name, page, errors)
        _check_responsive(name, page, name in mobile_names, errors)
        _check_accessibility(name, page, errors)
        _check_requirements(name, page, errors)

    _check_responsive_matrix(data, target, errors)

    page_names = {p.get("page_name") for p in pages if _is_str(p.get("page_name"))}
    _check_prototype(data, page_names, families, errors)
    _check_validation(data, errors)
    _check_gaps(data, errors)

    if not _is_list(data.get("assumptions")) and not isinstance(data.get("assumptions"), list):
        errors.append("assumptions is missing — use [] if none were needed")

    # --- sitemap / pages must describe the same set ---
    sitemap_names: Set[str] = set()
    for node in sitemap:
        if isinstance(node, dict):
            if node.get("page"):
                sitemap_names.add(node["page"])
            for child in node.get("children") or []:
                sitemap_names.add(child)

    for missing in sorted(page_names - sitemap_names):
        errors.append("Page '{0}' is specced but absent from the sitemap".format(missing))
    for missing in sorted(sitemap_names - page_names):
        errors.append("Sitemap references '{0}' but no page spec exists".format(missing))

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    src = sys.argv[1]
    blob = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()

    try:
        data = coerce_json(blob)
    except (json.JSONDecodeError, IndexError) as exc:
        print("FAIL — invalid JSON: {0}".format(exc))
        return 1

    errors = validate(data)
    if errors:
        print("FAIL — {0} violation(s):\n".format(len(errors)))
        for err in errors:
            print("  - {0}".format(err))
        return 1

    print(
        "PASS — {0} pages, target '{1}', design system '{2}' clean.".format(
            len(data.get("pages", [])),
            data.get("target"),
            (data.get("design_system") or {}).get("name"),
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
