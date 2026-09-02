#!/usr/bin/env python3
"""Self-tests for harness/validate_stories.py.

Runs the validator over harness/tests/samples/*.md and asserts:
  - good-*.md  -> passes (exit 0), no errors
  - bad-*.md   -> fails (exit 1), and the expected diagnostic substring appears

No dependencies. Run: python3 harness/tests/run_tests.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS))

import validate_stories as v  # noqa: E402

SAMPLES = Path(__file__).resolve().parent / "samples"

# bad sample -> a substring that must appear in one of its error messages
EXPECTED_BAD = {
    "bad-missing-open-questions.md": "Open questions",
    "bad-one-criterion.md": ">= 2 acceptance criteria",
    "bad-no-story-sentence.md": "missing story sentence",
    "bad-placeholder.md": "placeholder",
    "bad-no-personas.md": "Personas",
    "bad-empty.md": "empty",
}


def run() -> int:
    failures: list[str] = []
    checked = 0

    for md in sorted(SAMPLES.glob("*.md")):
        rep = v.validate_text(md.read_text(encoding="utf-8"), md.name)
        checked += 1
        errs = [m for _, m in rep.errors]

        if md.name.startswith("good-"):
            if rep.errors:
                failures.append(f"{md.name}: expected PASS but got errors: {errs}")
            else:
                print(f"ok    {md.name}  (PASS, {rep.story_count} stories)")
        elif md.name.startswith("bad-"):
            if not rep.errors:
                failures.append(f"{md.name}: expected FAIL but validator passed")
                continue
            needle = EXPECTED_BAD.get(md.name)
            if needle is None:
                failures.append(f"{md.name}: no expected-substring registered in run_tests.py")
            elif not any(needle.lower() in e.lower() for e in errs):
                failures.append(
                    f"{md.name}: expected an error containing {needle!r}, got: {errs}"
                )
            else:
                print(f"ok    {md.name}  (FAIL as expected: {needle!r})")
        else:
            failures.append(f"{md.name}: sample name must start with 'good-' or 'bad-'")

    # every registered bad sample must exist
    for name in EXPECTED_BAD:
        if not (SAMPLES / name).is_file():
            failures.append(f"{name}: registered in run_tests.py but sample file is missing")

    print()
    if failures:
        print(f"FAILED ({len(failures)} problem(s)):")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(f"PASSED — {checked} sample(s) validated as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
