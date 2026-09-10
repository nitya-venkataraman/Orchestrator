#!/usr/bin/env python3
"""Self-tests for the ux-pipeline Tier-1 validators.

Runs every fixture under tests/fixtures/<skill-name>/ through
`validators.run_tier1()` — the same entry point the orchestrator's gate calls —
and asserts:

  - good-*.json  -> passes, with and without upstream context
  - bad-*.json   -> fails, and the registered diagnostic substring appears

A fixture may carry a sidecar `<name>.context.json` holding the upstream
artifacts (`synthesized_insights`, `problem_statement`, `persona_profile`,
`wireframe_specs`, `raw_research_data`). Cross-stage traceability checks are
skipped when their upstream artifact is absent — a deliberate softness
documented in validators/__init__.py, which means a bare
`python3 validators/<stage>.py file.json` is a weaker check than the gate's.
CONTEXT_ONLY registers the fixtures that prove it: they must FAIL with context
and PASS without it. If that ever inverts, either the softness leaked into a
check that should always run, or a traceability check stopped running.

No dependencies. Run: python3 ux-pipeline/tests/run_tests.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))

from validators import run_tier1  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"

Case = Tuple[str, str]  # (stage, fixture filename)

# bad fixture -> a substring that must appear in one of its violations
EXPECTED_BAD: Dict[Case, str] = {
    # --- Stage 1 ---
    ("discovery-synthesis", "bad-one-theme.json"): "outside allowed range 2-6",
    ("discovery-synthesis", "bad-frequency-exceeds-sources.json"): "exceeds source_count",
    ("discovery-synthesis", "bad-no-quotes.json"): "has no quotes",
    ("discovery-synthesis", "bad-severity-enum.json"): "severity 'critical' not in",
    ("discovery-synthesis", "bad-quote-not-verbatim.json"): "not found verbatim in the corpus",
    ("discovery-synthesis", "bad-source-is-a-name.json"): "does not open with a participant identifier",
    ("discovery-synthesis", "bad-source-is-an-email.json"): "contains an email address",
    ("discovery-synthesis", "bad-no-corpus.json"): "corpus is missing",
    # --- Stage 2 ---
    ("strategy-definition", "bad-four-personas.json"): "Expected 2-3 personas, found 4",
    ("strategy-definition", "bad-journey-too-short.json"): "Journey stage count 2 outside 4-7",
    ("strategy-definition", "bad-hmw-prefix.json"): "does not start with 'How might we'",
    ("strategy-definition", "bad-ungrounded-persona.json"): "is not a Stage-1 theme",
    # --- Stage 3 ---
    ("ideation-concepting", "bad-rice-arithmetic.json"): "!= recomputed",
    ("ideation-concepting", "bad-impact-scale.json"): "impact 1.75 not in",
    ("ideation-concepting", "bad-one-direction.json"): "Direction count 1 outside 2-3",
    ("ideation-concepting", "bad-unknown-hmw.json"): "does not match any Stage-2 HMW",
    ("ideation-concepting", "bad-no-success-metric.json"): "has no success_metric",
    # --- Stage 4 ---
    ("wireframe-ia", "bad-raw-hex.json"): "colour must be a design-system token",
    ("wireframe-ia", "bad-allcaps-cta.json"): "is ALL CAPS",
    ("wireframe-ia", "bad-missing-state.json"): "states.empty is missing or empty",
    ("wireframe-ia", "bad-orphan-page.json"): "is unreachable from the web entry page",
    ("wireframe-ia", "bad-new-without-why.json"): "reuse before you create",
    ("wireframe-ia", "bad-identical-a11y.json"): "identical to page",
    ("wireframe-ia", "bad-contrast-no-evidence.json"): "cites no evidence",
    ("wireframe-ia", "bad-touch-target-too-small.json"): "nothing at or above the minimum",
    ("wireframe-ia", "bad-heuristics-incomplete.json"): "heuristic_review does not cover",
    ("wireframe-ia", "bad-heuristics-all-clean-no-reason.json"): "a review that was not run",
    # The pre-page-builder artifact shape. Kept as a fixture so the schema it
    # drifted to can never quietly come back.
    ("wireframe-ia", "bad-legacy-schema.json"): "Missing required key: 'pages'",
    # --- Stage 5 ---
    ("delivery-handoff", "bad-no-criteria.json"): "has no acceptance_criteria",
    ("delivery-handoff", "bad-allcaps-cta.json"): "is ALL CAPS",
    ("delivery-handoff", "bad-unknown-persona.json"): "is not a Stage-2 persona",
    ("delivery-handoff", "bad-uncovered-screen.json"): "is not covered by any story",
    ("delivery-handoff", "bad-a11y-dropped-at-handoff.json"): "no story carrying accessibility_criteria",
    ("delivery-handoff", "bad-write-story-uninstrumented.json"): "declares no analytics_events",
    # --- Stage 6 ---
    ("evaluation-planning", "bad-no-consequence.json"): "would change nothing is theatre",
    ("evaluation-planning", "bad-too-few-participants.json"): "participants.count must be an integer >= 5",
    ("evaluation-planning", "bad-too-few-tasks.json"): "Task count 2 outside 3-8",
    ("evaluation-planning", "bad-method-enum.json"): "method 'survey' not in",
    ("evaluation-planning", "bad-segment-not-persona.json"): "is not a Stage-2 persona",
    ("evaluation-planning", "bad-task-page-unknown.json"): "is not a Stage-4 page",
    ("evaluation-planning", "bad-metric-unplanned.json"): "has no metric_plan entry",
    ("evaluation-planning", "bad-lost-unknown-baseline.json"): "absent from open_baselines",
    ("evaluation-planning", "bad-event-not-in-handoff.json"): "is not a Stage-5 analytics event",
}

# Fixtures whose violation exists only when the upstream artifact is supplied.
# These must FAIL with context and PASS without it.
CONTEXT_ONLY: Set[Case] = {
    ("discovery-synthesis", "bad-quote-not-verbatim.json"),
    ("strategy-definition", "bad-ungrounded-persona.json"),
    ("ideation-concepting", "bad-unknown-hmw.json"),
    ("delivery-handoff", "bad-unknown-persona.json"),
    ("delivery-handoff", "bad-uncovered-screen.json"),
    ("delivery-handoff", "bad-a11y-dropped-at-handoff.json"),
    ("delivery-handoff", "bad-write-story-uninstrumented.json"),
    ("evaluation-planning", "bad-segment-not-persona.json"),
    ("evaluation-planning", "bad-task-page-unknown.json"),
    ("evaluation-planning", "bad-metric-unplanned.json"),
    ("evaluation-planning", "bad-lost-unknown-baseline.json"),
    ("evaluation-planning", "bad-event-not-in-handoff.json"),
}

# Every alias run_tier1 must resolve, per the four stage vocabularies in
# ux-pipeline/CLAUDE.md. A path that silently doesn't resolve is the failure
# mode that table exists to warn about.
STAGE_ALIASES: Dict[str, List[str]] = {
    "discovery-synthesis": ["discovery", "discovery-synthesis", "discovery_review"],
    "strategy-definition": ["strategy", "strategy-definition", "strategy_review"],
    "ideation-concepting": ["ideation", "ideation-concepting", "ideation_review"],
    "wireframe-ia": ["wireframe", "wireframe-ia", "wireframe_review"],
    "delivery-handoff": ["delivery", "delivery-handoff", "delivery_review"],
    "evaluation-planning": ["evaluation", "evaluation-planning", "evaluation_review"],
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _context_for(fixture: Path) -> Optional[dict]:
    sidecar = fixture.parent / (fixture.stem + ".context.json")
    return _load(sidecar) if sidecar.is_file() else None


def _check_stage_registries(failures: List[str]) -> int:
    """
    Every stage must be registered in all six places that name it.

    ux-pipeline/CLAUDE.md warns that four different vocabularies exist for the
    same stages and that getting one wrong "produces a path that silently
    doesn't resolve". Adding a stage means touching orchestrator ORDER/SKILL and
    its node, the validator map, rubrics._STAGE_TO_FILE, the rubric file, and the
    skill directory. Miss one and the failure shows up at graph-build time, or
    not until a run reaches that stage. This checks all of them by reading the
    sources, so langgraph does not need to be installed.
    """
    pipeline_src = PIPELINE
    orch = (pipeline_src / "orchestrator.py").read_text(encoding="utf-8")
    rub = (pipeline_src / "rubrics.py").read_text(encoding="utf-8")

    order_match = re.search(r"^ORDER = \[(.*?)\]", orch, re.MULTILINE | re.DOTALL)
    if not order_match:
        failures.append("orchestrator.py: could not find ORDER")
        return 0
    order = [s.strip().strip('"\'') for s in order_match.group(1).split(",") if s.strip()]

    nodes = set(re.findall(r'builder\.add_node\("(\w+)"', orch))

    # Scope the SKILL lookup to its own block — several other stage-keyed dicts
    # in this module have the same line shape.
    skill_block = re.search(r"^SKILL = \{(.*?)^\}", orch, re.MULTILINE | re.DOTALL)
    if not skill_block:
        failures.append("orchestrator.py: could not find the SKILL map")
        return 0
    skill_map = dict(re.findall(r'"([\w-]+)":\s*"([\w-]+)"', skill_block.group(1)))
    checked = 0

    for stage in order:
        checked += 1
        if stage not in nodes:
            failures.append(
                "stage {0!r} is in ORDER but has no builder.add_node — the "
                "`for node in ORDER` edge loop will fail at graph build".format(stage)
            )
        skill = skill_map.get(stage)
        if not skill:
            failures.append("stage {0!r} is in ORDER but absent from SKILL".format(stage))
            continue
        if not (pipeline_src / "skills" / skill / "SKILL.md").is_file():
            failures.append("stage {0!r}: skills/{1}/SKILL.md is missing".format(stage, skill))
        if not (PIPELINE.parent / "rules" / "rubrics" / (skill + ".md")).is_file():
            failures.append("stage {0!r}: rules/rubrics/{1}.md is missing".format(stage, skill))
        if '"{0}"'.format(stage) not in rub or '"{0}"'.format(skill) not in rub:
            failures.append(
                "stage {0!r}: rubrics._STAGE_TO_FILE does not map both {0!r} and "
                "{1!r}".format(stage, skill)
            )
        for alias in (stage, skill):
            try:
                run_tier1(alias, {}, None)
            except ValueError:
                failures.append(
                    "stage {0!r}: run_tier1 has no validator for alias {1!r}".format(stage, alias)
                )
        if not (FIXTURES / skill).is_dir():
            failures.append("stage {0!r}: no fixture directory tests/fixtures/{1}/".format(stage, skill))
    return checked


def _check_aliases(failures: List[str]) -> int:
    """run_tier1 must accept the node name, the skill name, and the _review suffix."""
    checked = 0
    for stage, aliases in STAGE_ALIASES.items():
        good = sorted((FIXTURES / stage).glob("good-*.json"))
        if not good:
            failures.append("{0}: no good-*.json fixture to check aliases against".format(stage))
            continue
        artifact = _load(good[0])
        baseline = run_tier1(stage, artifact, None)
        for alias in aliases:
            checked += 1
            if run_tier1(alias, artifact, None) != baseline:
                failures.append(
                    "{0}: alias {1!r} does not resolve to the same validator".format(stage, alias)
                )
    return checked


def run() -> int:
    failures: List[str] = []
    checked = 0

    if not FIXTURES.is_dir():
        print("no fixtures directory at {0}".format(FIXTURES))
        return 1

    for stage_dir in sorted(p for p in FIXTURES.iterdir() if p.is_dir()):
        stage = stage_dir.name
        fixtures = [f for f in sorted(stage_dir.glob("*.json"))
                    if not f.name.endswith(".context.json")]
        if not fixtures:
            failures.append("{0}: fixture directory is empty".format(stage))
            continue

        for fx in fixtures:
            checked += 1
            case: Case = (stage, fx.name)
            label = "{0}/{1}".format(stage, fx.name)
            artifact = _load(fx)
            context = _context_for(fx)

            try:
                bare = run_tier1(stage, artifact, None)
                full = run_tier1(stage, artifact, context) if context is not None else bare
            except Exception as exc:  # a validator must never raise on real input
                failures.append("{0}: validator raised {1}: {2}".format(label, type(exc).__name__, exc))
                continue

            if fx.name.startswith("good-"):
                if bare or full:
                    failures.append(
                        "{0}: expected PASS, got {1}".format(label, sorted(set(bare) | set(full)))
                    )
                else:
                    print("ok    {0}  (PASS)".format(label))

            elif fx.name.startswith("bad-"):
                needle = EXPECTED_BAD.get(case)
                if needle is None:
                    failures.append("{0}: no expected substring registered in run_tests.py".format(label))
                    continue

                if case in CONTEXT_ONLY:
                    if context is None:
                        failures.append("{0}: registered CONTEXT_ONLY but has no .context.json".format(label))
                        continue
                    if bare:
                        failures.append(
                            "{0}: CONTEXT_ONLY fixture should PASS without context, got {1}".format(label, bare)
                        )
                        continue
                    violations = full
                else:
                    violations = full or bare

                if not violations:
                    failures.append("{0}: expected FAIL but the validator passed".format(label))
                elif not any(needle.lower() in v.lower() for v in violations):
                    failures.append(
                        "{0}: expected a violation containing {1!r}, got {2}".format(label, needle, violations)
                    )
                else:
                    suffix = " [context-only]" if case in CONTEXT_ONLY else ""
                    print("ok    {0}  (FAIL as expected: {1!r}){2}".format(label, needle, suffix))

            else:
                failures.append("{0}: fixture name must start with 'good-' or 'bad-'".format(label))

    # every registered fixture must exist
    for stage, name in EXPECTED_BAD:
        if not (FIXTURES / stage / name).is_file():
            failures.append("{0}/{1}: registered in run_tests.py but the fixture is missing".format(stage, name))

    alias_checks = _check_aliases(failures)
    print("ok    stage aliases  ({0} alias resolutions)".format(alias_checks))
    registry_checks = _check_stage_registries(failures)
    print("ok    stage registries  ({0} stage(s) wired end to end)".format(registry_checks))

    print()
    if failures:
        print("FAILED ({0} problem(s)):".format(len(failures)))
        for f in failures:
            print("  - {0}".format(f))
        return 1

    print("PASSED — {0} fixture(s) validated as expected.".format(checked))
    return 0


if __name__ == "__main__":
    sys.exit(run())
