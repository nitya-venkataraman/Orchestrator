# User Stories — Online flight booking flow (NYC → ATL walkthrough)

_Generated: 2026-09-02 · Sources: Pasted narrative — flight-booking walkthrough (NYC→ATL, Fri Sep 25 – Mon Sep 28, 1 adult, economy): section 1 Search form, section 2 Results page, section 3 Picking the outbound, section 4 Return leg, section 5 Bundle interstitial, section 6 Checkout (Your flights / Seats / Bags / Checkout), and the closing "true cost" summary._

## Personas
- **Traveler** — someone booking a round-trip economy flight for themselves.
- **Price-sensitive traveler** — compares fares, add-ons, and total cost closely before booking.
- **Flexible-date traveler** — can shift departure or return dates to get a lower fare.

---

## Epic: Searching for a trip

### US-1: Clear a pre-filled origin
**As a** traveler, **I want to** clear the geolocation-guessed origin in one step **so that I can** enter my real departure city without the two values merging.

**Acceptance criteria**
- Given the origin field is pre-filled from my location, when I use the field's clear control, then the field is emptied completely.
- Given the origin field already holds a value, when I start typing a new city, then my text replaces the existing value instead of being appended to it.
- Given the guessed origin is wrong, when I view the search form, then the origin field is editable rather than locked.

**Priority:** High  ·  **Notes:** In the walkthrough the field was pre-filled with Singapore (SIN) and typing appended text, forcing a manual clear.

### US-2: Search every airport in a metro area
**As a** price-sensitive traveler, **I want to** choose a whole metro area as my origin **so that I can** let all nearby airports compete in one price list.

**Acceptance criteria**
- Given I type a city served by several airports, when I view the origin suggestions, then an "All Airports" option for that city is offered.
- Given I pick the "All Airports" origin, when results load, then flights from each airport in the metro area appear together in one list.
- Given I chose an all-airports origin, when I read a result, then the specific departure airport for that flight is shown.

**Priority:** Medium

### US-3: Limit results to nonstop flights
**As a** traveler, **I want to** restrict results to nonstop flights **so that I can** avoid connections on both legs.

**Acceptance criteria**
- Given results include nonstop and one-stop flights, when I apply the nonstop filter, then only nonstop itineraries remain.
- Given the nonstop filter is available, when I view it, then the number of nonstop options is shown before I apply it.

**Priority:** Medium

---

## Epic: Understanding the price before choosing

### US-4: Compare fares across nearby dates
**As a** flexible-date traveler, **I want to** see the lowest fare for each date around my trip **so that I can** move my dates to a cheaper day.

**Acceptance criteria**
- Given I am on the results page, when I view the flexible-dates strip, then each date shows its lowest available fare.
- Given prices vary sharply within one week (for example $172 one day and $1,030 another), when I select a different date in the strip, then results refresh for that date.
- Given my current dates are selected, when I view the strip, then those dates are highlighted with their price.

**Priority:** High

### US-5: See what each price tier includes
**As a** price-sensitive traveler, **I want to** see what is bundled at each price level on the results page **so that I can** understand the cheapest fare's limits before I click it.

**Acceptance criteria**
- Given the lowest fare starts at $205, when I view the price breakdown, then it states that this fare has no carry-on and no seat selection.
- Given "carry-on included" and "seat choice included" start at higher prices, when I view the breakdown, then each option is shown with its own starting price.
- [ ] The lowest advertised price is displayed next to the restrictions that make it the lowest.

**Priority:** High

### US-6: Sort results by price
**As a** price-sensitive traveler, **I want to** sort results by price **so that I can** see the cheapest options first.

**Acceptance criteria**
- Given results default to "Recommended" order, when I switch the sort to "Price", then results reorder from cheapest to most expensive.
- Given I have sorted by price, when results reload for a different date, then the price sort is kept.

**Priority:** Medium  ·  **Notes:** Default sort in the walkthrough was "Recommended", not price.

### US-7: See how the price compares to typical for the route
**As a** price-sensitive traveler, **I want to** see my itinerary's price compared with what is typical for the route **so that I can** judge whether to book now.

**Acceptance criteria**
- Given I view my selected itinerary, when the price summary loads, then it labels the fare as low, typical, or high for the route.
- Given the fare is labelled "typical", when I read the label, then it explains that the comparison is based on recent prices for the same route.

