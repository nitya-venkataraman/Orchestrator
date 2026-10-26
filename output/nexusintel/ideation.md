# Ideation & Concepting — NexusIntel

**Stage 3 of 6** · 11 RICE-scored features and 3 design directions. Every feature's `hmw` is an exact match to a Stage-2 statement; every RICE score recomputed by the validator.

> **Reach is an assumption, not a measurement.** Stage 1 recorded that no participant gave a volume figure. `reach: 120` stands for profile builds per quarter across the screening team and `reach: 40` for booked positions under monitoring. Both are placeholders. They set the *ordering* of this backlog, so if the real ratio between screening volume and portfolio size differs materially, the ranking moves. `confidence` is set from evidence strength: 1.0 where two participants specified the behaviour, 0.5 where the need came from the PRD rather than a user.

---

## Feature backlog — RICE ranked

| Rank | Feature | R | I | C | E | RICE | Addresses |
|---|---|---|---|---|---|---|---|
| 1 | **Click-to-Source Provenance** | 120 | 3 | 1.0 | 3 | **120.0** | HMW3 · One error voids the profile |
| 2 | **Outstanding-Input Tracker** | 120 | 2 | 0.8 | 3 | **64.0** | HMW4 · Email round-trips burn the deadline |
| 3 | **In-Profile Review Threads** | 120 | 1 | 1.0 | 2 | **60.0** | HMW4 · Email round-trips burn the deadline |
| 4 | **Entity Precedent Timeline** | 120 | 3 | 0.8 | 5 | **57.6** | HMW1 · Firm memory hunted manually |
| 5 | **Model Template Auto-Population** | 120 | 2 | 0.8 | 5 | **38.4** | HMW2 · Deal terms trapped in documents |
| 6 | **Add-Back and Pro-Forma Challenge Flags** | 120 | 2 | 0.8 | 5 | **38.4** | HMW3 · One error voids the profile |
| 7 | **Credit Agreement Term Extraction** | 120 | 3 | 0.8 | 8 | **36.0** | HMW2 · Deal terms trapped in documents |
| 8 | **Decision-Carrying Alert Feed** | 40 | 3 | 0.8 | 5 | **19.2** | HMW5 · Late, undifferentiated risk signals |
| 9 | **Inbox and Drive Ingestion** | 120 | 2 | 0.5 | 8 | **15.0** | HMW1 · Firm memory hunted manually |
| 10 | **Auto-Built Org and Guarantee Chart** | 120 | 2 | 0.5 | 8 | **15.0** | HMW2 · Deal terms trapped in documents |
| 11 | **Continuous Position Health Score** | 40 | 3 | 0.5 | 13 | **4.6** | HMW5 · Late, undifferentiated risk signals |

### Detail

**Click-to-Source Provenance** · RICE 120.0

Every figure in the profile links to the exact sentence in the document it came from, shown in place without leaving the profile or opening the underlying agreement.

*Addresses:* How might we let a reviewer satisfy themselves that a figure is right without leaving the profile they are reading?

**Outstanding-Input Tracker** · RICE 64.0

The profile itself declares what it is waiting on, who owns the request, when it was made and how long it has been outstanding, so a blocked dependency is visible to everyone on the deal rather than sitting in one associate's inbox.

*Addresses:* How might we keep the deal clock from being held hostage to a reply that has not arrived?

**In-Profile Review Threads** · RICE 60.0

A reviewer returns a defect on the line item it concerns and the associate answers it there, so a correction never becomes a round of email and a minor fix is never absorbed silently to avoid one.

*Addresses:* How might we keep the deal clock from being held hostage to a reply that has not arrived?

**Entity Precedent Timeline** · RICE 57.6

Searching a target name returns a chronological record of every prior touch the firm has had with that entity, its sponsors and its subsidiaries — which desk, which people, which meetings, which IC memos, which prior agreements — before any build work starts.

*Addresses:* How might we make a firm's own prior contact with a target visible at the moment someone starts evaluating it, including the contact nobody remembers?

**Model Template Auto-Population** · RICE 38.4

Extracted figures populate the profile model directly, so financials are never re-keyed from a PDF and the template's formulas are never manually repaired.

*Addresses:* How might we shorten the distance between a term written into a credit agreement and a number an analyst can act on?

**Add-Back and Pro-Forma Challenge Flags** · RICE 38.4

Flags adjustments that warrant a question rather than acceptance: an EBITDA add-back described as one-time that recurs across periods, or a vendor pull not adjusted for a recent acquisition.

*Addresses:* How might we let a reviewer satisfy themselves that a figure is right without leaving the profile they are reading?

**Credit Agreement Term Extraction** · RICE 36.0

Reads a credit agreement end to end and returns the figures that decide the credit: covenant definitions and thresholds, leverage ratios, the definition of EBITDA in this document, and the amortization schedule.

*Addresses:* How might we shorten the distance between a term written into a credit agreement and a number an analyst can act on?

**Decision-Carrying Alert Feed** · RICE 19.2

A ranked feed where each entry carries the three things needed to act: what changed, the firm's direct exposure, and the current distance to the covenant threshold.

