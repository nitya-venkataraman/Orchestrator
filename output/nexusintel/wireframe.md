# Wireframes & IA — NexusIntel

**Stage 4 of 6** · target **web** · design system **Material 3 (baseline profile)** (`baseline`) · **8 pages** · **11 prototype flows**

**Figma:** https://www.figma.com/design/V091wDoNmDuw3J0N9P4Y5K

Direction: **A + B + C composite** — The Verifiable Profile, The Firm's Memory, and The Standing Watch, selected by the reviewer at the Stage-3 fork. All five HMWs and all eleven Stage-3 features are in scope.

> **Revision applied.** A native iOS family (M01–M03) was specified, passed the gate, and was then cut at reviewer revision. No participant described phone use, and carrying the monitored book on a device conflicted with the only stated security requirement in the corpus. `target` moved from `both` to `web`; `mobile_platform` is now `null`. See assumptions 3 and 4.

---

## UX interpretation

**Primary user.** The Screening Associate, who builds the borrower profile, with the Credit Risk Reviewer who gates it and the Managing Director who carries the position after it closes

**User goal.** Reach judgment sooner: spend the screening window analysing a borrower rather than locating, transcribing and reformatting the data about it, and then keep that underwriting work alive as the reference the position is monitored against

**Business goal.** Compress initial vetting from roughly three days toward the same day so term sheets are issued faster, protect the Credit Committee date from rework loops, and shorten the interval between a borrower's condition changing and the firm acting on it

**Main task.** Take an entity name to a signed-off, source-verifiable borrower profile, and then to a continuously monitored position whose covenant thresholds trace back to the clauses extracted at underwriting

**Context.** Institutional deal desks working against live closing dates. Deep, sustained desktop work on large documents and financial models, on wide screens, for hours at a time. Every source is confidential and desk-walled.

**Entry point.** An entity name — arriving as a queue assignment for the associate, a review notification for the reviewer, or a ranked alert for the Managing Director

**Expected outcome.** A profile in which every figure carries the sentence it came from, defects are returned on the line they concern rather than by email, and the covenant thresholds established at underwriting become the live measure of the position

### Business rules

- Every committed figure retains the source offset it was extracted from; a figure whose source cannot be resolved is marked unverifiable rather than displayed as ordinary
- Desk separation is enforced on read: a walled precedent item may be shown to exist, with its desk and date, but never its content
- Sign-off is individual, non-delegable and audited, and is blocked while any first-read figure is unverifiable or any blocking thread is open
- An extracted covenant threshold carries forward as the monitoring reference; a position with no extracted threshold is reported as not measurable, never as comfortable
- The attention band is capped at five items on both surfaces; a sixth displaces the weakest rather than lengthening the list
- An acknowledgement records that a signal was seen and retains its reason; it never deletes the signal
- A score computed from stale feeds must state its computation time; stale data is never presented as current

### Constraints

- Single-tenant deployment inside the firm's own cloud perimeter, with no user prompt, search history or ingested document leaving it
- Role-based access control must keep Private Equity deal notes invisible to Liquid Strategies unless explicitly permitted, since the failure mode is a compliance breach rather than a defect
- Credit agreements routinely exceed three hundred pages, so extraction must stream and be partially useful rather than complete-or-nothing
- WCAG AA across both surfaces; risk severity may never be carried by colour alone
- Desktop-first, but every page must remain usable down to phone width, because a Managing Director will open a link on a phone even though no participant described that as their working surface.

---

## Primary journey

1. Associate opens the screening queue and sees the assigned profile with its remaining window and any blocking input
2. Associate searches the entity and reads what the firm already knows, attaching the relevant precedent to the profile
3. Associate uploads the credit agreement, reconciles extracted terms against their source passages, and commits them
4. Committed terms populate the profile model, so the associate begins on leverage and thesis rather than transcription
5. Associate reviews challenge flags raised on recurring add-backs and unadjusted vendor pulls, and submits for review
6. Reviewer opens on total leverage, then liquidity runway, then structure and guarantees, verifying each figure against its source in place
7. Reviewer adjudicates challenge flags and returns any defect as a thread on the figure it concerns, then signs off
8. The covenant thresholds extracted at underwriting become the live monitoring reference for the booked position
9. Managing Director receives a ranked alert carrying the issue, the exposure and the distance to breach, and acknowledges or escalates

### Error scenarios covered

- A scanned agreement has no text layer, so extraction returns nothing and manual entry must remain available with source attachment intact
- A vendor feed fails mid-build, so affected figures show their last known value and its date rather than a zero
- A source clause cannot be resolved at review time, making a first-read figure unverifiable and blocking sign-off
- The scoring pipeline is unavailable, so the last computed scores render with their computation time stated and a stale banner
- Two reviewers open the same profile, and only one sign-off may be recorded
- A position booked before the platform existed has no extracted threshold and reports as not measurable

---

## Sitemap

| Page | Route | Children |
|---|---|---|
| **01 - Screening Queue** | `/screening` | 02 - Precedent Search, 03 - Document Extraction, 04 - Borrower Profile |
| **02 - Precedent Search** | `/precedent` | — |
| **03 - Document Extraction** | `/profile/:id/extraction` | — |
| **04 - Borrower Profile** | `/profile/:id` | 05 - Corporate Structure, 06 - Risk Review |
| **05 - Corporate Structure** | `/profile/:id/structure` | — |
| **06 - Risk Review** | `/profile/:id/review` | — |
| **07 - Portfolio Watch** | `/portfolio` | 08 - Position Detail |
| **08 - Position Detail** | `/portfolio/:positionId` | — |

---

## Pages

### 01 - Screening Queue

*The Screening Associate* · primary action: **Open profile**

The associate's entry point: every profile assigned to them, what stage it is at, how much of its 72-hour window is spent, and precisely what it is blocked on — so a stalled dependency is visible on arrival instead of being discovered at the deadline.

**Content structure**

- Global entity search bar, always available, accepting a company, sponsor or subsidiary name
- Queue summary strip: profiles in flight, profiles blocked, profiles due within 24 hours
- Assigned-profile list, sorted by remaining window ascending, each row carrying stage, elapsed clock and blocking reason
- Outstanding-input panel listing every request awaiting a reply, its owner, and its age
- Recently viewed entities

**Navigation.** Persistent left sidebar with Screening Queue, Portfolio Watch and Precedent Search. The queue is the default landing route for the associate role.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Screening Queue | `Layout` | reused | — |
| Section / Queue Summary | `Section` | reused | — |
| Component / Global Entity Search | `Search` | reused | idle, suggesting, no-match |
| Component / Profile Queue Row | `List` | reused | in-progress, blocked, in-review, returned, complete |
| Component / Deal Clock | `ProgressIndicator` | reused | ample, tightening, overdue, paused |
| Component / Outstanding Input Item | `List` | reused | awaiting, overdue, received |
| Component / Queue Filter | `Filter` | reused | all, blocked, due-soon |
| Component / Primary Sidebar | `Sidebar` | reused | expanded, collapsed |

**Interactions**

- Typing an entity name suggests matches from the CRM, the document repository and external vendor indexes, labelled by origin
- Selecting a queue row opens the profile at the stage it was left
- The clock meter exposes elapsed and remaining time as text on hover and focus, not only as a filled bar
- Chasing an outstanding input re-sends the request and stamps the item without leaving the queue
- Filtering to blocked is a single control, since it is the state the associate most needs to act on

