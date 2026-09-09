# Harness for the UserStoryGenerator skill

Three independent layers that check the skill at
[`.claude/skills/user-story-generator/`](../.claude/skills/user-story-generator/SKILL.md)
keeps its promises: every story in the required sentence form, ≥ 2 acceptance criteria,
personas and epics and open questions present, no invented scope.

| Layer | Command | Needs | Speed | What it proves |
|-------|---------|-------|-------|----------------|
| **1. Validator** | `python3 harness/validate_stories.py <file>` | Python 3 only | instant | A given backlog file is well-formed. |
| **2. Local runner** | `python3 harness/run.py` | `claude` CLI | minutes | The skill, run end to end on real fixtures, produces valid output. |
| **3. Eval suite** | `claude plugin eval ./.claude/skills/user-story-generator` | early access + API key | minutes, ×3 runs | Regression + quality scoring with LLM graders. |

`make help` lists the shortcuts (`make test`, `make lint`, `make validate FILE=…`,
`make run`, `make eval`).

## 1. Deterministic validator — `validate_stories.py`

Lints one or more Markdown files against the skill's output rules. No LLM, no deps.

```bash
python3 harness/validate_stories.py output/delivery/user-stories-2026-09-02.md
python3 harness/validate_stories.py --strict --json "output/delivery/*.md"
```

- **errors** (exit 1): missing title/sources line, missing Personas/Epic/Open-questions
  section, a story with no story sentence or < 2 acceptance criteria, leftover `<...>`
  template placeholders.
- **warnings** (exit 1 only with `--strict`): generic "user" role, non-sequential US
  numbers, implementation keywords in a story sentence, a criterion that is neither
  Given/When/Then nor a `- [ ]` checkbox.

The skill runs this on itself as its final step (see `SKILL.md` → Process → Validate).

### Self-tests

```bash
python3 harness/tests/run_tests.py
```

Runs the validator over `tests/samples/good-*.md` (must pass) and `tests/samples/bad-*.md`
(must fail with a specific diagnostic). Add a sample + register its expected substring in
`tests/run_tests.py` whenever you add a rule.

## 2. Local runner — `run.py`

For each directory in `fixtures/`, assembles a throwaway project (skill + that fixture's
files as `inputs/`), runs `claude -p` headless, then validates the generated file.

```bash
python3 harness/run.py                      # all fixtures
python3 harness/run.py --fixture happy-path  # one
python3 harness/run.py --model claude-sonnet-5 --keep
```

Writes `harness/results/<timestamp>.json` and copies each generated backlog to
`harness/results/latest-<fixture>.md` for inspection. Exit 0 only if every fixture passes
the strict validator.

### Fixtures

| Fixture | Inputs | Exercises |
|---------|--------|-----------|
| `happy-path` | meeting notes + PRD excerpt | normal decomposition, scope boundaries |
| `multi-format` | email + CSV + Slack export | reads every source, lists all of them |
| `ambiguous-input` | one vague founder DM | restraint — no invented backlog, heavy Open questions |
| `bundled-need` | one sentence, 5 capabilities | splitting a bundled requirement |

## 3. `claude plugin eval` suite — `../.claude/skills/user-story-generator/evals/`

Best-practice eval format. **`claude plugin eval` is early-access**; where it is not
enabled it prints a notice and exits without running — that is expected, the other two
layers still cover you.

```bash
claude plugin eval ./.claude/skills/user-story-generator \
  --eval-dir .claude/skills/user-story-generator/evals

claude plugin eval ./.claude/skills/user-story-generator --case bundled-need --verbose
```

Each `evals/<case>/` has a `prompt.md` (inputs inlined) and `graders/`:

- `file_exists` — the skill wrote a Markdown backlog.
- `regex` — story sentence form; required sections; sources line; story count.
- `llm` — scored against [`references/rubric.md`](../.claude/skills/user-story-generator/references/rubric.md):
  faithful to inputs, one action per story, real benefits, no invented scope.

The `llm` graders and the human review checklist share that one rubric file — update it in
one place.

## CI

[`.github/workflows/harness.yml`](../.github/workflows/harness.yml):

- **validate** + **lint** run on every push/PR (Python only, always).
- **eval** runs only on `main` and only if the `ANTHROPIC_API_KEY` secret is set;
  `continue-on-error: true` while the feature is early-access.
