# rules/

The rulebook for the Superlap UX pipeline, kept here — outside `ux-pipeline/` — because it
is the **single source of truth**. Its consumer is `ux-pipeline/`:
`ux-pipeline/validators/*.py` implement the Tier-1 rules; `ux-pipeline/rubrics.py` +
`ux-pipeline/orchestrator.py` `judge()` score Tier-2 against `rubrics/`; each
`ux-pipeline/skills/*/SKILL.md` points here for its Output contract.

## Files

| Path | What |
|---|---|
| [`CONTRACTS.md`](CONTRACTS.md) | Per stage: the JSON schema and the deterministic Tier-1 rules. Plus gate semantics, status vocabulary, cache keying. Links to the rubric for each stage's Tier-2. |
| [`rubrics/`](rubrics/) | The Tier-2 scoring rubrics — one file per stage plus [`rubrics/README.md`](rubrics/README.md) (the shared 1–5 scoring contract). Dimensions, weights, score anchors, calibration notes, and the machine-readable pass rule. |

## Keeping it in sync

- Stage 4 is **design-system agnostic** — it enforces no component allowlist. The
  **base-role taxonomy** and **forbidden styling substrings** in `CONTRACTS.md`
  § Stage 4 are implemented as `BASE_ROLES` / `FORBIDDEN` in
  `ux-pipeline/validators/wireframe.py`; change them here first, then there.
- Each rubric's **dimension keys and weights** live only in its `json` block;
  `python3 ux-pipeline/rubrics.py --check` asserts every file's weights sum to 1.0.
- The **Superlap skills on claude.ai** carry their own copies of these contracts and
  quality bars — they are not in this repo and nothing here can check them. When you
  change a rule or a rubric criterion, re-sync those skills by hand.

Change a rule here first, then propagate to the validators and the rubrics.
