# Hi-Fi Self-Check

Run against every hi-fi frame before returning. Fix failures; anything that can't be fixed
inside the design system goes into `design_system_gaps`.

## Fidelity to the wireframe
- [ ] Every wireframe frame has a hi-fi counterpart (`wireframe_node_id` recorded).
- [ ] Sections, content order, and hierarchy match the wireframe — nothing dropped or added.
- [ ] Real copy from the wireframe/specs is kept; no lorem ipsum unless the wireframe had it.

## Design-system conformance
- [ ] Every UI element is an instance of a DS component (no detached instances, no
      hand-drawn look-alikes).
- [ ] Every fill, stroke, text style, spacing, radius, and effect is bound to a DS variable
      or style — zero raw hex values or unbound numbers.
- [ ] Component variants (size, state, emphasis) chosen from the DS, not overridden by hand.

## Layout
- [ ] Auto layout on frames and stacks; nothing positioned absolutely without reason.
- [ ] One frame per breakpoint present in the wireframe; reflow matches the wireframe intent.
- [ ] No text overflow or clipping at any breakpoint.

## States
- [ ] Default, empty, loading, error, and success states exist wherever the wireframe or
      `wireframe_specs` implies them.
- [ ] Interactive components show hover/focus/disabled where the DS provides those variants.

## Accessibility (WCAG AA)
- [ ] Text contrast ≥ 4.5:1 (≥ 3:1 for large text and UI component boundaries).
- [ ] Visible focus indicator on interactive elements.
- [ ] Touch targets ≥ 44×44 on mobile breakpoints.
- [ ] Meaning is not conveyed by color alone.

## Housekeeping
- [ ] Frames named `<Screen> / <Breakpoint> / <State>`; layers named meaningfully.
- [ ] Wireframe page untouched.
