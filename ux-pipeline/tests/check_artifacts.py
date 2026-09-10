#!/usr/bin/env python3
"""Validate the committed run artifacts in output/ against the current contract.

The committed artifacts are the pipeline's regression corpus: a stage whose rules
tighten should be shown to still admit real work, and an artifact that drifts off
its schema should fail loudly. This is the check that catches a
`output/<slug>/wireframe.json` quietly reverting to a pre-page-builder shape.

Version handling follows `rules/CONTRACTS.md` § Contract versioning:

  - Artifacts stamped at the current CONTRACT_VERSION are validated strictly and
    any violation fails the build.
  - Artifacts stamped older, or unstamped, are reported as LEGACY and skipped.
    They record a run that happened under a contract that no longer exists;
    hand-writing today's fields into one would mean inventing the data this
    pipeline exists to not invent. Re-run the stage to bring it current.

Each project folder is validated as a whole, so cross-stage traceability
(persona -> theme, feature -> HMW, story -> page) is actually exercised rather
than skipped for want of context.

No dependencies. Run: python3 ux-pipeline/tests/check_artifacts.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

PIPELINE = Path(__file__).resolve().parents[1]
ROOT = PIPELINE.parent
sys.path.insert(0, str(PIPELINE))

from validators import CONTRACT_VERSION, artifact_version, run_tier1  # noqa: E402

# output/ filename -> (stage, context keys this stage needs from its siblings)
# The filenames are the "output filenames" vocabulary in ux-pipeline/CLAUDE.md —
# a mix of skill names and node names. Getting it wrong resolves to nothing.
STAGES = [
    ("discovery-synthesis.json", "discovery-synthesis", {}),
    ("strategy.json", "strategy-definition", {"synthesized_insights": "discovery-synthesis.json"}),
    ("ideation.json", "ideation-concepting", {"problem_statement": "strategy.json"}),
    ("wireframe.json", "wireframe-ia", {}),  # self-contained; no upstream needed
    ("delivery.json", "delivery-handoff",
     {"persona_profile": "strategy.json", "wireframe_specs": "wireframe.json"}),
    ("evaluation.json", "evaluation-planning",
     {"persona_profile": "strategy.json", "journey_map": "strategy.json",
      "feature_matrix": "ideation.json", "wireframe_specs": "wireframe.json",
      "developer_handoff_stories": "delivery.json"}),
]


def _load(path: Path) -> Optional[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL  {0}: unreadable ({1})".format(path, exc))
        return None
    return data if isinstance(data, dict) else None


def run() -> int:
    out = ROOT / "output"
    if not out.is_dir():
        print("no output/ directory — nothing to check")
        return 0

    failures: List[str] = []
    checked = 0
    legacy = 0

    for project in sorted(p for p in out.iterdir() if p.is_dir()):
        artifacts: Dict[str, dict] = {}
        for filename, _stage, _needs in STAGES:
            data = _load(project / filename) if (project / filename).is_file() else None
            if data is not None:
                artifacts[filename] = data

        if not artifacts:
            continue
        print("\n{0}/".format(project.name))

        for filename, stage, needs in STAGES:
            artifact = artifacts.get(filename)
            if artifact is None:
                continue

            version = artifact_version(artifact)
            if version != CONTRACT_VERSION:
                legacy += 1
                print("  legacy  {0:<26} (contract {1}; current is {2})".format(
                    filename, version or "unstamped", CONTRACT_VERSION))
                continue

            context = {
                key: artifacts[src] for key, src in needs.items() if src in artifacts
            }
            checked += 1
            violations = run_tier1(stage, artifact, context or None)
            if violations:
                print("  FAIL    {0}  ({1} violation(s))".format(filename, len(violations)))
                for v in violations[:10]:
                    print("            - {0}".format(v))
                if len(violations) > 10:
                    print("            … and {0} more".format(len(violations) - 10))
                failures.append("{0}/{1}".format(project.name, filename))
            else:
                print("  ok      {0}".format(filename))

    print()
    if failures:
        print("FAILED — {0} artifact(s) violate the current contract:".format(len(failures)))
        for f in failures:
            print("  - {0}".format(f))
        return 1

    print("PASSED — {0} artifact(s) conform to contract {1}; {2} legacy artifact(s) skipped.".format(
        checked, CONTRACT_VERSION, legacy))
    return 0


if __name__ == "__main__":
    sys.exit(run())
