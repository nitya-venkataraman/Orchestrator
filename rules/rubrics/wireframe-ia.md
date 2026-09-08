# Rubric — Stage 4: wireframe-ia

Scores a page-builder artifact (target + design system + UX interpretation +
user flow + sitemap + page specs + responsive matrix + prototype flows +
assumptions + validation). Read [`README.md`](README.md) first. Tier-1
(`ux-pipeline/validators/wireframe.py`) already enforces the base-role taxonomy,
the page and component naming patterns, the raw-colour ban, the required state
and accessibility keys, the responsive coverage, prototype reachability, and
sitemap↔pages parity as a mechanical scan — this rubric judges whether the IA
actually *serves the requirement*, whether the design-system discipline is real
rather than merely literal, whether the states and responsive behaviour are
genuine design decisions, and whether the pages are buildable.

This is the strictest gate in the pipeline. `pass_when` (below) requires
`ds_compliance` to be a **5** — a 4 is not good enough here, because a spec that
quietly invents a component, ignores the design system it claims to reuse, or
fudges its tokens looks fine in review and becomes a build problem later.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `ds_compliance` | 0.25 | The resolved design system is real and actually used: components carry that system's names, `reused` genuinely outnumbers `new`, and every `new` component has a `why_new` that survives scrutiny. Every visual decision is a token from `design_system.tokens`, never a raw value. Page and component naming follows the convention throughout. Every real gap is a `design_system_gaps` entry, not a stretched component. |
| `ia_coherence` | 0.20 | The flow, sitemap, and page set are a recognizable consequence of *this* requirement (or the chosen direction) — they would not fit a different one equally well. `ux_interpretation` is specific, not restated boilerplate. Depth ≤ 3; page order follows the primary journey; no page exists only to hold navigation. |
| `state_and_responsive_coverage` | 0.20 | Every declared state is a real treatment naming the specific behaviour, and `success` / `disabled` appear wherever the page warrants them. Responsive behaviour genuinely recomposes — the table becomes a card list, the sidebar becomes a drawer — rather than restating "scales down", and `responsive_matrix` covers the components that actually change. |
| `accessibility_rigor` | 0.15 | Accessibility decisions are concrete, page-specific, and AA-grade: named contrast ratios or token pairs, a real tab order and focus treatment, visible labels with error identification, targets measured against the minimum, and a stated heading hierarchy. Nothing relies on colour alone. |
| `requirements_completeness` | 0.20 | A developer could scope every page from its `requirements` block alone — named data, concrete endpoints, genuine edge cases, honest open questions — and the `prototype_flows` let a user actually complete the primary journey with sensible triggers and transitions. |

## Score anchors

### `ds_compliance`
- **5** — No raw colour value, no off-taxonomy role, no left-over `SL-*`. Components carry the resolved system's real names; new components are few and justified; naming convention is followed on every page and component; any novel pattern has a corresponding `design_system_gap`.
- **3** — Passes the literal Tier-1 scan, but the "reused" design system is nominal (generic names that no real library would use), most components are marked `new` with thin justifications, or an obvious gap (a multi-step progress indicator, a persistent mini-player) was solved by stretching `Card` / `BottomSheet` instead of being flagged.
- **1** — Would only pass Tier-1 on a technicality; the declared design system is not visibly used, or components do things the system doesn't support and the spec doesn't say so.

### `ia_coherence`
- **5** — Swap in a different requirement and this sitemap would clearly be wrong; the pages follow the primary journey; structure is flat and purposeful; `ux_interpretation` reads as an actual interpretation.
- **3** — Sensible IA, but generic — it supports the problem space rather than the specific requirement, or `ux_interpretation` mostly paraphrases the input back.
- **1** — Sitemap organized by data model, padded with routing-only pages, or contradicts the chosen direction.

### `state_and_responsive_coverage`
- **5** — Every state names the specific treatment ("skeleton rows on the results list, header stays live"); empty states offer exactly one next action; errors say what happened and how to recover; the responsive matrix shows real recomposition at every breakpoint.
- **3** — States are present but one or two are perfunctory ("shows a spinner", "displays an error"), `success` is missing on a page that writes data, or a responsive row says "scales down" / "same as desktop" where the layout plainly must change.
- **1** — States are placeholders across pages, or the responsive behaviour is desktop scaled down with no recomposition anywhere.

### `accessibility_rigor`
- **5** — Contrast cites ratios or token pairs; focus and tab order are described per page; labels cover error identification and form instructions; targets are measured; heading hierarchy is stated. Colour is never the only signal.
- **3** — Keys are filled but generic — "meets WCAG AA", "keyboard accessible", "labels present" — repeated near-verbatim across pages.
- **1** — Boilerplate copied on every page, or accessibility contradicts the design (a colour-only error state, targets under the minimum).

### `requirements_completeness`
- **5** — Named data, concrete endpoints, edge cases that matter for that page, and a prototype whose triggers and transitions plausibly complete the journey.
- **3** — Requirements are present but thin on one or two pages — `data_dependencies` says "backend API" instead of an endpoint, or `edge_cases` just repeats "handle errors" — or the prototype is technically connected but skips a step a user would need.
- **1** — Requirements blocks are boilerplate copied across pages, or the load-bearing pages have generic requirements.

## Calibration

`ia_coherence` catches the generic spec. A sitemap that would fit any
requirement equally well means the input didn't actually shape anything — that's
a 2, regardless of how clean the pages are.

`ds_compliance` is scored past the substring scan. Tier-1 catches a raw hex; it
does not catch a `design_system` block that claims to reuse "Acme DS" while
every component is marked `new`, or a `Card` pinned across five pages as a
faux-sticky panel. Those are what `why_new` and a `design_system_gaps` entry
exist for.

`state_and_responsive_coverage` is where the PDF's two hardest rules live: *do
not design only the happy path*, and *do not simply scale the desktop UI down*.
Score both literally.

`requirements_completeness` is the dimension most likely to be padded. "Handles
errors gracefully" is not an edge case. "GET /orders/{id} — 404 when the order is
purged after 90 days" is.

## Common failure modes

- Empty `design_system_gaps` on a spec with an obviously novel pattern.
- Every component marked `new` with a `why_new` that restates the component name.
- A declared design system whose token names appear nowhere in the page specs.
- Sitemap depth > 3, or a page that only holds links.
- `states.loading` = "shows a spinner"; `states.error` = "displays an error".
- No `success` state on a page whose `primary_action` writes data.
- `responsive` rows that say "scales down" or "same as desktop" at every breakpoint.
- A `Table` that stays a table at 375px.
- Accessibility blocks identical across every page.
- `requirements.data_dependencies` that names no concrete endpoint or service.
- `prototype_flows` that satisfy reachability but skip a step the journey needs.
- `primary_action` labels that are ALL CAPS or over four words.

```json
{
  "stage": "wireframe-ia",
  "weights": {
    "ds_compliance": 0.25,
    "ia_coherence": 0.20,
    "state_and_responsive_coverage": 0.20,
    "accessibility_rigor": 0.15,
    "requirements_completeness": 0.20
  },
  "pass_when": "min>=4 and scores['ds_compliance']>=5"
}
```
