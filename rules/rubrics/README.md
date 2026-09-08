# rules/rubrics/

The **Tier-2** scoring rubrics for the Superlap UX pipeline — one file per stage. A stage
artifact reaches a human only after Tier-1 (`ux-pipeline/validators/<stage>.py`) passes
**and** the Tier-2 judge scores it acceptable against the stage's rubric here.

These files are the single source for the scoring criteria, their weights, the anchor
descriptions, and the pass rule. `rules/CONTRACTS.md` no longer carries them — it links
here. `ux-pipeline/rubrics.py` loads them; `ux-pipeline/orchestrator.py` `judge()` scores
against them.

## The scoring contract (every stage inherits this)

**Scale.** Score each dimension **1–5**, where 5 = fully met, 1 = absent or wrong. This is
the same scale as `.claude/skills/user-story-generator/references/rubric.md`. Use the
whole range — a 3 is a real, common score for work that is present but soft.

**Stance.** Judge the artifact against its *source material* — the raw research, or the
upstream approved artifacts — as if someone else wrote it and you were asked to find the
weakest claim in it. Scoring your own generation has an obvious bias; counter it
deliberately. An inflated score defeats the gate, and the human downstream is relying on it
having been honest.

**Evidence.** Every dimension score must cite evidence: a verbatim quote from the source, a
specific artifact field, or a named absence ("no theme covers the pricing complaint raised
by P03, P07, P11").

**Default pass rule.** Acceptable when **every dimension ≥ 4**, OR **every dimension ≥ 3
and the weighted mean ≥ 4.0**. A stage may tighten or loosen this — its own `pass_when`
(in the ```json block of its rubric file) is authoritative. The per-stage rules preserve
the ordering the pipeline was designed with (wireframe strictest, ideation most lenient).

**Weighted mean.** `Σ(dimension_score × weight)`, weights summing to 1.0.

**Required judge output.**

```json
{
  "<dimension_key>": {
    "score": 4,
    "rationale": "one or two sentences",
    "evidence": "quote or field reference"
  },
  "...": {},
  "weighted_mean": 4.15,
  "pass": true
}
```

On a fail, the weak dimensions and their rationales become the `revision_feedback` for the
stage's next attempt. The gate allows 2 such retries, then escalates to the human anyway
(see `rules/CONTRACTS.md` § Gate semantics).

## Per-stage files

| Stage | File | Tightening / loosening |
|---|---|---|
| 1 — discovery-synthesis | [`discovery-synthesis.md`](discovery-synthesis.md) | default |
| 2 — strategy-definition | [`strategy-definition.md`](strategy-definition.md) | default |
| 3 — ideation-concepting | [`ideation-concepting.md`](ideation-concepting.md) | looser — every dim ≥ 3 and weighted mean ≥ 3.7 |
| 4 — wireframe-ia | [`wireframe-ia.md`](wireframe-ia.md) | stricter — `ds_compliance` must be 5 |
| 5 — delivery-handoff | [`delivery-handoff.md`](delivery-handoff.md) | default |

## Keeping in sync

- The dimension keys and weights live **only** in each file's ```json block. The prose
  table restates them for readers — if you change one, change both, and the verification
  step (`python3 ux-pipeline/rubrics.py <stage>`) asserts the weights sum to 1.0.
- Stages 1–4 mirror the *Quality bar* sections of the vendored
  `.claude/skills/superlap-*/SKILL.md`. Those still carry inline copies; when you change a
  criterion here, update the vendored skill's Quality bar too (and re-upload it — it syncs
  to claude.ai).
