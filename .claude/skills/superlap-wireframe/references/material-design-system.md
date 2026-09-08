# Material Design 3 — an optional baseline profile

> **Status: optional baseline, not the law.** This stage is **design-system
> agnostic** — see `page-builder-reference.md`, which is the enforced reference.
> Reuse whatever design system the project already has. Reach for this file only
> when no design system was supplied and none is linkable in Figma; then set
> `design_system.source = "baseline"`, `design_system.name = "Material 3"`, and
> record the choice in `assumptions`.
>
> The `MD-*` component names below are **not** an allowlist any more. When you
> use this profile, a spec entry still needs a `base` role from the taxonomy in
> `page-builder-reference.md` §2 — e.g.
> `{"name": "Component / MD-Card", "base": "Card", "source": "reused"}`.
> The `md.sys.*` token names below are exactly the sort of token names
> `design_system.tokens` should carry.

---

## Material Design 3 — Wireframe Design System (MD-DS)

Material 3, mobile-first. The system exists so wireframe specs are **checkable by
machine** — every screen maps to a named `MD-` component and an `md.sys.*`
token, so the validator can prove compliance instead of a human eyeballing it.

Within this profile, two rules carry most of the weight:

1. **Prefer the sanctioned `MD-` components.** A need with no component is a
   *Design System Gap* to flag — never a component invented mid-spec.
2. **Never emit a raw value.** Colour, type, shape, elevation, and spacing are
   `md.sys.*` tokens or the 4dp grid. No hex, no `px`, no `rgb()`.

Material's depth model **is** elevation and its shape scale **is** rounded
corners — so, unlike a brutalist system, those are expressed through tokens
(`md.sys.elevation.level2`, `md.sys.shape.corner.large`), never banned.

---

## 1. Platform — Android or iOS

Every run targets one platform. **Ask "Android or iOS?" if it was not supplied**
(as a `platform` input, or inside the input JSON). Material 3 is the component
and token vocabulary for **both** — the platform answer only changes layout
conventions:

| Aspect | `android` | `ios` |
|---|---|---|
| Primary nav | `MD-NavigationBar` (bottom), 3–5 destinations | `MD-NavigationBar` styled as a bottom tab bar |
| Top bar | `MD-TopAppBar` small/center, back arrow leading | `MD-TopAppBar` as nav bar: back chevron + title, large-title on scroll |
| Back affordance | system back gesture + top-bar arrow | left-edge swipe-back + top-left chevron |
| Status-bar inset | 24dp | 44–59pt (notch / Dynamic Island) |
| Bottom safe area | 48dp gesture nav | 34pt home indicator |
| Min touch target | 48×48dp | 44×44pt |
| System font | Roboto / Roboto Flex | SF Pro (Text / Display) |
| Sheets | `MD-BottomSheet` standard / modal | `MD-BottomSheet` with detents (half / full) |
| Overscroll | stretch | rubber-band |

Record the choice as `"platform": "android" | "ios"`. Each screen's `hierarchy`
names the safe-area insets it must respect and the nav pattern it uses.

---

## 2. Component library (this profile's components — no longer an allowlist)

These are the entire vocabulary. A spec that names anything else fails Tier-1.

