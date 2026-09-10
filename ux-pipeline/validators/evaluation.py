#!/usr/bin/env python3
"""
Stage 6 (evaluation-planning) Tier-1 validator — deterministic, no LLM.

Implements `rules/CONTRACTS.md` § Stage 6:
  - objective and what_would_change_the_design non-empty
  - method in {moderated, unmoderated}; participants.count >= 5 with segments
    and recruit_from
  - every segment names a Stage-2 persona (only when the Stage-2 artifact is
    passed as context["persona_profile"])
  - 3-8 tasks, each with scenario, success_criteria, a journey_stage matching a
    Stage-2 journey stage, and pages that are all Stage-4 pages (only when those
    artifacts are passed as context)
  - every Stage-3 success_metric appears exactly once in metric_plan, and every
    metric_plan event names a Stage-5 analytics_event (same context condition)
  - every Stage-3 metric with an unknown baseline is listed in open_baselines

Usage:
    python3 validators/evaluation.py output/<project-slug>/evaluation.json
Exit 0 = pass, 1 = violations.
"""
from __future__ import annotations

import json
import sys
from typing import List, Optional, Set

METHODS = {"moderated", "unmoderated"}
MIN_TASKS, MAX_TASKS = 3, 8
MIN_PARTICIPANTS = 5


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


