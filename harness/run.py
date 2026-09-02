#!/usr/bin/env python3
"""Local runner for the UserStoryGenerator skill.

For each fixture under harness/fixtures/, this:
  1. runs the `claude` CLI headless with the skill available, pointing it at the fixture,
  2. captures the generated Markdown,
  3. runs harness/validate_stories.py --strict on it,
  4. records the result and writes harness/results/<timestamp>.json.

This is the "works today" path — it does not need `claude plugin eval` early access.
It DOES need the `claude` CLI on PATH and a working auth/session.

Usage:
    python3 harness/run.py                     # all fixtures
    python3 harness/run.py --fixture happy-path
    python3 harness/run.py --model claude-sonnet-5 --timeout 300
    python3 harness/run.py --keep                # keep the per-run work dirs
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "harness" / "fixtures"
RESULTS = REPO / "harness" / "results"
VALIDATOR = REPO / "harness" / "validate_stories.py"
SKILL_SRC = REPO / ".claude" / "skills" / "user-story-generator"

PROMPT = """\
Use the user-story-generator skill.

Read every file in the `inputs/` directory of this project and convert the material into
a structured user-story backlog. Follow the skill's output template exactly. Write the
result to `output/{name}.md`. Then run the skill's validate step and fix any errors.
"""


def have_claude() -> bool:
    return shutil.which("claude") is not None


def run_fixture(name: str, model: str | None, timeout: int, keep: bool) -> dict:
    fixture_dir = FIXTURES / name
    inputs = sorted(p.name for p in fixture_dir.iterdir() if p.is_file())
    work = Path(tempfile.mkdtemp(prefix=f"usg-{name}-"))
    result: dict = {"fixture": name, "inputs": inputs, "workdir": str(work)}
    try:
        # Assemble an isolated project: the skill + this fixture's inputs.
        shutil.copytree(SKILL_SRC, work / ".claude" / "skills" / "user-story-generator")
        shutil.copytree(REPO / "harness", work / "harness",
                        ignore=shutil.ignore_patterns("results", "fixtures", "__pycache__"))
        (work / "inputs").mkdir()
        for f in fixture_dir.iterdir():
            if f.is_file():
                shutil.copy(f, work / "inputs" / f.name)
        (work / "output").mkdir()

        cmd = [
            "claude", "-p", PROMPT.format(name=name),
            "--permission-mode", "acceptEdits",
            "--allowedTools", "Read,Write,Edit,Bash,Glob,Grep",
        ]
        if model:
            cmd += ["--model", model]

        proc = subprocess.run(
            cmd, cwd=work, capture_output=True, text=True, timeout=timeout
        )
        result["claude_exit"] = proc.returncode
        if proc.returncode != 0:
            result["error"] = (proc.stderr or proc.stdout or "").strip()[-2000:]

        produced = sorted((work / "output").glob("*.md"))
        result["output_files"] = [p.name for p in produced]
        if not produced:
            result["status"] = "no-output"
            return result

        target = produced[0]
        vproc = subprocess.run(
            [sys.executable, str(VALIDATOR), "--strict", "--json", str(target)],
            capture_output=True, text=True,
        )
        try:
            vreport = json.loads(vproc.stdout)
        except json.JSONDecodeError:
            vreport = {"raw": vproc.stdout}
        result["validator_exit"] = vproc.returncode
        result["validator"] = vreport
        result["status"] = "pass" if vproc.returncode == 0 else "fail"

        # keep a copy of the generated file next to the results
        RESULTS.mkdir(exist_ok=True)
        shutil.copy(target, RESULTS / f"latest-{name}.md")
        return result
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        return result
    finally:
        if keep:
            result["workdir_kept"] = str(work)
        else:
            shutil.rmtree(work, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fixture", action="append", help="fixture name (repeatable); default: all")
    ap.add_argument("--model", default=None, help="model id passed to `claude --model`")
    ap.add_argument("--timeout", type=int, default=420, help="per-fixture timeout, seconds")
    ap.add_argument("--keep", action="store_true", help="keep per-run work directories")
    args = ap.parse_args(argv)

    if not have_claude():
        print("error: `claude` CLI not found on PATH.", file=sys.stderr)
        print("Install Claude Code, or use `claude plugin eval` — see harness/README.md.", file=sys.stderr)
        return 2

    names = args.fixture or sorted(p.name for p in FIXTURES.iterdir() if p.is_dir())
    missing = [n for n in names if not (FIXTURES / n).is_dir()]
    if missing:
        print(f"error: no such fixture(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    runs = [run_fixture(n, args.model, args.timeout, args.keep) for n in names]

    RESULTS.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    out = RESULTS / f"{stamp}.json"
    passed = sum(1 for r in runs if r.get("status") == "pass")
    summary = {"timestamp": stamp, "total": len(runs), "passed": passed, "runs": runs}
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n{'FIXTURE':<20} {'STATUS':<10} DETAIL")
    print("-" * 60)
    for r in runs:
        detail = ""
        if r.get("status") == "fail":
            errs = r.get("validator", {}).get("reports", [{}])[0].get("errors", [])
            detail = f"{len(errs)} validator error(s)"
        elif r.get("status") in {"no-output", "timeout"}:
            detail = r.get("error", "")[:40]
        print(f"{r['fixture']:<20} {r.get('status',''):<10} {detail}")
    print("-" * 60)
    print(f"{passed}/{len(runs)} passed   ->  {out.relative_to(REPO)}")

    return 0 if passed == len(runs) else 1


if __name__ == "__main__":
    sys.exit(main())
