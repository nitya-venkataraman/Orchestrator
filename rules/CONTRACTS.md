# Stage Contracts, Rules, and Rubrics

The single rulebook for every stage of the Superlap UX pipeline — shared by the
LangGraph `ux-pipeline/` scaffold and the vendored `.claude/skills/superlap-*`
skills (see [`README.md`](README.md)). For each stage: the JSON it emits and the
deterministic **Tier-1** structural rules (`ux-pipeline/validators/<stage>.py`
re-implements these). The **Tier-2** LLM-judge rubric — dimensions, weights,
score anchors, pass rule — lives per stage in [`rubrics/`](rubrics/); each Tier 2
section below links to it.

Stages 1–4 are ported verbatim from
`.claude/skills/superlap-pipeline/references/contracts.md` so both consumers
enforce exactly the same contract. Keep them in sync — the `BASE_ROLES` /
`FORBIDDEN` lists and every check function in
`ux-pipeline/validators/wireframe.py` must stay byte-identical to
`.claude/skills/superlap-wireframe/scripts/validate_ds.py`, and the page-builder
reference (`.claude/skills/superlap-wireframe/references/page-builder-reference.md`)
must match its copy in `.claude/skills/superlap-pipeline/references/`. Material 3
is now only an optional baseline profile
(`references/material-design-system.md`, tokens extracted to
`ux-pipeline/skills/wireframe-ia/references/material-design-tokens.json`).

## Contents