*Addresses:* How might we make a portfolio signal arrive early enough, and specific enough, to change what a Managing Director does that day?

**Inbox and Drive Ingestion** · RICE 15.0

Indexes the places firm memory actually lives — Outlook, SharePoint, shared and local drives, the credit document repository — into the precedent store, with the metadata tagging that keeps Private Equity notes invisible to Liquid Strategies unless permitted.

*Addresses:* How might we make a firm's own prior contact with a target visible at the moment someone starts evaluating it, including the contact nobody remembers?

**Auto-Built Org and Guarantee Chart** · RICE 15.0

Derives the ultimate parent, co-issuers and guarantors from the agreement set and renders the corporate structure, marking which entities are on the hook for the debt and which subsidiaries are unrated or offshore.

*Addresses:* How might we shorten the distance between a term written into a credit agreement and a number an analyst can act on?

**Continuous Position Health Score** · RICE 4.6

Ingests daily alternative signals against each booked position and scores deviation from the sector benchmark, replacing the quarterly spreadsheet cycle with a standing measure.

*Addresses:* How might we make a portfolio signal arrive early enough, and specific enough, to change what a Managing Director does that day?

---

## Design directions

Three genuinely different products, not three feature bundles. They differ in primary user, entry point, and core object — a document, a graph, and a feed. **The pipeline does not pick one; you do.**

### A. The Verifiable Profile

The product is the borrower profile itself, turned from a static deliverable into a live, interrogable document. Extraction fills it, provenance backs every figure, and review happens inside it. The associate stops transcribing and stops formatting for trust; the reviewer stops reopening agreements to check what she is reading.

**Differentiator.** Trust is the feature, not a by-product. Every other approach treats extraction as the goal and leaves the reviewer to believe the output; this one treats the reviewer's five-minute verification as the thing being built, and extraction exists to serve it.

**Tradeoff.** Does nothing for the portfolio after the deal is booked. The Managing Director's three-months-too-late problem is untouched — and he is the one who described a line of users out the door. This direction wins the workflow and leaves the buying signal unaddressed.

*Addresses:* HMW2 · Deal terms trapped in documents, HMW3 · One error voids the profile, HMW4 · Email round-trips burn the deadline

---

### B. The Firm's Memory

The product is the cross-asset knowledge graph. The entry point is a target name and the payload is everything the firm already knows about it, drawn from CRM, repositories, drives and inboxes across every desk. Extraction and provenance are how the graph gets populated and trusted, not ends in themselves.

**Differentiator.** It is the only capability no incumbent has. Per the brief's own competitive read, DealCloud carries the CRM but cannot search unstructured internal content, and Preqin and PitchBook have no internal context at all. This is the one direction a competitor cannot answer by shipping a feature.

**Tradeoff.** Cold start. Value on day one is near zero and grows with corpus coverage and adoption, in a firm that expects immediate leverage — and the associate's 48-72 hour build barely moves until the graph is dense. It also carries the heaviest compliance surface: the RBAC wall between Private Equity and Liquid Strategies is load-bearing here, and getting it wrong is an insider-trading problem, not a bug.

*Addresses:* HMW1 · Firm memory hunted manually, HMW2 · Deal terms trapped in documents

---

### C. The Standing Watch

The product is continuous monitoring of booked positions. The pre-close profile is not the deliverable but the baseline: the covenant thresholds and exposure figures extracted at underwriting become the reference the daily signal is measured against, so screening work is retained rather than filed.

**Differentiator.** It is the only direction that closes the gap between a borrower's condition changing and the firm knowing, and the only one aimed squarely at the persona who controls the budget. It also reframes the profile build as an investment that keeps paying rather than a document that is archived.

**Tradeoff.** It bets on the thinnest evidence in the corpus. Post-close monitoring was raised by one participant of three, while the associate's build and the reviewer's rework — five consecutive high-drop-off journey stages — are largely out of scope. It is also the highest technical risk: the alternative-data signals it depends on were named by the product team, not by any user, and no participant was ever asked what false-positive rate they would tolerate.

*Addresses:* HMW5 · Late, undifferentiated risk signals, HMW3 · One error voids the profile

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/ideation.py` returned 0 errors with Stage 2 as `problem_statement`: 11 features in range, every `hmw` an exact upstream match, every RICE score recomputed within tolerance, 3 directions each carrying a tradeoff.

**Tier 2 — judge: 0.87** (threshold 0.70)

| Criterion | Weight | Score | Note |
|---|---|---|---|
| `hmw_linkage` | 0.30 | 0.95 | Every feature maps to one specific HMW by exact string; all five HMWs carry at least one feature. |
| `rice_integrity` | 0.30 | 0.72 | **Weakest dimension.** The arithmetic is exact but `reach` rests on invented volumes — Stage 1 explicitly recorded that no participant supplied one. Effort is unvalidated by any engineer. The ranking is therefore directionally useful and numerically soft. |
| `direction_distinctness` | 0.40 | 0.92 | The three directions have different primary users, entry points and core objects, and each tradeoff names a cost the direction genuinely cannot avoid. |
