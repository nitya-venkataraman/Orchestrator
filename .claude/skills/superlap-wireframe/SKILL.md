---
name: superlap-wireframe
description: Stage 4 of the Superlap UX pipeline, and a standalone Figma page builder. Turns requirements, user stories, research, or a chosen design direction into production-ready web pages and mobile screens in Figma — UX interpretation, user flow, sitemap, page-by-page architecture, responsive behaviour across breakpoints, all UI states, WCAG AA accessibility, build requirements, and a wired clickable prototype. Design-system agnostic — it reuses whatever design system the project already has. Use whenever someone needs wireframes, page or screen specs, a sitemap, information architecture, responsive layouts, component specifications, a dashboard/form/table/wizard/portal/landing page, or wants requirements or user stories turned into UI — and whenever they mention wireframing, information architecture, page building, responsive design, design systems, Figma screens, or the Superlap pipeline. Also use it as stage 4 when running the full pipeline.
---

# Wireframing & IA — Stage 4 (Figma Page Builder)

Requirements in; a validated page-architecture spec plus a real Figma file out —
high-fidelity, responsive, accessible, and wired as a clickable prototype.

This stage has the strictest gate in the pipeline (judge threshold **0.80**)
because a spec that quietly invents a component, skips the error state, or
scales the desktop layout down instead of recomposing it looks fine in review
and becomes a build problem later.

**Read `references/page-builder-reference.md` before writing any spec.** The base
component-role taxonomy, the page and component naming patterns, the
breakpoints, the required state keys, and the accessibility keys all live there,
and both validators check against them literally.

This skill is **design-system agnostic**. It does not own a component library —
it reuses whichever design system the project already has, and falls back to a
documented baseline only when none is available.
`references/material-design-system.md` is one such optional baseline profile, not
the law.

## Inputs

Accept whatever was supplied — from the user's message, from files, or from a
Stage-3 ideation JSON. **Do not require all of them.** Where information is
missing, make a reasonable UX assumption and record it in `assumptions`.

**Required**

- `requirements` — the source material in any shape: business or user
  requirements, user stories, acceptance criteria, UX research, interview
  transcripts, existing flows or wireframes, screenshots, API specs, existing
  code. In pipeline mode this is the `features` array of a Stage-3
  `IdeationOutput`.
- `target` — `web`, `mobile`, or `both`. **If absent, ask and wait.** It decides
  breakpoints versus safe areas, and the page-naming family.
- `mobile_platform` — `android` or `ios`. Required when `target` is `mobile` or
  `both`; **ask if absent**. Must be omitted when `target` is `web`.

**Optional**

- `design_system` — a component library, token file, Figma library, styleguide,
  or existing product code. Strongly preferred; see Method step 2.
- `design_direction` — in pipeline mode, the one direction a human chose from
  Stage 3. Design for that one. Other directions are dead; do not hedge by
  blending them.
- `strategy` — Stage-2 personas / journey, for grounding the flow and sitemap
  order.
- `revision_feedback`.

## Method

Work the stages in order. Do not start visual styling before you understand the
user goal.

1. **Confirm the target.** If `target` (and `mobile_platform` where it applies)
   was not supplied, ask and stop until answered. Everything downstream depends
   on it.

2. **Resolve the design system.** In priority order: a system supplied in the
   input → a library already linked in Figma (`get_libraries`,
   `search_design_system`) → a documented baseline. Record the outcome in
   `design_system` with `source: "existing"` or `"baseline"`; a `baseline` must
   be paired with an `assumptions` entry naming what you chose and why.

3. **Write the UX interpretation** (`ux_interpretation`) before designing:
   primary user, user goal, business goal, main task, context, entry point,
   expected outcome, required data, business rules, constraints, dependencies.
   Do not invent business rules when requirements state them.

4. **Define the experience** (`user_flow`): the primary journey as ordered
   steps, the supporting tasks, and the error scenarios. Name the states the
   requirement implies — this is where you decide the design is not only the
   happy path.

5. **Sitemap.** Derive the page set from the flow, ordered by the journey rather
   than the data model. Depth ≤ 3. If a page exists only to hold navigation,
   delete it. Do not create unnecessary pages.

6. **Name the pages** per the reference §3: `NN - Title` for web, `MNN - Title`
   for mobile, two digits, unique within the family, ordered by the journey. A
   `both` target carries both families, sharing titles where it is the same
   experience.

