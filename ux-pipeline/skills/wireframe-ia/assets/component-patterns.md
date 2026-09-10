# Page & Component Patterns (Wireframe Reference)

Narrative guidance for the wireframe stage. The machine-checked vocabulary — the
base-role taxonomy, the naming patterns, the required state and accessibility
keys — lives in `../../../rules/CONTRACTS.md` § Stage 4 and is enforced by
`ux-pipeline/validators/wireframe.py`.

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

## Accessibility (WCAG 2.2 AA)

Per page, concrete and specific — seven keys:

| Key | What it must say | Checked how |
|---|---|---|
| `contrast` | 4.5:1 body, 3:1 large text and non-text UI — as a ratio, or as two named colour tokens | Tier-1 requires the ratio or the token pair |
| `touch_targets` | The size, against the minimum: 48dp Android, 44pt iOS, 44px web | Tier-1 requires a measurement that meets it |
| `keyboard_focus` | Tab order and the visible focus treatment | Tier-2 |
| `labels` | Visible labels, error identification, form instructions | Tier-2 |
| `reading_order` | DOM order, one `h1`, no skipped heading levels | Tier-2 |
| `status_messages` | How an async result reaches someone not watching that region, and whether it is polite or assertive | Tier-2 |
| `motion` | The `prefers-reduced-motion` treatment, or that there is no motion to reduce | Tier-2 |

**Never rely on colour alone** — pair it with an icon, text, or shape.

**Never rely on sight alone.** Every state in `## States` that arrives
asynchronously — loading resolving, an error appearing, a success landing —
needs a corresponding announcement. A spinner replaced by results is a silent
event to a screen-reader user unless something says so. Choose politeness
deliberately: *polite* for progress and counts that must not interrupt reading,
*assertive* only where the change alters what the visible content means (a
failed data source, a figure that became unverifiable).

**Write each page's block for that page.** Two byte-identical accessibility
blocks are a Tier-1 violation, because different pages have different focus
orders and different things to announce. If two pages genuinely share a
treatment, say so in each one's own terms rather than pasting.

## Voice

Button and CTA labels: sentence case, verb-first, ≤ 4 words ("Add to cart",
"Save", "Track order"). No ALL CAPS, no trailing period, no "Click here".