**States**

| State | Treatment |
|---|---|
| `default` | Queue populated, ordered by tightest remaining window first. |
| `loading` | Row skeletons hold the final row height so the list does not reflow when data lands; the summary strip shows placeholder counts rather than zeros. |
| `empty` | No profiles assigned: an empty state naming what will appear here and offering Start new profile, distinct from the filtered-to-nothing state, which offers to clear the filter. |
| `error` | Queue could not load: an inline error region retaining the sidebar and search, with a retry that does not lose the active filter. |
| `success` | A chased request is confirmed with a toast and an immediate item state change to awaiting, timestamped. |
| `disabled` | Chase is disabled with a tooltip reason when a request was already re-sent within the last four hours. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Three columns: sidebar, queue list, outstanding-input panel. Queue rows show stage, clock, blocking reason and owner inline. |
| `laptop` | Sidebar collapses to icons. Queue and outstanding-input panel keep their split; row metadata drops the owner column. |
| `tablet` | Outstanding-input panel moves below the queue as a titled section rather than a side rail; two columns become one flow. |
| `mobile` | Single column. Queue rows recompose into stacked cards: entity name and clock on the first line, stage and blocking reason beneath. The summary strip becomes a horizontally scrollable chip row. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified at 4.5:1 rather than assumed. Risk severity is never carried by colour alone — every severity state pairs its md.sys.color.error or md.sys.color.tertiary treatment with a text label and a distinct icon shape. The clock meter's tightening and overdue states change both fill token and label text. |
| `keyboard_focus` | Tab order follows the visual column order. Every dialog and popover traps focus, returns it to the trigger on dismiss, and closes on Escape. Focus rings use md.sys.color.primary at a 3:1 minimum against both md.sys.color.surface and md.sys.color.surface-container-high, and are never removed on mouse interaction. The global search is reachable from anywhere with a documented shortcut and announces result counts to assistive technology. |
| `labels` | Every queue row is a single labelled link naming the entity and its stage, so a screen-reader user is not read six unlabelled cells. The clock exposes an accessible value in hours remaining, not a percentage. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp between adjacent targets, including the provenance affordance attached to each figure, which is a full-height row hit area rather than a small inline icon. |
| `reading_order` | Search, then summary, then queue, then outstanding inputs. The sidebar is a landmark navigation region skippable by a visible skip link. |

**Requirements**

*Data dependencies:* Profile assignment service; Deal calendar for deadline dates; Outstanding-request log; Entity index across CRM, repository and vendor feeds

*Permissions:* Associate role; Read access limited to deals on the signed-in user's desk, enforced by the metadata tagging that separates desks

*Edge cases:*

- A profile whose deadline has already passed must render as overdue rather than as a negative remaining value
- An entity that matches several records with the same name must disambiguate by sponsor and jurisdiction before opening
- A request whose recipient has left the firm must surface as unowned rather than silently awaiting
- A profile reassigned mid-build must appear in the new owner's queue without losing elapsed clock

*Open questions:*

- Should the clock pause while an input is outstanding, given the associate cannot act? Marcus and Alex describe the clock as continuing to run, but neither was asked whether it should.
- Is queue ordering by tightest deadline correct, or should blocked profiles sort first?

---

### 02 - Precedent Search

*The Screening Associate* · primary action: **Attach to profile**

Answers the question the associate currently answers by canvassing systems by hand: has this firm touched this entity, its sponsors or its subsidiaries before, and what did we conclude. Assembles a single chronological record from the CRM, the credit document repository, SharePoint, shared drives and mailboxes, bounded by the desk-separation rules.

**Content structure**

- Entity header with resolved identity: legal name, ultimate parent, sponsor, jurisdiction
- Relationship map of the entity, its sponsors and its subsidiaries, each node marked as touched or untouched
- Chronological precedent timeline: meetings, investment committee memos, prior agreements, credit decisions, each with desk, date and participants
- Walled-item notice listing the count of matching records the signed-in user may not see and how to request them
- Coverage indicator stating which repositories were searched and when each was last indexed

**Navigation.** Reachable from the global search on any page and from the primary sidebar. Attaching a precedent set carries the user forward into the profile.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Precedent Search | `Layout` | reused | — |
| Section / Entity Identity | `Section` | reused | — |
| Component / Relationship Map | `Chart` | reused | compact, expanded, untouched-only |
| Component / Precedent Timeline Entry | `List` | reused | meeting, memo, agreement, decision, walled |
| Component / Desk Attribution Chip | `Chip` | reused | own-desk, other-desk, restricted |
| Component / Coverage Indicator | `Banner` | reused | complete, partial, stale-index |
| Component / Access Request | `Form` | reused | idle, submitting, submitted |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |

**Interactions**

- Selecting a timeline entry opens its source excerpt in the provenance popover without leaving the page
- Expanding a subsidiary in the relationship map extends the timeline to include that entity rather than replacing it
- A walled item shows that it exists, its desk and its date, but never its content — requesting access opens a logged request to the owning desk
- Attaching a precedent set writes the selected entries into the profile so the associate never re-finds them

**States**

| State | Treatment |
|---|---|
| `default` | Timeline populated, newest first, with the relationship map showing touched nodes emphasised. |
| `loading` | The timeline streams in per repository, each source showing its own progress row, so a slow mailbox index does not hold back CRM results already available. |
| `empty` | No prior contact found: states plainly that all five repositories were searched, names them and their index dates, and offers to widen the search to sponsor and subsidiary names. This is a finding, not a failure, and is worded as one. |
| `error` | One or more repositories unreachable: results render from those that responded, with a persistent banner naming which source is missing so a partial answer is never mistaken for a complete one. |
| `success` | Attachment confirmed with a toast and a count of entries carried into the profile. |
| `disabled` | Attach is disabled with a stated reason until at least one entry is selected. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Two columns: relationship map fixed left, timeline scrolling right, entity header spanning both. |
| `laptop` | Map narrows and drops to a compact variant showing one generation at a time with a control to step up or down the structure. |
| `tablet` | Map moves above the timeline as a collapsible section, defaulting to collapsed so the timeline is the first content in view. |
| `mobile` | Map becomes a summary line stating the entity, its parent and the number of related entities, expandable to a full-screen view. Timeline entries stack with desk and date above the summary. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Touched and untouched map nodes differ in shape and label as well as fill. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The relationship map is fully keyboard-navigable: arrow keys move between sibling nodes, Enter expands, and each node announces its name, relationship and whether the firm has touched it. |
| `labels` | The map has a text-equivalent structure list conveying the same parent, co-issuer and guarantor relationships in reading order. Timeline entries announce as 'meeting, London Private Equity, March 2024' rather than as unlabelled dates. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. |
| `reading_order` | Entity identity, then coverage indicator, then timeline, then relationship map. The coverage indicator precedes results deliberately: a user must know what was searched before reading what was found. |

**Requirements**

*Data dependencies:* Entity resolution service; CRM connector; Document repository index; Mailbox and drive index with permission metadata; Desk-separation policy service

*Permissions:* Associate role; Results filtered by the metadata tagging that keeps one desk's notes invisible to another unless explicitly permitted