7. **Spec each page.** For every page define `purpose`, `primary_user`,
   `primary_action` (sentence case, verb-first, ≤ 4 words), `secondary_actions`,
   `content_structure` (ordered top to bottom, most important first),
   `navigation`, `components`, `data`, and `interactions`.

   Each `components` entry is an object: `name` (`Page|Section|Component /
   <Name>` — whatever the resolved design system calls it), `base` (a role from
   the fixed taxonomy in the reference §2), `source` (`reused` or `new`),
   `variants`, and `why_new` when it is new. **Reuse before you create.**

8. **Responsive behaviour.** Every web page carries all four breakpoints
   (`desktop` 1440 / `laptop` 1280 / `tablet` 768 / `mobile` 375); every mobile
   page carries at least `mobile`. Fill `responsive_matrix` for the major
   components — what Navigation, Cards, Table, Form, Sidebar, and Actions each
   do at every breakpoint. **Do not simply scale the desktop UI down; recompose
   it.** A row that says "scales down" everywhere is a failure, not an answer.

9. **All UI states.** `states.default`, `loading`, `empty`, `error` are required
   on every page; add `success` and `disabled` wherever the page writes data or
   has a conditionally unavailable control. Loading names the specific skeleton
   regions. Empty says why there is no data and offers the next action. Error
   says what went wrong in the user's terms and how to recover.

10. **Accessibility, designed in.** Every page carries an `accessibility` object
    with `contrast`, `keyboard_focus`, `labels`, `touch_targets`, and
    `reading_order` — WCAG AA, concrete, page-specific. Never rely on colour
    alone.

11. **Build requirements per page.** A `requirements` object with
    `data_dependencies` (concrete endpoints/services/stores, e.g. `GET
    /orders/{id}`), `permissions`, `edge_cases` (offline, partial data, expired
    auth, long text, slow network), and `open_questions`.

12. **Interaction and prototype.** Fill `prototype_flows` — `from`, `trigger`,
    `to`, `interaction` — so the primary journey is walkable end to end. Every
    page must be reachable from its family's entry page; the validator checks
    this literally.

13. **Flag gaps rather than inventing.** If a need maps to no base role, emit a
    `design_system_gaps` entry naming the need, the nearest role, and why it
    doesn't fit. A named gap is a design finding; an invented component is debt.

14. **Validate.** Fill the `validation` object (`ux`, `ui`, `responsive`,
    `accessibility`, `prototype`) and run the bundled validator:

    ```bash
    python scripts/validate_ds.py path/to/wireframe.json
    ```

    It re-implements the exact Tier-1 checks the pipeline runs, so you catch
    violations before they cost a retry. Fix every one.

15. **Render to Figma** once the validator passes — see **Step 15 — Render to
    Figma** below.

## Output contract

Every run produces:

1. **The validated JSON artifact** — schema below. The machine contract, parsed
   literally by `validate_ds.py` and the pipeline gate. Do not rename fields, add
   prose inside it, or drop required keys.
2. **A new Figma file** per Step 15, URL captured in `figma_file_url`.
3. **Two files in `output/`:**
   - `output/wireframe-<slug>.json` — pretty-printed JSON artifact
   - `output/wireframe-<slug>.md` — human-readable rendering (below)
   Same `<slug>` as earlier stages. Overwrite on re-run.
4. **The visible reply is the Markdown rendering** — the contents of the `.md`
   file and nothing else. Raw JSON only if asked.

### Schema

Return **only** this JSON — no prose, no code fence — when asked for the
artifact.

