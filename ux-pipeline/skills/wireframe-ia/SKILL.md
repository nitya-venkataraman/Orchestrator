---
name: wireframe-ia
description: Use this skill to generate sitemaps, information architecture, and text-based wireframe specs for the selected UX concept, strictly conforming to the Superlap brutalist design system. Triggered as Node 4 of the UX pipeline.
---

# Wireframing & Information Architecture

## Steps
1. Read `selected_concept` (human-approved from Node 3).
2. Load `references/superlap-design-tokens.json` and `assets/component-patterns.md` — ALL layout, color, and typography decisions must map to these tokens. Never invent new hex values, font sizes, or radii.
3. Generate a hierarchical sitemap.
4. Write text-based wireframe specs per screen: hero/marquee treatment, grid structure (3-col → 2-col → 1-col collapse), card components (use Poster Event Card pattern), CTA style (text-as-button, no filled buttons), spacing (4px-based scale), and border/radius rules (0px sharp edges except drawers/badges).

## Output contract
Return `sitemap`, `wireframe_specs`, and set `design_tokens_applied = true`. If a layout need falls outside the existing token set, flag it as an explicit "Design System Gap" rather than inventing a value.
