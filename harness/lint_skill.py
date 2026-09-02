#!/usr/bin/env python3
"""Structural lint for the user-story-generator skill and its eval suite.

Checks (no LLM, no dependencies):
  - SKILL.md has YAML frontmatter with a non-empty `description`
  - every referenced references/*.md file exists
  - every evals/<case>/ has a prompt.md with frontmatter and a non-empty graders/ dir
  - every grader .md declares a known `type`

Run: python3 harness/lint_skill.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / ".claude" / "skills" / "user-story-generator"
KNOWN_GRADERS = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}


def frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", text)


def main() -> int:
    problems: list[str] = []

    skill_md = SKILL / "SKILL.md"
    if not skill_md.is_file():
        print(f"FAIL: {skill_md} not found")
        return 1

    fm, body = frontmatter(skill_md.read_text(encoding="utf-8"))
    if not fm:
        problems.append("SKILL.md: missing YAML frontmatter")
    elif not re.search(r"^description:\s*\S", fm, re.MULTILINE) and "description:" not in fm:
        problems.append("SKILL.md: frontmatter has no `description`")
    else:
        desc_block = re.search(r"description:\s*(?:>-?|\|-?)?\s*\n?((?:.|\n)*?)(?:\n\w[\w-]*:|\Z)", fm)
        if desc_block and not desc_block.group(1).strip():
            problems.append("SKILL.md: `description` is empty")

    for ref in re.findall(r"\(references/([A-Za-z0-9_\-./]+\.md)\)", body):
        if not (SKILL / "references" / ref).is_file():
            problems.append(f"SKILL.md references missing file: references/{ref}")

    evals_dir = SKILL / "evals"
    if not evals_dir.is_dir():
        problems.append("evals/ directory not found")
    else:
        cases = [d for d in evals_dir.iterdir() if d.is_dir()]
        if not cases:
            problems.append("evals/ has no cases")
        for case in sorted(cases):
            prompt = case / "prompt.md"
            if not prompt.is_file():
                problems.append(f"evals/{case.name}: missing prompt.md")
            else:
                pfm, _ = frontmatter(prompt.read_text(encoding="utf-8"))
                if not pfm:
                    problems.append(f"evals/{case.name}/prompt.md: missing frontmatter")
                elif "plugins:" not in pfm:
                    problems.append(f"evals/{case.name}/prompt.md: frontmatter has no `plugins:`")
            graders = case / "graders"
            gfiles = sorted(graders.glob("*.md")) if graders.is_dir() else []
            if not gfiles:
                problems.append(f"evals/{case.name}: no graders/*.md")
            for g in gfiles:
                gfm, _ = frontmatter(g.read_text(encoding="utf-8"))
                tm = re.search(r"^type:\s*(\S+)", gfm, re.MULTILINE)
                if not tm:
                    problems.append(f"evals/{case.name}/graders/{g.name}: no `type:`")
                elif tm.group(1) not in KNOWN_GRADERS:
                    problems.append(
                        f"evals/{case.name}/graders/{g.name}: unknown type {tm.group(1)!r}"
                    )

    if problems:
        print(f"FAIL ({len(problems)} problem(s)):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("PASS — skill and eval suite are structurally sound.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
