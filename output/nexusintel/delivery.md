# Delivery Handoff — NexusIntel

**Stage 5 of 6** · **17 stories** across **8 screens** · 3 personas

Every story ties to a Stage-2 persona and a Stage-4 page. Acceptance criteria turn the Stage-4 empty, error and edge-case specs into checkable scenarios rather than restating the happy path.

---

## Coverage

| Screen | Stories | Persona |
|---|---|---|
| 01 - Screening Queue | US-1, US-2 | The Screening Associate |
| 02 - Precedent Search | US-3, US-4 | The Screening Associate |
| 03 - Document Extraction | US-5, US-6 | The Screening Associate |
| 04 - Borrower Profile | US-7, US-8, US-9 | The Screening Associate |
| 05 - Corporate Structure | US-10 | The Credit Risk Reviewer |
| 06 - Risk Review | US-11, US-12, US-13 | The Credit Risk Reviewer |
| 07 - Portfolio Watch | US-14, US-15 | The Managing Director |
| 08 - Position Detail | US-16, US-17 | The Managing Director |

---

## Stories

### 01 - Screening Queue

#### US-1 — see every profile assigned to me ordered by how much of its window is …

**As** The Screening Associate, **I want to** see every profile assigned to me ordered by how much of its window is left, with its blocking reason on the row, **so that** a stalled dependency is visible when I arrive rather than discovered at the deadline.

`screen: 01 - Screening Queue`

| | Given | When | Then |
|---|---|---|---|
| 1 | I have four profiles assigned and one is waiting on a sponsor input | I open the screening queue | the blocked profile shows a blocking chip naming the outstanding input, and the queue is ordered with the tightest remaining window first |
| 2 | a profile's deadline has already passed | I view it in the queue | its clock reads overdue with the elapsed time, and never a negative remaining value |
| 3 | I have no profiles assigned | I open the screening queue | I see an empty state naming what will appear here and offering to start a new profile, visibly different from a filter that matched nothing |

#### US-2 — re-send an outstanding request from the queue without opening the prof…

**As** The Screening Associate, **I want to** re-send an outstanding request from the queue without opening the profile, **so that** chasing a blocked dependency costs one action instead of a context switch.

`screen: 01 - Screening Queue`

| | Given | When | Then |
|---|---|---|---|
| 1 | an input has been outstanding for 26 hours | I chase it from the outstanding-input panel | the request is re-sent, the item is stamped with the new time and moves to awaiting, and I stay on the queue |
| 2 | I re-sent the same request 40 minutes ago | I view that item | the chase control is disabled and states when it was last sent, rather than being silently inert |

### 02 - Precedent Search

#### US-3 — search a target name and see every prior contact this firm has had wit…

**As** The Screening Associate, **I want to** search a target name and see every prior contact this firm has had with it, its sponsors and its subsidiaries, **so that** I stop re-underwriting a company the firm has already met.

`screen: 02 - Precedent Search`

| | Given | When | Then |
|---|---|---|---|
| 1 | the London private equity desk met this borrower's CFO in 2024 | I search the entity name | that meeting appears on the precedent timeline with its desk, date and the debt constraints noted at the time |
| 2 | no repository holds any prior contact | the search completes | I am told plainly that all five repositories were searched, which they were and when each was last indexed, so an absence reads as a finding rather than a failure |
| 3 | the mailbox index has not refreshed for longer than its freshness threshold | I view results | a coverage indicator declares that source stale rather than presenting its results as current |

#### US-4 — see that a precedent record exists on another desk even when I may not…

**As** The Screening Associate, **I want to** see that a precedent record exists on another desk even when I may not read it, **so that** I know the firm holds relevant knowledge and can request it, instead of concluding there is none.

`screen: 02 - Precedent Search`

| | Given | When | Then |
|---|---|---|---|
| 1 | a matching record belongs to a desk walled from mine | I view the precedent timeline | the entry shows its desk and date but never its content, and offers to request access |
| 2 | I request access to a walled record | the request is submitted | it is logged against the owning desk and I see its pending state, and no content is disclosed before it is granted |

### 03 - Document Extraction

#### US-5 — have covenant definitions, leverage ratios, the EBITDA definition and …

**As** The Screening Associate, **I want to** have covenant definitions, leverage ratios, the EBITDA definition and the amortisation schedule extracted from a credit agreement and shown beside the sentence they came from, **so that** I reconcile figures instead of re-typing them, and nothing enters the model unreviewed.

`screen: 03 - Document Extraction`