- [Stage 1 — discovery-synthesis](#stage-1--discovery-synthesis)
- [Stage 2 — strategy-definition](#stage-2--strategy-definition)
- [Stage 3 — ideation-concepting](#stage-3--ideation-concepting)
- [Stage 4 — wireframe-ia](#stage-4--wireframe-ia)
- [Stage 5 — delivery-handoff](#stage-5--delivery-handoff)
- [Gate semantics](#gate-semantics)
- [Cache keying](#cache-keying)

---

## Stage 1 — discovery-synthesis

State key: `synthesized_insights` (the artifact) — reads `raw_research_data`.

**Output**

```json
{
  "themes": [{
    "name": "string", "insight": "string", "frequency": 0,
    "quotes": [{"text": "verbatim", "source": "string"}],
    "severity": "high|medium|low"
  }],
  "gaps": ["string"],
  "source_count": 0
}
```

**Tier 1**

- Valid JSON, matches shape above.
- 2–6 themes; each has ≥ 1 quote.
- Each quote's `text` appears verbatim in the source corpus (checked when
  `raw_research_data` is supplied as context).
- `1 ≤ frequency ≤ source_count`.
- `severity` ∈ {high, medium, low}.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/discovery-synthesis.md`](rubrics/discovery-synthesis.md)
(`evidence_grounding`, `theme_distinctness`, `signal_coverage`). Pass rule in that file.

Persisted files: `output/discovery-synthesis-<slug>.{json,md}`.

---

## Stage 2 — strategy-definition

State keys: `persona_profile`, `journey_map`, `problem_statement` — reads
`synthesized_insights`.

**Output**

```json
{
  "personas": [{
    "name": "string", "type": "primary|secondary", "context": "string",
    "goals": ["string"], "frustrations": ["string"],
    "quote": "verbatim", "grounded_in": ["theme name"]
  }],
  "journey": [{
    "stage": "string", "actions": ["string"], "emotion": "string",
    "friction": ["string"], "dropoff_risk": "high|medium|low"
  }],
  "hmw_statements": [{"statement": "How might we ...", "derived_from": "string"}]
}
```

**Tier 1**

- Exactly 2 personas: one `primary`, one `secondary`.
- Every `statement` starts with "how might we" (case-insensitive).
- 4–7 journey stages; 3–5 HMW statements.
- `dropoff_risk` ∈ {high, medium, low}.
- Every `grounded_in` entry matches a theme name from Stage 1 (checked when the
  Stage-1 artifact is supplied as context).

**Tier 2** — scored 1–5 per dimension against
[`rubrics/strategy-definition.md`](rubrics/strategy-definition.md)
(`persona_grounding`, `hmw_quality`, `journey_realism`). Pass rule in that file.

Persisted files: `output/strategy-<slug>.{json,md}`.

---

## Stage 3 — ideation-concepting

State keys: `feature_matrix`, `concept_proposals` — reads `problem_statement`,
`persona_profile`.

**Output**

```json
{
  "features": [{
    "name": "string", "description": "string", "hmw": "string",
    "reach": 0, "impact": 0.25, "confidence": 0.8,
    "effort": 1.0, "rice_score": 0.0
  }],
  "design_directions": [{
    "name": "string", "summary": "string", "differentiator": "string",
    "hmws_addressed": ["string"], "tradeoff": "string"
  }]
}
```

**Tier 1**

- 6–12 features; every `hmw` matches an HMW from Stage 2 (checked when the
  Stage-2 artifact is supplied as context).
- `impact` ∈ {0.25, 0.5, 1, 2, 3}; `confidence` ∈ {0.5, 0.8, 1.0};
  `effort` ≥ 0.5; `reach` ≥ 1.
- RICE recompute: `round(reach * impact * confidence / max(effort, 0.5), 1)`
  must be within 0.5 of the stated `rice_score` (relative tolerance for large
  scores: within 1%).
- 2–3 directions, each with a non-empty `tradeoff`.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/ideation-concepting.md`](rubrics/ideation-concepting.md)
(`hmw_linkage`, `rice_integrity`, `direction_distinctness`). The most lenient pass rule in
the pipeline — divergence is not punished as hard as fabrication. Rule in that file.

Persisted files: `output/ideation-<slug>.{json,md}`.

---

## Stage 4 — wireframe-ia

State keys: `target`, `mobile_platform`, `design_system`, `ux_interpretation`,
`user_flow`, `sitemap`, `wireframe_specs` (the `pages` array),
`responsive_matrix`, `prototype_flows`, `design_system_gaps`, `assumptions`,
`validation`, `design_tokens_applied`, `figma_file_url` — reads `feature_matrix`,
`concept_proposals`, `selected_concept` / `selected_direction`, `target_surface`
(`web` | `mobile` | `both`) and `mobile_platform` (`android` | `ios`, required
when the surface includes mobile), both set at the `select_direction` fork, plus
`design_system_input` when the project has a design system.

Design system: **agnostic**. This stage owns no component library — it reuses
whichever system the project already has, and falls back to a documented
baseline only when none is supplied or linkable. The enforced vocabulary is the
fixed **base-role taxonomy**, the page and component naming patterns, the
breakpoints, and the required state/accessibility keys, all in
`.claude/skills/superlap-wireframe/references/page-builder-reference.md`
(mirrored under `.claude/skills/superlap-pipeline/references/`, narrated in
`ux-pipeline/skills/wireframe-ia/assets/component-patterns.md`). Material 3
survives as one *optional* baseline profile in `material-design-system.md` with
its tokens extracted to
`ux-pipeline/skills/wireframe-ia/references/material-design-tokens.json` — it is
no longer an allowlist.

**Output**

```json
{
  "target": "web | mobile | both",
  "mobile_platform": "android | ios | null",
  "design_system": {
    "name": "string", "source": "existing | baseline",
    "tokens": {"color": ["string"], "typography": ["string"], "spacing": ["string"]}
  },
  "ux_interpretation": {
    "primary_user": "string", "user_goal": "string", "business_goal": "string",
    "main_task": "string", "context": "string", "entry_point": "string",
    "expected_outcome": "string", "required_data": ["string"],
    "business_rules": ["string"], "constraints": ["string"], "dependencies": ["string"]
  },
  "user_flow": {"primary_journey": ["string"], "supporting_tasks": ["string"],
                "error_scenarios": ["string"]},
  "sitemap": [{"page": "01 - Login", "path": "/route", "children": ["string"]}],
  "pages": [{
    "page_name": "02 - Dashboard", "purpose": "string", "primary_user": "string",
    "primary_action": "string", "secondary_actions": ["string"],
    "content_structure": ["string"], "navigation": "string",
    "components": [{"name": "Component / KPI Card", "base": "Card",
                    "source": "reused | new", "variants": ["string"],
                    "why_new": "string — required when source is 'new'"}],
    "data": ["string"], "interactions": ["string"],
    "states": {"default": "string", "loading": "string", "empty": "string",
               "error": "string", "success": "string", "disabled": "string"},
    "responsive": {"desktop": "string", "laptop": "string",
                   "tablet": "string", "mobile": "string"},
    "accessibility": {"contrast": "string", "keyboard_focus": "string",
                      "labels": "string", "touch_targets": "string",
                      "reading_order": "string"},
    "requirements": {"data_dependencies": ["string"], "permissions": ["string"],
                     "edge_cases": ["string"], "open_questions": ["string"]}
  }],
  "responsive_matrix": [{"component": "string", "desktop": "string",
                         "tablet": "string", "mobile": "string"}],
  "prototype_flows": [{"from": "01 - Login", "trigger": "string",
                       "to": "02 - Dashboard", "interaction": "string"}],
  "design_system_gaps": [{"need": "string", "nearest_role": "string",
                          "why_insufficient": "string"}],
  "assumptions": ["string"],
  "validation": {"ux": ["string"], "ui": ["string"], "responsive": ["string"],
                 "accessibility": ["string"], "prototype": ["string"]},
  "design_tokens_applied": true,
  "figma_file_url": "string | null"
}
```

**Tier 1**

- `target` is `web` | `mobile` | `both`. `mobile_platform` is `android` | `ios`,
  required when `target` is `mobile` or `both`, forbidden when it is `web`.
- `design_system` names a system and declares `source` (`existing` | `baseline`);
  a `baseline` source requires a non-empty `assumptions`. `tokens.color`,
  `.typography`, `.spacing` are each non-empty.
- No raw hex and no `rgb()`/`rgba()` anywhere — colour is always a token. `px`
  **is** allowed: the breakpoints (1440 / 1280 / 768 / 375) and the 44×44px touch
  minimum are px by definition. No left-over `--sl-*` / `SL-*` / "brutalist"
  vocabulary.
- 3–12 pages. Page names match `NN - Title` (web) or `MNN - Title` (mobile);
  numbers unique within a family; the families present match `target`.
- Component `name` matches `Page|Section|Component / <Name>`; `base` is in the
  base-role taxonomy; `source` is `reused` | `new`; a `new` component carries a
  `why_new`.
- Every page has a non-empty `purpose`, `primary_user`, `primary_action`,
  `navigation`, `content_structure`, `data`, `interactions`; `states.default`,
  `.loading`, `.empty`, `.error`; all five `accessibility` keys; and
  `requirements.data_dependencies` + `.edge_cases`.
- Web pages carry all four `responsive` breakpoints; mobile pages carry
  `responsive.mobile`.
- `responsive_matrix` is non-empty unless `target` is `mobile`, each row covering
  `component` / `desktop` / `tablet` / `mobile`.
- `prototype_flows` is non-empty; every `from`/`to` names a specced page; every
  page is reachable from its family's entry (lowest-numbered) page.
- `ux_interpretation` required keys, `user_flow.primary_journey`, and all five
  `validation` keys are populated. `design_tokens_applied` is `true`.
- `design_system_gaps` is present (may be `[]`); each entry's `nearest_role` is a
  base role.
- `primary_action` is not ALL CAPS and is ≤ 4 words.
- Sitemap and page specs describe the same set.
- `figma_file_url` is optional — a URL string once the Figma render step ran,
  `null` if it failed. Exempt from the hex/forbidden-term scan.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/wireframe-ia.md`](rubrics/wireframe-ia.md)
(`ds_compliance`, `ia_coherence`, `state_and_responsive_coverage`,
`accessibility_rigor`, `requirements_completeness`). The strictest pass rule in
the pipeline — `ds_compliance` must be a 5. Rule in that file.

Persisted files: `output/wireframe-<slug>.{json,md}`. The `.md` follows the final
review format — UX Interpretation, User Flow, Sitemap, Pages Created, Components
Used, Responsive Behaviour, Accessibility, Prototype, Design System Gaps,
Assumptions, Validation — and is the HITL surface.

---

## Stage 5 — delivery-handoff

State keys: `developer_handoff_stories`, `microcopy` — reads `sitemap`,
`wireframe_specs` (and `persona_profile` for the traceability check).

**Output**

```json
{
  "stories": [{
    "id": "US-1",
    "persona": "string — a Stage-2 persona name",
    "capability": "string",
    "benefit": "string",
    "screen": "string — a Stage-4 page_name",
    "acceptance_criteria": [{"given": "string", "when": "string", "then": "string"}]
  }],
  "microcopy": {
    "cta_primary": "Sentence case verb first",
    "empty_states": {"<screen>": "string"},
    "error_states": {"<screen>": "string"},
    "confirmations": {"<screen>": "string"}
  }
}
```

**Tier 1**

- ≥ 1 story; every story has a non-empty `persona`, `capability`, `benefit`, and
  ≥ 1 acceptance criterion, each with non-empty `given` / `when` / `then`.
- Every `persona` matches a persona name from Stage 2 (checked when the Stage-2
  artifact is supplied as context).
- Every `page` in `pages` from Stage 4 is referenced by ≥ 1 story (checked when
  the Stage-4 artifact is supplied as context). Legacy Stage-4 artifacts using
  `screens` / `screen_name` are still accepted.
- Every value under `microcopy.cta_primary` and any nested `cta_*` key is a
  sentence-case label, not ALL CAPS (brand rule).
- `id` values, if present, are unique.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/delivery-handoff.md`](rubrics/delivery-handoff.md)
(`story_completeness`, `traceability`, `voice_consistency`). Pass rule in that file.

Persisted files: `output/delivery-<slug>.{json,md}`. The `.md` — Jira-style
stories with Given/When/Then plus microcopy tables — is the HITL surface.

---

## Gate semantics

```
run stage
  ├─ TIER 1 structural   ─FAIL→ retry with the concrete error list      (max 2)
  ├─ TIER 2 rubric score ─FAIL→ retry with weak-dimension feedback      (max 2)
  └─ PASS ─► HITL ─revise→ retry with human feedback (counter resets)
                  └approve→ persist artifact, next stage
```

Tier 2 scores each rubric dimension 1–5; the weighted mean is
`Σ (dimension_score × weight)`, weights per `rubrics/<stage>.md` summing to 1.0. Whether
that constitutes a pass is the `pass_when` rule in the same file, applied by
`ux-pipeline/rubrics.py` `evaluate()` — the default is "every dimension ≥ 4, or every
dimension ≥ 3 and weighted mean ≥ 4.0", tightened for wireframe and loosened for ideation.

Retries exhausted (`attempt > 2`) escalates the artifact to the human anyway,
labelled with what the gate objected to and `escalated = true`. A stuck stage
usually means the input is wrong, and a human reading the failure is faster than
a fourth attempt.

**Status vocabulary** for `stage_status` / `workspace/run.json`: `PENDING`,
`RUNNING`, `AWAITING_APPROVAL`, `APPROVED`, `ESCALATED`.

A human **revise** resets that stage's attempt counter — a human asking for a
change is not a failed attempt — and invalidates the stage's cache so the rerun
regenerates instead of returning the artifact that was just rejected.

---

## Cache keying

```
key        = sha256(f"{run_id}:{stage}:{attempt}:{input_hash}")[:16]
input_hash = sha256("||".join([raw_inputs, prior_context, revision_feedback,
                               selected_direction, target_surface,
                               mobile_platform, design_system_input]))[:12]
```

Content-addressing is what makes the cache safe rather than merely fast. When
nothing that shapes the output has changed, the cached artifact comes back —
identical to what the human approved. When feedback, the selected direction, the
target surface, the mobile platform, or the supplied design system changes, the
hash changes, the cache misses, and a real regeneration happens.
`target_surface`, `mobile_platform`, and `design_system_input` only shape the
wireframe stage.

Invalidate a stage explicitly on every revision path — auto-gate failure and
human rejection alike — so a rerun can never hand back the artifact that was
just rejected.
