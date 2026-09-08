# Ideation & Concepting — Flight Booking

From the 5 HMWs in [strategy-flight-booking.md](strategy-flight-booking.md). RICE reach is
modeled on a stated assumption of ~50,000 travelers per quarter through the booking flow
(the corpus is a single walkthrough, so most confidence values are low). No winner is
selected here — a human picks the direction for Stage 4.

`rice = (reach x impact x confidence) / effort`

---

## Features, by RICE score

| # | Feature | HMW | Reach | Impact | Conf. | Effort | RICE |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | Price-first default sort | H2 | 50,000 | 2 | 0.8 | 0.5 | **160,000.0** |
| 2 | Neutral decline language | H5 | 50,000 | 1 | 0.8 | 0.5 | **80,000.0** |
| 3 | Symmetric accept/decline controls | H5 | 50,000 | 2 | 0.8 | 1.5 | **53,333.3** |
| 4 | Running trip-cost card | H1 | 50,000 | 3 | 0.8 | 3.0 | **40,000.0** |
| 5 | All-in price toggle | H1 | 50,000 | 3 | 0.8 | 4.0 | **30,000.0** |
| 6 | Cheaper-nearby-date nudge | H2 | 40,000 | 2 | 0.5 | 2.0 | **20,000.0** |
| 7 | Inline what's-included strip | H2 | 50,000 | 1 | 0.8 | 2.0 | **20,000.0** |
| 8 | Mixed-carrier risk flag | H4 | 50,000 | 1 | 0.5 | 1.5 | **16,666.7** |
| 9 | Return options shown as totals | H4 | 50,000 | 1 | 0.5 | 1.5 | **16,666.7** |
| 10 | Fix "Continue without bags?" copy | H3 | 15,000 | 0.5 | 1.0 | 0.5 | **15,000.0** |
| 11 | One-time traveler profile | H1 | 50,000 | 2 | 0.5 | 5.0 | **10,000.0** |
| 12 | Single pricing source of truth | H3 | 20,000 | 2 | 0.8 | 6.0 | **5,333.3** |

**HMW key** — H1: see the real price before committing to a fare · H2: surface the choices that
most affect price · H3: keep cost info consistent and trustworthy · H4: weigh a cheaper option
against its trade-offs · H5: a pressure-free way to decline add-ons.

### Feature detail

1. **Price-first default sort** — Change the default results sort from Recommended to Price
   low-to-high, with the previous sort one tap away.
2. **Neutral decline language** — Replace the self-incriminating insurance decline copy with a
   factual statement of the choice, shown alongside the 24-hour free-cancellation fact.
3. **Symmetric accept/decline controls** — Render decline and accept as equal-weight controls on
   interstitials, insurance, and SMS opt-in, with no pre-checked boxes.
4. **Running trip-cost card** — A persistent breakdown of fare plus seat, bags, and fees, visible
   from results through checkout, updating as choices change.
5. **All-in price toggle** — A results-page control that recalculates every fare to include a
   typical carry-on and seat so shown prices reflect what a normal traveler pays.
6. **Cheaper-nearby-date nudge** — Inline banner on results when a date within a few days is
   materially cheaper, showing the delta.
7. **Inline what's-included strip** — Move the fare-structure disclosure out of the sidebar onto
   every result card (carry-on / seat / change-fee).
8. **Mixed-carrier risk flag** — When a selection would combine two airlines, show a plain-language
   note about separate rebooking and delay liability before it is added.
9. **Return options shown as totals** — Display the full itinerary total on each return option,
   with the delta kept as a smaller secondary number.
10. **Fix "Continue without bags?" copy** — Make the dialog reflect actual cart contents (carry-on
    included) instead of a hardcoded incorrect string.
11. **One-time traveler profile** — Traveler states baggage/seat/flexibility needs once; the system
    marks which fare class is cheapest for them.
12. **Single pricing source of truth** — One service computes every price shown on the fare panel,
    bags page, and checkout so figures never disagree.

---

## Design Directions — pick one for Stage 4

### A. The number is the number

The core failure is the displayed price itself. Make every price shown, from the first results
screen on, an all-in figure that includes what a typical traveler buys — the system assembles
that realistic bundle, not the user.

- **Only this direction:** no price anywhere in the flow excludes carry-on and seat by default;
  headline figure and paid figure are the same number.
- **Addresses:** H1, H2, H3
- **Trade-off:** All-in prices look higher than competitors' headline fares, which can hurt
  comparison-shopping conversion; travelers who want the bare à la carte fare lose the
  stripped-down view.

### B. Guided fare coach

Travelers cannot be expected to decode fare structure. Ask a few questions up front (bags, seat,
flexibility), then steer the traveler to the right fare class and date, collapsing the fare-panel
decision into a recommendation.

- **Only this direction:** the product makes the fare-class and date call on the traveler's
  behalf instead of presenting options to compare.
- **Addresses:** H1, H2, H4
- **Trade-off:** Adds an upfront step; the fare-structure scrutinizer feels railroaded and
  distrusts a flow that decides for them; a wrong recommendation damages trust more than a
  confusing menu would.

### C. Honest broker checkout

The damage is concentrated in the back half of the flow. Leave search and results mostly alone;
rebuild fare-selection-through-checkout around consistent totals, symmetric accept/decline
choices, and explicit trade-off disclosure.

- **Only this direction:** scope is deliberately limited to the decision and confirmation steps;
  discovery is treated as good enough.
- **Addresses:** H3, H4, H5
- **Trade-off:** Does nothing for the traveler who overpays at the results stage by keeping the
  default date and sort — leaves the two highest-severity themes only partly addressed.

---

### The bet, in one sentence each

| | Central bet | Who does the work |
|---|---|---|
| **A** | The number on screen must equal the number you pay | System (bundles a realistic profile) |
| **B** | The user shouldn't have to understand fares at all | System (recommends fare + date) |
| **C** | Discovery is fine; trust breaks at decision + checkout | Shared — user still chooses, with honest information |

A and B disagree on how much to automate for the scrutinizer persona; C disagrees with both on
where the problem even is.