*Edge cases:*

- An entity whose name matches several unrelated companies must resolve by sponsor and jurisdiction before any timeline is shown
- An index older than its freshness threshold must be declared stale rather than presented as current
- A precedent item whose author has left the firm must still attribute the desk
- A subsidiary that changed ownership between the prior contact and now must show the relationship as historical, not current
- Zero results must be distinguishable from an unreachable repository at a glance

*Open questions:*

- What is the acceptable index lag before a repository is treated as stale? No participant was asked.
- Who approves a walled-item access request, and against what service level? The compliance stakeholder was not interviewed.

---

### 03 - Document Extraction

*The Screening Associate* · primary action: **Commit terms**

Turns a credit agreement into structured, committable figures. Every extracted term is shown beside the sentence it came from with an extraction confidence, so the associate reconciles rather than re-types, and nothing enters the model unreviewed.

**Content structure**

- Document rail listing every uploaded agreement and its extraction status
- Extraction summary: terms found, terms needing review, terms not found
- Grouped term list — covenant definitions and thresholds, leverage ratios, the EBITDA definition as written in this document, and the amortisation schedule
- Source panel showing the live document with the citing passage highlighted
- Conflict tray for terms that two documents define differently

**Navigation.** Entered from a profile or directly from the queue. Committing terms advances to the profile workspace with the model populated.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Document Extraction | `Layout` | reused | — |
| Component / Document Upload | `Upload` | reused | idle, uploading, parsing, parsed, failed |
| Component / Extracted Term Row | `List` | **new** | high-confidence, needs-review, conflicted, not-found, accepted |
| Component / Source Passage Viewer | `Card` | reused | highlighted, multi-passage, not-found |
| Component / Extraction Confidence | `Badge` | reused | high, medium, low, not-found |
| Component / Conflict Resolver | `Modal` | reused | two-source, multi-source, resolved |
| Component / Term Group | `Accordion` | reused | collapsed, expanded, needs-review |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |

**Interactions**

- Selecting a term scrolls the source panel to the citing passage and highlights it, so the eye never leaves the pairing
- Correcting a value in place records both the extracted original and the analyst's override, and marks the row as accepted with an override
- A term found in two documents with different values raises a conflict that must be resolved before commit rather than silently taking the first
- Low-confidence and not-found terms are surfaced together as the review worklist, so the associate's attention goes where extraction was weakest
- Committing writes only accepted rows, and every committed figure keeps its source offset for later provenance

**States**

| State | Treatment |
|---|---|
| `default` | Terms grouped by type, review worklist pinned above, source panel showing the passage for the selected term. |
| `loading` | Parsing shows per-page progress with terms appearing as they are found, since a 300-page agreement takes long enough that an all-or-nothing spinner would be a blocking wait. |
| `empty` | No terms extracted: names the likely causes — a scanned image without a text layer, an unsupported structure — and offers manual entry with the source passage still attachable, so a failed extraction never blocks the profile. |
| `error` | Extraction service unavailable: uploaded documents are retained, the page states clearly that nothing has been lost, and offers retry or manual entry. |
| `success` | Commit confirmed with a count of committed terms and a link into the populated model. |
| `disabled` | Commit is disabled while any conflict is unresolved, with the disabled control naming the number of conflicts outstanding. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Three panes: document rail, term list, source panel. Selecting a term updates the source pane without scroll loss. |
| `laptop` | Document rail collapses to a dropdown; term list and source panel keep the side-by-side pairing, which is the core value of the screen. |
| `tablet` | Source panel becomes a bottom sheet that opens on term selection at half height, preserving the term list above it. |
| `mobile` | Term list is the page; selecting a term opens the source passage full-screen with a back control returning to the same scroll position. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Extraction confidence is a labelled badge reading high, medium or low, never a colour alone; highlighted passages carry an underline in addition to their md.sys.color.tertiary-container fill. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. Term rows are a single tab stop with arrow-key navigation between them; the source panel is reachable without traversing every row. |
| `labels` | Each term row announces the term name, extracted value, confidence and whether it needs review. The source passage is announced as a quotation with its document and page. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. Value override inputs meet the same minimum and are not smaller than the row that contains them. |
| `reading_order` | Review worklist first, then term groups, then the source panel — the order in which the work is actually done. |

**Requirements**

*Data dependencies:* Document parsing and extraction service; Term taxonomy; Document storage with page and offset addressing; Conflict detection against already-committed terms

*Permissions:* Associate role; Write access to the profile's model; Document access inherited from the deal's permission set

*Edge cases:*

- A scanned agreement without a text layer must be detected and reported as such, not returned as zero terms
- A term defined by reference to another clause must capture the referenced clause, not the pointer
- An amended and restated agreement must supersede the original, and the supersession must be visible
- A document larger than the parser's limit must be handled by segmentation rather than rejection
- An override that contradicts a high-confidence extraction should be recorded but not blocked — the analyst may be right

*Open questions:*

- What extraction confidence threshold should force review? No participant was asked what error rate is tolerable.
- Should a committed term auto-update if a later amendment is uploaded, or require re-confirmation?

---

### 04 - Borrower Profile

*The Screening Associate* · primary action: **Submit for review**

The live profile itself — the artefact that replaces the hand-built spreadsheet. Every figure is populated from committed extractions, carries its source, and can be interrogated in place. This is where the associate's analysis finally happens instead of their transcription.

**Content structure**

- Profile header: entity, sponsor, deal size, stage, remaining window
- Key metrics band — total leverage ratio, adjusted EBITDA with its add-back trail, liquidity runway across cash and revolver capacity
- Financial model section with period columns and every figure provenance-linked
- Adjusted EBITDA breakdown listing each add-back, its stated rationale and whether it recurs in prior periods
- Attached precedent panel carrying what the firm already knew, brought forward from precedent search
- Investment thesis and industry headwinds, authored by the associate
- Outstanding inputs still blocking completion

**Navigation.** Reached from the queue, from extraction commit, or from search. Submitting hands off to risk review. Corporate structure and extraction are one click away and return to the same scroll position.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Borrower Profile | `Layout` | reused | — |
| Section / Key Metrics | `Section` | reused | — |
| Component / Metric Tile | `Card` | reused | default, overridden, stale-source, missing-input |
| Component / Financial Model Table | `Table` | reused | quarterly, annual, pro-forma-adjusted, comparison |
| Component / Add-Back Trail | `List` | reused | one-time, recurring, disputed |
| Component / Thesis Editor | `Textarea` | reused | empty, drafting, saved |
| Component / Outstanding Input Item | `List` | reused | awaiting, overdue, received |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |
| Component / Challenge Flag | `Badge` | **new** | recurring-addback, unadjusted-proforma, stale-source, resolved, dismissed |

**Interactions**

- Selecting any figure opens its provenance popover showing the sentence it came from, or naming the vendor pull and its timestamp where the source is a feed rather than a document
- An add-back that also appears in prior periods raises a challenge flag automatically, with the prior occurrences listed as its evidence
- A vendor pull not adjusted for a recent acquisition raises a challenge flag naming the acquisition and its date
- Overriding a figure keeps the original visible and records who changed it and why, so the reviewer sees the adjustment rather than only its result
- Submitting for review is blocked while any required input is outstanding, and the block names them

**States**

