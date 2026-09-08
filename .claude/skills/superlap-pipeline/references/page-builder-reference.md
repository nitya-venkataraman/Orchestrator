# Page Builder Reference

The machine-checked vocabulary and the layout conventions for the Wireframing &
IA stage. `scripts/validate_ds.py` and `ux-pipeline/validators/wireframe.py`
check against this file literally — the base-role taxonomy, the naming patterns,
the breakpoints, and the required state and accessibility keys are all enforced.

This stage is **design-system agnostic**. It does not own a component library.
It reuses whichever design system the project already has, and falls back to a
documented baseline only when none is supplied.

---

## 1. Design system resolution

Before speccing anything, resolve the design system in this order:

1. **A design system supplied in the input** — a component library, a token
   file, a Figma library, a styleguide URL, or existing product code. Use its
   component names, its token names, its naming conventions. This is the
   preferred path.
2. **A design system already linked to the Figma file** — discover it with
   `get_libraries` and `search_design_system`.
3. **No design system available** — pick a documented baseline (Material 3 is
   available as a profile in `material-design-system.md`), say so in
   `assumptions`, and use its token names.

Record the outcome in `design_system`:

```json
{"name": "Acme DS 2.4", "source": "existing",
 "tokens": {"color": ["color.surface.default"], "typography": ["type.heading.lg"],
            "spacing": ["space.400"]}}
```

`source` is `existing` (a real system was supplied or discovered) or `baseline`
(none was available and you chose one). A `baseline` value **must** be paired
with an `assumptions` entry naming the system you chose and why.

**Reuse before you create.** Only create a new component when no existing
component can satisfy the requirement. Every component entry declares
`"source": "reused"` or `"source": "new"`, and every `new` component needs a
one-line justification in `why_new`.

---

## 2. Base component roles (the enforced taxonomy)

A component's `name` is free text — whatever the resolved design system calls
it. Its `base` is the **role** it plays, and must be one of these. The role
taxonomy is fixed so the spec stays checkable across any design system.

**Structure** — `Header`, `Footer`, `Navigation`, `Sidebar`, `Breadcrumb`,
`Tabs`, `Layout`, `Section`, `Divider`

**Content** — `Card`, `List`, `Table`, `Avatar`, `Badge`, `Chip`, `Icon`,
`Link`, `Accordion`, `Carousel`, `Chart`, `Stepper`

**Input** — `Button`, `Input`, `Textarea`, `Select`, `Checkbox`, `Radio`,
`Switch`, `Slider`, `DatePicker`, `TimePicker`, `Search`, `Filter`, `Upload`,
`Form`

**Navigation & overflow** — `Pagination`, `Menu`, `Tooltip`, `Modal`, `Drawer`,
`BottomSheet`, `Popover`, `FAB`

**Feedback** — `Toast`, `Alert`, `Banner`, `Confirmation`, `ProgressIndicator`,
`Skeleton`, `EmptyState`, `LoadingState`, `ErrorState`

If a need maps to no role above, that is a **design-system gap**, not a licence
to invent a role. Emit a `design_system_gaps` entry naming the need, the nearest
role, and why it does not fit.

---

## 3. Naming conventions

Enforced by regex in Tier-1.

**Pages** — `NN - Title` for web, `MNN - Title` for mobile:

```
01 - Login          M01 - Login
02 - Dashboard      M02 - Home
03 - Application Details
```

Numbers are two digits, ordered by the primary journey, and unique within their
family. A `both` target carries both families, and a web page and its mobile
counterpart should share a title where they are the same experience
(`03 - Application Details` / `M03 - Application Details`).

**Components** — `<Layer> / <Name>` where `<Layer>` is `Page`, `Section`, or
`Component`:

```
Page / Dashboard
Section / Summary
Component / KPI Card
Component / Data Table
Component / Primary Button
```

**Variants** — meaningful states only, e.g. a Button as
`Primary | Secondary | Tertiary | Destructive | Disabled | Loading`.

---

## 4. Breakpoints and viewports

### Web

| Breakpoint | Width | Notes |
|---|---|---|
| `desktop` | 1440px | Default design width |
| `laptop` | 1280px | Same structure, tighter gutters |
| `tablet` | 768px | Recomposition starts here |
| `mobile` | 375px | Single column |

