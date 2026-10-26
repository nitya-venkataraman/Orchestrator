# Evaluation Plan — NexusIntel

**Stage 6 of 6** · **7 tasks** · **9 participants** across 3 segments · **11 metrics planned**, 7 with an open baseline

Stages 1–5 make claims; this stage plans how they get checked. Every task names a Stage-2 journey stage and Stage-4 pages, every metric traces to a Stage-3 `success_metric`, and every unknown baseline is declared rather than estimated.

---

## Objective

Decide whether the extract-verify-review chain can be trusted end to end before build: whether an associate will commit machine-extracted terms without re-keying them, and whether a reviewer will accept a figure on provenance alone rather than reopening the agreement. If either answer is no, the time savings the business case rests on do not exist, whatever the rest of the design does.

### What would change the design

If associates in T2 re-key rather than commit, extraction confidence is not doing its job and the reconciliation UI on 03 is rebuilt before build starts — the feature's whole premise fails, not a detail of it. If reviewers in T4 reopen the agreement instead of using provenance, the click-to-source treatment on 04/06 is redesigned and the review-time target is withdrawn from the business case rather than quietly missed. If two or more participants in T5 confirm sign-off without reading the dialog, the 10-minute reversal window becomes the primary safeguard and the dialog is demoted, because a confirmation people click through is decoration. If T7 participants act on stale scores believing them current, the staleness treatment on 07 is escalated from a banner to a blocking state.

---

## Participants

**9 participants**, moderated study.

| Segment | Stage-2 persona |
|---|---|
| The Screening Associate | ✓ |
| The Credit Risk Reviewer | ✓ |
| The Managing Director | ✓ |

**Recruiting.** Four associates and three reviewers from mid-market credit desks who build profiles by hand today, plus two MDs with booked-portfolio responsibility. Recruited through the two desks that took part in discovery, excluding the eleven already interviewed so the design is not tested on the people who described the problem.

---

## Tasks

### T1 — Assignment and orientation (Associate)

> You've picked up a new borrower this morning and the credit committee meets Thursday. Get as far as you can toward being ready.

**Success:** Participant establishes what the firm already knows about the entity before starting original work, unaided, and can say afterwards what the blocking input was without being prompted.

**Pages:** `01 - Screening Queue`, `02 - Precedent Search`
  
**Probes:** Match between system and the real world; Recognition rather than recall

### T2 — Extracting terms from source documents (Associate)

> Here is the credit agreement for that borrower. You need the covenant package and the leverage definitions in a state you'd be willing to put your name to.

**Success:** Participant commits terms rather than re-keying them, and when asked which figures they checked individually, names the low-confidence ones rather than 'all of them' or 'none'. Time to commit recorded against the four-to-five-hour baseline.

**Pages:** `03 - Document Extraction`
  
**Probes:** Flexibility and efficiency of use; Error prevention

### T3 — Extracting terms from source documents (Associate)

> Two of the documents in that set define EBITDA differently. Get the profile to a state you'd submit.

**Success:** Participant notices the conflict without being told it exists, and resolves it deliberately rather than by accepting whichever value the interface offered first.

**Pages:** `03 - Document Extraction`, `04 - Borrower Profile`
  
**Probes:** Error prevention; Help and documentation

### T4 — Risk review and verification (Credit Risk Reviewer)

> You're reviewing this profile. Decide whether you'd sign it off.

**Success:** Participant verifies at least three figures via provenance rather than opening the source agreement, and reaches a sign-off decision inside ten minutes against the twenty-to-thirty-minute baseline.

**Pages:** `06 - Risk Review`, `04 - Borrower Profile`, `05 - Corporate Structure`
  
**Probes:** Recognition rather than recall; Visibility of system status

### T5 — Risk review and verification (Credit Risk Reviewer)

> Sign this profile off. Then: you've realised you signed the wrong one.

**Success:** Participant recovers without assistance and without contacting an administrator. Whether they noticed the confirmation before confirming is recorded separately — a confirmation people click through is not a safeguard.

**Pages:** `06 - Risk Review`
  
**Probes:** User control and freedom

### T6 — Defect return and rework loop (Reviewer and Associate)

> A figure on this review can't be traced to a source clause. Do what you'd normally do.

**Success:** Participant returns the defect against the specific figure rather than as a general comment, and does not attempt to sign off around it.

**Pages:** `06 - Risk Review`, `04 - Borrower Profile`
  
**Probes:** Help users recognize, diagnose and recover from errors

### T7 — Post-close portfolio monitoring (Managing Director)

> It's Monday morning and you have twenty minutes before your first meeting. Tell me what in the portfolio needs you this week.

**Success:** Participant acts on or dismisses each attention item from the feed entry alone, and correctly states whether the scores they acted on were current — the stale-score case is included in the fixture data.

**Pages:** `07 - Portfolio Watch`, `08 - Position Detail`
  
**Probes:** Consistency and standards; Visibility of system status

---

## Metric plan