| State | Treatment |
|---|---|
| `default` | Model populated, metrics computed, challenge flags raised where the data warrants and nowhere else. |
| `loading` | Metric tiles and model rows render as skeletons at final height; committed extracted terms appear first because they are local, with vendor pulls filling in after. |
| `empty` | A new profile with nothing committed yet: the model shows its structure with each section naming the document or feed that would populate it, and links to extraction. An empty profile still communicates what a complete one contains. |
| `error` | A vendor feed failed: affected figures render as unavailable with the reason and the last known value and its date, rather than as zero or a blank cell. A missing figure is never presented as a real one. |
| `success` | Submission confirmed, profile moves to in-review, reviewer notified, and the associate's queue row updates. |
| `disabled` | Submit is disabled while inputs are outstanding or a challenge flag is unresolved; the disabled control names the specific blocker rather than saying the action is unavailable. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Model table at full period width beside a persistent right rail carrying precedent and outstanding inputs. |
| `laptop` | Right rail becomes a collapsible drawer; the model keeps all period columns, since comparing periods is the reason the table exists. |
| `tablet` | Model table gains horizontal scroll with the line-item column pinned, so a row label is never lost while scanning periods. Precedent and outstanding inputs move to tabs below. |
| `mobile` | The model recomposes from a table into per-period cards, one line item per row within each period — a wide financial table cannot be honestly shrunk, so it changes form. Metric tiles stack one per row and the thesis editor becomes full-width. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Challenge flags carry an icon and the word Challenge in addition to their md.sys.color.error-container fill. Overridden figures are marked with a text superscript, not only a tint. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The model table supports standard grid navigation with arrow keys, Home and End; the provenance popover opens from the keyboard on the focused cell and returns focus to it. |
| `labels` | Every model cell has a programmatic row and column header association, so a screen-reader user hears 'Total leverage ratio, Q3 2026, 4.2 times' rather than a bare number. Each metric tile names its unit. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. Provenance affordances on table cells extend to the full cell rather than a corner icon. |
| `reading_order` | Header, then key metrics, then outstanding inputs, then model, then add-back trail, then precedent, then thesis. Outstanding inputs sit high deliberately: they determine whether the rest can be finished. |

**Requirements**

*Data dependencies:* Committed term store with source offsets; Vendor financial feed connectors with timestamps; Pro-forma adjustment detection; Add-back recurrence history; Precedent attachment records; Review submission workflow

*Permissions:* Associate role for edit; Reviewer and MD roles for read; Desk-scoped visibility on attached precedent

*Edge cases:*

- A borrower with no prior periods cannot have recurrence detection run against it and must say so rather than reporting no recurring add-backs
- An acquisition closing between the vendor pull and the profile build must invalidate the pull, not merely annotate it
- A figure with two committed sources must show both and mark the conflict rather than averaging or picking
- Concurrent edits by two associates on the same profile must not silently overwrite
- A profile submitted and then returned must retain the reviewer's threads rather than resetting to a clean state

*Open questions:*

- Should an unresolved challenge flag hard-block submission, or warn and record? Elena described losing trust in the whole profile, but was not asked whether she wants the system to enforce that.
- What is the retention rule for override history once a deal closes?

---

### 05 - Corporate Structure

*The Credit Risk Reviewer* · primary action: **Confirm structure**

The org chart that currently costs four to five hours in PowerPoint, derived instead from the agreements. Shows the ultimate parent, co-issuers and guarantors, and marks who is actually on the hook for the debt and which subsidiaries are unrated or offshore.

**Content structure**

- Structure canvas: ultimate parent at the root, issuers, co-issuers, guarantors and non-guarantor subsidiaries
- Guarantee overlay marking which entities guarantee which obligations
- Entity detail panel: jurisdiction, rating status, guarantee position, cash-flow relationship
- Structural concern list — unrated offshore subsidiaries, non-guarantor entities holding material cash, entities added since the last agreement
- Derivation note stating which documents the structure was built from

**Navigation.** Opened from the profile and from risk review; returns to the caller at its prior scroll position. Not a standalone destination in the sidebar.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Corporate Structure | `Layout` | reused | — |
| Component / Structure Canvas | `Chart` | reused | full, guarantee-overlay, cash-flow-overlay, print |
| Component / Entity Node | `Card` | reused | parent, issuer, co-issuer, guarantor, non-guarantor, unrated-offshore |
| Component / Structural Concern | `Alert` | reused | unrated-offshore, non-guarantor-cash, newly-added, unverified |
| Component / Overlay Toggle | `Switch` | reused | off, on, unavailable |
| Component / Entity Detail | `Drawer` | reused | closed, open, loading |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |

**Interactions**

- Selecting an entity opens its detail drawer and its derivation — the clause that establishes its role
- Toggling the guarantee overlay recolours and relabels edges by obligation, with a legend that names each edge type in text
- A structural concern selects and centres the entity it concerns rather than merely describing it
- Confirming the structure records reviewer sign-off on the guarantee package specifically, which is one of the three things the reviewer checks first

**States**

| State | Treatment |
|---|---|
| `default` | Full structure rendered from the root, guarantee overlay off, concerns listed beside the canvas. |
| `loading` | The canvas draws progressively from the root outward, so the parent and first generation are readable before deep subsidiaries resolve. |
| `empty` | Structure could not be derived from the available documents: states which documents were searched, that no structural clauses were found in them, and offers manual construction — the reviewer must never be shown an empty canvas that implies a flat structure. |
| `error` | Partial derivation: renders what was derived and marks unresolved branches explicitly as unverified rather than omitting them, because an entity silently missing from a guarantee chart is the failure mode that matters here. |
| `success` | Confirmation recorded against the profile with reviewer identity and timestamp. |
| `disabled` | Confirm is disabled while any branch is unverified, naming the unverified entities. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Canvas fills the viewport with the concern list and entity detail as a right rail. |
| `laptop` | Canvas keeps full width; concern list collapses to a counted, expandable summary bar. |
| `tablet` | Canvas becomes pan-and-zoom with fit-to-width default; entity detail opens as a bottom sheet. |
| `mobile` | The tree recomposes into an indented, expandable outline rather than a shrunken canvas — a structure chart at phone width is unreadable as a graphic but perfectly readable as a nested list. Guarantee position becomes a labelled row on each entity. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Guarantor and non-guarantor entities differ by border treatment and an explicit text label, never by fill alone. The overlay legend is text, not a colour key. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The canvas is a keyboard-navigable tree: arrow keys traverse siblings and generations, Enter opens detail, and the current node is announced with its full path from the root. |
| `labels` | The canvas has an equivalent nested list exposing the same relationships in reading order. Each node announces name, jurisdiction, rating status and guarantee position. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. Entity nodes meet the minimum at every zoom level; zooming out clusters nodes rather than shrinking their hit areas below the threshold. |
| `reading_order` | Derivation note, then structural concerns, then structure, then entity detail. The concerns precede the chart because they are what the reviewer is looking for in it. |

**Requirements**

*Data dependencies:* Entity graph derivation service; Guarantee package terms; Jurisdiction and rating reference data; Source clause addressing; Prior structure versions for change detection

*Permissions:* Reviewer role for confirm; Associate role for read and flag; Document access inherited from the deal

*Edge cases:*