| | Given | When | Then |
|---|---|---|---|
| 1 | I upload a 300-page credit agreement | extraction runs | terms appear as they are found with per-page progress, rather than a single blocking wait, and each term shows its extraction confidence |
| 2 | I select an extracted term | the source panel updates | it scrolls to and highlights the citing passage, showing the document, page and clause |
| 3 | the agreement is a scanned image with no text layer | extraction completes | I am told that specifically, and offered manual entry with source attachment still available, rather than being shown zero terms |

#### US-6 — be stopped from committing terms while two documents define the same t…

**As** The Screening Associate, **I want to** be stopped from committing terms while two documents define the same term differently, **so that** a conflict is resolved deliberately instead of the first value silently winning.

`screen: 03 - Document Extraction`

| | Given | When | Then |
|---|---|---|---|
| 1 | two uploaded documents state different total leverage covenants | I attempt to commit | commit is disabled and names the number of unresolved conflicts, and each conflict shows both values with their sources |
| 2 | I resolve a conflict by choosing one source | I commit | only accepted rows are written, and each committed figure retains the source offset it came from |

### 04 - Borrower Profile

#### US-7 — have the profile model populated from committed extractions rather tha…

**As** The Screening Associate, **I want to** have the profile model populated from committed extractions rather than re-keyed from PDFs, **so that** I reach the leverage math and the thesis while there is still time to think about them.

`screen: 04 - Borrower Profile`

| | Given | When | Then |
|---|---|---|---|
| 1 | I have committed the extracted terms | I open the borrower profile | the key metrics band and the financial model are populated, and no figure required manual transcription |
| 2 | a vendor feed fails during the build | I view an affected figure | it renders as unavailable with the reason, the last known value and its date, and never as zero or an empty cell |

#### US-8 — be shown a challenge flag when an add-back described as one-time also …

**As** The Screening Associate, **I want to** be shown a challenge flag when an add-back described as one-time also appears in prior periods, **so that** I answer the reviewer's objection before she raises it, instead of anticipating it through formatting.

`screen: 04 - Borrower Profile`

| | Given | When | Then |
|---|---|---|---|
| 1 | a 5.0m consulting fee is added back as one-time and the same fee appears in the two prior years | the profile computes adjusted EBITDA | a challenge flag is raised on that add-back listing the prior occurrences as its evidence |
| 2 | a vendor pull has not been adjusted for an acquisition that closed after the pull date | the profile loads | a challenge flag names the acquisition and its date |
| 3 | the borrower has no prior periods | the profile loads | recurrence detection reports that it could not run, rather than reporting no recurring add-backs |

#### US-9 — open the source of any figure in the profile without leaving the page

**As** The Screening Associate, **I want to** open the source of any figure in the profile without leaving the page, **so that** a number is never something I have to take on trust.

`screen: 04 - Borrower Profile`

| | Given | When | Then |
|---|---|---|---|
| 1 | I select a figure extracted from a document | the provenance popover opens | it shows the citing sentence in its surrounding paragraph with the document, page and clause, and a link that opens the agreement at that position |
| 2 | I select a figure that came from a vendor feed rather than a document | the provenance popover opens | it names the feed and the timestamp of the pull instead of a sentence |
| 3 | a figure's source cannot be resolved | I select it | the popover states that the source could not be located, visibly distinct from a popover that is still loading |

### 05 - Corporate Structure

#### US-10 — see the corporate structure and guarantee package derived from the agr…

**As** The Credit Risk Reviewer, **I want to** see the corporate structure and guarantee package derived from the agreements rather than drawn by hand, **so that** I can establish who is on the hook for the debt in the first minutes of a review.

`screen: 05 - Corporate Structure`

| | Given | When | Then |
|---|---|---|---|
| 1 | the agreement set establishes a parent, an issuer, two co-issuers and a non-guarantor subsidiary | I open corporate structure | each entity shows its role, jurisdiction and guarantee position, with unrated offshore subsidiaries marked by label and shape, not colour alone |
| 2 | one branch cannot be derived from the available documents | I view the structure | that branch is shown explicitly as unverified rather than omitted, and confirm is disabled while it remains so |
| 3 | no structural clauses are found in any document | I open the page | I am told which documents were searched and offered manual construction, rather than shown an empty canvas implying a flat structure |

### 06 - Risk Review

#### US-11 — have the review open on total leverage, then liquidity runway, then th…

**As** The Credit Risk Reviewer, **I want to** have the review open on total leverage, then liquidity runway, then the guarantee package, in that order, **so that** my review starts where I always start instead of where the document happens to begin.

`screen: 06 - Risk Review`

| | Given | When | Then |
|---|---|---|---|
| 1 | a profile has been submitted | I open the risk review | the first-read band presents those three in that order, and the company overview is collapsed at the bottom |
| 2 | the full model is still loading | the first-read band has resolved | I can begin reading and verifying while the rest arrives |

#### US-12 — return a defect as a thread on the figure it concerns

