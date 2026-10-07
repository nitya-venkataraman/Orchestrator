---
name: hifi-design
description: Use this skill to turn a Figma wireframe into high-fidelity design screens in Figma, built exclusively from a Figma design system's components, variables, and styles. Takes a Figma wireframe URL and a Figma design system URL as input. Triggered as Node 5 of the UX pipeline (after wireframe-ia, before delivery-handoff), or whenever someone asks to "make this hi-fi", "apply the design system to the wireframe", or "produce visual design screens" from Figma.
---

# High-Fidelity Design (Figma)

Requires the Figma MCP server. The Figma design system is the **only** source of visual
truth for this phase — do not use `superlap-design-tokens.json` or any other local token file.

## Steps
1. Read `figma_wireframe_url` and `figma_design_system_url`, plus `selected_concept`,
   `sitemap`, and `wireframe_specs` for intent, content, and required states. If either URL is
   missing, stop and return an empty `hifi_screens` with a blocking entry in
   `design_system_gaps` — never invent screens, components, or styles.
2. Parse each URL into `fileKey` / `nodeId`:
   - `figma.com/design/:fileKey/:name?node-id=1-2` → nodeId `1:2` (`-` becomes `:`)
   - `figma.com/design/:fileKey/branch/:branchKey/:name` → use `branchKey` as the fileKey
3. **Read the wireframe.** `get_metadata` on the wireframe node to enumerate screen frames
   (name, size, breakpoint, hierarchy), then `get_screenshot` per frame.
4. **Read the design system.** `get_libraries`, `search_design_system`, and `get_variable_defs`
   on the design-system file to collect components and variants, variables
   (color / typography / spacing / radius / effects), and text styles.
5. **Map.** Every wireframe element → a DS component + variant. Every color, type size,
   spacing, radius, and shadow → a DS variable or style. A need with no match is a
   **Design System Gap** — record it; never fill it with a raw hex, ad-hoc size, or a
   detached instance.
6. **Build.** Load the Figma `figma-use` skill (fallback: `skill://figma/figma-use/SKILL.md`)
   before any `use_figma` call. In the wireframe file, create a page named
   `Hi-Fi — <selected_concept name>` and build one hi-fi frame per wireframe frame from DS
   component instances with bound variables and auto layout. Keep the wireframe's
   information architecture and content order. Never modify the wireframe page itself.
7. **States and breakpoints.** Add a frame for each state the wireframe or specs imply
   (default, empty, loading, error, success) and for each breakpoint present in the wireframe.
8. **Self-check.** `get_screenshot` every hi-fi frame and run
   [references/hifi-checklist.md](references/hifi-checklist.md). Fix what fails; record what
   can't be fixed within the design system as a gap.
9. On a revision pass (`feedback_loop` set), update the existing `Hi-Fi — …` page in place
   rather than creating a new one, and address every point in the feedback.

## Output contract
Return:
- `hifi_screens` — list of `{name, wireframe_node_id, figma_node_id, figma_url, breakpoint,
  states, components_used}`, one per hi-fi frame.
- `hifi_figma_page_url` — link to the `Hi-Fi — …` page.
- `design_system_gaps` — list of `{screen, need, reason}`; empty list if none.
