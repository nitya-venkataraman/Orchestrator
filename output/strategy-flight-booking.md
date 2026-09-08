# Strategy Definition — Flight Booking

Derived from the 6 discovery themes ([discovery-synthesis-flight-booking.md](discovery-synthesis-flight-booking.md)).
One expert source, so personas carry inferred traits only where a theme names them
("a normal traveler," the fare-panel scrutiny).

---

## Personas

### Primary — The headline-fare traveler

Books a round-trip economy flight for one adult, working from the advertised fare and expecting
that number to be close to the final price.

- **Goals:** Book the cheapest workable round-trip · Know the real all-in total before paying ·
  Not overpay by choosing the wrong fare tier
- **Frustrations:** Headline fare excludes carry-on, seat, and bags — clear only deep in the flow ·
  The cheapest fare can cost more than a higher tier once seats/bags are added · Same charge shown
  differently on different screens · Add-ons arrive pre-checked with decline links hidden
- **Quote:** "that $361.79 is not what this trip costs if you're a normal traveler."
- **Grounded in:** True cost hidden in skippable panels · Price levers aren't the default view ·
  Upsell nudges shape the defaults · Cost figures contradict across steps

### Secondary — The fare-structure scrutinizer

Opens the fare-class panel instead of skimming it; weighs trade-offs like a split-airline
itinerary before committing. Their need for full visibility constrains how much the flow can be
simplified.

- **Goals:** Keep full visibility into fare structure and change/refund rules · Avoid itineraries
  that split delay risk across two airlines · Control which airports and fare class are in play
- **Frustrations:** Search form resists correction (geolocation append, single-airport default) ·
  Return leg switches to deltas and silently re-prices the outbound · Cheapest return quietly
  creates a mixed-carrier itinerary with no flag
- **Quote:** "that would have made it a mixed-carrier itinerary, where a delay on one airline
  isn't the other's problem."
- **Grounded in:** Return-leg screen changes the rules · Search form defaults fight the user ·
  True cost hidden in skippable panels · Price levers aren't the default view

---

## Current-State Journey

| Stage | Emotion | Drop-off | Key friction |
|---|---|---|---|
| 1. Set up the search | wary | low | Origin pre-filled with wrong city, appends instead of replacing; single-airport default silently narrows results |
| 2. Scan the results | skeptical | medium | Defaults to "Recommended" not price; real fare structure buried in the sidebar; same week swings $172 to $1,000+ |
| 3. Pick the outbound fare | cautious | medium | Fare-class panel is "the step people skim past"; cheap fare's true cost not obvious when choosing it |
| 4. Choose the return | confused | medium | Pricing switches to deltas; cheapest option splits carriers; picking a fare re-prices the outbound |
| 5. Dismiss the upsell | annoyed | low | Full-screen bundle interstitial; "No thanks" is a text link under the blue button |
| 6. Add seats and bags | frustrated | high | No free seat anywhere ($36-$94); bag price "$95 roundtrip" vs "$49" per direction; "Continue without bags?" dialog is wrong |
| 7. Check out | distrustful | medium | Forced insurance choice with self-incriminating decline; SMS box pre-ticked; nonrefundable + $150 change fee |

Emotion arc: wary -> skeptical -> cautious -> confused -> annoyed -> **frustrated** -> distrustful.
The break point is stage 6.

---

## How Might We

1. **How might we help a traveler see the price they will actually pay before they commit to a
   fare?** — from "Pick the outbound fare"
2. **How might we surface the choices that most affect price so a traveler does not miss them by
   accepting the defaults?** — from "Scan the results"
3. **How might we keep cost information consistent and trustworthy as a traveler moves through the
   booking?** — from "Add seats and bags"
4. **How might we let a traveler weigh a cheaper option against its trade-offs, such as a
   split-airline itinerary?** — from "Choose the return"
5. **How might we give a traveler a clear, pressure-free way to decline add-ons they do not
   want?** — from "Dismiss the upsell"