```json
{
  "target": "web",
  "mobile_platform": null,
  "design_system": {
    "name": "Acme DS 2.4",
    "source": "existing",
    "tokens": {
      "color": ["color.surface.default"],
      "typography": ["type.heading.lg"],
      "spacing": ["space.400"]
    }
  },
  "ux_interpretation": {
    "primary_user": "string", "user_goal": "string", "business_goal": "string",
    "main_task": "string", "context": "string", "entry_point": "string",
    "expected_outcome": "string", "required_data": ["string"],
    "business_rules": ["string"], "constraints": ["string"],
    "dependencies": ["string"]
  },
  "user_flow": {
    "primary_journey": ["ordered step"],
    "supporting_tasks": ["string"],
    "error_scenarios": ["string"]
  },
  "sitemap": [{"page": "01 - Login", "path": "/login", "children": ["02 - Dashboard"]}],
  "pages": [
    {
      "page_name": "02 - Dashboard",
      "purpose": "string — one sentence",
      "primary_user": "string",
      "primary_action": "Sentence case verb first",
      "secondary_actions": ["string"],
      "content_structure": ["ordered top-to-bottom, most important first"],
      "navigation": "string",
      "components": [
        {"name": "Component / KPI Card", "base": "Card", "source": "reused",
         "variants": ["Default", "Loading"]},
        {"name": "Section / Filter Bar", "base": "Filter", "source": "new",
         "why_new": "string — why no existing component fits"}
      ],
      "data": ["string"],
      "interactions": ["string"],
      "states": {
        "default": "string", "loading": "string", "empty": "string",
        "error": "string", "success": "string", "disabled": "string"
      },
      "responsive": {
        "desktop": "string", "laptop": "string",
        "tablet": "string", "mobile": "string"
      },
      "accessibility": {
        "contrast": "string", "keyboard_focus": "string", "labels": "string",
        "touch_targets": "string", "reading_order": "string"
      },
      "requirements": {
        "data_dependencies": ["GET /orders/{id}"],
        "permissions": ["string"],
        "edge_cases": ["string"],
        "open_questions": ["string"]
      }
    }
  ],
  "responsive_matrix": [
    {"component": "Navigation", "desktop": "Full navigation",
     "tablet": "Reduced navigation", "mobile": "Menu"}
  ],
  "prototype_flows": [
    {"from": "01 - Login", "trigger": "Tap Sign in", "to": "02 - Dashboard",
     "interaction": "Smart animate, 300ms ease-out"}
  ],
  "design_system_gaps": [
    {"need": "string", "nearest_role": "Stepper", "why_insufficient": "string"}
  ],
  "assumptions": ["string"],
  "validation": {
    "ux": ["string"], "ui": ["string"], "responsive": ["string"],
    "accessibility": ["string"], "prototype": ["string"]
  },
  "design_tokens_applied": true,
  "figma_file_url": "https://www.figma.com/design/… — set by Step 15, null if it failed"
}
```

Validator constraints:

- `target` is `web` | `mobile` | `both`. `mobile_platform` is `android` | `ios`,
  required for `mobile`/`both` and forbidden for `web`.
- `design_system` names a system and declares `source`; a `baseline` source
  requires a non-empty `assumptions`. `tokens.color` / `.typography` / `.spacing`
  are non-empty.
- No raw hex and no `rgb()`/`rgba()` anywhere — colour is always a token.
  (`px` **is** allowed: the breakpoints and the 44×44px touch minimum are px by
  definition.) `figma_file_url` is exempt from the scan.
- No left-over `--sl-*` / `SL-*` / "brutalist" vocabulary.
- 3–12 pages. Page names match `NN - Title` (web) or `MNN - Title` (mobile),
  numbers unique within a family, families matching `target`.
- Component `name` matches `Page|Section|Component / <Name>`; `base` is in the
  role taxonomy; `source` is `reused` or `new`; a `new` component has `why_new`.
- Every page has non-empty `purpose`, `primary_user`, `primary_action`,
  `navigation`, `content_structure`, `data`, `interactions`; `states.default`,
  `loading`, `empty`, `error`; the five `accessibility` keys; and
  `requirements.data_dependencies` + `edge_cases`.
- Web pages carry all four breakpoints in `responsive`; mobile pages carry
  `mobile`.
- `responsive_matrix` non-empty (unless `target` is `mobile`), each row covering
  desktop/tablet/mobile.
- `prototype_flows` non-empty; every `from`/`to` is a real page; every page is
  reachable from its family's entry page.
- `ux_interpretation`, `user_flow.primary_journey`, and all five `validation`
  keys are populated. `design_tokens_applied` is `true`.
- `design_system_gaps` may be empty — but an empty array alongside a novel
  interaction pattern usually means something got quietly invented.
- `primary_action` is not ALL CAPS and is ≤ 4 words.

### Markdown rendering (`.md` file and the visible reply)

Follow the PDF's final review format.

- `# Wireframing & IA — <Project>` title, then a header block: the target
  (and mobile platform), the design system and whether it was reused or a
  baseline, the selected direction if there was one, the `validate_ds.py`
  result, and `Figma: <figma_file_url>`.
- `## UX Interpretation` — the interpretation as a definition list.
- `## User Flow` — the primary journey as numbered steps, then supporting tasks
  and error scenarios.
- `## Sitemap` — the route tree as an indented code block.
- `## Pages Created` — one `### <page_name> — \`<path>\`` per page with its
  purpose, primary user, primary and secondary actions, a **Content structure**
  list, a **Components** table (name / base / reused-or-new / variants), a
  **States** block covering all declared states, a **Responsive** line, an
  **Accessibility** block, and a `#### Requirements` block.
