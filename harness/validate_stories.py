#!/usr/bin/env python3
"""Deterministic validator for UserStoryGenerator output.

Checks a generated user-stories Markdown file against the rules the
`user-story-generator` skill promises to follow:

  - a "# User Stories — ..." title and a "_Generated: ... Sources: ..._" line
  - a "## Personas" section with at least one persona bullet
  - at least one "## Epic:" heading
  - every "### US-<n>:" story has the required story sentence
    ("As a ... I want to ... so that I can ...") and >= 2 acceptance criteria
  - an "## Open questions" section
  - no un-filled template placeholders

Errors fail the check (exit 1). Softer issues are warnings and only fail with
--strict. Pure standard library, no dependencies.

Usage:
    python3 harness/validate_stories.py output/flight-booking/user-stories-2026-09-02.md
    python3 harness/validate_stories.py --strict --json output/*/user-stories-*.md
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

STORY_SENTENCE_RE = re.compile(
    r"\*\*as an?\*\*\s+.+?,\s*\*\*i want to\*\*\s+.+?\s+\*\*so that i can\*\*\s+.+?[.]",
    re.IGNORECASE,
)
STORY_HEADING_RE = re.compile(r"^#{3}\s+US-(\d+)\s*:\s*(.+?)\s*$")
EPIC_HEADING_RE = re.compile(r"^#{2}\s+Epic:\s*\S")
PERSONA_BULLET_RE = re.compile(r"^\s*[-*]\s+\*\*.+?\*\*\s*[—:-]\s*\S")
GENERATED_LINE_RE = re.compile(r"_generated:.*sources:.*_", re.IGNORECASE)
GWT_RE = re.compile(r"^\s*[-*]\s+given\b.*\bthen\b", re.IGNORECASE)
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+\S")
BULLET_RE = re.compile(r"^\s*[-*]\s+\S")

PLACEHOLDER_RE = re.compile(
    r"<[^>\n]{1,40}>"
    r"|\[user-type\]|\[action\]|\[benefit/gain\]|\[user\s*type\]"
    r"|<user-type>|<action>|<benefit/gain>|<epic name>|<short title>|<date>",
    re.IGNORECASE,
)

IMPL_KEYWORDS = [
    "api", "endpoint", "database", "sql", "backend", "frontend", "react",
    "kafka", "webhook", "microservice", "schema", "kubernetes", "redis",
    "graphql", "rest call", "lambda function",
]
IMPL_KEYWORD_RE = re.compile(
    r"(?<![a-z])(" + "|".join(re.escape(k) for k in IMPL_KEYWORDS) + r")(?![a-z])",
    re.IGNORECASE,
)


@dataclass
class Report:
    path: str
    errors: list[tuple[int, str]] = field(default_factory=list)
    warnings: list[tuple[int, str]] = field(default_factory=list)
    story_count: int = 0

    def error(self, line: int, msg: str) -> None:
        self.errors.append((line, msg))

    def warn(self, line: int, msg: str) -> None:
        self.warnings.append((line, msg))

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "ok": self.ok,
            "story_count": self.story_count,
            "errors": [{"line": ln, "message": m} for ln, m in self.errors],
            "warnings": [{"line": ln, "message": m} for ln, m in self.warnings],
        }


def _story_blocks(lines: list[str]) -> list[tuple[int, str, list[str]]]:
    """Return (start_line, us_number_str, block_lines) for each US-<n> heading."""
    blocks: list[tuple[int, str, list[str]]] = []
    current: tuple[int, str, list[str]] | None = None
    for idx, raw in enumerate(lines, start=1):
        m = STORY_HEADING_RE.match(raw)
        if m:
            if current:
                blocks.append(current)
            current = (idx, m.group(1), [])
        elif current is not None:
            if re.match(r"^#{1,3}\s", raw) and not raw.startswith("#### "):
                blocks.append(current)
                current = None
            else:
                current[2].append(raw)
    if current:
        blocks.append(current)
    return blocks


def validate_text(text: str, path: str) -> Report:
    rep = Report(path=path)
    lines = text.splitlines()
    if not text.strip():
        rep.error(0, "file is empty")
        return rep

    # Title
    title_line = next((i for i, l in enumerate(lines, 1) if l.startswith("# ")), None)
    if title_line is None:
        rep.error(0, "missing top-level '# ...' title")
    elif not re.match(r"^#\s+User Stories\b", lines[title_line - 1]):
        rep.warn(title_line, "title should start with '# User Stories'")

    # Generated / sources line
    if not any(GENERATED_LINE_RE.search(l) for l in lines):
        rep.error(0, "missing '_Generated: ... · Sources: ..._' line")

    # Personas
    persona_hdr = next(
        (i for i, l in enumerate(lines, 1) if re.match(r"^#{2}\s+Personas\b", l, re.I)),
        None,
    )
    if persona_hdr is None:
        rep.error(0, "missing '## Personas' section")
    else:
        section = _section_lines(lines, persona_hdr)
        if not any(PERSONA_BULLET_RE.match(l) for l in section):
            rep.error(persona_hdr, "'## Personas' has no '- **Name** — description' bullet")

    # Epics
    if not any(EPIC_HEADING_RE.match(l) for l in lines):
        rep.error(0, "no '## Epic: ...' heading found")

    # Open questions
    if not any(re.match(r"^#{2}\s+Open questions\b", l, re.I) for l in lines):
        rep.error(0, "missing '## Open questions' section")

    # Placeholders
    for i, l in enumerate(lines, 1):
        m = PLACEHOLDER_RE.search(l)
        if m:
            rep.error(i, f"un-filled template placeholder: {m.group(0)!r}")

    # Stories
    blocks = _story_blocks(lines)
    rep.story_count = len(blocks)
    if not blocks:
        rep.error(0, "no '### US-<n>: ...' stories found")

    seen_numbers: list[int] = []
    for start, num_str, block in blocks:
        seen_numbers.append(int(num_str))
        body = "\n".join(block)

        sentence_match = STORY_SENTENCE_RE.search(body)
        if not sentence_match:
            rep.error(
                start,
                f"US-{num_str}: missing story sentence "
                "'**As a** ..., **I want to** ... **so that I can** ...'",
            )
        else:
            snippet = sentence_match.group(0)
            if re.search(r"\*\*as an?\*\*\s+users?\b", snippet, re.IGNORECASE):
                rep.warn(start, f"US-{num_str}: story uses generic 'user' as the role")
            impl = IMPL_KEYWORD_RE.search(snippet)
            if impl:
                rep.warn(
                    start,
                    f"US-{num_str}: story sentence names an implementation detail "
                    f"({impl.group(0)!r})",
                )

        crit_idx = next(
            (k for k, l in enumerate(block) if re.match(r"^\s*\*\*acceptance criteria\*\*", l, re.I)),
            None,
        )
        if crit_idx is None:
            rep.error(start, f"US-{num_str}: missing '**Acceptance criteria**' block")
            continue
        crit_bullets = []
        for l in block[crit_idx + 1:]:
            if BULLET_RE.match(l):
                crit_bullets.append(l)
            elif l.strip() and not l.startswith(" "):
                break
        if len(crit_bullets) < 2:
            rep.error(
                start,
                f"US-{num_str}: needs >= 2 acceptance criteria, found {len(crit_bullets)}",
            )
        for cb in crit_bullets:
            if not (GWT_RE.match(cb) or CHECKBOX_RE.match(cb)):
                rep.warn(
                    start,
                    f"US-{num_str}: criterion is neither Given/When/Then nor a checkbox: "
                    f"{cb.strip()[:60]!r}",
                )

    if seen_numbers and seen_numbers != list(range(seen_numbers[0], seen_numbers[0] + len(seen_numbers))):
        rep.warn(0, f"US numbers are not sequential: {seen_numbers}")

    return rep


def _section_lines(lines: list[str], header_line: int) -> list[str]:
    out: list[str] = []
    for l in lines[header_line:]:
        if re.match(r"^#{1,2}\s", l):
            break
        out.append(l)
    return out


def _print_report(rep: Report) -> None:
    status = "PASS" if rep.ok else "FAIL"
    print(f"[{status}] {rep.path}  ({rep.story_count} stories)")
    for ln, msg in rep.errors:
        loc = f"{rep.path}:{ln}" if ln else rep.path
        print(f"  error  {loc}  {msg}")
    for ln, msg in rep.warnings:
        loc = f"{rep.path}:{ln}" if ln else rep.path
        print(f"  warn   {loc}  {msg}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="Markdown files or globs to validate")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--json", action="store_true", help="emit a JSON report on stdout")
    args = ap.parse_args(argv)

    expanded: list[str] = []
    for p in args.paths:
        hits = sorted(glob.glob(p))
        expanded.extend(hits if hits else [p])

    reports: list[Report] = []
    for path in expanded:
        fp = Path(path)
        if not fp.is_file():
            rep = Report(path=path)
            rep.error(0, "file not found")
            reports.append(rep)
            continue
        reports.append(validate_text(fp.read_text(encoding="utf-8"), path))

    failed = False
    for rep in reports:
        if not rep.ok or (args.strict and rep.warnings):
            failed = True

    if args.json:
        print(json.dumps({"failed": failed, "reports": [r.to_dict() for r in reports]}, indent=2))
    else:
        for rep in reports:
            _print_report(rep)
        print()
        print("RESULT:", "FAIL" if failed else "PASS")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