**Priority:** Low

---

## Epic: Choosing a fare class

### US-8: Compare fare classes for a selected flight
**As a** price-sensitive traveler, **I want to** compare the fare classes offered for a flight **so that I can** see what each extra dollar buys.

**Acceptance criteria**
- Given I select a flight, when the fare-class panel opens, then each fare lists its price and what it includes.
- Given the cheapest fare costs less than the next one up, when I read the panel, then it states that the cheapest fare charges extra for a seat and applies a change fee.
- Given a refundable fare exists, when I read the panel, then it is identified as refundable and priced.

**Priority:** High  ·  **Notes:** Walkthrough fares: Main Base $291, Main $331, Even More $400, Main Flex $598 (refundable).

### US-9: Know when a fare choice re-prices the whole trip
**As a** traveler, **I want to** be told that picking a fare applies it to every leg **so that I can** avoid being surprised when my outbound price changes.

**Acceptance criteria**
- Given I am choosing a fare on one leg, when the fare panel is shown, then it states that all flights will be updated to match the selected fare.
- Given I pick a higher fare on the return, when the itinerary updates, then the outbound price changes to match and the new total is shown.

**Priority:** Medium

---

## Epic: Building the itinerary

### US-10: See the running total while picking the return
**As a** price-sensitive traveler, **I want to** see the resulting trip total on each return option, not just the price change **so that I can** know what I will actually pay.

**Acceptance criteria**
- Given return fares are shown as deltas such as "+$71", when I view a return option, then the resulting itinerary total is also shown.
- Given I select a return flight, when the itinerary summary updates, then it shows the combined total for both legs.

**Priority:** Medium

### US-11: Be warned about a mixed-carrier itinerary
**As a** traveler, **I want to** be warned when I combine flights from different airlines **so that I can** understand that neither airline is responsible for the other's delays.

**Acceptance criteria**
- Given a cheaper return is operated by a different airline, when I view that option, then it is flagged as a separate-airline itinerary.
- Given I select flights from two airlines, when I continue, then a note explains that a disruption on one airline may not be rebooked by the other.

**Priority:** Medium  ·  **Notes:** In the walkthrough a Frontier return showed "+$0" but would have created a mixed-carrier trip.

---

## Epic: Add-ons, seats, and bags

### US-12: Decline a bundle offer and continue
**As a** traveler, **I want to** dismiss a full-screen bundle offer easily **so that I can** continue booking the flight on its own.

**Acceptance criteria**
- Given a full-screen "flight + car" bundle interstitial appears, when I look for the decline option, then a clearly labelled decline control is visible without scrolling.
- Given I decline the bundle, when the interstitial closes, then I return to the booking flow at the step I left.
- [ ] The decline control is not presented only as a low-contrast text link beneath the accept button.

**Priority:** Medium

### US-13: See seat-selection costs before committing to a fare
**As a** price-sensitive traveler, **I want to** know the seat fees for a fare before I book it **so that I can** judge the fare's true cost.

**Acceptance criteria**
- Given I have selected a fare, when I open the seat map, then the price of every selectable seat is shown.
- Given the fare has no free seats anywhere in the cabin, when I scroll the full seat map, then this is stated plainly rather than left for me to infer.
- Given I do not want to pay for a seat, when I skip seat selection, then I am told a seat will be assigned at check-in at no charge.

**Priority:** High  ·  **Notes:** In the walkthrough every seat was $36–$94, with none free as far back as row 27.

### US-14: Budget checked-bag fees from a consistent figure
**As a** price-sensitive traveler, **I want to** see baggage fees expressed consistently across screens **so that I can** budget without converting per-direction and round-trip numbers.

**Acceptance criteria**
- Given checked bags cost extra, when I view baggage prices on any screen, then each price is labelled as either per-direction or round-trip.
- Given one screen showed "$49" and another "from $95", when I compare them, then both state the same trip scope so the figures reconcile.

**Priority:** Medium

### US-15: Get an accurate "continue without bags" confirmation
**As a** traveler, **I want to** see a skip-bags confirmation that describes what my trip actually includes **so that I can** avoid being misled into thinking I have no carry-on.

