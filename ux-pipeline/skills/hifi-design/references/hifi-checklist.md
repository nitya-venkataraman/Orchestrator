# Hi-fi checklist

Run this before returning. Every line is either met or a logged `design_system_gaps`
entry; none is "close enough".

## Fidelity to the wireframe
- [ ] One hi-fi frame for every wireframe frame, including its state frames and its
      breakpoint variants. Nothing dropped, nothing added.
- [ ] Information architecture and content order match the wireframe, top to bottom.
- [ ] Copy is the wireframe's (or the page spec's) copy — not rewritten, not lorem ipsum.
- [ ] The wireframe page is untouched.

## Design-system use
- [ ] 100% of components are instances of design-system components, at the right variant.
      No detached instances, no look-alike frames.
- [ ] 100% of colour, type, space and radius values are bound to design-system variables
      or text styles. No raw hex, no `rgb()`, no ad-hoc pixel value.
- [ ] Anything the system cannot express is in `design_system_gaps` with the screen, the
      need, and why no existing component or variable covers it.
- [ ] Nothing was drawn from `superlap-design-tokens.json` or a remembered "usual" system.

## States and breakpoints
- [ ] default, loading, empty and error exist for every page; success and disabled where
      the page writes data or disables a control.
- [ ] Every breakpoint the wireframe carries is present, recomposed rather than scaled.

## Accessibility
- [ ] Text and meaningful non-text contrast meets WCAG AA (4.5:1 body, 3:1 large text and
      UI components), computed from the system's own tokens.
- [ ] Touch and click targets meet the system's minimum.
- [ ] State is never carried by colour alone.
- [ ] Text does not overflow or clip at the longest realistic string, or at the narrowest
      breakpoint.

## Naming and hygiene
- [ ] Frames are named as the wireframe names them; state frames append ` / <state>`.
- [ ] Layers are named, not `Frame 123`. Auto Layout throughout.
- [ ] Every frame has its node id recorded in `hifi_screens`.