- `## Components Used` — reused components in one list, newly created ones in
  another with their `why_new`.
- `## Responsive Behaviour` — the `responsive_matrix` as a table.
- `## Accessibility` — the key decisions across pages.
- `## Prototype` — the `prototype_flows` as a table.
- `## Design System Gaps` — the entries, or "None."
- `## Assumptions` — the entries, or "None."
- `## Validation` — the five `validation` lists as sub-sections.

## Step 15 — Render to Figma

Run this only after the spec passes `scripts/validate_ds.py`. A malformed spec
should never reach Figma. Build **high fidelity**, not labelled boxes.

1. **Create the file.** Load the `figma-create-new-file` skill, then call
   `create_new_file` with `editorType: "design"` and `fileName: "<slug> —
   <target>"`. Resolve `planKey` from `whoami`; if the user has more than one
   plan, ask which team/org to use, otherwise use the single one.

2. **Build it incrementally.** Load `figma-generate-design` and `figma-use`,
   then drive `use_figma`:
   - **Link the design system.** `get_libraries` on the file; if the resolved
     system is available, `search_design_system` scoped to its `libraryKey` and
     instance its real components. If nothing is linkable, build local
     components styled to the baseline — either way the spec is the source of
     truth.
   - **Variables** for the `design_system.tokens` the spec references — colour,
     typography, spacing — and bind them to properties. Never a raw value.
   - **Components with variants** for the meaningful states, e.g. a Button as
     `Primary | Secondary | Tertiary | Destructive | Disabled | Loading`.
   - **Cover frame:** the `<slug>`, the target, the design system, the selected
     direction if any, and the route tree from `sitemap`.
   - **One frame per page**, in sitemap order, named exactly as `page_name`.
     Web: 1440 wide, with 1280 / 768 / 375 variants for any page whose
     `responsive` entries differ structurally. Mobile: `390×844pt` for `ios`,
     `360×800dp` for `android`, with platform chrome and safe-area insets drawn.
     Compose `content_structure` top to bottom with **Auto Layout** and
     responsive constraints; use real components, real type, real tokens.
   - **State frames** for each page's non-default states — loading skeletons,
     empty, error, success — as variants or adjacent frames.
   - **Prototype connections** for every `prototype_flows` entry, using the
     stated trigger and interaction, so the primary journey is walkable.
   - **A "Responsive Behaviour" frame** rendering `responsive_matrix`.
   - **A "Requirements" frame** listing each page's `requirements` block.
   - **A "Design System Gaps" frame** if `design_system_gaps` is non-empty.
   - Keep the layer hierarchy clean and semantically named throughout
     (reference §3).

3. **Record the URL.** Take the file URL from the `create_new_file` result, set
   it as `figma_file_url` in the JSON artifact, put it in the `.md` header, and
   report it in your reply.

If file creation or `use_figma` fails, still emit the JSON and `.md` (with
`figma_file_url` null) and say the Figma step could not complete and why — do not
block the spec on it.

## Quality bar

Judge threshold **0.80** — the highest in the pipeline.

| Criterion | Weight | What it checks |
|---|---|---|
| `ds_compliance` | 0.25 | Reuse before creation, every `new` component justified; every visual decision a token, never a raw value; naming conventions followed; real gaps flagged rather than worked around |
| `ia_coherence` | 0.20 | Flow, sitemap and page set follow the journey and serve the *specific* requirement or chosen direction; depth ≤ 3; no unnecessary or nav-only pages |
| `state_and_responsive_coverage` | 0.20 | All required states are real treatments, not placeholders; responsive behaviour genuinely recomposes rather than scaling down |
| `accessibility_rigor` | 0.15 | WCAG AA decisions are concrete and page-specific; contrast, focus, labels, targets, reading order all substantive; nothing relies on colour alone |
| `requirements_completeness` | 0.20 | Buildable per page — real data, concrete endpoints, genuine edge cases — and a prototype that completes the primary journey |

`ia_coherence` catches the generic spec — a sitemap that would fit any
requirement equally well means the input didn't actually shape anything.

## Revision handling

`revision_feedback` is direction on the previous artifact. Structural failures
are literal — a raw hex, an off-taxonomy base role, a missing state, an
unreachable page — so fix exactly what's named and rerun the validator. Judge
feedback on `ia_coherence` usually means going back to the user goal and asking
what it implies for structure, not renaming pages.
