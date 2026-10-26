# Run Summary — NexusIntel

**Run date:** 2026-09-10 · **Project slug:** `nexusintel` · **Source:** Product Brief — NexusIntel (AI-Driven Cross-Asset Sourcing & Portfolio Analytics)

Six stages, all approved. Brought to contract 2.0 on 2026-09-10: quote sources de-identified to participant IDs, a corpus block added, success metrics and analytics events threaded through, accessibility carried into acceptance criteria, a ten-heuristic review run against the design (six findings, all fixed in the spec), and a Stage-6 evaluation plan added. This run replaced an earlier partial `nexusintel` run whose Stage 1–2 artifacts were built from a single-interview corpus and stated that no associate had been interviewed — no longer true once P01 and P02 were added.

---

## Artifacts

| Stage | Artifact | Score | Revisions |
|---|---|---|---|
| 1 · Discovery synthesis | [discovery-synthesis.json](discovery-synthesis.json) · [.md](discovery-synthesis.md) | 0.88 / 0.75 | 0 |
| 2 · Strategy definition | [strategy.json](strategy.json) · [.md](strategy.md) | 0.88 / 0.75 | 0 |
| 3 · Ideation & concepting | [ideation.json](ideation.json) · [.md](ideation.md) | 0.87 / 0.70 | 0 |
| 4 · Wireframes & IA | [wireframe.json](wireframe.json) · [.md](wireframe.md) | 0.89 / 0.80 | 1 (iOS family cut) |
| 5 · Delivery handoff | [delivery.json](delivery.json) · [.md](delivery.md) | 4.7 / 5 | 0 |

**Figma:** https://www.figma.com/design/V091wDoNmDuw3J0N9P4Y5K — 8 frames at 1440x1024, 42 token variables, 2 component sets with 5 variants each, 11 prototype connections wired from `01 - Screening Queue`.

**Review board:** https://miro.com/app/board/uXjVHoJ6JQk=/ — Miro, 9 frames, all six stages plus a current/future user-journey flow diagram and a decisions-and-risks agenda. Generated 2026-09-11.

---

## Human decisions

| Decision | Choice |
|---|---|
| Stage 2 persona count | **3 personas**, waiving the contract's exactly-2 rule. All three users were interviewed directly; dropping one would have discarded first-hand evidence. `validators/strategy.py` was **not** modified — the two errors are recorded as an override in `workspace/run.json`. |
| Design direction | **A + B + C composite** — The Verifiable Profile, The Firm's Memory, The Standing Watch. Covers all 5 HMWs and all 11 features. |
| Target surface | Chosen as **web + iOS**, then revised to **web only** after Stage 4 gated. |
| Design system | None supplied → documented **Material 3 baseline**, recorded in `assumptions`. |

---

## What the run produced

- **6 evidence-backed themes** from 3 interviews, 18 verbatim-verified quotes, 8 declared gaps
- **3 personas**, a 7-stage current-state journey with 5 consecutive high-drop-off stages, **5 HMWs**
- **11 RICE-scored features** and 3 design directions
- **8 page specs** with full state, responsive and WCAG AA accessibility coverage; 11 prototype flows
- **17 developer-ready user stories** with Given/When/Then, plus microcopy for every screen

---

## Findings the owners need

These are the things that get lost inside the JSON. They are not blockers on the artifacts; they are decisions someone has to make before this gets built.

### For the product owner

1. **Predictive deal sourcing has no user evidence.** All three participants described building or reviewing a profile for a target already on the desk. The brief's headline claim — identifying targets before they launch formal auction processes — is unsupported by this corpus and was not carried into any stage.
2. **The 1.5σ threshold and the Credit Health Score are PRD constructs no user reacted to.** No participant was asked what false-positive rate they would tolerate, and the credibility of the entire monitoring surface rests on that number.
3. **Reach figures in the RICE backlog are invented.** No participant gave a volume. The ordering that puts pre-close features above monitoring features follows from placeholders (120 profile builds/quarter, 40 monitored positions), and moves if the real ratio differs. This held `rice_integrity` to 0.72 — the lowest dimension in the run.
4. **The Managing Director's away-from-desk case is now unaddressed by design.** The iOS family was cut deliberately, not overlooked. If research establishes that need, it should re-enter at the direction fork rather than be retrofitted.
5. **No compliance, IT or security stakeholder was interviewed.** The single-tenant VPC and the RBAC wall between Private Equity and Liquid Strategies are asserted requirements. The RBAC wall is load-bearing in `02 - Precedent Search`, where getting it wrong is an insider-trading problem rather than a defect.

### For the design system owner

Five needs the base-role taxonomy cannot express, each with its nearest role and why that role falls short. Two are load-bearing across six pages:

| Need | Nearest role | Why it fails |
|---|---|---|
| A control that renders a source excerpt with its citing sentence highlighted, its document, page and clause re… | `Popover` | A Popover carries free text anchored to a trigger. This control has a compound structured payload and two states a Popover does not model — source still resolving, and source could… |
| A meter expressing signed distance to a fixed threshold that can be approached from either side and crossed | `ProgressIndicator` | A ProgressIndicator models monotonic progress toward completion, where the end of the track is the goal. Covenant headroom has a fixed marker mid-track that represents failure rath… |
| A flag that carries an assertion requiring adjudication, holding its evidence and recording an accept or dismi… | `Badge` | A Badge is a static status label with no interaction contract. This carries evidence, an adjudication decision, the deciding user and a reason, all of which become part of the prof… |
| A two-column reconciliation row pairing an extracted value with its source excerpt, an editable override and a… | `List` | A List item renders content in one direction. This is a reconciliation control between what was extracted and what will be committed, holding two competing values at once with an a… |
| An accessible text-equivalent structure for the corporate-structure canvas and the relationship map | `Chart` | The baseline offers no pattern for a graph that must be equally navigable as a keyboard tree and as a screen-reader outline. Both views are specified here per page, but the pattern… |

Also: **Material 3 is a poor fit for this product.** Its default density is looser than these screens want, and an institutional credit tool needs a stronger data-table and financial-numeral treatment. The baseline was used because nothing else was supplied.

---

## Verification

```bash
python3 ux-pipeline/rubrics.py --check
```

All five stage validators were run with their upstream artifact supplied as context, not just the bare CLI:

| Stage | Validator | Context passed | Errors |
|---|---|---|---|
| 1 | `synthesis.py` | `raw_research_data` | 0 |
| 2 | `strategy.py` | `synthesized_insights` | 2 — both the authorized persona-count override |
| 3 | `ideation.py` | `problem_statement` | 0 |
| 4 | `wireframe.py` | `feature_matrix` | 0 |
| 5 | `delivery.py` | `persona_profile` + `wireframe_specs` | 0 |
