# User Stories — <project / feature name>

_Generated: 2026-09-02 · Sources: samples/bad-placeholder (notes)_

## Personas
- **Operator** — a warehouse staff member fulfilling orders.

## Epic: <epic name>

### US-1: Scan an item
**As an** operator, **I want to** scan an item barcode **so that I can** confirm the right product was picked.

**Acceptance criteria**
- Given a pick list is open, when I scan a matching barcode, then the line is marked picked.
- Given I scan the wrong barcode, when it does not match, then I see an error and the line stays open.

**Priority:** High

---

## Open questions
- What handheld scanner models must be supported?
