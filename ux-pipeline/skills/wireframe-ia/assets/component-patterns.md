# Page & Component Patterns (Wireframe Reference)

Narrative guidance for the wireframe stage. The machine-checked vocabulary — the
base-role taxonomy, the naming patterns, the required state and accessibility
keys — lives in `../../../rules/CONTRACTS.md` § Stage 4 and mirrors
`.claude/skills/superlap-wireframe/references/page-builder-reference.md`.

This stage is **design-system agnostic**. Reuse whatever system the project has;
`references/material-design-tokens.json` is only a baseline token set for when
none is available.

## Naming

- **Pages** — `NN - Title` (web) or `MNN - Title` (mobile), two digits, ordered
  by the primary journey, unique within the family: `01 - Login`,
  `02 - Dashboard`, `M01 - Login`, `M02 - Home`.
- **Components** — `<Layer> / <Name>` where `<Layer>` is `Page`, `Section`, or
  `Component`: `Page / Dashboard`, `Section / Summary`, `Component / KPI Card`.
- **Variants** — meaningful states only:
  `Primary | Secondary | Tertiary | Destructive | Disabled | Loading`.

The `name` is whatever the resolved design system calls it. The `base` is the
**role** it plays, from the fixed taxonomy. If nothing in the taxonomy fits, that
is a `design_system_gaps` entry, not a new role.

## Page chrome

- **Web** — `Header` with global `Navigation`; `Breadcrumb` where depth > 1;
  `Sidebar` for a persistent section nav; `Footer` for secondary links. Sticky
  positioning only where the element is genuinely pinned.
- **Mobile** — bottom `Navigation` (3–5 destinations), a top `Header`, and back
  affordance per platform (back arrow on Android, back chevron + title on iOS).
  Respect safe areas: status inset (24dp Android / 47–59pt iOS) and bottom inset
  (48dp gesture nav / 34pt home indicator). Primary actions clear the bottom
  inset.
- **Secondary nav within a page** — `Tabs` directly under the header.

## Content

- **Card** for a bounded unit — a summary, a status, a preview. Not for a
  full-width list.
- **List** for repeated rows with a `Divider` between them; leading avatar/icon,
  trailing metadata or icon action.
- **Table** on web for multi-column comparable data; on mobile it recomposes to
  a card/list, never a pinch-zoom table.
- **Primary action** — exactly one per page (`Button` primary, or a `FAB` on
  mobile) — never two competing. Secondary actions are outlined or text.
- **Feedback** — `Toast` for transient confirmation (≤ 1 line, ≤ 1 action);
  `Modal` / `Confirmation` only for a blocking decision; `Drawer` /
  `BottomSheet` for supplementary actions or a short form; `Alert` / `Banner`
  for persistent page-level conditions.

## Forms

- `Input` / `Textarea` / `Select` with visible labels and helper or error text
  below. Never a placeholder as the only label.
- Choice controls: `Radio` (one of many), `Checkbox` (many), `Switch` (a single
  setting immediately applied), `Select` (a long list).
- Pickers: `DatePicker` / `TimePicker`; `Menu` for a short dropdown.
- Web forms are 2-column at desktop and tablet, 1-column at mobile, with stacked
  actions.

## Responsive recomposition

Do not scale the desktop UI down — recompose it.

| Component | Desktop 1440 | Tablet 768 | Mobile 375 |
|---|---|---|---|
| Navigation | Full navigation | Reduced navigation | Menu |
| Cards | 3-column | 2-column | 1-column |
| Table | Full table | Horizontal scroll | Card / list |
| Form | 2-column | 2-column | 1-column |
| Sidebar | Visible | Collapsed | Drawer |
| Actions | Inline | Inline | Stacked |

`laptop` 1280 is usually desktop's structure with tighter gutters — say so
rather than omitting it.

## States

Every page: `default`, `loading`, `empty`, `error`. Add `success` where the page
writes data, and `disabled` where a control is conditionally unavailable.

- **Loading** names the regions and the skeleton shape, not "shows a spinner".
- **Empty** says why there is no data and offers exactly one next action.
- **Error** says what happened in the user's terms, then how to recover.
- **Success** confirms completion and offers the next relevant action.
- **Disabled** says why it is unavailable and what would enable it.

## Accessibility (WCAG AA)

Per page, concrete and specific: `contrast` (4.5:1 body, 3:1 large text and
non-text UI, named token pairs), `keyboard_focus` (tab order and the visible
focus treatment), `labels` (visible labels, error identification, form
instructions), `touch_targets` (against the ~44×44px minimum), `reading_order`
(DOM order, one `h1`, no skipped heading levels).

**Never rely on colour alone** — pair it with an icon, text, or shape.

## Voice

Button and CTA labels: sentence case, verb-first, ≤ 4 words ("Add to cart",
"Save", "Track order"). No ALL CAPS, no trailing period, no "Click here".
