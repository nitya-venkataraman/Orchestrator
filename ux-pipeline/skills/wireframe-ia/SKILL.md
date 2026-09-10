---
name: wireframe-ia
description: Use this skill to build production-ready web pages and mobile screens — UX interpretation, user flow, sitemap, page-by-page architecture, responsive behaviour across breakpoints, all UI states, WCAG 2.2 AA accessibility, a ten-heuristic usability critique, per-page build requirements, and a wired clickable Figma prototype. Design-system agnostic; reuses whatever design system the project already has. Triggered as Node 4 of the UX pipeline.
allowed-tools: Read, Write, Bash, Skill, mcp__Figma__create_new_file, mcp__Figma__use_figma, mcp__Figma__get_libraries, mcp__Figma__search_design_system, mcp__Figma__whoami
---

# Wireframing & Information Architecture (Figma Page Builder)

## Inputs

From state: `feature_matrix` (the prioritized features), `concept_proposals` +
`selected_concept` / `selected_direction` (the human-chosen direction),
`target_surface` (`web` | `mobile` | `both`) and `mobile_platform`
(`android` | `ios`, required when the surface includes mobile) — both set at the
`select_direction` fork — and `design_system_input` (a component library, token
file, Figma library, styleguide, or existing code) when the project has one.

Where information is missing, make a reasonable UX assumption and record it in
`assumptions` rather than stalling.

## Steps

1. Read `selected_direction` (human-approved from Node 3) and `target_surface`.
   If `target_surface` is missing, stop and ask web / mobile / both; if it
   includes mobile and `mobile_platform` is missing, ask Android or iOS. Every
   layout decision depends on these.
2. **Resolve the design system.** Priority: `design_system_input` → a library
   already linked in Figma (`get_libraries`, `search_design_system`) → a
   documented baseline. Load `assets/component-patterns.md` for the enforced
   vocabulary and `references/material-design-tokens.json` for a baseline token
   set. Record `design_system` as `{name, source, tokens}`; `source: "baseline"`
   requires an `assumptions` entry naming what you chose and why. **Reuse before
   you create** — every `new` component needs a `why_new`.
3. Write `ux_interpretation` (primary user, user goal, business goal, main task,
   context, entry point, expected outcome, required data, business rules,
   constraints, dependencies) **before** designing. Do not invent business rules
   when the requirements state them.
4. Write `user_flow`: the primary journey as ordered steps, supporting tasks,
   and error scenarios. Decide here that the design is not only the happy path.
5. Generate the sitemap from the flow, ordered by the Stage-2 journey rather
   than the data model. Depth ≤ 3; no nav-only or unnecessary pages. Name pages
   `NN - Title` (web) / `MNN - Title` (mobile), two digits, unique per family.
6. Spec each page: `purpose`, `primary_user`, `primary_action` (sentence case,
   verb-first, ≤ 4 words), `secondary_actions`, `content_structure` (ordered
   top→bottom, most important first), `navigation`, `components` (objects with
   `name` / `base` role / `source` / `variants` / `why_new`), `data`, and
   `interactions`. 3–12 pages; sitemap and pages describe the same set.
7. **Responsive behaviour.** Every web page carries `desktop` 1440 / `laptop`
   1280 / `tablet` 768 / `mobile` 375; every mobile page carries `mobile`. Fill
   `responsive_matrix` for the major components. Recompose — do not scale the
   desktop UI down.
8. **All UI states.** `default`, `loading`, `empty`, `error` on every page; add
   `success` and `disabled` where the page writes data or disables a control.
   Real treatments, not "shows a spinner".
9. **Accessibility, designed in.** Per page: `contrast`, `keyboard_focus`,
   `labels`, `touch_targets`, `reading_order`, `status_messages`, `motion` —
   **WCAG 2.2 AA**, concrete, specific. `contrast` cites a ratio or two named
   colour tokens and `touch_targets` cites a measurement, because Tier-1 checks
   those two for evidence and a bare "meets WCAG AA" fails. `status_messages`
   says how each async result from step 8 reaches someone not watching that
   region; `motion` names the `prefers-reduced-motion` treatment. Never rely on
   colour alone, and never on sight alone. Write each page's block for that
   page — two identical blocks are a Tier-1 violation.