**As** The Credit Risk Reviewer, **I want to** return a defect as a thread on the figure it concerns, **so that** a correction never becomes a round of email, and a small fix I absorb myself stops being invisible.

`screen: 06 - Risk Review`

| | Given | When | Then |
|---|---|---|---|
| 1 | I find that the leverage math is wrong | I post a blocking thread on that figure | the associate sees it against the figure rather than as a message, and the profile records it as blocking |
| 2 | I fix a minor formatting defect myself | the fix is saved | it is recorded as a reviewer edit with the associate's original still visible, so the rework is visible rather than absorbed silently |

#### US-13 — be prevented from signing off while a first-read figure cannot be veri…

**As** The Credit Risk Reviewer, **I want to** be prevented from signing off while a first-read figure cannot be verified, **so that** my signature never sits behind a number whose source is broken.

`screen: 06 - Risk Review`

| | Given | When | Then |
|---|---|---|---|
| 1 | a figure in the first-read band has an unresolvable source | I attempt to sign off | sign-off is disabled, the control names the specific blocker, and the reason is available to assistive technology rather than only visible |
| 2 | every blocking thread is resolved and every first-read source resolves | I sign off | the sign-off is recorded against me individually with a timestamp, the associate is notified, and the committee packet is marked ready |

### 07 - Portfolio Watch

#### US-14 — see at most five positions that need me today, each stating what chang…

**As** The Managing Director, **I want to** see at most five positions that need me today, each stating what changed, our exposure and the distance to breach, **so that** I am told what to do about a position rather than shown fifty things that are true about it.

`screen: 07 - Portfolio Watch`

| | Given | When | Then |
|---|---|---|---|
| 1 | more than five positions deviate from their benchmark | I open portfolio watch | exactly five appear, ranked, and a sixth displaces the weakest rather than lengthening the list |
| 2 | a position's transit times have risen 14% and it sits 0.30x from its covenant | I read its attention item | the item carries the change, the direct exposure figure and the distance to the threshold in one sentence |
| 3 | nothing is outside tolerance | I open portfolio watch | I am told that explicitly, with the number of positions monitored and when signals last refreshed, so silence is distinguishable from a system that is not running |

#### US-15 — never be shown a health score computed from stale feeds as though it w…

**As** The Managing Director, **I want to** never be shown a health score computed from stale feeds as though it were current, **so that** I do not act on a number that stopped being true days ago.

`screen: 07 - Portfolio Watch`

| | Given | When | Then |
|---|---|---|---|
| 1 | the scoring pipeline is unavailable | I open portfolio watch | the last computed scores render with their computation time stated and a persistent banner that they are not current |
| 2 | a signal feed has stopped updating | scores are computed | that position's score confidence is degraded rather than the score being frozen at its last value |
| 3 | a position was booked before the platform existed and has no extracted covenant threshold | I view it | it reports as not measurable, never as comfortable headroom |

### 08 - Position Detail

#### US-16 — open the clause that defines the covenant a distance-to-breach was mea…

**As** The Managing Director, **I want to** open the clause that defines the covenant a distance-to-breach was measured against, **so that** I can check the definition behind the number instead of trusting the calculation.

`screen: 08 - Position Detail`

| | Given | When | Then |
|---|---|---|---|
| 1 | a position is 0.30x from its total leverage covenant | I select that covenant | the clause extracted at underwriting opens, showing the sentence, the document and the page |
| 2 | the covenant was amended after booking | I view it | the amended threshold is shown and the change is marked, rather than the original standing silently |
| 3 | the source clause cannot be resolved | I view the covenant | the threshold is still shown and explicitly marked as unsourced, because withholding it would be worse than showing it unverified |

#### US-17 — acknowledge a signal or escalate it to workout review, with either rec…

**As** The Managing Director, **I want to** acknowledge a signal or escalate it to workout review, with either recorded, **so that** seeing a problem and acting on it are distinguishable afterwards.

`screen: 08 - Position Detail`

| | Given | When | Then |
|---|---|---|---|
| 1 | I have read an attention item | I acknowledge it | the acknowledgement is timestamped against me, the item moves to recently acknowledged, and the signal and its reason are retained rather than deleted |
| 2 | an acknowledged position deteriorates further | scores refresh | it returns to the attention band rather than remaining acknowledged |
| 3 | I do not hold workout authority | I view the escalation control | it is disabled and names the role required, rather than being hidden |

---

## Microcopy

### Calls to action

Primary: **Open profile** · Secondary: **Chase outstanding input** · Destructive: **Escalate to workout**

All sentence case, verb first, three words or fewer.

