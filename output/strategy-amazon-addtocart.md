# Strategy Definition — Amazon Add-to-Cart

Two personas, a six-stage current-state journey, and five How-Might-We statements, all derived
from the six themes in `discovery-synthesis-amazon-addtocart.json`. Only one person appears in the
corpus and a second is implied by the brief they set, so the secondary persona is the thinner of
the two — flagged below.

---

## Personas

### Primary — The Delegated Task Shopper

Working a storefront on someone else's behalf against an explicit brief: search a generic category,
pick the best option, add it to cart, stop before checkout. Knows the category by name but arrives
with no product in mind, and works in a browser window narrow enough that the buy box is clipped at
the right edge.

**Goals**
- Reach one defensible pick without reading ten thousand listings
- Keep the path from a search result to a cart as short as possible
- Get an unambiguous signal that the item actually landed in the cart
- Stay inside the brief and stop exactly where they were told to

**Frustrations**
- A shipping and pricing locale is substituted without being asked, and dismissing the banner does not undo it
- Pressing Enter opens the suggestion list instead of running the search
- Three different authority badges sit on three different products with nothing to rank them against each other
- Some listings hide the cart behind a "See options" detour and others do not
- The Add to Cart button is off-canvas, and once found it sits beside a Buy Now button that skips checkout entirely

> "Let me pull the full text of the results to compare more options"

*Grounded in:* Storefront guesses the wrong locale · Search stalls at the suggestion list ·
Competing badges replace a ranked answer · Variant picking is a hidden tax · Primary action sits
off-canvas · Confirmation closes the loop

### Secondary — The Absent Requester

The person the purchase is for, not at the keyboard. Sets the boundary of the task up front — add
to cart, do not check out — and reads the outcome afterwards, judging both the pick and whether the
boundary held. Learns about anything odd only in the closing summary.

**Goals**
- Understand why this item was chosen over the alternatives, not just that it was chosen
- Trust that the session stopped where they said it would stop
- See the price they would actually pay, in the currency they expect

**Frustrations**
- The locale and currency substitution surfaces only after the fact, as a closing flag
- The decision about which options were dropped for step count is made before they can weigh in
- Fixing the currency is handed back to them as an unstarted task

> "If you want USD pricing, that'd mean explicitly setting a US delivery address."

*Grounded in:* Storefront guesses the wrong locale · Variant picking is a hidden tax ·
Confirmation closes the loop

---

## Current-State Journey

| Stage | Emotion | Drop-off | Key friction |
|---|---|---|---|
| 1. Lands and gets redirected by geography | interrupted | low | Shipping/pricing context applied from detected location without being asked; the banner is dismissible but the INR pricing behind it is not |
| 2. Types the query and nothing happens | puzzled | low | Enter opens autocomplete instead of firing the search; the shopper must diagnose that nothing happened before recovering |
| 3. Faces ten thousand results | overwhelmed | **high** | No single authority to defer to — badges compete rather than rank; prices in INR on a US storefront; comparing properly means working outside the interface built to do it |
| 4. Re-ranks by proof instead of by badge | decisive | medium | Step count silently vetoes products never judged on merit; what each badge certifies is never explained |
| 5. Verifies the product and hunts for the button | obstructed | **high** | The one control the session exists to reach is outside the viewport; three recovery moves before it is clickable; Buy Now adjacent and must be consciously avoided |
| 6. Adds, confirms, and stops short | satisfied | low | The substituted currency survives into the subtotal; the locale problem is raised only after the task is done |

Emotion moves interrupted → puzzled → overwhelmed → decisive → obstructed → satisfied. The two
high-risk stages are both about *reaching* a decision or an action, not about the products
themselves.

---

## How Might We

1. **How might we let someone act on a storefront's assumption about where they are, at the moment that assumption changes what they see?** *(Lands and gets redirected by geography)*
2. **How might we help a shopper reach one defensible choice without leaving the results in order to compare them?** *(Faces ten thousand results)*
3. **How might we make competing trust signals mean something a shopper can actually weigh against each other?** *(Competing badges replace a ranked answer)*
4. **How might we keep the effort of reaching a cart from deciding which product wins?** *(Variant picking is a hidden tax)*
5. **How might we make sure the action a shopper came to take is never the hardest one to find?** *(Verifies the product and hunts for the button)*
