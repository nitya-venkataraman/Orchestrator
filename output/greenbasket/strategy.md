# Strategy Definition — GreenBasket

*Stage 2 · Superlap UX pipeline · judge 0.89*

## Personas

### The Sunday-night reorder — PRIMARY

45, parent of young kids. Runs a weekly Ocado main shop and treats GreenBasket as a veg-and-bakery top-up, ordering late on Sunday after the kids are asleep — the only free time in his week. Very low tolerance for app friction; has already cancelled GreenBasket once.

**Goals**
- Recreate last week's basket with a few swaps in a couple of taps, not eleven minutes of searching
- Know whether delivery lands morning or afternoon so it fits around the household's week
- Keep buying the better-quality produce without the ordering feeling like work
- Never be surprised by what's in the box on delivery day

**Frustrations**
- No reorder or buy-again — every staple is searched and re-added one at a time each week
- Out-of-stock items are swapped silently, discovered only when unpacking
- 'Monday' is the whole delivery window; no AM/PM and no update when it slips
- One more bad order and he's back to Ocado full-time

> "I timed it last Sunday. Eleven minutes. Eleven minutes to order essentially the same things I ordered the week before."

*Grounded in: Weekly reorder rebuilt by hand, Silent substitutions with no control, Delivery timing left unsaid, GreenBasket is the side shop*

### The market-stall seeker — SECONDARY

31, works in marketing at a B Corp. Shops across GreenBasket, Abel & Cole and Sainsbury's and has built a spreadsheet to compare them. Wants online grocery to feel like her Saturday trip to Broadway Market — seasonality, producer stories, a sense of discovery — and would consolidate onto GreenBasket if the range allowed.

**Goals**
- Be inspired while browsing, not just work through a list
- See and share the producers and stories behind the food
- Feel a personal sustainability impact that builds over time
- Consolidate onto one grocery service and drop the comparison spreadsheet

**Frustrations**
- Browse is an unsorted grid with no seasonal or editorial layer; search is the only reliable path
- Producer stories are buried in the blog and there's nothing shareable
- The Impact Score is a context-free number that makes her feel nothing
- Thin staples range keeps her tied to other retailers

> "it was like someone had built a gorgeous storefront and then put a spreadsheet inside it."

*Grounded in: Storefront with no editorial layer, Impact Score means nothing, GreenBasket is the side shop*

## Current-state journey

### 1. Remembering to order  ·  *reluctant*  ·  dropoff: medium

Actions: Realise GreenBasket hasn't been done this week; Open the app late on Sunday once the kids are asleep

Friction:
- No booked slot or recurring order, so it slips a day or more
- Competes with the only free hour of the week

### 2. Rebuilding last week's basket  ·  *exasperated*  ·  dropoff: high

Actions: Look for order history, give up digging for it; Search each staple individually and add it to the cart

Friction:
- No reorder, buy-again, or 'my regulars' list
- Roughly eleven minutes to reassemble a near-identical order

### 3. Filling the gaps elsewhere  ·  *resigned*  ·  dropoff: medium

Actions: Note the staples GreenBasket doesn't carry; Plan a separate Ocado or Sainsbury's order for the rest

Friction:
- Thin range means GreenBasket can only ever be a partial shop
- Managing a split basket across two or three retailers

### 4. Looking for something new  ·  *curious*  ·  dropoff: medium

Actions: Check the homepage for anything changed; Scroll the category grid, then fall back to search

Friction:
- No seasonal or editorial layer; the grid is the same every week
- Producer stories are hidden in the blog, not in the browse flow

### 5. Checking out and picking a slot  ·  *uneasy*  ·  dropoff: low

Actions: Review the cart; Choose a delivery day and place the order

Friction:
- Delivery is a day only, no morning/afternoon choice
- No visibility into how a missing item will be handled

### 6. Waiting for delivery  ·  *anxious*  ·  dropoff: medium

Actions: Track the order; Re-plan meals if it looks late

Friction:
- No proactive message when an order slips — up to 36 hours of silence
- ETA never narrows from the original day

### 7. Unpacking the order  ·  *torn*  ·  dropoff: high

Actions: Unpack and notice any substitutions; Glance at the Impact Score

Friction:
- Silent swaps — drumsticks for thighs, sliced white for sourdough — undercut real delight in the produce quality
- The Impact Score is a number with no context, so the order's benefit is invisible

## How Might We

1. How might we let a returning shopper recreate their usual order without hunting down each item?  
   *from: Rebuilding last week's basket*
2. How might we keep shoppers in control when something they wanted turns out to be unavailable?  
   *from: Silent substitutions with no control*
3. How might we make a delivery's timing predictable enough to plan a household around?  
   *from: Delivery timing left unsaid*
4. How might we help shoppers feel what their order achieved without asking them to interpret a score?  
   *from: Impact Score means nothing*
5. How might we make browsing feel like discovering a market rather than scanning a list?  
   *from: Storefront with no editorial layer*
