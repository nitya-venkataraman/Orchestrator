# Strategy Definition — NexusIntel

**Stage 2 of 6** · Personas, current-state journey, and How-Might-We statements. Every `grounded_in` entry resolves to a Stage-1 theme name; every persona quote is a verbatim substring of the corpus.

> ⚠️ **Human-authorized contract exception.** The Stage-2 contract permits exactly two personas (one primary, one secondary). This run carries **three**, at the reviewer's explicit direction, because all three users were interviewed directly and dropping one would discard first-hand evidence. `ux-pipeline/validators/strategy.py` was **not modified** — it still reports the two persona-count errors, and they are recorded as an override in `workspace/run.json`. Every other Tier-1 rule passes.

---

## Personas

### The Screening Associate · `primary`

> I feel like a glorified data entry clerk for the first two days.

The analyst who assembles the foundational borrower profile end to end, on a 48-72 hour clock, before anyone senior sees it. Opens with the entity name and no context: checks Capital IQ and Bloomberg to establish public or private, then the internal CRM, Salesforce and the credit document repository for any prior firm contact. Builds the org chart by hand from PDF credit agreements and pitch books, re-keys financials into an Excel template, and only reaches the actual risk analysis late on the second night. Interviewed directly; every trait below is his own account of his own work.

**Goals**

- Reach the leverage math and the investment thesis while there is still time to think about them, instead of at midnight on day two
- Establish on day one whether the firm has touched this client, its sponsors or its subsidiaries before
- Get the covenant definitions, debt schedule and EBITDA definition out of the credit agreement without reading 300 pages
- Hand the reviewer a profile that survives first contact, so no rework loop starts
- Stop the clock running while he waits on a sponsor reply he cannot chase directly

**Frustrations**

- Roughly 70% of the window goes to finding and formatting data and only 30% to analysis
- Mapping the ultimate parent, co-issuers and guarantors of a PE-backed structure alone consumes 4 to 5 hours of the first day
- Financials arrive as PDFs to be copied by hand into a template whose formulas break
- An incomplete submission from the sponsor stalls him for 24 hours while his own deadline keeps moving
- Time spent on font consistency is time spent anticipating a reviewer's objection rather than answering it

*Grounded in:* `Sourcing crowds out analysis`, `Firm memory hunted manually`, `Deal terms trapped in documents`, `Email round-trips burn the deadline`, `One error voids the profile`

---

### The Credit Risk Reviewer · `secondary`

> If I catch an error like that, I lose trust in the whole profile.

The director who signs off — or does not — on the finished profile, in a 20 to 30 minute initial review that gates the Credit Committee date. Reads in a fixed order: total leverage ratio and how adjusted EBITDA was built, then liquidity runway across cash and revolver capacity, then the corporate structure and guarantee package. Skips the company history outright. Interviewed directly.

**Goals**

- Confirm in the first minutes who is actually on the hook for the debt and whether cash is leaking to unrated offshore subsidiaries
- Check an add-back or a pro-forma adjustment against its source without reopening the underlying agreement
- Complete an initial review in five minutes rather than thirty, with more confidence rather than less
- Return a defect without triggering a rework loop that moves the committee date

**Frustrations**

- Vendor pulls accepted without adjusting for pro-forma numbers from a recent acquisition
- Management EBITDA add-backs taken at face value — a 'one-time' fee that recurred three years running
- A single caught error costs her confidence in the whole file, not just the line it appeared on
- Static PDFs and Word documents that cannot be interrogated, so verification means reopening a 300-page agreement herself
- Fixing small defects personally to avoid a round of email that would cost more than the fix

*Grounded in:* `Deal terms trapped in documents`, `One error voids the profile`, `Email round-trips burn the deadline`

---

### The Managing Director · `secondary`

> We lose massive leverage by not knowing what the firm already knows.