| Screen | Primary | Secondary |
|---|---|---|
| 01 - Screening Queue | Open profile | Start new profile |
| 02 - Precedent Search | Attach to profile | Request access |
| 03 - Document Extraction | Commit terms | Upload another document |
| 04 - Borrower Profile | Submit for review | Request input |
| 05 - Corporate Structure | Confirm structure | Flag concern |
| 06 - Risk Review | Sign off | Return with comments |
| 07 - Portfolio Watch | Open position | Acknowledge |
| 08 - Position Detail | Acknowledge signal | Open clause |

### Empty states

Each names the condition. Where there is something to do, exactly one action is offered; where there genuinely is nothing to do, none is — a clean review and a quiet portfolio are findings, not gaps.

| Screen | Copy |
|---|---|
| 01 - Screening Queue | No profiles assigned to you. Start a new profile to begin. |
| 02 - Precedent Search | No prior contact found. All five repositories were searched — CRM, credit documents, SharePoint, shared drives and mailboxes. Widen the search to sponsor and subsidiary names. |
| 03 - Document Extraction | No terms extracted. This usually means a scanned document with no text layer. You can enter terms manually and still attach the source passage. |
| 04 - Borrower Profile | Nothing committed yet. Upload a credit agreement to populate the model. |
| 05 - Corporate Structure | No structure could be derived from the documents searched. Upload the guarantee and security deed. |
| 06 - Risk Review | No challenge flags and no open threads. Add-back recurrence, pro-forma adjustment and source resolution were all checked and passed. |
| 07 - Portfolio Watch | Nothing needs your attention today. 40 positions monitored, signals refreshed 14 minutes ago. |
| 08 - Position Detail | This position is within tolerance on every covenant. Last checked 14 minutes ago. |

### Error states

What happened, then what to do. No apologies, and no error implies data was lost when it was not.

| Screen | Copy |
|---|---|
| 01 - Screening Queue | The queue could not load. Your filter has been kept — try again. |
| 02 - Precedent Search | One repository did not respond. These results are incomplete, and the missing source is named above. |
| 03 - Document Extraction | Extraction is unavailable. Your uploaded documents have been kept — nothing has been lost. |
| 04 - Borrower Profile | This figure is unavailable because its feed failed. The last known value and its date are shown instead. |
| 05 - Corporate Structure | One branch could not be derived. It is marked unverified rather than left out. |
| 06 - Risk Review | This figure's source could not be resolved, so it cannot be verified. Sign-off is blocked while it sits in the first read. |
| 07 - Portfolio Watch | Scores are not current. The scoring pipeline is unavailable; these were computed at 06:12 today. |
| 08 - Position Detail | No covenant threshold was extracted for this position, so headroom is not measurable. It is not zero, and it is not comfortable. |

### Confirmations

What was recorded and what followed from it.

| Screen | Copy |
|---|---|
| 01 - Screening Queue | Request re-sent. The item is now awaiting a reply. |
| 02 - Precedent Search | 4 precedent entries attached to the profile. |
| 03 - Document Extraction | 12 terms committed. The model has been populated. |
| 04 - Borrower Profile | Submitted for review. The assigned reviewer has been notified. |
| 05 - Corporate Structure | Structure confirmed. Your sign-off on the guarantee package is recorded. |
| 06 - Risk Review | Signed off. The committee packet is marked ready. |
| 07 - Portfolio Watch | Acknowledged. The signal and its reason have been kept. |
| 08 - Position Detail | Escalated to workout review. The credit team has been notified. |

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/delivery.py` returned **0 errors** with Stage 2 as `persona_profile` and Stage 4 as `wireframe_specs`: 17 unique story ids, every story carrying persona, capability, benefit and at least one complete Given/When/Then, every persona resolving to a Stage-2 persona, every screen resolving to a Stage-4 page, all 8 pages covered, and no ALL-CAPS CTA.

**Tier 2 — judge: weighted mean 4.7 / 5** · pass rule `min>=4 or (min>=3 and weighted_mean>=4.0)` → **pass**

| Dimension | Weight | Score | Note |
|---|---|---|---|
| `story_completeness` | 0.40 | 5 | Each story is one capability with a benefit that is an outcome rather than a reworded capability. Criteria cover the main path plus the edge cases that matter for that screen — the unresolvable source, the scanned PDF, the borrower with no prior periods, the stale feed. |
| `traceability` | 0.30 | 5 | All 8 Stage-4 pages are exercised by at least one story against their stated purpose, including the utilitarian ones. Persona attribution follows the page's `primary_user` throughout. |
| `voice_consistency` | 0.30 | 4 | CTAs are sentence-case, verb-first and three words or fewer after a revision pass; error copy is blame-free and in what-happened-then-what-to-do order. Held at 4 because three empty states offer no action — defensible, since they describe states where nothing needs doing, but it departs from the rubric's single-action anchor. |