Use Auto Layout and responsive constraints. Avoid fixed positioning unless the
element is genuinely pinned (a sticky header, a persistent action bar). Prefer
flexible grids and responsive containers over fixed widths.

### Mobile

| Platform | Reference viewport | Status inset | Bottom inset |
|---|---|---|---|
| `ios` | 390 × 844pt | 47–59pt | 34pt home indicator |
| `android` | 360 × 800dp | 24dp | 48dp gesture nav |

Minimum interactive target is approximately **44 × 44px** (44pt iOS / 48dp
Android). Account for safe areas, bottom navigation, keyboard avoidance,
scrolling, bottom sheets, modals, and gestures where appropriate.

---

## 5. Responsive recomposition

Do not scale the desktop UI down — recompose it. Baseline behaviour to adapt,
not to copy verbatim:

| Component | Desktop | Tablet | Mobile |
|---|---|---|---|
| Navigation | Full navigation | Reduced navigation | Menu |
| Cards | 3-column | 2-column | 1-column |
| Table | Full table | Horizontal scroll | Card / list |
| Form | 2-column | 2-column | 1-column |
| Sidebar | Visible | Collapsed | Drawer |
| Actions | Inline | Inline | Stacked |

Every major component gets a row in `responsive_matrix` stating what it does at
each breakpoint. A row that says "scales down" at every breakpoint is a failure,
not an answer.

---

## 6. Required UI states

Every page declares these four; `success` and `disabled` are required wherever
the page has a write action or a conditionally unavailable control.

| State | What it must say |
|---|---|
| `default` | The normal populated state |
| `loading` | The specific loading or skeleton behaviour — which regions, what shape |
| `empty` | Why there is no data **and** the next action offered |
| `error` | What went wrong in the user's terms **and** how to recover |
| `success` | Confirmation of completion **and** the next relevant action |
| `disabled` | Why the action is unavailable and what would enable it |

"Shows a spinner" is not a loading state. "Handles errors gracefully" is not an
error state. Do not design only the happy path when the requirement implies
other states.

---

## 7. Accessibility (WCAG AA)

Considered during design, not added at the end. Every page carries an
`accessibility` object; these five keys are required and non-empty:

- `contrast` — the contrast decisions, and the token pairs that satisfy AA
  (4.5:1 body text, 3:1 large text and non-text UI).
- `keyboard_focus` — tab order and the visible focus treatment.
- `labels` — visible labels, error identification, and form instructions.
- `touch_targets` — sizes and spacing against the 44×44px minimum.
- `reading_order` — DOM/reading order and heading hierarchy (one `h1`, no
  skipped levels).

Optional: `screen_reader` (roles, landmarks, live regions), `motion`
(reduced-motion behaviour).

**Never rely on colour alone** to convey state, error, or meaning — pair it with
an icon, text, or shape.

---

## 8. Interaction and prototype

Define interactions for navigation, buttons, forms, search, filters, sorting,
pagination, tabs, modals, drawers, confirmation, error recovery, and success
feedback.

`prototype_flows` wires the clickable connections:

```json
{"from": "01 - Login", "trigger": "Tap Sign in", "to": "02 - Dashboard",
 "interaction": "Smart animate, 300ms ease-out"}
```

Tier-1 checks that every `from` and `to` names a real page, and that the whole
primary journey is reachable from the first page — the PDF's "can the user
complete the primary journey?" made mechanical.

---

## 9. Figma implementation

- **Frames** for pages, one per page, named exactly as `page_name`.
- **Auto Layout** everywhere the content flows; responsive constraints on the
  rest.
- **Components** with **variants** for meaningful states.
- **Variables** bound to the resolved design system's tokens — colour,
  typography, spacing — not raw values.
- **Semantic naming** and a clean, consistent layer hierarchy per §3.
- **Prototype connections** for `prototype_flows`.

Colour is always a token. A raw hex or `rgb()` anywhere in the spec is a Tier-1
failure. `px` is allowed — the web breakpoints and touch-target minimums are
expressed in px by definition — but a spacing or type value that had a token
available and used a raw number instead is a Tier-2 markdown.

---

## 10. Voice

Button and CTA labels: sentence case, verb-first, short ("Add to cart", "Save",
"Track order"). No ALL CAPS, no trailing period, no "Click here". Errors say
what happened, then what to do. Empty states state the condition, then offer one
action.
