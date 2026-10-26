# Discovery Synthesis — Travel Booking Walkthrough

**Corpus:** 1 source (a single annotated booking walkthrough: NYC→ATL, Sep 25–28, JetBlue, $361.79).
Every theme below is `frequency: 1` because one person produced this teardown.

---

## Themes

### 1. True cost hidden in skippable panels — severity: high

To learn what the trip really costs, the traveler has to dig through a left sidebar and a
fare-class panel the flow lets you skim past. The $205/$361 headline carries no carry-on, no
seat, and no checked bag; the real total is nearer **$493** — the point at which the pricier
bundled "Main" fare would have been the better buy.

- "So the $205 headline is a fare with no carry-on and no seat." *(Results / left sidebar)*
- "Clicking it opens a fare-class panel — this is the step people skim past" *(Picking the outbound)*
- "I scrolled to row 27 and there was not one free seat on this fare." *(Checkout / Seats)*
- "total $361.79, flagged as \"typical\" for this route." *(Checkout / Your flights)*
- "that $361.79 is not what this trip costs if you're a normal traveler." *(closing flag)*
- "at which point the $331 \"Main\" fare, which includes the seat, was the better buy from the start." *(closing flag)*

### 2. Price levers aren't the default view — severity: high

The two controls that move price the most — shifting dates on the flexible-dates strip and
re-sorting by price instead of "Recommended" — are both off by default. A traveler who touches
neither can pay several times more for the same route in the same week.

- "Sep 23 was $172, my Sep 25 was $205, and Sun Sep 27 was **$1,030**." *(flexible-dates strip)*
- "If your dates move at all, this strip is the highest-leverage thing on the page." *(flexible-dates strip)*
- "Default sort is \"Recommended,\" not price. I'd switch that." *(Results page)*

### 3. Return-leg screen changes the rules — severity: medium

On the return leg the traveler has to re-read the screen: it now shows price *deltas* instead of
totals, dangles a "+$0" option that would split the booking across two airlines, and only a
small warning notes that picking a fare re-prices the outbound too.

- "Prices show as *deltas* now, not totals." *(Return leg)*
- "that would have made it a mixed-carrier itinerary, where a delay on one airline isn't the other's problem." *(Return leg)*
- "so choosing a nicer fare here re-prices the outbound too." *(Return leg)*

### 4. Upsell nudges shape the defaults — severity: medium

At each decision point the traveler has to hunt for the free or decline option: a full-screen
bundle interstitial hides "No thanks" as a text link, trip insurance forces an explicit
self-incriminating opt-out, and the SMS-alerts box is pre-checked.

- "\"No thanks\" is a text link under the blue button." *(Bundle & Save modal)*
- "you must actively tick \"I understand my $361.79 non-refundable flight booking won't be protected.\"" *(Checkout / insurance)*
- "The SMS-alerts checkbox is pre-ticked." *(Checkout)*
- "Fine print: nonrefundable, $150/ticket change fee, free cancellation within 24 hours of booking." *(Checkout)*

### 5. Cost figures contradict across steps — severity: medium

No single cost figure can be taken at face value because the screens disagree — checked bags
read "$95 roundtrip" in one place and "$49" per direction in another, and a "Continue without
bags?" dialog wrongly says the trip has no carry-on.

- "Watch this number — the fare panel said \"$49,\" which is per direction." *(Checkout / Bags)*
- "the \"Continue without bags?\" confirmation claims your trip has \"no carry-on or checked bags,\" which contradicts the page above it." *(Checkout / Bags)*
- "It's wrong; your carry-on is included." *(Checkout / Bags)*

### 6. Search form defaults fight the user — severity: low

Setting up the search takes corrective work: the origin field pre-fills the wrong city from
geolocation and appends rather than replaces typed input, and the traveler has to know to pick
"All Airports" so nearby airports compete.

- "typing over it appends rather than replaces. I had to hit the X first." *(Search form)*
- "rather than a single airport, which is what lets JFK, LGA and EWR compete in one list." *(Search form)*

---

## Gaps

- **One expert participant.** They already reason about fare classes and mixed-carrier risk — no
  evidence of how the "normal traveler" the conclusion rests on actually behaves.
- **Single session, single path.** One route (NYC→ATL), one date range, one airline, one site —
  no basis for saying the pricing structure or patterns generalize.
- **Checkout never completed.** The walkthrough describes the checkout screen but never submits
  payment or reaches confirmation; final steps and post-purchase friction are unobserved.
- **No think-aloud / emotional data.** It's an annotated teardown, so we don't know where the
  user actually hesitated, felt anxious, or nearly abandoned.
- **No metrics or competitive baseline.** No time, clicks, errors, or completion data, and no
  comparison with other sites — severities are judgment, not measurement.
- **Desktop only.** No mobile, tablet, or accessibility observations.
- **Untested assertions.** Claims that the flexible-dates strip and sort control behave as
  expected come from inspection, not testing.
- **Internal inconsistency in the source.** The return leg reads "$361.80" while the running
  total reads "$361.79."