- A circular ownership relationship must render without infinite recursion and be flagged as circular
- An entity appearing in the agreement but absent from vendor reference data must render as unrated rather than be dropped
- A guarantee that is limited or capped must not display as a full guarantee
- A structure derived from a superseded agreement must be marked as such
- More than roughly two hundred entities must degrade to a navigable outline rather than an unusable canvas

*Open questions:*

- Does confirmation of structure carry the same weight as sign-off on the profile, or is it a separate record? Not established in research.
- What reference source is authoritative for offshore entity ratings?

---

### 06 - Risk Review

*The Credit Risk Reviewer* · primary action: **Sign off**

The reviewer's twenty-to-thirty-minute read, rebuilt to be a five-minute one. Opens on the three things she checks first, in her order, with every figure verifiable in place and every defect returnable on the line it concerns instead of by email.

**Content structure**

- Review header: entity, associate, submission time, committee date and how much slack remains before it moves
- First-read band in the reviewer's stated order — total leverage ratio with its adjusted EBITDA construction, then liquidity runway across cash and revolver capacity, then corporate structure and guarantee package
- Challenge flags awaiting adjudication, each with its evidence attached
- Open review threads and their status
- Full model, collapsed by default and expandable
- Company overview, collapsed by default because the reviewer skips it

**Navigation.** Reached from the reviewer's own queue and from a submission notification. Sign-off and return both exit to the reviewer queue.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Risk Review | `Layout` | reused | — |
| Section / First Read | `Section` | reused | — |
| Component / Metric Tile | `Card` | reused | default, overridden, stale-source, missing-input |
| Component / Review Thread | `Accordion` | reused | open, answered, resolved, blocking |
| Component / Liquidity Runway | `Chart` | reused | cash-only, cash-and-revolver, projected, insufficient-data |
| Component / Sign-Off Panel | `Form` | reused | ready, blocked, submitted |
| Component / Financial Model Table | `Table` | reused | quarterly, annual, pro-forma-adjusted, comparison |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |
| Component / Challenge Flag | `Badge` | **new** | recurring-addback, unadjusted-proforma, stale-source, resolved, dismissed |

**Interactions**

- Every figure in the first-read band opens its source sentence in place — this is the interaction the reviewer described as taking her review from thirty minutes to five, and it is the reason this direction was built
- Adjudicating a challenge flag records accept or dismiss with a reason, and the reason becomes part of the profile's record
- Returning a defect posts a thread on the specific figure rather than sending a message, so a correction never becomes a round of email
- A minor defect the reviewer chooses to fix herself is recorded as a reviewer edit, keeping the associate's original visible, so silent absorption becomes visible rework data rather than invisible goodwill
- Sign-off requires every blocking thread resolved; non-blocking threads may remain open and travel with the profile

**States**

| State | Treatment |
|---|---|
| `default` | First-read band populated, challenge flags listed, model collapsed, overview collapsed. |
| `loading` | The first-read band resolves before the full model loads, so the reviewer can begin the read she always begins with while the rest arrives. |
| `empty` | A profile submitted with no challenge flags and no open threads: says so explicitly and states what was checked to reach that conclusion, so an empty flag list reads as a clean profile rather than as a check that did not run. |
| `error` | A figure's source cannot be resolved: that figure is marked unverifiable with the reason, and sign-off treats unverifiable figures in the first-read band as blocking. The reviewer's trust problem is not solved by hiding a broken link. |
| `success` | Sign-off recorded, associate notified, committee packet marked ready. |
| `disabled` | Sign off is disabled while a blocking thread or an unadjudicated challenge flag remains; the control names the count and links to the first one. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | First-read band across the top at full width, threads in a right rail, model below. |
| `laptop` | Threads rail collapses to a counted drawer; the first-read band keeps its three-across layout. |
| `tablet` | First-read band stacks to a single column in the reviewer's stated order; threads become a tab beside the model. |
| `mobile` | Single column throughout. The first-read band becomes three full-width cards in order, each expandable to its source. Threads are a badge-counted section that opens full-screen. The reviewer described wanting a dashboard rather than a document, and at phone width that means a prioritised stack, not a shrunken grid. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Thread status is conveyed by label and icon as well as fill; blocking threads carry the word Blocking. The liquidity runway chart marks its insufficient-data state with a hatched pattern and a caption, not a colour. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The first-read band is reachable in three tab stops. Provenance opens and closes without leaving the keyboard, and the sign-off control announces its blocking reason when disabled rather than being silently inert. |
| `labels` | Each first-read tile announces metric, value, unit and verification status. Threads announce their author, target figure and status. The sign-off control's disabled reason is programmatically associated with it, not only visual. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. Adjudication controls on challenge flags are full-size buttons, since a mis-tap here changes a recorded decision. |
| `reading_order` | Header and committee slack, then first read, then challenge flags, then threads, then model, then overview last — the reverse of a conventional document, matching the order the reviewer actually reads in. |

**Requirements**

*Data dependencies:* Submitted profile store; Challenge flag engine with evidence links; Review thread service; Committee calendar; Sign-off audit log; Prior profile history

*Permissions:* Reviewer role for sign-off and adjudication; Associate role for read and reply; Sign-off is not delegable and must record the individual reviewer

*Edge cases:*

- A profile returned and resubmitted must show what changed since the previous read, so the reviewer does not re-read the whole file
- A challenge flag raised on a figure that is subsequently overridden must re-evaluate rather than persist against a stale value
- A committee date moved earlier must recompute slack and re-sort the reviewer queue
- Two reviewers opening the same profile must not both sign off
- A profile whose source documents are withdrawn mid-review must mark affected figures unverifiable immediately

*Open questions:*

- Should a reviewer's own inline fix require associate acknowledgement? Elena described fixing silently to avoid email; whether she wants that surfaced was not asked.
- What is the escalation path when sign-off is blocked and the committee date cannot move?

---

### 07 - Portfolio Watch

*The Managing Director* · primary action: **Open position**

The Managing Director's standing view of booked positions, ranked by what deserves attention today. Replaces the quarterly spreadsheet cycle with a continuous measure, and answers the objection to fifty flashing lights by ranking rather than flagging.

**Content structure**

- Attention band: at most five positions the system asserts are worth the MD's time today, each with its reason in one sentence
- Exposure summary: total committed, drawn, and the share sitting in positions currently narrowing toward a covenant
- Position table with health score, direction of travel, covenant headroom and direct exposure
- Signal provenance rail naming which alternative signals moved and when they were last refreshed
- Recently acknowledged items, so an acknowledgement is auditable rather than a dismissal

**Navigation.** A primary sidebar destination and the default landing route for the MD role. Positions open into detail and return to the same scroll position.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Portfolio Watch | `Layout` | reused | — |
| Section / Attention Band | `Section` | reused | — |
| Component / Attention Item | `Card` | reused | deteriorating, improving, new-signal, acknowledged |
| Component / Position Row | `Table` | reused | stable, narrowing, at-threshold, breached, insufficient-data |
| Component / Health Score Trend | `Chart` | reused | sparkline, expanded, insufficient-history |
| Component / Covenant Headroom Meter | `ProgressIndicator` | **new** | comfortable, narrowing, at-threshold, breached, unknown |
| Component / Exposure Summary | `Card` | reused | default, drilldown |
| Component / Signal Freshness | `Banner` | reused | current, delayed, stale |

