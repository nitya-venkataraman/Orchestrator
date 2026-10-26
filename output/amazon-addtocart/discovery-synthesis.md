# Discovery Synthesis — Amazon Add-to-Cart Walkthrough

**Corpus:** 1 source (a single narrated desktop session: land on amazon.com → search
"colored pencils" → compare results → open the Crayola 36ct product page → add to cart, stopping
before checkout). Every theme below is `frequency: 1` because one session produced all of it,
and it was driven by an AI agent on the shopper's behalf rather than by a human participant.

---

## Themes

### 1. Storefront guesses the wrong locale — severity: high

The shopper lands on amazon.com and the site silently substitutes an India shipping-and-pricing
context it inferred from location. The banner announcing it reads as an interruption and gets
dismissed, but the substituted currency survives the dismissal — it follows the shopper through
search, the product page, and the cart subtotal. By the end of the session the shopper knows what
would fix it and still has not fixed it.

- "We're showing you items that ship to India" *(Landing / location banner)*
- "I notice prices are showing in INR even on amazon.com — likely due to my detected location, a minor quirk I'll flag." *(Results page)*
- "that's Amazon auto-detecting my location and showing India pricing/shipping rather than USD, not something I changed" *(Closing flag)*
- "If you want USD pricing, that'd mean explicitly setting a US delivery address." *(Closing flag)*

### 2. Search stalls at the suggestion list — severity: medium

Committing the query with Enter opens the autocomplete list instead of running the search. The
shopper has to notice that nothing happened, then click their own words back out of the dropdown
before any results exist.

- "I see a dropdown of autocomplete suggestions appeared instead of the search actually firing" *(Search)*
- "hitting Enter actually triggered Amazon's autocomplete dropdown rather than firing the search directly" *(Recap step 2)*
- "Small UX quirk worth knowing about when automating Amazon." *(Recap step 2)*

### 3. Competing badges replace a ranked answer — severity: high

Ten thousand results arrive with three different authority badges spread across three different
products — "Overall Pick" on one, "Best Seller" on another, "Amazon's Choice" on the page the
shopper eventually opens. With no single authority to defer to, the shopper abandons the grid
entirely, pulls the whole result set as text, and re-ranks it themselves on review volume and
recent purchase counts.

- "1-48 of over 10,000 results for colored pencils." *(Results page)*
- "a KALOUR 72-count set marked \"Overall Pick\"" *(Results page)*
- "a Crayola set marked \"Best Seller\"" *(Results page)*
- "Let me pull the full text of the results to compare more options" *(Results page)*
- "That's a huge trust signal" *(Deliberation)*
- "badged \"Amazon's Choice,\" 100K+ bought in the past month" *(Product page)*

### 4. Variant picking is a hidden tax — severity: medium

Products whose listing has no single default offer get eliminated on step count. The shopper drops
the premium Prismacolor sets specifically because reaching a cart from them requires a "See options"
detour — and then names the *absence* of that detour as a reason the winner won. The choice
architecture, not the product, decided this.

- "those require clicking through \"See options\" to pick a specific offer rather than a direct Add to Cart — more steps for what's meant to be a straightforward pick" *(Deliberation)*
- "required extra \"See options\" clicks since there was no single default offer" *(Recap step 3)*
- "a clean one-click \"Add to Cart\" path — no ambiguous variant selection needed" *(Recap step 4)*

### 5. Primary action sits off-canvas — severity: high

The one control the entire session exists to reach is clipped outside the viewport. Three recovery
moves — locate, scroll into view, scroll right — happen before the buy box is usable. And when it
finally is, Add to Cart arrives adjacent to a Buy Now button the shopper has to consciously steer
around to avoid being thrown into checkout.

- "Now let me locate the \"Add to Cart\" button (it's cut off on the right side of my screenshot)" *(Product page)*
- "That element seems to be off-canvas — let me scroll it into view first." *(Product page)*
- "The buy box is partially cut off on the right edge of the viewport." *(Product page)*
- "I'll click \"Add to Cart\" — and deliberately avoid \"Buy Now,\" which would skip straight to checkout." *(Product page)*

### 6. Confirmation closes the loop — severity: low

The one moment the interface answers unambiguously. Three redundant signals fire at once — banner,
cart badge, subtotal — and the shopper treats the task as finished on the spot, without opening the
cart to double-check. This is the part that works; noting it so a redesign doesn't quietly remove it.

- "a green \"Added to cart\" confirmation appeared, cart icon now shows 1 item, and the subtotal reads ₹621.44" *(Product page / post-add)*
- "confirmed by the green \"Added to cart\" banner, cart icon updating to 1 item, and subtotal showing ₹621.44" *(Recap step 5)*
- "I'm stopping right here, exactly as asked, before touching \"Proceed to checkout." *(Product page / post-add)*

---

## Gaps

- One source only — a single narrated desktop session driven by an AI agent on behalf of a user, not a human participant. Every theme is `frequency: 1` and none of them is corroborated by a second observer.
- The session is one task (search a generic category, add one item) on one category. Nothing is known about repeat purchase, reorder, saved lists, or a cart that already has items in it.
- The viewport is the agent's browser window, so the off-canvas buy box may be a narrow-window artifact rather than a defect every shopper hits. Window width was never recorded.
- The flow was deliberately stopped before checkout, so cart review, shipping, payment, and order confirmation are entirely unobserved.
- No mobile or app session — all evidence is desktop web, yet the downstream stages of this pipeline target a mobile platform.
- No price sensitivity data: the shopper's own budget, willingness to pay for the premium sets, or reaction to the INR amounts is never stated.
- The locale mismatch is described but never resolved, so we do not know what the address-change flow costs a shopper who tries to fix it.