def _is_str(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _persona_names(context: Optional[dict]) -> Optional[Set[str]]:
    doc = _load(context, "persona_profile")
    if not doc or not isinstance(doc.get("personas"), list):
        return None
    return {p.get("name") for p in doc["personas"] if isinstance(p, dict) and p.get("name")}


def _journey_stages(context: Optional[dict]) -> Optional[Set[str]]:
    doc = _load(context, "journey_map") or _load(context, "persona_profile")
    if not doc or not isinstance(doc.get("journey"), list):
        return None
    return {s.get("stage") for s in doc["journey"] if isinstance(s, dict) and s.get("stage")}


def _page_names(context: Optional[dict]) -> Optional[Set[str]]:
    doc = _load(context, "wireframe_specs")
    if not doc:
        return None
    for collection, key in (("pages", "page_name"), ("screens", "screen_name")):
        entries = doc.get(collection)
        if isinstance(entries, list):
            return {e.get(key) for e in entries if isinstance(e, dict) and e.get(key)}
    return None


def _success_metrics(context: Optional[dict]):
    """{metric name: baseline} from the Stage-3 artifact, or None."""
    doc = _load(context, "feature_matrix")
    if not doc or not isinstance(doc.get("features"), list):
        return None
    out = {}
    for f in doc["features"]:
        if not isinstance(f, dict):
            continue
        metric = f.get("success_metric")
        if isinstance(metric, dict) and metric.get("name"):
            out[metric["name"]] = metric.get("baseline")
    return out or None


def _event_names(context: Optional[dict]) -> Optional[Set[str]]:
    doc = _load(context, "developer_handoff_stories")
    if not doc or not isinstance(doc.get("stories"), list):
        return None
    names = set()
    for s in doc["stories"]:
        if not isinstance(s, dict):
            continue
        for ev in s.get("analytics_events") or []:
            if isinstance(ev, dict) and ev.get("event"):
                names.add(ev["event"])
    return names or None


def validate(data: dict, context: Optional[dict] = None) -> List[str]:
    errors: List[str] = []

    test = data.get("usability_test")
    if not isinstance(test, dict):
        errors.append("Missing or non-dict 'usability_test'")
        test = {}

    for key in ("objective", "what_would_change_the_design"):
        if not _is_str(test.get(key)):
            errors.append(
                "usability_test.{0} is missing or empty — a test whose result would "
                "change nothing is theatre".format(key)
            )

    method = test.get("method")
    if method not in METHODS:
        errors.append(
            "usability_test.method {0!r} not in {1}".format(method, sorted(METHODS))
        )

    persona_names = _persona_names(context)
    participants = test.get("participants")
    if not isinstance(participants, dict):
        errors.append("usability_test.participants is missing")
    else:
        count = participants.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < MIN_PARTICIPANTS:
            errors.append(
                "usability_test.participants.count must be an integer >= {0} "
                "(got {1!r})".format(MIN_PARTICIPANTS, count)
            )
        segments = participants.get("segments")
        if not isinstance(segments, list) or not segments:
            errors.append("usability_test.participants.segments is missing or empty")
        elif persona_names is not None:
            for seg in segments:
                if seg not in persona_names:
                    errors.append(
                        "participants segment {0!r} is not a Stage-2 persona — testing "
                        "with people the research never described tells you about a "
                        "different product".format(seg)
                    )
        if not _is_str(participants.get("recruit_from")):
            errors.append("usability_test.participants.recruit_from is missing or empty")

    journey_stages = _journey_stages(context)
    page_names = _page_names(context)
    tasks = test.get("tasks")
    if not isinstance(tasks, list):
        errors.append("Missing or non-list 'usability_test.tasks'")
        tasks = []
    if tasks and not (MIN_TASKS <= len(tasks) <= MAX_TASKS):
        errors.append(
            "Task count {0} outside {1}-{2}".format(len(tasks), MIN_TASKS, MAX_TASKS)
        )

    for i, task in enumerate(tasks, 1):
        label = (task.get("id") if isinstance(task, dict) else None) or "task {0}".format(i)
        if not isinstance(task, dict):
            errors.append("Task {0} is not an object".format(i))
            continue
        for key in ("scenario", "success_criteria"):
            if not _is_str(task.get(key)):
                errors.append("Task '{0}' has no {1}".format(label, key))

        stage = task.get("journey_stage")
        if not _is_str(stage):
            errors.append("Task '{0}' has no journey_stage".format(label))
        elif journey_stages is not None and stage not in journey_stages:
            errors.append(
                "Task '{0}' journey_stage {1!r} is not a Stage-2 journey stage".format(
                    label, stage
                )
            )

        pages = task.get("pages")
        if not isinstance(pages, list) or not pages:
            errors.append("Task '{0}' names no pages".format(label))
        elif page_names is not None:
            for page in pages:
                if page not in page_names:
                    errors.append(
                        "Task '{0}' page {1!r} is not a Stage-4 page".format(label, page)
                    )

        probes = task.get("probes")
        if probes is not None and not isinstance(probes, list):
            errors.append("Task '{0}' probes must be a list".format(label))

    # --- metric plan ---
    plan = data.get("metric_plan")
    if not isinstance(plan, list):
        errors.append("Missing or non-list 'metric_plan'")
        plan = []

    planned: List[str] = []
    event_names = _event_names(context)
    for i, row in enumerate(plan, 1):
        if not isinstance(row, dict):
            errors.append("metric_plan entry {0} is not an object".format(i))
            continue
        name = row.get("metric")
        label = name or "entry {0}".format(i)
        if not _is_str(name):
            errors.append("metric_plan entry {0} has no metric".format(i))
        else:
            planned.append(name)
        for key in ("feature", "baseline_source", "read_after"):
            if not _is_str(row.get(key)):
                errors.append("metric_plan {0!r} has no {1}".format(label, key))
        # `events` may legitimately be empty: not every metric is read from a UI
        # event — index coverage, a backend report, an ops figure. What Tier-1
        # can check is that any event named actually exists downstream; whether
        # an empty list is honest or lazy is `metric_integrity`'s call.
        events = row.get("events")
        if not isinstance(events, list):
            errors.append("metric_plan {0!r} events must be a list".format(label))
        elif event_names is not None:
            for ev in events:
                if ev not in event_names:
                    errors.append(
                        "metric_plan {0!r} event {1!r} is not a Stage-5 analytics "
                        "event".format(label, ev)
                    )

    open_baselines = data.get("open_baselines")
    if not isinstance(open_baselines, list):
        errors.append("open_baselines is missing — use [] if every baseline is known")
        open_baselines = []

    metrics = _success_metrics(context)
    if metrics is not None:
        for missing in sorted(set(metrics) - set(planned)):
            errors.append(
                "Stage-3 success_metric {0!r} has no metric_plan entry — a metric "
                "declared at ideation and never planned for is the same as not having "
                "declared it".format(missing)
            )
        for extra in sorted(set(planned) - set(metrics)):
            errors.append(
                "metric_plan {0!r} is not a Stage-3 success_metric".format(extra)
            )
        for name in sorted(planned):
            if planned.count(name) > 1:
                errors.append("metric_plan covers {0!r} more than once".format(name))
                break
        for name, baseline in sorted(metrics.items()):
            # A Stage-3 baseline may be the bare word or a sentence that opens
            # with it ("unknown — no current system records this").
            unknown = (
                isinstance(baseline, str)
                and baseline.strip().lower().startswith("unknown")
            )
            # The entry names the metric and says how it would be established, so
            # match on containment rather than equality.
            listed = any(
                isinstance(entry, str) and name in entry for entry in open_baselines
            )
            if unknown and not listed:
                errors.append(
                    "Stage-3 metric {0!r} has an unknown baseline but is absent from "
                    "open_baselines — not knowing is allowed, losing track of what you "
                    "don't know is not".format(name)
                )

    return errors


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: evaluation.py <artifact.json|->")
        return 2
    raw = sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()
    try:
        data = _coerce(raw)
    except json.JSONDecodeError as exc:
        print("FAIL — not valid JSON: {0}".format(exc))
        return 1

    errors = validate(data)
    if errors:
        print("FAIL — {0} Tier-1 violation(s):\n".format(len(errors)))
        for e in errors:
            print("  - {0}".format(e))
        return 1

    tasks = ((data.get("usability_test") or {}).get("tasks")) or []
    print("PASS — {0} task(s), {1} metric(s) planned.".format(
        len(tasks), len(data.get("metric_plan") or [])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