**Interactions**

- The attention band is capped at five items by design — the constraint is the product, and a sixth item displaces the weakest rather than extending the list
- Each attention item states what changed, the firm's direct exposure and the current distance to the covenant threshold, which is the three-part payload the MD specified
- Selecting a position opens detail; acknowledging records that the MD saw it, with the reason retained rather than dismissed
- Covenant headroom is shown as signed distance to threshold, so approaching from a comfortable position and sitting just inside a breach are visibly different
- Signal freshness is always on screen, because a score computed from stale feeds is worse than no score

**States**

| State | Treatment |
|---|---|
| `default` | Attention band populated, positions ranked by score deterioration, exposure summary current. |
| `loading` | Attention band and exposure summary resolve first from cached scores; the full position table streams, since the MD's decision is usually made from the band alone. |
| `empty` | Nothing warrants attention today: an explicit statement that all positions are within tolerance, naming the number monitored and when signals last refreshed. Silence must be distinguishable from a system that is not running. |
| `error` | Scoring pipeline unavailable: the last computed scores render with their computation time stated prominently and a banner that scores are not current. A stale score presented as live is the failure that would cost this product its credibility. |
| `success` | Acknowledgement confirmed inline, the item moves to recently acknowledged, and the band re-ranks. |
| `disabled` | Acknowledge is disabled on positions outside the MD's desk, with the reason given as desk scope rather than a generic denial. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Attention band across the top, position table below at full width, signal rail on the right. |
| `laptop` | Signal rail collapses into the freshness banner; the position table drops the sector column. |
| `tablet` | Attention items become a single-column stack; the position table keeps score, headroom and exposure and moves the rest behind row expansion. |
| `mobile` | Attention band only, as full-width cards; the position table becomes a searchable list reachable by an explicit control. At phone width the MD is checking whether anything needs them, not scanning a portfolio, so the page becomes the answer to that question rather than a compressed table. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Direction of travel is an arrow shape plus a text label, never a red or green fill alone — the entire value of this page rests on a distinction that must survive colour blindness. Breached positions carry a text label reading Breached. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The attention band is the first tab stop after navigation. Acknowledgement is keyboard-reachable per item without entering the position detail. |
| `labels` | Each attention item is announced as a single sentence carrying change, exposure and headroom, so the payload is identical for a screen-reader user. Sparklines expose their trend as a text summary naming direction and period. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. Acknowledge controls are full-size and separated from the row's open action by at least 8dp, since the two have very different consequences. |
| `reading_order` | Signal freshness, then attention band, then exposure summary, then position table. Freshness precedes the scores deliberately. |

**Requirements**

*Data dependencies:* Position and exposure ledger; Covenant thresholds from underwriting extraction; Alternative signal feed connectors with refresh timestamps; Sector benchmark reference data; Scoring pipeline; Acknowledgement audit log

*Permissions:* MD role; Desk-scoped position visibility; Acknowledgement recorded against the individual, not the desk

*Edge cases:*

- A position booked before the platform existed has no extracted covenant thresholds and must render as insufficient data rather than as comfortable headroom
- A signal feed that stops updating must degrade the score's confidence rather than freezing the score at its last value
- A borrower with fewer than the minimum history points cannot be benchmarked and must say so
- A covenant amended after booking must supersede the extracted threshold
- An acknowledged item whose condition worsens further must return to the band rather than stay acknowledged

*Open questions:*

- What deviation threshold should raise an item into the attention band? The brief proposes 1.5 sigma, but no participant was asked what false-positive rate they would tolerate, and the band's credibility depends entirely on that number.
- Is five the right cap for the attention band? It follows from the MD's objection to fifty, but the specific number is an inference.
- Who receives the alert when the MD is unavailable, and does acknowledgement transfer?

---

### 08 - Position Detail

*The Managing Director* · primary action: **Acknowledge signal**

The full account behind one attention item: what changed, what the firm's exposure is, how far the position is from breaching, and which underwriting covenant that distance is measured against — with the covenant traceable back to the clause extracted at deal time.

**Content structure**

- Position header: borrower, desk, committed and drawn exposure, current health score and direction
- Signal narrative: a plain statement of what changed, by how much, over what period, and which feed observed it
- Covenant headroom detail per covenant, each showing the threshold, the current value and the signed distance
- Exposure breakdown by facility, showing what is actually at risk rather than only the headline commitment
- Score history with the contributing signals marked at the points they moved it
- Link back to the underwriting profile and the clause each threshold came from

**Navigation.** Opened from the attention band or the position table on 07 - Portfolio Watch. Returns to the caller's scroll position.

**Components**

| Component | Base | Source | Variants |
|---|---|---|---|
| Page / Position Detail | `Layout` | reused | — |
| Section / Signal Narrative | `Section` | reused | — |
| Component / Exposure Summary | `Card` | reused | default, drilldown |
| Component / Health Score Trend | `Chart` | reused | sparkline, expanded, insufficient-history |
| Component / Covenant Headroom Meter | `ProgressIndicator` | **new** | comfortable, narrowing, at-threshold, breached, unknown |
| Component / Signal Contribution | `List` | reused | primary-driver, contributing, noise, suppressed |
| Component / Escalation Action | `Confirmation` | reused | idle, confirming, submitted |
| Component / Provenance Popover | `Popover` | **new** | closed, loading, resolved, unresolved, multi-source |

**Interactions**

- Each covenant threshold opens the clause it was extracted from, so the MD can see the definition the distance is computed against rather than trusting the number
- Signal contributions are ranked so the primary driver is identifiable, answering the objection that a dashboard shows everything and explains nothing
- Acknowledging records that the MD saw the signal and retains the reason; it does not delete the item
- Escalating to workout review is a confirmed action that creates a record and notifies the credit team, because it has consequences outside this screen
- Adjusting alerting for this position is scoped to the position and is logged, so tuning never silently hides a deteriorating asset

**States**

| State | Treatment |
|---|---|
| `default` | Narrative, headroom detail and exposure breakdown all populated, score history charted with drivers marked. |
| `loading` | The signal narrative and headroom resolve first; score history and facility breakdown fill in after, since the decision is usually made from the first two. |
| `empty` | A position with no active signal: states that the position is within tolerance on every covenant, lists the covenants checked and when signals last refreshed, rather than rendering a blank detail page. |
| `error` | A covenant with no extracted threshold renders as not measurable with an explicit reason and a link to supply it, never as comfortable headroom. Absence of a threshold must never read as absence of risk. |
| `success` | Acknowledgement or escalation confirmed inline with a timestamped record and the resulting notification named. |
| `disabled` | Escalate is disabled where the signed-in user lacks workout authority, naming the role required rather than hiding the control. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| `desktop` | Two columns: narrative and headroom left, exposure and score history right. |
| `laptop` | Single wide column with headroom and exposure side by side beneath the narrative. |
| `tablet` | Fully stacked in decision order: narrative, headroom, exposure, history. |
| `mobile` | Narrative and the single tightest covenant headroom above the fold; exposure and history behind expandable sections. On a phone the MD is deciding whether this needs them now, so the page leads with the answer and keeps the evidence one tap away. |

**Accessibility**

