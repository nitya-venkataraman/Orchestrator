# Rubric — Stage 4b: hifi-design

Scores a hi-fi artifact (`hifi_screens` + `hifi_figma_page_url` + `design_system_gaps`).
Read [`README.md`](README.md) first. Tier-1 (`ux-pipeline/validators/hifi.py`) already
checks that both Figma URLs are present, that every screen carries well-formed node ids,
a known breakpoint, known states and ≥ 1 component, that no component entry is a raw
colour, that every gap is complete, and (given the wireframe) that every page has a
screen. This rubric judges whether the screens are *faithful to the wireframe*, whether
the design-system discipline is real rather than merely literal, whether the states and
breakpoints are genuine, and whether they are accessible.

The Figma design system is the only source of truth for look and feel. `pass_when`
(below) requires `ds_fidelity` to be a **5** — a screen that quietly detaches an
instance, hard-codes a value, or restyles a component looks fine in review and becomes a
build problem later — and `accessibility` to be at least a **4**.

## Dimensions

| Key | Weight | What "5" looks like |
|---|---|---|
| `ds_fidelity` | 0.35 | Every component is an instance of a component the supplied system actually contains, at the right variant; every colour, type, space and radius value is bound to its variable or style. Every need the system could not express is a gap with a specific reason — none is papered over with a raw value or a look-alike frame. |
| `wireframe_fidelity` | 0.25 | Every wireframe frame has its hi-fi counterpart; information architecture, content order and copy are the wireframe's. Nothing is dropped, and nothing is added that the wireframe or page spec did not ask for. |
| `state_and_breakpoint_coverage` | 0.20 | Each page's states and each breakpoint the wireframe carries are present as real treatments, recomposed per breakpoint rather than scaled. |
| `accessibility` | 0.20 | Text and UI contrast meets WCAG AA, computed from the system's tokens and cited; targets meet the system's minimum; no state is carried by colour alone; text survives the longest realistic string at the narrowest breakpoint. |

## Score anchors

### `ds_fidelity`
- **5** — A reviewer clicking through the frames finds only intact instances and bound variables; every gap names the screen, the need, and why no existing component or variable covers it.
- **3** — Mostly instances, but one or two frames carry a hard-coded value or a detached component, or a gap's reason is generic ("not in the system").
- **1** — Screens are drawn rather than assembled; the design system is decoration.

### `wireframe_fidelity`
- **5** — Overlaying each hi-fi frame on its wireframe shows the same structure and the same words.
- **3** — Structure holds, but a section is reordered, a state frame is missing, or copy was rewritten.
- **1** — The hi-fi is a different design from the wireframe that was approved.

### `state_and_breakpoint_coverage`
- **5** — default / loading / empty / error (plus success and disabled where the page needs them) exist for every page at every breakpoint the wireframe has, each a deliberate design.
- **3** — Default frames at every breakpoint, but states exist only at desktop, or error states are a banner pasted on the default.
- **1** — Default frames only.

### `accessibility`
- **5** — Contrast ratios are cited from token pairs and meet AA; targets and focus treatments are present; no information rides on colour alone.
- **3** — Contrast is plausibly fine but unchecked, or one state relies on colour alone.
- **1** — Contrast failures visible by eye, or no consideration of accessibility.

## Calibration

`ds_fidelity` is the dimension that slips. It is easy to bind the variables on the hero
screens and quietly hard-code a divider colour or a one-off padding on the utilitarian
ones. Before scoring, sample at least three frames and check their instances and bindings
directly rather than reading `components_used`, which is the artifact's own claim.

A blocked artifact (`blocking_gaps` set, no screens) is not scored — it is shown to the
human so they can supply the missing URL.

## Common failure modes

- A detached instance restyled to match the wireframe.
- A raw hex or an ad-hoc spacing value "just for this frame".
- A gap logged with the reason "not available" and no nearest alternative considered.
- State frames only at desktop; the mobile breakpoint is a scaled copy.
- Copy tidied up in transit, so the hi-fi no longer says what the wireframe said.
- Contrast asserted ("meets AA") with no token pair or ratio behind it.

```json
{
  "stage": "hifi-design",
  "weights": {
    "ds_fidelity": 0.35,
    "wireframe_fidelity": 0.25,
    "state_and_breakpoint_coverage": 0.20,
    "accessibility": 0.20
  },
  "pass_when": "min>=4 and scores['ds_fidelity']>=5"
}
```
