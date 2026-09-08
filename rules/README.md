# rules/

The rulebook for the Superlap UX pipeline, kept here — outside `ux-pipeline/` — because it
is the **single source of truth** shared by two consumers:

- **`ux-pipeline/`** — the LangGraph scaffold. `ux-pipeline/validators/*.py` implement the
  Tier-1 rules; `ux-pipeline/rubrics.py` + `ux-pipeline/orchestrator.py` `judge()` score
  Tier-2 against `rubrics/`; each `ux-pipeline/skills/*/SKILL.md` points here for its
  Output contract.
- **`.claude/skills/superlap-*`** — the vendored conversational skills. Their canonical
  contract is `.claude/skills/superlap-pipeline/references/contracts.md`.

## Files

| Path | What |
|---|---|
| [`CONTRACTS.md`](CONTRACTS.md) | Per stage: the JSON schema and the deterministic Tier-1 rules. Plus gate semantics, status vocabulary, cache keying. Links to the rubric for each stage's Tier-2. |
| [`rubrics/`](rubrics/) | The Tier-2 scoring rubrics — one file per stage plus [`rubrics/README.md`](rubrics/README.md) (the shared 1–5 scoring contract). Dimensions, weights, score anchors, calibration notes, and the machine-readable pass rule. |

## Keeping it in sync

- **Stages 1–4** of `CONTRACTS.md` must stay aligned with
  `.claude/skills/superlap-pipeline/references/contracts.md`. `CONTRACTS.md` is the fuller
  version (it also carries Stage 5 — delivery-handoff — which the vendored pipeline stops
  short of).
- Stage 4 is **design-system agnostic** — it enforces no component allowlist. The
  **base-role taxonomy** and **forbidden styling substrings** in `CONTRACTS.md`
  § Stage 4 must match `BASE_ROLES` / `FORBIDDEN` — and every check function — in
  both `ux-pipeline/validators/wireframe.py` and
  `.claude/skills/superlap-wireframe/scripts/validate_ds.py`, byte for byte.
- Each rubric's **dimension keys and weights** live only in its ```json block;
  `python3 ux-pipeline/rubrics.py --check` asserts every file's weights sum to 1.0.
  The vendored skills' inline *Quality bar* sections still mirror Stages 1–4 — update
  them (and re-upload) when a rubric changes.

Change a rule here first, then propagate to the validators, the rubrics, and the vendored
copies.