| Aspect | Decision |
|---|---|
| `contrast` | Body text is md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; secondary text uses md.sys.color.on-surface-variant, verified rather than assumed. Severity is never carried by colour alone — every md.sys.color.error treatment is paired with a text label and a distinct icon shape. Headroom states are labelled Comfortable, Narrowing, At threshold or Breached in text alongside their token treatment. Score direction uses an arrow shape plus a worded change. |
| `keyboard_focus` | Tab order follows visual column order. Dialogs and popovers trap focus, return it to the trigger on dismiss, and close on Escape. Focus rings use md.sys.color.primary at 3:1 minimum against md.sys.color.surface and md.sys.color.surface-container-high, never suppressed on mouse interaction. The covenant list and its provenance links are fully keyboard-operable; the escalation confirmation traps focus and requires an explicit confirm rather than defaulting to it. |
| `labels` | The signal narrative is a single readable sentence carrying change, exposure and distance to breach, so the payload is identical in audio. Each headroom meter announces threshold, current value and signed distance with units. |
| `touch_targets` | All interactive targets are at least 44x44px with at least 8dp separation. The provenance affordance is a full-height row hit area, not a small inline icon. The escalate control is separated from acknowledge by at least 24dp given the difference in consequence. |
| `reading_order` | Header, then narrative, then headroom, then exposure, then history, then links back to underwriting. |

**Requirements**

*Data dependencies:* Position and facility ledger; Covenant thresholds with source clause offsets; Signal feed observation store; Score attribution service; Escalation workflow; Acknowledgement audit log

*Permissions:* MD role for acknowledge; Workout authority for escalate; Desk-scoped position visibility

*Edge cases:*

- A covenant whose definition was amended after booking must show the amended threshold and mark the change
- A signal that reversed after triggering must show the reversal rather than leaving a stale narrative
- A position with multiple covenants breaching simultaneously must rank them by severity rather than listing them arbitrarily
- A facility drawn to zero must not report exposure at its committed amount
- An escalation raised twice for the same signal must be idempotent

*Open questions:*

- Does acknowledgement suppress the signal for a period, and if so how long? No participant was asked.
- What authority is required to escalate to workout review, and does it differ by exposure size?

---

## Responsive matrix

| Component | Desktop | Tablet | Mobile |
|---|---|---|---|
| Component / Financial Model Table | Full period columns visible side by side, line-item column at natural width | Horizontal scroll with the line-item column pinned so a row label is never lost | Recomposes into per-period cards, one line item per row — a wide financial table changes form rather than shrinking |
| Component / Structure Canvas | Full graphical tree with guarantee overlay toggles | Pan-and-zoom canvas, fit-to-width by default, detail in a bottom sheet | Becomes an indented expandable outline; guarantee position becomes a labelled row per entity |
| Component / Relationship Map | Fixed left column beside the scrolling timeline | Collapsible section above the timeline, collapsed by default | A summary line naming entity, parent and related count, expandable to full screen |
| Component / Profile Queue Row | Single row carrying stage, clock, blocking reason and owner | Row drops the owner column, keeps clock and blocking reason | Stacked card: entity and clock on the first line, stage and blocking reason beneath |
| Component / Attention Item | Horizontal band of up to five cards above the position table | Single-column stack, table below | Full-width cards become the whole page; the position table moves behind an explicit control |
| Component / Source Passage Viewer | Persistent third pane beside the term list | Bottom sheet at half height, opening on term selection | Full-screen view with back returning to the same scroll position |
| Component / Provenance Popover | Anchored popover beside the figure | Anchored popover, repositioned to stay within the viewport | Bottom sheet at half height, since an anchored popover cannot show a passage legibly at phone width |
| Component / Covenant Headroom Meter | Horizontal meter with threshold marker and numeric distance inline | Horizontal meter, numeric distance beneath | Compact meter with the worded state and signed distance stacked beneath |
| Component / Review Thread | Right rail, always visible beside the model | Tab beside the model, badge-counted | Badge-counted section opening full-screen |
| Component / Primary Sidebar | Expanded with labels | Collapsed to icons with tooltips | Collapses to a top app bar with a drawer; the drawer traps focus and closes on Escape |

---

## Prototype flows

| From | Trigger | To | Interaction |
|---|---|---|---|
| 01 - Screening Queue | Selecting an assigned profile row | **04 - Borrower Profile** | Push, opening the profile at the stage it was left |
| 01 - Screening Queue | Submitting an entity name in the global search | **02 - Precedent Search** | Push with the resolved entity in context |
| 01 - Screening Queue | Selecting Portfolio Watch in the primary sidebar | **07 - Portfolio Watch** | Route change, sidebar persists |
| 02 - Precedent Search | Attaching the selected precedent set | **03 - Document Extraction** | Push, carrying the attached entries into the profile |
| 03 - Document Extraction | Committing accepted terms | **04 - Borrower Profile** | Push with the model populated from committed terms |
| 04 - Borrower Profile | Selecting View corporate structure | **05 - Corporate Structure** | Push; back returns to the prior scroll position |
| 05 - Corporate Structure | Confirming structure or selecting back | **04 - Borrower Profile** | Pop to the prior scroll position |
| 04 - Borrower Profile | Submitting for review | **06 - Risk Review** | Push; blocked while any required input is outstanding |
| 06 - Risk Review | Recording sign-off | **01 - Screening Queue** | Pop to the queue with the profile row updated to complete |
| 07 - Portfolio Watch | Selecting an attention item or position row | **08 - Position Detail** | Push; back returns to the prior scroll position |
| 08 - Position Detail | Selecting View underwriting profile | **04 - Borrower Profile** | Push into the profile the covenant thresholds were extracted from |

---

## Design system gaps

Five needs the baseline taxonomy cannot express. Findings for the design-system owner, not licence to invent roles.

**1. A control that renders a source excerpt with its citing sentence highlighted, its document, page and clause reference, and a deep link back into the agreement at that position**

*Nearest base role:* `Popover`

*Why insufficient:* A Popover carries free text anchored to a trigger. This control has a compound structured payload and two states a Popover does not model — source still resolving, and source could not be located — and the second must be visually distinct from an ordinary empty popover, because a reviewer treating an unresolved source as a missing one is exactly the trust failure this direction exists to prevent.

**2. A meter expressing signed distance to a fixed threshold that can be approached from either side and crossed**

*Nearest base role:* `ProgressIndicator`

*Why insufficient:* A ProgressIndicator models monotonic progress toward completion, where the end of the track is the goal. Covenant headroom has a fixed marker mid-track that represents failure rather than completion, values that continue past it, and a distinct fifth state for no current data that must never render as zero headroom.

**3. A flag that carries an assertion requiring adjudication, holding its evidence and recording an accept or dismiss decision against the profile**

*Nearest base role:* `Badge`

*Why insufficient:* A Badge is a static status label with no interaction contract. This carries evidence, an adjudication decision, the deciding user and a reason, all of which become part of the profile's audit record — it has a lifecycle rather than a value.

**4. A two-column reconciliation row pairing an extracted value with its source excerpt, an editable override and an extraction-confidence indicator, acceptable in place**

*Nearest base role:* `List`

*Why insufficient:* A List item renders content in one direction. This is a reconciliation control between what was extracted and what will be committed, holding two competing values at once with an accept action that resolves them, plus a not-found state where there is no extracted value to reconcile against.