| Component | Purpose | Common variants |
|---|---|---|
| `MD-TopAppBar` | Screen chrome: title, nav icon, actions | small, center-aligned, medium, large |
| `MD-NavigationBar` | Primary destination switch (bottom) | 3–5 items, with / without labels |
| `MD-NavigationRail` | Primary nav at `medium` window size | — |
| `MD-NavigationDrawer` | Secondary / overflow destinations | modal, standard |
| `MD-Tabs` | Switch views within one screen | primary, secondary, scrollable |
| `MD-Button` | Action trigger | elevated, filled, filled-tonal, outlined, text |
| `MD-FAB` | The screen's single most important action | fab, small, large, extended |
| `MD-IconButton` | Compact icon-only action | standard, filled, tonal, outlined |
| `MD-Card` | A bounded content unit | elevated, filled, outlined |
| `MD-List` | Vertical set of related items | one-, two-, three-line items |
| `MD-TextField` | Data entry: text, search, select trigger | filled, outlined |
| `MD-Chip` | Compact attribute / filter / action | assist, filter, input, suggestion |
| `MD-Dialog` | Blocking decision or focused task | basic, full-screen |
| `MD-BottomSheet` | Supplementary content / actions from an edge | standard, modal |
| `MD-Snackbar` | Brief, low-priority feedback | single-line, with action |
| `MD-Menu` | Contextual list of choices | dropdown, cascading |
| `MD-Slider` | Select from a range | continuous, discrete, range |
| `MD-Switch` | Toggle a single setting | — |
| `MD-Checkbox` | Select zero-or-more from a set | — |
| `MD-RadioButton` | Select exactly one from a set | — |
| `MD-SegmentedButton` | Choose among 2–5 related options | single-, multi-select |
| `MD-ProgressIndicator` | Ongoing process | linear, circular; determinate / indeterminate |
| `MD-SearchBar` | Entry point to search + results | bar, view |
| `MD-Divider` | Separate list / layout groups | full-width, inset |
| `MD-Badge` | Count / dot on an icon | small (dot), large (number) |
| `MD-DatePicker` | Pick a date | docked, modal, input |
| `MD-TimePicker` | Pick a time | dial, input |

**Composition rule.** A "hero", a "stat row", an "empty state" are
*arrangements* of these components, not new components. Name the arrangement in
prose; name the component in the spec field the validator reads.

---

## 3. Tokens

Never emit a raw hex, `px`, `rgb()`, or font size. Emit the token name.

### 3.1 Colour — `md.sys.color.*` roles

`primary` · `on-primary` · `primary-container` · `on-primary-container` ·
`secondary` · `on-secondary` · `secondary-container` · `on-secondary-container` ·
`tertiary` · `on-tertiary` · `tertiary-container` ·
`surface` · `surface-container-lowest` · `surface-container-low` ·
`surface-container` · `surface-container-high` · `surface-container-highest` ·
`on-surface` · `on-surface-variant` ·
`outline` · `outline-variant` ·
`error` · `on-error` · `error-container` · `on-error-container` ·
`inverse-surface` · `inverse-on-surface` · `scrim`

Contrast: body text ≥ 4.5:1, large text and non-text UI ≥ 3:1. Use container
roles for tonal fills; never a raw tint.

### 3.2 Type — `md.sys.typescale.*`

`display-large` · `display-medium` · `display-small` ·
`headline-large` · `headline-medium` · `headline-small` ·
`title-large` · `title-medium` · `title-small` ·
`body-large` · `body-medium` · `body-small` ·
`label-large` · `label-medium` · `label-small`

Screen title = `title-large` (or `headline-small` for a landing screen). Body
copy = `body-medium`. All `MD-Button` / `MD-NavigationBar` labels = `label-large`.

### 3.3 Shape — `md.sys.shape.corner.*`

`none` · `extra-small` (4dp) · `small` (8dp) · `medium` (12dp) ·
`large` (16dp) · `extra-large` (28dp) · `full`

`MD-Card` = `medium`. `MD-Button` / `MD-Chip` = `full`. `MD-BottomSheet` /
`MD-Dialog` top corners = `extra-large`. `MD-TextField` filled = `extra-small`.

### 3.4 Elevation — `md.sys.elevation.*`

`level0` (0dp) · `level1` (1dp) · `level2` (3dp) · `level3` (6dp) ·
`level4` (8dp) · `level5` (12dp)

Resting `MD-Card` elevated = `level1`. `MD-TopAppBar` on scroll = `level2`.
`MD-FAB` = `level3`. `MD-Menu` / `MD-Dialog` = `level3`. Prefer a
`surface-container*` tonal step over elevation where either would read.