| Metric | Feature | Events | Readable after |
|---|---|---|---|
| Hours from receiving the agreement set to a committed term sheet | Credit Agreement Term Extraction | `extraction_terms_committed` | 20 committed agreements, roughly six weeks at current deal flow |
| Hours to a verified corporate structure and guarantee package | Auto-Built Org and Guarantee Chart | `structure_derived` | 20 derived structures; manual_edits per structure is the honest read, not derivation count |
| Minutes per risk review spent reopening source documents to verify a figure | Click-to-Source Provenance | `figure_provenance_opened`, `review_first_read_opened` | 30 completed reviews, roughly one quarter |
| Lead time between a deterioration signal and it reaching the MD | Continuous Position Health Score | _not event-derived_ | Two quarters — the baseline is a three-month lag, so a shorter window cannot show movement |
| Share of profile model fields re-keyed by hand from a PDF | Model Template Auto-Population | `profile_model_populated` | 20 populated profiles |
| Share of questionable add-backs raised at review rather than after close | Add-Back and Pro-Forma Challenge Flags | `addback_challenge_raised` | One quarter, and only alongside the post-close review that supplies the denominator |
| Round trips to close a returned defect | In-Profile Review Threads | `review_defect_raised`, `signoff_blocked_unverifiable` | 20 defect threads |
| Share of targets where prior firm contact is surfaced before manual hunting begins | Entity Precedent Timeline | _not event-derived_ | Not readable until that event exists — tracked in open_baselines rather than assumed |
| Share of firm precedent reachable by search rather than by asking a colleague | Inbox and Drive Ingestion | _not event-derived_ | First full index pass, then monthly |
| Deal-clock days lost waiting on an unowned outstanding request | Outstanding-Input Tracker | _not event-derived_ | One quarter of tracked requests |
| Share of alerts acted on without opening another system to decide | Decision-Carrying Alert Feed | _not event-derived_ | Not readable until those events exist |

### Baseline sources

- **Hours from receiving the agreement set to a committed term sheet** — Stage-2 journey stage 3 — four to five hours of day one, from associate interviews
- **Hours to a verified corporate structure and guarantee package** — Stage-2 journey stage 3 — the same four-to-five-hour figure, which is org-chart time specifically
- **Minutes per risk review spent reopening source documents to verify a figure** — Stage-2 journey stage 5 — twenty to thirty minutes per review, from the reviewer interview
- **Lead time between a deterioration signal and it reaching the MD** — Stage-2 journey stage 7 — signals surfacing roughly three months late, from the MD interview. Read from the scoring pipeline's own signal-to-surface log, not from a UI event: the metric is about when the system knew, not when someone looked.
- **Share of profile model fields re-keyed by hand from a PDF** — unknown — no current system records how much of a model is re-keyed; the fields_rekeyed_by_hand property establishes it from first use
- **Share of questionable add-backs raised at review rather than after close** — unknown — today these are caught inconsistently and nothing records the misses; needs a retrospective read of post-close findings to establish
- **Round trips to close a returned defect** — unknown — the current loop runs over email and is not countable; first 20 threads establish it
- **Share of targets where prior firm contact is surfaced before manual hunting begins** — unknown. Not instrumented at launch: the metric needs an event on 02 that Stage 5 did not specify, because 02 is a read page and the instrumentation rule only floors write pages. Add precedent_surfaced before build.
- **Share of firm precedent reachable by search rather than by asking a colleague** — Index coverage report from the ingestion service — a backend figure, not a UI event; the denominator is the store inventory taken during discovery
- **Deal-clock days lost waiting on an unowned outstanding request** — unknown — deal-clock days lost to unowned requests is not recorded anywhere today; the tracker's own ageing report establishes it from first use
- **Share of alerts acted on without opening another system to decide** — unknown. Same gap as the precedent timeline: 07 and 08 are read-and-acknowledge pages, so Stage 5 specified no events for them. Acknowledge and escalate both need instrumenting before this is readable.

---

## Open baselines

Not knowing a baseline is allowed. Losing track of which ones are unknown is not.

- Share of targets where prior firm contact is surfaced before manual hunting begins — needs a precedent_surfaced event on 02, absent from Stage 5. Owner: the delivery stage, before build.
- Share of firm precedent reachable by search rather than by asking a colleague — needs the store inventory from discovery turned into a denominator. Owner: platform, at first index pass.
- Share of profile model fields re-keyed by hand from a PDF — establishes itself from the fields_rekeyed_by_hand property on first use; no retrospective read possible.
- Share of questionable add-backs raised at review rather than after close — needs a retrospective read of post-close findings to supply the denominator. Owner: credit risk, one quarter.
- Deal-clock days lost waiting on an unowned outstanding request — not recorded anywhere today; the tracker establishes its own baseline from first use.
- Round trips to close a returned defect — the current email loop is not countable; first 20 threads establish it.
- Share of alerts acted on without opening another system to decide — needs acknowledge and escalate events on 07/08, absent from Stage 5. Owner: the delivery stage, before build.
