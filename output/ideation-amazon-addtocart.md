# Ideation & Concepting — Amazon Add-to-Cart

From the 5 HMWs in [strategy-amazon-addtocart.md](strategy-amazon-addtocart.md). RICE reach is
modeled on a stated assumption of ~100,000 shoppers per quarter through the search-to-cart flow,
scaled per feature by the share of sessions the friction touches. The corpus is a single session,
so `confidence` is 0.5 on eight of eleven features — 0.8 only where the corpus flagged the same
friction three separate times. **No winner is selected here**; a human picks the direction for Stage 4.

`rice = (reach × impact × confidence) / effort`

---

## Feature Backlog (RICE)

| Feature | HMW | Reach | Impact | Conf. | Effort | RICE |
|---|---|---:|---:|---:|---:|---:|
| **Persistent add bar** | HMW5 | 100,000 | 2 | 0.8 | 1.5 | **106,666.7** |
| **Confirmation that survives the scroll** | HMW5 | 100,000 | 1 | 0.5 | 1.0 | **50,000.0** |
| **Deciding facts on the row** | HMW2 | 60,000 | 2 | 0.5 | 1.5 | **40,000.0** |
| **Badge provenance** | HMW3 | 60,000 | 1 | 0.5 | 1.0 | **30,000.0** |
| **One ranked answer, shown its work** | HMW3 | 100,000 | 3 | 0.5 | 5.0 | **30,000.0** |
| **Add the default variant from results** | HMW4 | 45,000 | 2 | 0.8 | 3.0 | **24,000.0** |
| **Variant depth shown before the click** | HMW4 | 45,000 | 1 | 0.5 | 1.0 | **22,500.0** |
| **Compare tray** | HMW2 | 45,000 | 3 | 0.5 | 4.0 | **16,875.0** |
| **Inline locale switch** | HMW1 | 20,000 | 2 | 0.8 | 2.0 | **16,000.0** |
| **Locale settled at entry** | HMW1 | 20,000 | 1 | 0.5 | 1.0 | **10,000.0** |
| **Dual-currency price line** | HMW1 | 20,000 | 1 | 0.5 | 1.5 | **6,666.7** |

Each feature, one line:

- **Persistent add bar** — The add-to-cart control is pinned within reach at every scroll position, with the checkout shortcut demoted out of accidental range.
- **Confirmation that survives the scroll** — The added state persists as a bar carrying the running subtotal and an undo, rather than a banner that disappears on its own.
- **Deciding facts on the row** — Rating count, recent purchase volume, and variant depth surface on the result row itself, so comparison never needs a second screen at all.
- **Badge provenance** — Tapping any authority badge says what it certifies, over what window, and against which set of products.
- **One ranked answer, shown its work** — A single top recommendation per query that states the two facts it won on, replacing the competing badges with one accountable pick.
- **Add the default variant from results** — Listings with a sensible default offer get a direct add control on the row; multi-variant listings get an inline picker instead of a page hop.
- **Variant depth shown before the click** — A listing declares how many choices stand between the shopper and a cart, so effort is visible while comparing rather than discovered afterwards.
- **Compare tray** — Pin up to four results and see them side by side on specs, rating volume, and delivered price, without ever leaving the results page.
- **Inline locale switch** — The ship-to banner becomes a control rather than an announcement: country and currency change in place and every price on the page re-renders without leaving it.
- **Locale settled at entry** — The storefront asks once, before any results exist, and never re-asks — moving the decision ahead of the screens that would otherwise inherit the ambiguity.
- **Dual-currency price line** — Every price carries both the storefront currency and the detected-locale currency, so there is nothing to switch and no ambiguity to resolve later.

> **Read the top row with suspicion.** *Persistent add bar* leads the backlog partly because its
> effort is booked at 1.5 person-months. Pinning the control is cheap; demoting the checkout
> shortcut out of accidental reach is a merchandising argument, not a layout change. If that
> effort is understated, the ranking shifts.

---

## Design Directions

### Decide in the Grid

**The bet.** The product page is the bottleneck, not the catalogue. Everything needed to choose between options and to add one of them belongs in the results list, so a shopper who knows the category never has to open a product page at all.

**Only this direction.** Collapses comparison and the add action into a single surface — the only direction where a successful session never leaves the results page.

**Addresses:** HMW2 · HMW4

**Gives up.** The result row gets dense fast, and products that genuinely need explaining — variants, sizing, compatibility — are under-served by a row. It also gives up whatever persuasion the product page was doing, on the assumption it was doing none.

### One Answer, Shown Its Work

**The bet.** Shoppers in a generic category do not want to compare; they want a pick they can defend. The system takes the ranking decision and earns the right to it by exposing the evidence behind every recommendation.

**Only this direction.** Replaces competing authority badges with one accountable recommendation and the reasoning it rests on — the only direction that moves the decision from the shopper to the system.

**Addresses:** HMW2 · HMW3

**Gives up.** An enormous trust burden concentrated in one place: a single bad top pick poisons the whole surface, and there is no cheap way to recover it. Shoppers who came to browse lose the browse.

### Never Lose the Thread

**The bet.** The shopping model is fine; the continuity around it is broken. Fix the four moments where the interface drops the shopper — the silent locale swap, the dead Enter key, the clipped primary action, the vanishing confirmation — and the existing flow works.

**Only this direction.** Touches only state, context, and reachability. It is the one direction that changes no ranking, no comparison, and no merchandising.

**Addresses:** HMW1 · HMW5

**Gives up.** Deliberately declines the ten-thousand-results decision problem, which is the highest drop-off stage in the journey. It makes a frustrating flow smooth without making a hard choice easier.

---

The three bets are not compatible. *Decide in the Grid* moves the decision, *One Answer* makes
the decision, and *Never Lose the Thread* explicitly declines to touch the decision at all. A
reasonable team could disagree about which is right — which is the point of the fork.

**The human picks the direction.** This stage does not recommend one.