**Acceptance criteria**
- Given my fare includes a carry-on, when the "Continue without bags?" dialog appears, then it says my carry-on is included and only checked bags are omitted.
- Given the dialog summarises my baggage, when I read it, then it does not contradict the baggage summary on the page behind it.

**Priority:** High  ·  **Notes:** The walkthrough's confirmation claimed the trip had "no carry-on or checked bags", which was wrong.

---

## Epic: Checkout and policies

### US-16: Provide passenger details that match my ID
**As a** traveler, **I want to** enter my passenger and contact details in the checkout step **so that I can** have a booking that matches my travel document.

**Acceptance criteria**
- Given I reach the checkout step, when I fill the passenger form, then it collects legal name, gender, and date of birth as shown on my photo ID.
- Given a name must match my document, when I enter it, then on-screen guidance says it must match my government photo ID.
- Given contact and billing details are required, when I complete the form, then email, phone, and full billing address are captured.

**Priority:** High

### US-17: Make an informed choice about trip insurance
**As a** price-sensitive traveler, **I want to** accept or decline trip insurance as an explicit choice **so that I can** avoid being charged for it by default.

**Acceptance criteria**
- Given trip insurance costs $26.23, when I reach that step, then neither "add" nor "decline" is pre-selected.
- Given I decline insurance, when I continue, then I must actively acknowledge that my non-refundable booking is unprotected.
- Given I have not chosen either option, when I try to proceed, then I cannot continue until I choose.

**Priority:** Medium

### US-18: Opt in to SMS alerts rather than opt out
**As a** traveler, **I want to** have SMS alert checkboxes start unchecked **so that I can** receive only the messages I chose.

**Acceptance criteria**
- Given the checkout page offers SMS alerts, when the page loads, then the SMS-alerts checkbox is unchecked.
- Given I want SMS alerts, when I tick the box, then I am opted in.

**Priority:** Medium  ·  **Notes:** In the walkthrough this checkbox was pre-ticked.

### US-19: Review change and cancellation terms before paying
**As a** traveler, **I want to** see the fare's cancellation and change terms before payment **so that I can** know my obligations if my plans change.

**Acceptance criteria**
- Given the fare is non-refundable, when I view the checkout summary, then it states the ticket is non-refundable and that the change fee is $150 per ticket.
- Given free cancellation is available within 24 hours of booking, when I read the terms, then the length of that window and its cutoff are stated.

**Priority:** High

---

## Epic: Comparing the true cost

### US-20: Compare fares on a realistic all-in price
**As a** price-sensitive traveler, **I want to** see an estimated total that already includes a checked bag and a seat **so that I can** compare a cheap fare against an inclusive fare fairly.

**Acceptance criteria**
- Given a basic fare excludes a seat and a checked bag, when I view it next to the inclusive fare, then an all-in estimate adds a representative seat and checked-bag cost.
- Given the inclusive fare includes a seat and changes, when I compare all-in totals, then the comparison shows which fare is cheaper once likely extras are added.
- [ ] The all-in estimate states which extras it assumes (one checked bag and one standard seat).

**Priority:** High  ·  **Notes:** In the walkthrough the $361.79 basic fare rises to roughly $493 with a bag and a seat, above the inclusive "Main" fare.

---

## Open questions
- Which booking platform is this? The stories are written platform-neutrally; the target site/app should be confirmed.
- Is the "All Airports" behaviour (fares from every metro-area airport competing in one list) expected for all multi-airport cities, or only some?
- The baggage figures conflict: is "$49" per direction and "$95" round trip, or is one of them wrong? This must be resolved before writing the reconciliation rule in US-14.
- "All flights will be updated to match your fare selection" — can travelers mix fare classes across legs at all, or is one fare class enforced for the whole trip?
- Are the trip-insurance price ($26.23) and the $150-per-ticket change fee fixed, or do they vary by itinerary?
- For US-20, how many representative extras should the all-in estimate assume — always one bag and one seat, or a configurable set?
- The inputs say nothing about accessibility (keyboard and screen-reader support) for the seat map, the flexible-dates strip, or the bundle interstitial. What is the required standard?
- Should the decline control on interstitials (US-12) be a full button rather than a text link? This is a design decision for the team.