Runs large-scale corporate lending and opportunistic credit, and carries the position after the deal is booked. Frames the team's constraint as speed and informational symmetry rather than capital allocation. Consumes the Associate's screening work as a decision input and the portfolio's risk posture as a standing feed. Interviewed directly. Deployment isolation is his stated precondition for adoption at all.

**Goals**

- Issue term sheets faster than competing lenders, because speed is what wins the deal in this market
- See what another desk already learned about a target at the moment of screening, not after
- Catch distress while a workout or refinancing can still be structured — see smoke before there is a fire
- Receive a risk signal that already contains the decision: the issue, the exposure, and the trigger point
- Keep proprietary deal data inside the firm's own cloud perimeter

**Frustrations**

- Initial vetting takes three days because the inputs are scattered across filings, private databases, relationship logs and macro feeds
- Another desk's prior coverage sits in a legacy PDF or a personal Outlook inbox, invisible exactly when it would create leverage
- Covenant compliance is keyed quarterly into spreadsheets, so a breach surfaces about three months after the fact
- Monitoring products present fifty simultaneous flags and leave the interpretation to him

*Grounded in:* `Firm memory hunted manually`, `Sourcing crowds out analysis`, `Late, undifferentiated risk signals`

---

## Current-state journey

One continuous path from assignment to post-close monitoring, crossing all three personas. Six of seven stages carry a high or medium drop-off risk.

| # | Stage | Emotion | Drop-off |
|---|---|---|---|
| 1 | Assignment and orientation (Associate) | Apprehension | `low` |
| 2 | Hunting internal precedent (Associate) | Low-grade doubt | `high` |
| 3 | Extracting terms from source documents (Associate) | Grinding | `high` |
| 4 | Modelling and thesis under a live clock (Associate) | Pressure | `high` |
| 5 | Risk review and verification (Credit Risk Reviewer) | Guarded | `high` |
| 6 | Defect return and rework loop (Reviewer and Associate) | Strain on both sides | `high` |
| 7 | Post-close portfolio monitoring (Managing Director) | Reactive | `medium` |

### 1. Assignment and orientation (Associate)

**Emotion:** Apprehension — the size of the build is clear before any of it is possible

**Drop-off risk:** `low`

*Actions*

- Receives the entity name and opens a tracking spreadsheet
- Checks Capital IQ and Bloomberg to establish whether the company is public or private
- Scopes how much of the structure will have to be built by hand

*Friction*

- No indication yet whether the firm has prior history with this name
- Coverage quality for a mid-market private borrower is unknown until he is already inside the vendor tools

### 2. Hunting internal precedent (Associate)

**Emotion:** Low-grade doubt — he cannot tell the difference between no history and history he failed to find

**Drop-off risk:** `high`

*Actions*

- Searches the internal CRM and Salesforce for the client, its sponsors and its subsidiaries
- Searches the credit document repository for prior agreements
- Asks colleagues informally where older coverage might sit

*Friction*

- Prior work stored in a personal Outlook inbox or a local drive is unreachable by any search he can run
- Another desk's coverage of a subsidiary two years ago is invisible unless someone remembers it

### 3. Extracting terms from source documents (Associate)

**Emotion:** Grinding — the work is legible as effort and illegible as judgment

**Drop-off risk:** `high`

*Actions*

- Parses hundreds of pages of PDF credit agreements and pitch books
- Traces the ultimate parent, co-issuers and guarantors and draws the org chart in PowerPoint
- Copies financials out of PDFs into the Excel template

*Friction*

- Four to five hours of the first day go to the org chart alone
- The template's formulas break under manual entry
- Nothing he transcribes carries a pointer back to the sentence it came from

### 4. Modelling and thesis under a live clock (Associate)

**Emotion:** Pressure — the analysis he was hired for begins on the second night

**Drop-off risk:** `high`

*Actions*

- Calculates leverage metrics and evaluates industry headwinds
- Writes the investment thesis
- Emails the deal team for a missing cash flow statement or footnotes and waits

