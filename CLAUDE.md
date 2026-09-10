# AI POC

Two workflows share this repo:

1. **UserStoryGenerator** (`.claude/skills/user-story-generator/`) — raw project inputs in
   any format → a validated user-story backlog. Entry point: `/generate-user-stories`.
2. **ux-pipeline/** — a six-stage research-to-design-to-evaluation pipeline. See
   [ux-pipeline/CLAUDE.md](ux-pipeline/CLAUDE.md); its rulebook is [rules/](rules/).

Both write everything a project produces into one folder, `output/<project-slug>/`.

## Commands

| Command | What it runs |
|---|---|
| `make test` | `harness/tests/run_tests.py` — validator self-tests |
| `make ux-test` | rubric check + `ux-pipeline/tests/` fixtures + `output/` conformance |
| `make lint` | `harness/lint_skill.py` — skill + eval-suite structure |
| `make validate FILE=<f>` | `validate_stories.py --strict` on one backlog |
| `make run` | `harness/run.py` — skill end to end on `harness/fixtures/*` (needs `claude` CLI) |
| `make eval` | `claude plugin eval` — LLM graders (early access + API key) |

`make help` lists them. See [harness/README.md](harness/README.md) for what each layer proves.

CI ([.github/workflows/harness.yml](.github/workflows/harness.yml)) runs the self-tests,
the validator, the lint, and the ux-pipeline checks on every push and PR. It does **not**
run `make run`. The eval job runs only on `main` pushes, is gated on `ANTHROPIC_API_KEY`,
and never blocks the build.

## Writing backlogs

- One file per run: `output/<project-slug>/user-stories-<date>.md`, `<project-slug>` being
  a kebab-case name derived from the material. Ask if the material names no clear project.
- **Always** finish by running `python3 harness/validate_stories.py --strict <file>` and
  fixing every error. The skill's process includes this step; don't skip it.
- Keep the story voice user-centric — describe outcomes, not implementation.
- When inputs are ambiguous or incomplete, list open questions rather than inventing detail.

## `output/` is gitignored except backlogs

The allowlist tracks only `output/*/user-stories-*`. Everything else in a project
folder — the six pipeline stage artifacts and `RUN-SUMMARY.md` — is regenerated per run
and never committed, so any new pipeline stage is ignored automatically without touching
[.gitignore](.gitignore). Project directories are un-ignored first, because git cannot
re-include a file inside an excluded directory.
