# Stage Contracts, Rules, and Rubrics

**`CONTRACT_VERSION: 2.0`** — every artifact records the contract it was produced
under, as a top-level `contract_version`. Read [§ Contract
versioning](#contract-versioning) before changing a rule in this file.

The single rulebook for every stage of the Superlap UX pipeline, and the source
of truth for the LangGraph `ux-pipeline/` scaffold (see
[`README.md`](README.md)). For each stage: the JSON it emits and the
deterministic **Tier-1** structural rules (`ux-pipeline/validators/<stage>.py`
re-implements these). The **Tier-2** LLM-judge rubric — dimensions, weights,
score anchors, pass rule — lives per stage in [`rubrics/`](rubrics/); each Tier 2
section below links to it.

Change a rule here first; the validators implement this file, they do not
redefine it. Material 3 is only an optional baseline profile, its tokens
extracted to
`ux-pipeline/skills/wireframe-ia/references/material-design-tokens.json`.

## Contents

- [Stage 1 — discovery-synthesis](#stage-1--discovery-synthesis)
- [Stage 2 — strategy-definition](#stage-2--strategy-definition)
- [Stage 3 — ideation-concepting](#stage-3--ideation-concepting)
- [Stage 4 — wireframe-ia](#stage-4--wireframe-ia)
- [Stage 5 — delivery-handoff](#stage-5--delivery-handoff)
- [Stage 6 — evaluation-planning](#stage-6--evaluation-planning)
- [Gate semantics](#gate-semantics)
- [Cache keying](#cache-keying)
- [Contract versioning](#contract-versioning)

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
  "source_count": 0,
  "corpus": {"method": "string", "participant_count": 0,
             "segments": ["string"], "collection_window": "string",
             "known_bias": ["string"]}
}
```

**Tier 1**

- Valid JSON, matches shape above.
- 2–6 themes; each has ≥ 1 quote.
- Each quote's `text` appears verbatim in the source corpus (checked when
  `raw_research_data` is supplied as context).
- `1 ≤ frequency ≤ source_count`.
- `severity` ∈ {high, medium, low}. Derived, not felt: frequency × consequence,
  per the table in
  `ux-pipeline/skills/discovery-synthesis/references/synthesis-method.md`. A
  universal minor irritation is not high; a rare catastrophic case is not low.
- Every quote `source` **starts with a participant identifier** — a word carrying
  a number: `P07`, `Ticket-4412`, `Review-2891`, `Interview 3`. Role and context
  may follow (`P07 — credit risk reviewer, mid-market desk`); a personal name, an
  email address or an employer may not. Research participants were promised
  something, and this artifact is read by many more people than the raw corpus
  ever is. Tier-1 rejects a source that does not open with an identifier, and any
  source containing an email address.
- `corpus` is present, with a non-empty `method` and `participant_count ≥ 1`.
  `source_count` alone cannot tell a designer whether six themes came from six
  power users or sixty strangers, and every downstream stage treats this
  synthesis as the complete picture. `segments`, `collection_window` and
  `known_bias` are lists that may be empty only when genuinely unknown — a
  support-ticket corpus over-represents failure and a sales-call corpus
  over-represents enthusiasm, and saying so is a finding, not a disclaimer.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/discovery-synthesis.md`](rubrics/discovery-synthesis.md)
(`evidence_grounding`, `theme_distinctness`, `signal_coverage`). Pass rule in that file.

Persisted files: `output/<project-slug>/discovery-synthesis.{json,md}`.

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
    "friction": ["string"], "dropoff_risk": "high|medium|low",
    "current_metric": "string — optional, a known figure for this stage"
  }],
  "hmw_statements": [{"statement": "How might we ...", "derived_from": "string"}]
}
```

**Tier 1**

- 2–3 personas: exactly one `primary`, and one or two `secondary`. A third
  persona is a claim that the research supports three distinct people — it
  passes Tier-1 on structure and is judged on `persona_grounding` like any
  other, so an unsupported third scores badly rather than being blocked.
- Every `statement` starts with "how might we" (case-insensitive).
- 4–7 journey stages; 3–5 HMW statements.
- `dropoff_risk` ∈ {high, medium, low}.
- Every `grounded_in` entry matches a theme name from Stage 1 (checked when the
  Stage-1 artifact is supplied as context).
- `current_metric` is optional per stage — record it only where the research or
  the product analytics actually supply a figure, never as an estimate. It is
  where a Stage-3 `success_metric.baseline` is allowed to come from; a baseline
  with no `current_metric` behind it is `"unknown"`, not a guess.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/strategy-definition.md`](rubrics/strategy-definition.md)
(`persona_grounding`, `hmw_quality`, `journey_realism`). Pass rule in that file.

Persisted files: `output/<project-slug>/strategy.{json,md}`.

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
    "effort": 1.0, "rice_score": 0.0,
    "success_metric": {"name": "string", "baseline": "string | \"unknown\"",
                       "target": "string", "source": "string"}
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
- Every feature carries a `success_metric` with a non-empty `name` and `target`.
  A RICE `impact` is a claim that something moves; `success_metric` is the
  statement of *what* moves and *how you would know*. Without it, `impact` is
  unfalsifiable and the pipeline ships work it can never evaluate.
- `baseline` is `"unknown"` unless a real figure exists — a Stage-2 journey
  stage's `current_metric`, or product analytics named in `source`. **Never
  estimate a baseline**; "unknown" is the honest answer and is what the Stage-6
  evaluation plan is for. This is the same never-invent-data rule the rest of
  the pipeline runs on, applied to numbers.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/ideation-concepting.md`](rubrics/ideation-concepting.md)
(`hmw_linkage`, `rice_integrity`, `direction_distinctness`). The most lenient pass rule in
the pipeline — divergence is not punished as hard as fabrication. Rule in that file.

Persisted files: `output/<project-slug>/ideation.{json,md}`.

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
breakpoints, and the required state/accessibility keys — all specified below,
enforced by `ux-pipeline/validators/wireframe.py` and narrated in
`ux-pipeline/skills/wireframe-ia/assets/component-patterns.md`. Material 3
survives as one *optional* baseline profile, with its tokens extracted to
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
    "accessibility": {"contrast": "string — cites a ratio (N:1) or a token pair",
                      "keyboard_focus": "string", "labels": "string",
                      "touch_targets": "string — cites a measurement",
                      "reading_order": "string",
                      "status_messages": "string", "motion": "string"},
    "requirements": {"data_dependencies": ["string"], "permissions": ["string"],
                     "edge_cases": ["string"], "open_questions": ["string"]}
  }],
  "responsive_matrix": [{"component": "string", "desktop": "string",
                         "tablet": "string", "mobile": "string"}],
  "prototype_flows": [{"from": "01 - Login", "trigger": "string",
                       "to": "02 - Dashboard", "interaction": "string"}],
  "design_system_gaps": [{"need": "string", "nearest_role": "string",
                          "why_insufficient": "string"}],
  "heuristic_review": [{"heuristic": "string — one of the ten",
                        "page": "string — a page_name, or 'none'",
                        "severity": "high|medium|low|none",
                        "finding": "string", "fix": "string"}],
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
  `.loading`, `.empty`, `.error`; all seven `accessibility` keys; and
  `requirements.data_dependencies` + `.edge_cases`.

**Tier 1 — accessibility (WCAG 2.2 AA)**

Accessibility is the one quality the pipeline can partially *check* rather than
merely require, so it is checked. The standard is **WCAG 2.2 AA**, and the seven
keys are not a form to fill in:

- `contrast` must cite evidence, not a claim: either a ratio in `N:1` form
  (≥ 4.5:1 for body text, ≥ 3:1 for large text and non-text UI) or a named pair
  of `design_system.tokens.color` roles. "Meets WCAG AA" is not evidence.
- `touch_targets` must cite a measurement meeting the platform minimum — 48dp
  (Android), 44pt (iOS), 44px (web) — not "targets are large enough".
- `status_messages` says how an async result (the `loading` → `error` / `success`
  transitions the states block already requires) reaches someone who is not
  looking at that part of the screen. A state change announced only by colour or
  position is exactly the "never rely on colour alone" rule in another costume.
- `motion` names the reduced treatment under `prefers-reduced-motion`, or states
  that the page has no motion to reduce.
- `keyboard_focus`, `labels` and `reading_order` stay narrative, judged at Tier 2.
- **No two pages may carry a byte-identical `accessibility` block.** Identical
  blocks mean the accessibility was written once and pasted, which is the failure
  the whole section exists to prevent — different pages have different focus
  orders and different things to announce.
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
- `heuristic_review` covers **all ten** usability heuristics — one entry each,
  named exactly as
  `ux-pipeline/skills/wireframe-ia/references/usability-heuristics.md` lists them.
  Every entry carries a `finding` and a `fix`; `severity` ∈ {high, medium, low,
  none}; `page` is a specced page name, or `"none"` when the heuristic is clean.
  A `severity` of `none` requires `page` and `finding` to be `"none"` and the
  `fix` to state why the design already satisfies it. **At least one heuristic
  must carry a real finding** — ten-for-ten clean is not a clean bill of health
  on a real product, it is what a review that was never run looks like. This is
  the pipeline's only evaluative
  pass before a human sees the spec; it catches what the structural rules
  cannot — no way out of a state, no undo on an expensive action, a page that
  asks the user to remember what it could have shown.
- `primary_action` is not ALL CAPS and is ≤ 4 words.
- Sitemap and page specs describe the same set.
- `figma_file_url` is optional — a URL string once the Figma render step ran,
  `null` if it failed. Exempt from the hex/forbidden-term scan.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/wireframe-ia.md`](rubrics/wireframe-ia.md)
(`ds_compliance`, `ia_coherence`, `state_and_responsive_coverage`,
`accessibility_rigor`, `requirements_completeness`). The strictest pass rule in
the pipeline — `ds_compliance` must be a 5. Rule in that file.

Persisted files: `output/<project-slug>/wireframe.{json,md}`. The `.md` follows the final
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
    "acceptance_criteria": [{"given": "string", "when": "string", "then": "string"}],
    "accessibility_criteria": [{"given": "string", "when": "string", "then": "string"}],
    "analytics_events": [{"event": "string", "trigger": "string",
                          "properties": ["string"]}]
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
- **Every Stage-4 page is covered by ≥ 1 story carrying a non-empty
  `accessibility_criteria`**, each entry a full Given/When/Then (checked when the
  Stage-4 artifact is supplied as context). Stage 4 designs accessibility in per
  page; without this rule none of it becomes a testable requirement and it is
  silently dropped at the handoff boundary. Derive each from that page's
  `accessibility` block — the keyboard path, the labels and error
  identification, or what gets announced — not from a generic a11y checklist.
- **`analytics_events` is non-empty for any story whose Stage-4 page has a
  `primary_action` that writes data** (checked when the Stage-4 artifact is
  supplied as context). Each entry names an `event` and the `trigger` that fires
  it. This is what makes a Stage-3 `success_metric` observable after ship rather
  than aspirational.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/delivery-handoff.md`](rubrics/delivery-handoff.md)
(`story_completeness`, `traceability`, `voice_consistency`). Pass rule in that file.

Persisted files: `output/<project-slug>/delivery.{json,md}`. The `.md` — Jira-style
stories with Given/When/Then plus microcopy tables — is the HITL surface.

---

## Stage 6 — evaluation-planning

State keys: `evaluation_plan` — reads `journey_map`, `feature_matrix`,
`wireframe_specs`, `heuristic_review`, `developer_handoff_stories`.

The pipeline is otherwise generative from end to end: it researches, frames,
ideates, designs and hands off, and then stops. Nothing in stages 1–5 says how
anyone would find out whether the design worked. This stage closes that loop.
It plans evaluation; it does not run it — the output is a test plan and a
measurement plan a team executes after the build.

**Output**

```json
{
  "usability_test": {
    "objective": "string — the decision this test is meant to inform",
    "method": "moderated | unmoderated",
    "participants": {"count": 5, "segments": ["string — a Stage-2 persona"],
                     "recruit_from": "string"},
    "tasks": [{
      "id": "T1",
      "scenario": "string — what the participant is asked to do, in their words",
      "journey_stage": "string — a Stage-2 journey stage",
      "pages": ["string — a Stage-4 page_name"],
      "success_criteria": "string — observable behaviour, not satisfaction",
      "probes": ["string — a Stage-4 heuristic_review heuristic this task tests"]
    }],
    "what_would_change_the_design": "string"
  },
  "metric_plan": [{
    "metric": "string — a Stage-3 success_metric name",
    "feature": "string — the Stage-3 feature it belongs to",
    "events": ["string — a Stage-5 analytics_events event name"],
    "baseline_source": "string",
    "read_after": "string — when the metric first becomes readable"
  }],
  "open_baselines": ["string — a metric whose baseline is still unknown"]
}
```

**Tier 1**

- `usability_test.objective` and `what_would_change_the_design` are non-empty.
  A test whose result would change nothing is theatre; naming the consequence
  up front is what stops it being run for reassurance.
- `method` ∈ {moderated, unmoderated}. `participants.count` ≥ 5, with non-empty
  `segments` and `recruit_from`.
- Every `segments` entry names a Stage-2 persona (checked when the Stage-2
  artifact is supplied as context). Testing with people the research never
  described tells you about a different product.
- 3–8 tasks. Each has a non-empty `scenario` and `success_criteria`, a
  `journey_stage` matching a Stage-2 journey stage, and a non-empty `pages`
  list whose every entry is a Stage-4 page (both checked when those artifacts
  are supplied as context).
- Every Stage-3 `success_metric.name` appears exactly once in `metric_plan`
  (checked when the Stage-3 artifact is supplied as context). A metric declared
  at ideation and then never planned for is the same as not having declared it.
- Every `metric_plan.events` entry names a Stage-5 `analytics_events` event
  (checked when the Stage-5 artifact is supplied as context). The list **may be
  empty** — not every metric is read from a UI event; index coverage, a backend
  report and an ops figure are all legitimate sources, and `baseline_source`
  says which. Whether an empty list is honest or lazy is `metric_integrity`'s
  call, not Tier-1's.
- Every Stage-3 metric whose `baseline` is `"unknown"` appears in
  `open_baselines`. The pipeline is allowed not to know a baseline; it is not
  allowed to lose track of which ones it does not know.

**Tier 2** — scored 1–5 per dimension against
[`rubrics/evaluation-planning.md`](rubrics/evaluation-planning.md)
(`task_fidelity`, `risk_coverage`, `metric_integrity`). Pass rule in that file.

Persisted files: `output/<project-slug>/evaluation.{json,md}`.

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

**Score scale.** `judge_scores[stage]` — in state and in `workspace/run.json` — is
the Tier-2 **weighted mean on the 1–5 scale**, the same number `pass_when` is
applied to. It is never a 0–1 fraction and never a percentage; a run record
holding `0.88` where it should hold `4.4` is a bug in whatever wrote it. When
Tier-1 fails the judge never runs, so the value is `null`, not `0`.

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

---

## Contract versioning

Every artifact carries a top-level **`contract_version`** naming the contract it
was produced under. The current version is **`2.0`**.

**Why it exists.** The canonical copies of these rules live in the Superlap
skills on claude.ai, outside this repo, and `rules/README.md` is explicit that
nothing here can check them. Without a stamp, an artifact produced by a skill
still running an older copy of the rulebook is indistinguishable from one that
simply failed — and a rule tightened here is invisible to the runs that matter.
The stamp makes staleness detectable instead of silent.

**What the validators do with it.** Nothing — Tier-1 always checks the artifact
against the *current* rules, because a validator that softened itself per
version would defeat its own purpose. The stamp is for the humans and for CI.

**What CI does with it.** `.github/workflows/harness.yml` validates every
committed artifact stamped at the current version and fails on any violation.
An artifact stamped at an older version, or carrying no stamp at all, is
reported as **legacy** and does not fail the build: it is a record of a run that
happened under a contract that no longer exists, and retrofitting fields onto it
would mean inventing the data the pipeline forbids inventing. Re-run the stage
to bring it current; never hand-write the new fields into an old artifact.

**When to bump.** Raise the minor version when a stage gains a field or a rule
that existing artifacts would not satisfy. Raise the major version when a stage's
shape changes incompatibly. Record what changed here.

| Version | Changed |
|---|---|
| `1.0` | The original five-stage contract. |
| `2.0` | Stage 2: 2–3 personas (was exactly 2); optional journey `current_metric`. Stage 3: `success_metric` required per feature. Stage 4: WCAG 2.2 AA named; `accessibility.status_messages` and `.motion` required; `contrast` and `touch_targets` must cite evidence; no two pages may share an identical accessibility block; `heuristic_review` required. Stage 5: `accessibility_criteria` required per Stage-4 page; `analytics_events` required on write stories. New Stage 6 — `evaluation-planning`. |