*Friction*

- A sponsor reply can take 24 hours while his own deadline does not move
- He cannot chase the sponsor directly; the request routes through the deal team
- Formatting consumes time that anticipates an objection rather than answering it

### 5. Risk review and verification (Credit Risk Reviewer)

**Emotion:** Guarded — reading for the one thing that will invalidate the rest

**Drop-off risk:** `high`

*Actions*

- Reads total leverage ratio and interrogates the adjusted EBITDA add-backs
- Checks liquidity runway across cash and revolver capacity
- Examines the corporate structure and guarantee package for unrated offshore subsidiaries
- Skims past the company overview entirely

*Friction*

- Verifying any single number means reopening the 300-page agreement herself
- An unadjusted pro-forma pull or an unquestioned add-back costs her trust in the whole file
- Twenty to thirty minutes is spent establishing confidence rather than forming a view

### 6. Defect return and rework loop (Reviewer and Associate)

**Emotion:** Strain on both sides — she is spending her time on his work, he is redoing work he thought was finished

**Drop-off risk:** `high`

*Actions*

- Fixes minor formatting issues herself to avoid a round of email
- Returns the file when the leverage math is wrong
- Associate reworks against a deadline that has already partly elapsed

*Friction*

- Sign-off slips, the Credit Committee is postponed, and a live closing date comes into question
- The correction travels as email, so the cost of returning a defect is weighed against just absorbing it

### 7. Post-close portfolio monitoring (Managing Director)

**Emotion:** Reactive — informed of conditions that have already settled

**Drop-off risk:** `medium`

*Actions*

- Receives borrower-submitted covenant figures quarterly and has them keyed into spreadsheets
- Reviews compliance calculations at the quarterly cycle
- Scans monitoring dashboards for anything that warrants attention

*Friction*

- A breach or a dip in coverage ratios surfaces roughly three months after it happened, past the point where a workout can be structured
- Fifty simultaneous flags carry no ranking, no exposure figure and no distance to the covenant threshold

---

## How-Might-We statements

**1.** How might we make a firm's own prior contact with a target visible at the moment someone starts evaluating it, including the contact nobody remembers?

   *from* `Firm memory hunted manually`

**2.** How might we shorten the distance between a term written into a credit agreement and a number an analyst can act on?

   *from* `Deal terms trapped in documents`

**3.** How might we let a reviewer satisfy themselves that a figure is right without leaving the profile they are reading?

   *from* `One error voids the profile`

**4.** How might we keep the deal clock from being held hostage to a reply that has not arrived?

   *from* `Email round-trips burn the deadline`

**5.** How might we make a portfolio signal arrive early enough, and specific enough, to change what a Managing Director does that day?

   *from* `Late, undifferentiated risk signals`

Theme `Sourcing crowds out analysis` has no dedicated HMW — the contract caps the set at five, and that theme is the compound effect the other five relieve rather than an independent problem to solve.

---

## Gate result

**Tier 1 — 2 errors, both the authorized persona-count exception:** `Expected exactly 2 personas, found 3` and `Personas must be exactly one 'primary' and one 'secondary'`. Theme traceability, HMW prefixes, journey-stage count, HMW count and drop-off vocabulary all pass.

**Tier 2 — judge: 0.88** (threshold 0.75)

| Criterion | Weight | Score | Note |
|---|---|---|---|
| `persona_grounding` | 0.30 | 0.95 | All three personas were interviewed directly; every trait traces to a theme, every quote is verbatim. No described-but-not-interviewed persona in this run. |
| `hmw_quality` | 0.35 | 0.85 | Five well-formed, open statements, one per theme. #3 leans slightly solutioning in implying an in-context surface. |
| `journey_realism` | 0.35 | 0.85 | Emotions are drawn from described behaviour, not attributed sentiment. Stage 7 is a different lifecycle phase and user, so it reads as appended rather than continuous. |