### 3.5 Spacing — 4dp base grid

`4dp` · `8dp` · `12dp` · `16dp` · `24dp` · `32dp` · `48dp` · `64dp`.
Screen edge margin = `16dp`. Between related items = `8dp`. Between groups =
`24dp`. Nothing off the grid — if a gap "needs" 18dp, it needs 16 or 24.
Units: `dp` for layout, `sp` for type. Never `px`.

---

## 4. Layout — Material window size classes

| Class | Width | Layout | Primary nav |
|---|---|---|---|
| `compact` | < 600dp | single column, `16dp` edge margin | `MD-NavigationBar` (bottom) |
| `medium` | 600–839dp | single column or list-detail, wider margins | `MD-NavigationRail` |
| `expanded` | ≥ 840dp | list-detail / supporting pane | `MD-NavigationRail` or standard `MD-NavigationDrawer` |

Mobile-first: **the default `window_size_class` is `compact`**. State the class
on every screen. A screen that only reflows (no structural change) still
declares `compact`.

---

## 5. Voice

`MD-Button` and `cta_primary` labels are **sentence case, verb-first, ≤ 3
words** — "Add to cart", "Save", "Track order". Not ALL CAPS, no trailing
period, no "Click here". Error copy: what happened, then what to do, no apology.
Empty states: state the condition, offer exactly one action. Snackbars: ≤ 1
line, at most one action.

---

## 6. What a compliant screen spec looks like

```json
{
  "screen_name": "Order Tracking",
  "purpose": "Show the shopper where their in-flight order is right now.",
  "components": ["MD-TopAppBar", "MD-Card", "MD-List", "MD-Button", "MD-NavigationBar"],
  "window_size_class": "compact",
  "layout": "compact <600dp → 1-col, 16dp edge margin, bottom MD-NavigationBar; medium → MD-NavigationRail; expanded → list-detail",
  "hierarchy": [
    "MD-TopAppBar small — md.sys.color.surface, leading back arrow, title md.sys.typescale.title-large, respects the 24dp / 44pt status inset",
    "MD-Card elevated — md.sys.elevation.level1, md.sys.shape.corner.medium, current status + ETA, 16dp below the app bar",
    "MD-List two-line — stop-by-stop history, md.sys.color.on-surface-variant timestamps, inset MD-Divider between rows",
    "MD-Button filled — md.sys.color.primary, label-large, 24dp above the nav bar, clears the 48dp / 34pt bottom inset",
    "MD-NavigationBar — 4 destinations, Orders active"
  ],
  "states": {
    "empty": "No active order — a single MD-Button 'Start an order' centered on md.sys.color.surface.",
    "loading": "MD-ProgressIndicator circular indeterminate, centered.",
    "error": "MD-Snackbar with action 'Retry'; last known status stays visible."
  },
  "microcopy": {"cta_primary": "Track order"},
  "requirements": {
    "data": ["order id", "line items", "current fulfilment status", "ETA window", "courier stop history"],
    "interactions": ["pull-to-refresh", "tap a history row to expand", "tap the CTA to open the live map"],
    "data_dependencies": ["GET /orders/{id}", "GET /orders/{id}/tracking (polled ~30s)"],
    "permissions": [],
    "edge_cases": ["order already delivered", "tracking not yet available", "offline — show last cached status", "ETA slips past the window"],
    "open_questions": ["do we surface courier name / photo at this stage?"]
  }
}
```

Note what is absent: no hex, no `px`, no component outside the set, no invented
pattern. That is what passing looks like.

---

## 7. Declaring a gap

When a real need has no component, do not stretch one and do not invent one:

```json
{"need": "Persistent labelled checkout progress across 3 screens",
 "nearest_component": "MD-ProgressIndicator",
 "why_insufficient": "Linear determinate shows a ratio, not named steps or back-navigation between them; a stepper component is required."}
```

A named gap is a design finding. A quietly invented component is technical debt
that reaches production.
