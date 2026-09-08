# Stage Contracts, Rules, and Rubrics

Single reference for all four stages: the JSON each emits, the deterministic
Tier-1 rules, and the Tier-2 judge rubric with its threshold.

## Contents

- [Stage 1 — discovery-synthesis](#stage-1--discovery-synthesis)
- [Stage 2 — strategy-definition](#stage-2--strategy-definition)
- [Stage 3 — ideation](#stage-3--ideation)
- [Stage 4 — wireframe](#stage-4--wireframe)
- [Gate semantics](#gate-semantics)
- [Cache keying](#cache-keying)

---

## Stage 1 — discovery-synthesis

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
- Each quote's `text` appears verbatim in the source corpus.
- `1 ≤ frequency ≤ source_count`.
- `severity` ∈ {high, medium, low}.

**Tier 2 — threshold 0.75**

| Key | Weight | Criterion |
|---|---|---|
| `evidence_grounding` | 0.40 | Every theme supported by real quotes; no invented insights |
| `theme_distinctness` | 0.25 | Themes distinct, not overlapping or redundant |
| `signal_coverage` | 0.35 | Major signals captured; nothing high-frequency ignored |

---

## Stage 2 — strategy-definition

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
- Every `grounded_in` entry matches a theme name from Stage 1.

**Tier 2 — threshold 0.75**

| Key | Weight | Criterion |
|---|---|---|
| `persona_grounding` | 0.30 | Personas trace back to themes; no fabricated traits |
| `hmw_quality` | 0.35 | HMWs open, non-solutioning, correctly formed |
| `journey_realism` | 0.35 | Stages reflect actual described behavior and emotion |

---

## Stage 3 — ideation

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

- 6–12 features; every `hmw` matches an HMW from Stage 2.
- `impact` ∈ {0.25, 0.5, 1, 2, 3}; `confidence` ∈ {0.5, 0.8, 1.0};
  `effort` ≥ 0.5; `reach` ≥ 1.
- RICE recompute: `round(reach * impact * confidence / max(effort, 0.5), 1)`
  must be within 0.5 of the stated `rice_score`.
- 2–3 directions, each with a non-empty `tradeoff`.

**Tier 2 — threshold 0.70**

| Key | Weight | Criterion |
|---|---|---|
| `hmw_linkage` | 0.30 | Every feature maps to a specific HMW |
| `rice_integrity` | 0.30 | Scores internally consistent; inputs not inflated |
| `direction_distinctness` | 0.40 | Directions are genuinely different approaches |

---

## Stage 4 — wireframe

Inputs: the `features` and the chosen `design_directions[]` entry from Stage 3,
plus a `target` (`web` | `mobile` | `both`), a `mobile_platform`
(`android` | `ios`, required when the target includes mobile), and the project's
design system when it has one.

Design system: **agnostic**. This stage owns no component library — it reuses
whichever system the project already has and falls back to a documented baseline
only when none is supplied or linkable. The enforced vocabulary — the fixed
base-role taxonomy, the page and component naming patterns, the breakpoints, and
the required state/accessibility keys — is in
`references/page-builder-reference.md`. Material 3 survives as one *optional*
baseline profile in `references/material-design-system.md`; it is no longer an
allowlist.

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
- No raw hex and no `rgb()`/`rgba()` — colour is always a token. `px` **is**
  allowed (breakpoints and the 44×44px touch minimum are px by definition). No
  left-over `--sl-*` / `SL-*` / "brutalist" vocabulary.
- 3–12 pages. Page names match `NN - Title` (web) or `MNN - Title` (mobile);
  numbers unique within a family; families present match `target`.
- Component `name` matches `Page|Section|Component / <Name>`; `base` is in the
  base-role taxonomy; `source` is `reused` | `new`; a `new` component carries a
  `why_new`.
- Every page has a non-empty `purpose`, `primary_user`, `primary_action`,
  `navigation`, `content_structure`, `data`, `interactions`; `states.default`,
  `.loading`, `.empty`, `.error`; all five `accessibility` keys; and
  `requirements.data_dependencies` + `.edge_cases`.
- Web pages carry all four `responsive` breakpoints; mobile pages carry
  `responsive.mobile`. `responsive_matrix` non-empty unless `target` is `mobile`.
- `prototype_flows` non-empty; every `from`/`to` names a specced page; every page
  is reachable from its family's entry (lowest-numbered) page.
- `ux_interpretation` required keys, `user_flow.primary_journey`, and all five
  `validation` keys are populated. `design_tokens_applied` is `true`.
- `design_system_gaps` present (may be `[]`); each `nearest_role` is a base role.
- `primary_action` is not ALL CAPS and is ≤ 4 words.
- Sitemap and page specs describe the same set.
- `figma_file_url` is optional — a URL string once Step 15 rendered the file,
  `null` if that step failed. Exempt from the hex/forbidden-term scan.

**Tier 2 — threshold 0.80**

| Key | Weight | Criterion |
|---|---|---|
| `ds_compliance` | 0.25 | The resolved design system is genuinely reused; every `new` component justified; every value a token; naming convention followed; real gaps flagged |
| `ia_coherence` | 0.20 | Flow, sitemap and pages follow the journey and serve *this* requirement specifically |
| `state_and_responsive_coverage` | 0.20 | States are real treatments; responsive behaviour recomposes rather than scaling down |
| `accessibility_rigor` | 0.15 | WCAG AA decisions concrete and page-specific; nothing relies on colour alone |
| `requirements_completeness` | 0.20 | Buildable per page, and the prototype completes the primary journey |

---

## Gate semantics

```
run stage
  ├─ TIER 1 structural  ─FAIL→ retry with the concrete error list  (max 2)
  ├─ TIER 2 judge score ─FAIL→ retry with weak-criteria feedback   (max 2)
  └─ PASS ─► HITL ─revise→ retry with human feedback (counter resets)
                  └approve→ persist artifact, next stage
```

Weighted score: `Σ (criterion_score × weight)`, each criterion scored 0.0–1.0.
Compare against the stage threshold.

Retries exhausted (attempt > 2) escalates the artifact to the human anyway,
labelled with what the gate objected to. A stuck stage usually means the input
is wrong, and a human reading the failure is faster than a fourth attempt.

**Status vocabulary** for `run.json`: `PENDING`, `RUNNING`, `AWAITING_APPROVAL`,
`APPROVED`, `ESCALATED`.

---

## Cache keying

```
key = sha256(f"{run_id}:{stage}:{attempt}:{input_hash}")[:16]
input_hash = sha256("||".join([raw_inputs, prior_context, revision_feedback,
                               selected_direction, target, mobile_platform,
                               design_system_input]))[:12]
```

Content-addressing is what makes the cache safe rather than merely fast. When
nothing that shapes the output has changed, the cached artifact comes back —
identical to what the human approved. When feedback, the selected direction, the
target surface, the mobile platform, or the supplied design system changes, the
hash changes, the cache misses, and a real regeneration happens. `target`,
`mobile_platform`, and `design_system_input` matter only for the wireframe
stage.

Invalidate a stage explicitly on every revision path — auto-gate failure and
human rejection alike — so a rerun can never hand back the artifact that was
just rejected.
