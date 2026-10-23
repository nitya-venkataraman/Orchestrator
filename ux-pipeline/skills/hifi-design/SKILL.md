---
name: hifi-design
description: Use this skill to turn a Figma wireframe and a Figma design system into high-fidelity screens built in Figma — every element mapped to a design-system component or variable, every state and breakpoint the wireframe implies, and a logged gap wherever the system cannot express a need. Triggers on "hi-fi", "high-fidelity", "visual design", "apply the design system to the wireframe", or a pair of Figma URLs. Triggered as Node 5 of the UX pipeline; Node 6 then hands the design off.
allowed-tools: Read, Write, Bash, Skill, mcp__Figma__get_metadata, mcp__Figma__get_screenshot, mcp__Figma__get_design_context, mcp__Figma__get_variable_defs, mcp__Figma__get_libraries, mcp__Figma__search_design_system, mcp__Figma__use_figma
---

# Hi-Fi Design

## Inputs

From state: `figma_wireframe_url` and `figma_design_system_url` (**both required**),
plus `selected_concept`, `sitemap` and `wireframe_specs` for intent and content.
`figma_wireframe_url` falls back to the wireframe stage's `figma_file_url` when the
designer did not supply one. The Figma design system is the **only** source of truth
for look and feel — this skill does not read `superlap-design-tokens.json` or the
Material baseline that `wireframe-ia` falls back to.

## Steps

1. Read the inputs. If either URL is missing, stop: return `hifi_blocking_gaps` naming
   the missing URL, an empty `hifi_screens`, and `hifi_figma_page_url = null`. Do not
   invent screens, and do not substitute another design system or the baseline.
2. Parse each URL to `fileKey` / `nodeId`. In a node id, `-` becomes `:`; a branch URL
   (`/branch/<branchKey>/`) uses the `branchKey` as the file key.
3. **Read the wireframe.** `get_metadata` to enumerate the screen frames (the page
   frames, their state frames and their breakpoint variants), then `get_screenshot`
   for each one. Record each frame's node id — it becomes `wireframe_node_id`.
4. **Read the design system.** `get_libraries`, `search_design_system` and
   `get_variable_defs` to collect its components and variants, its variables (colour,
   type, space, radius) and its text styles.
5. **Map.** Each wireframe element → a design-system component and variant; each
   colour, size and space → a design-system variable or style. A need the system
   cannot express is a `design_system_gaps` entry `{screen, need, reason}` — never a
   raw hex, never an ad-hoc value, never a detached instance. Reuse before you
   create; nothing is drawn from scratch to look like a component.
6. **Build.** Load the Figma `figma-use` skill (fallback
   `skill://figma/figma-use/SKILL.md`) — mandatory before `use_figma`. Create a page
   `Hi-Fi — <selected_concept>` in the wireframe file and build one frame per
   wireframe frame from design-system instances with variables bound. **Never edit the
   wireframe page itself**; the wireframe stays the approved reference.
7. **States and breakpoints.** Cover every state the wireframe or the page spec
   implies (default, empty, loading, error, success, disabled) and every breakpoint
   the wireframe carries. Recompose per breakpoint — do not scale one frame.
8. **Self-check.** Load `references/hifi-checklist.md`. `get_screenshot` each hi-fi
   frame and compare it against its wireframe — information architecture, content
   order, nothing dropped — and against WCAG AA contrast using the system's own
   tokens. Fix what fails, or record it as a gap. Then run
   `python3 ux-pipeline/validators/hifi.py <your .json>` and fix every violation.

## Output contract

Conform to **`../../../rules/CONTRACTS.md` § Stage 4b — hifi-design** for the JSON
shape and the Tier-1 rules. Tier-2 scores it 1–5 per dimension against
[`../../../rules/rubrics/hifi-design.md`](../../../rules/rubrics/hifi-design.md).

1. Return to state: `hifi_screens` (a list of `{name, wireframe_node_id,
   figma_node_id, figma_url, breakpoint, states, components_used}`),
   `hifi_figma_page_url`, `hifi_blocking_gaps` (empty unless step 1 stopped), and
   `hifi_design_system_gaps` (a list of `{screen, need,
   reason}`; named apart from the wireframe stage's own `design_system_gaps`, which
   this stage must not overwrite). All JSON-serialisable.
2. Persist `output/<project-slug>/hifi.json` — the artifact in the shape CONTRACTS.md
   gives, with the gaps under `design_system_gaps` — and `output/<project-slug>/hifi.md`:
   header (concept, the wireframe and design-system URLs, `Figma: <hifi_figma_page_url>`,
   validator result), a table of screens (name, breakpoint, states, link), components
   used, and Design System Gaps. Reuse the run's `<project-slug>` folder; overwrite on
   re-run.
3. The Markdown is the surface shown at the HITL gate — not the JSON.