10. **Build requirements per page** — `data_dependencies` (concrete
    endpoints/services/stores), `permissions`, `edge_cases`, `open_questions`.
11. **Prototype.** Fill `prototype_flows` (`from` / `trigger` / `to` /
    `interaction`) so every page is reachable from its family's entry page and
    the primary journey is walkable.
12. **Critique what you just designed.** Load
    `references/usability-heuristics.md` and walk `user_flow.primary_journey`,
    then the error scenarios, against all ten heuristics. Record every one in
    `heuristic_review` — `{heuristic, page, severity, finding, fix}`. This is the
    pipeline's only evaluative pass before a human sees the spec, and steps 7–11
    structurally cannot catch what it looks for: a state with no way out, an
    expensive action with no undo, a page asking the user to remember what it
    could have shown. **Fix what you find** and record the fix; leave a finding
    open only when the fix is a scope or policy decision, and say so. Two real
    findings beat ten padded ones, and a heuristic you score clean needs a
    one-line reason.
13. Fill `validation` (`ux`, `ui`, `responsive`, `accessibility`, `prototype`)
    and `assumptions`.
14. **Self-check.** Run `python3 ux-pipeline/validators/wireframe.py <your .json>`
    — it re-implements the exact Tier-1 checks (base-role taxonomy, page and
    component naming, required states, the accessibility keys and their contrast
    and touch-target evidence, responsive coverage, prototype reachability, the
    ten-heuristic review, sitemap↔pages parity) — and fix every violation before
    rendering to Figma.
15. **Render to Figma, high fidelity.** Load `figma-create-new-file` and call
    `create_new_file` (`editorType: "design"`, `fileName: "<slug> —
    <target_surface>"`; resolve `planKey` via `whoami`, ask if the user has more
    than one plan). Then load `figma-generate-design` + `figma-use` and drive
    `use_figma`: link the resolved design system's library and instance its real
    components (else build local components styled to the baseline); create
    variables for the `design_system.tokens` and bind them; build components
    with variants for meaningful states; a cover frame with the route tree,
    target, and design system; one Auto Layout frame per page named exactly as
    `page_name` (web 1440 with 1280/768/375 variants where the structure
    changes; mobile `390×852pt` ios / `360×800dp` android with chrome and safe
    areas); state frames for the non-default states; **prototype connections for
    every `prototype_flows` entry**; a "Responsive Behaviour" frame; a
    "Requirements" frame; and a gaps frame if any were flagged. Capture the
    returned file URL as `figma_file_url`. If the Figma step fails, continue with
    `figma_file_url = null` and note why.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 4 — wireframe-ia** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/wireframe-ia.md`](../../../rules/rubrics/wireframe-ia.md)
— the strictest gate in the pipeline: `ds_compliance` must be a 5 and
`accessibility_rigor` at least a 4. A need outside the base-role taxonomy is a
`design_system_gaps` entry, never an invented role or a raw value.

1. Return `target`, `mobile_platform`, `design_system`, `ux_interpretation`,
   `user_flow`, `sitemap`, `wireframe_specs` (the `pages` array),
   `responsive_matrix`, `prototype_flows`, `design_system_gaps`,
   `heuristic_review`, `assumptions`, `validation`, `figma_file_url`, and set
   `design_tokens_applied = true` to state.
2. Persist `output/<project-slug>/wireframe.json` and `output/<project-slug>/wireframe.md`. The
   Markdown follows the final review format: header (target, design system and
   whether reused or baseline, selected direction, validator result, `Figma:
   <figma_file_url>`), then UX Interpretation, User Flow, Sitemap, Pages Created,
   Components Used (reused vs new), Responsive Behaviour, Accessibility,
   Prototype, Heuristic Review, Design System Gaps, Assumptions, Validation. Reuse the run's
   `<project-slug>` folder; overwrite on re-run.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
