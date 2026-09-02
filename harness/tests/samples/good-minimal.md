# User Stories — Newsletter signup

_Generated: 2026-09-02 · Sources: samples/good-minimal (notes)_

## Personas
- **Visitor** — someone browsing the marketing site who is not yet a subscriber.

## Epic: Subscription

### US-1: Subscribe with an email address
**As a** visitor, **I want to** enter my email address and subscribe **so that I can** receive the newsletter.

**Acceptance criteria**
- Given I am on the signup form, when I enter a valid email and submit, then I see a confirmation message.
- Given I enter an invalid email, when I submit, then the form is rejected and the field is flagged.

**Priority:** High

### US-2: Confirm my subscription
**As a** visitor, **I want to** confirm my address via a link **so that I can** prove the address is mine.

**Acceptance criteria**
- Given I subscribed, when I open the confirmation email and click the link, then my subscription becomes active.
- Given the link is older than 24 hours, when I click it, then I am told it expired and offered a resend.

**Priority:** Medium

---

## Open questions
- Do we need double opt-in for GDPR, or is single opt-in acceptable for this market?
