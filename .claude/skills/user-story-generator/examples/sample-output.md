# User Stories — Expense Tracker mobile app

_Generated: 2026-09-02 · Sources: examples/sample-input.md (kickoff call notes)_

## Personas
- **Employee** — submits expense claims while travelling or in office.
- **Manager** — reviews and approves their team's claims.
- **Finance team member (Sarah)** — processes approved claims and feeds accounting.

## Epic: Claim submission

### US-1: Submit a receipt from mobile
**As an** employee, **I want to** capture a receipt photo and submit a claim from my phone **so that I can** stop emailing receipts and re-keying them later.

**Acceptance criteria**
- Given I have a claim in progress, when I attach a photo and enter amount, date, and category, then I can submit it.
- Given a required field is empty, when I tap Submit, then submission is blocked and the missing field is highlighted.
- Given a claim is submitted, then it appears in my claims list with status "Pending approval".

**Priority:** High

### US-2: Create claims offline
**As an** employee, **I want to** create and queue claims without a network connection **so that I can** log expenses while travelling.

**Acceptance criteria**
- Given I have no connectivity, when I create a claim, then it is saved locally and marked "Not synced".
- Given connectivity is restored, when the app next opens or refreshes, then queued claims upload automatically and status updates.
- Given a sync conflict or failure, then the claim stays local and I see a retry option.

**Priority:** High

---

## Epic: Approval

### US-3: Approve or reject team claims
**As a** manager, **I want to** review my team's submitted claims and approve or reject each one **so that I can** control spend before it reaches finance.

**Acceptance criteria**
- Given a claim is submitted by my report, when I open my approvals queue, then I see the claim with receipt, amount, and category.
- Given I approve a claim, then its status becomes "Approved" and it enters the finance queue.
- Given I reject a claim, when I add a reason, then the employee is notified and the claim returns to them as "Rejected".

**Priority:** High

---

## Epic: Visibility

### US-4: Track claim status
**As an** employee, **I want to** see the current status of each claim **so that I can** know whether it has been approved and paid without chasing anyone.

**Acceptance criteria**
- Given I open my claims list, then each claim shows one of: Pending approval, Approved, Rejected, Paid.
- Given a claim's status changes, then I receive a notification.

**Priority:** Medium

---

## Epic: Finance processing

### US-5: Export approved claims to CSV
**As a** finance team member, **I want to** export approved claims as a CSV file **so that I can** import them into the accounting system without manual entry.

**Acceptance criteria**
- Given one or more approved claims exist, when I choose Export, then a CSV downloads containing employee, date, amount, category, and approval date.
- Given I have already exported a claim, then it is marked "Exported" and excluded from the default next export.

**Priority:** Medium

---

## Open questions
- Mileage claims were raised but not decided — are distance-based claims in scope for this release?
- Who marks a claim "Paid" — is it manual in the app, or driven by the accounting system?
- Are there per-category or per-claim spend limits that should trigger extra approval?