**5. An accessible text-equivalent structure for the corporate-structure canvas and the relationship map**

*Nearest base role:* `Chart`

*Why insufficient:* The baseline offers no pattern for a graph that must be equally navigable as a keyboard tree and as a screen-reader outline. Both views are specified here per page, but the pattern belongs in the design system rather than being re-derived on each surface that renders a graph.

---

## Assumptions

Each of these is a decision made without evidence. They are the first things to check before build.

1. No design system was supplied for this project, so Stage 4 falls back to the documented Material 3 baseline token set — colour roles, typescale, shape-corner scale, elevation levels and the 4dp spacing grid. Every value in these specs is a token name; if the firm has an existing library, this stage should be re-run against it and the token names remapped, which will change nothing structural.
2. Material 3 is a baseline, not a recommendation. For an institutional credit tool an information-dense system with a stronger data-table and financial-numeral treatment would likely serve better, and the baseline's default density is looser than these screens want.
3. A native mobile surface was specified and then deliberately cut at reviewer revision. No participant described using a phone, and the only participant who raised security described a single-tenant private cloud with no data leaving the perimeter — carrying the monitored book on a device conflicted with that requirement and had no evidence supporting it. The Managing Director's need for an actionable alert is served on the web surface, which remains usable at phone width.
4. Because the mobile family was cut, the Managing Director's away-from-desk case is unaddressed by design rather than by oversight. If research later establishes that need, it should re-enter at the direction fork rather than be retrofitted onto these pages.
5. The attention band cap of five follows from the Managing Director's objection to fifty flashing lights, but the specific number is an inference. No participant was asked how many items they would tolerate.
6. Page count reflects the composite A+B+C direction selected by the reviewer. HMW 1 (firm memory) is served by 02 - Precedent Search, which brings the Entity Precedent Timeline and Inbox and Drive Ingestion features into scope alongside directions A and C.
7. The 1.5 sigma deviation threshold in the PRD is carried as a business input, not a validated one. Stage 1 recorded that no participant was asked what false-positive rate they would accept, and the credibility of the entire monitoring surface rests on that number.
8. Contrast ratios are specified as requirements against token roles rather than verified numerically, because the baseline palette's concrete values are placeholders until the firm's own palette is supplied. Every pairing named here must be re-measured once real values exist.

---

## Validation

**ux**

- Each of the 8 pages traces to at least one Stage-2 HMW and at least one Stage-3 feature
- The primary journey covers the Stage-2 journey stages 1 through 7 without introducing a step no persona described
- Pages open on what each persona reads first: the reviewer's page leads with leverage, then liquidity runway, then structure, in her stated order, and buries the company overview she skips
- No page requires the associate to leave the profile to verify a figure, which was the source of the reviewer's thirty-minute read

**ui**

- Every colour reference in this artifact is a token name; the artifact contains no hex value and no rgb notation
- Every component name follows the Page, Section or Component naming pattern and declares a base role from the taxonomy
- Five components are declared new, each with a why_new naming what the nearest base role cannot express, and each is reused across at least two pages
- All other components are declared reused, so a control that means the same thing on two pages is the same component

**responsive**

- All 8 pages specify all four breakpoints: desktop, laptop, tablet and mobile
- The responsive matrix covers the ten components whose behaviour genuinely recomposes rather than scaling
- Wide content changes form rather than shrinking: the financial model becomes per-period cards, the structure canvas becomes an indented outline, the relationship map becomes a summary line
- 07 - Portfolio Watch becomes the attention band alone at phone width, on the reasoning that the question at that size is whether anything needs the user, not what the whole book looks like
- No native mobile family is specified; the web pages carry the phone case at their mobile breakpoint

**accessibility**

- No state anywhere is carried by colour alone; every severity, direction and status pairs its token treatment with a text label and a distinct shape
- Both graph components specify a keyboard tree and a text-equivalent outline conveying the same relationships
- Touch targets meet 44x44px, with at least 8dp separation and 24dp between actions of differing consequence
- Data tables carry programmatic row and column header association so a cell is announced with its metric and period
- Every disabled primary action announces its blocking reason programmatically rather than being silently inert

**prototype**

- 11 flows connect all 8 pages; every from and to names a specced page
- Every page is reachable from 01 - Screening Queue, the family entry
- The primary journey is completable end to end in the prototype, from queue through precedent, extraction, profile and review to sign-off, and separately from portfolio watch to position detail
- Return paths preserve scroll position wherever a page is entered from a list
- Rendered to Figma: 8 frames at 1440x1024, 42 token variables in md.sys.color and md.sys.spacing collections, 2 component sets with 5 variants each, and all 11 prototype connections wired with 01 - Screening Queue as the starting point

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/wireframe.py` returned **0 errors** with Stage 3 supplied as `feature_matrix`: 8 pages in range, page-name family correct, every component name and base role valid, every `new` component justified, no hex and no rgb notation anywhere, all four breakpoints on every page, all required state / accessibility / requirements keys populated, every page reachable from 01 - Screening Queue, and sitemap and page specs describing the same set.

**Tier 2 — judge: 0.89** (threshold 0.80)

| Criterion | Weight | Score | Note |
|---|---|---|---|
| `ds_compliance` | 0.25 | 0.90 | Every value is a token name; naming pattern followed throughout; 5 new components each justified and each reused across at least two pages; 5 genuine gaps flagged rather than invented roles. Held below full marks because the resolved baseline is Material 3, whose default density is a poor fit for an institutional credit tool — recorded in `assumptions` rather than hidden. |
| `ia_coherence` | 0.20 | 0.85 | Sitemap, flows and pages describe one set, and page order follows each persona's actual reading order. **Weakest dimension:** the composite direction produces two trees joined at a single link (08 → 04). Inherent to selecting A+B+C together, not a defect in execution. |
| `state_and_responsive_coverage` | 0.20 | 0.92 | Empty and error are distinguished with care on every page — 'silence must be distinguishable from a system that is not running' is applied consistently. Wide content recomposes rather than scaling. |
| `accessibility_rigor` | 0.15 | 0.88 | Nothing relies on colour alone anywhere; both graph components carry a keyboard tree and a text-equivalent outline; disabled actions announce their blocking reason. Held down because contrast is specified against token roles rather than verified numerically. |
| `requirements_completeness` | 0.20 | 0.90 | Every page carries data dependencies, permissions, edge cases and open questions, and the prototype completes the primary journey. Raised from 0.85 once the Figma file was rendered and all 11 connections wired. |

### Figma render

| | |
|---|---|
| File | [NexusIntel — Wireframes (Stage 4, web)](https://www.figma.com/design/V091wDoNmDuw3J0N9P4Y5K) |
| Frames | 8, at 1440x1024 |
| Variables | 42 across `md.sys.color` (28) and `md.sys.spacing` (14) — every fill bound to a token, none hard-coded |
| Component sets | `Component / Covenant Headroom Meter` (5 variants), `Component / Challenge Flag` (5 variants) |
| Prototype | 11 connections wired; starting point `01 - Screening Queue` |

Two defects were caught by screenshot review and fixed: metric tiles were clipping their values (fixed-height containers switched to hug), and default non-token white fills were showing through the coloured attention cards (cleared, preserving every variable-bound fill).
