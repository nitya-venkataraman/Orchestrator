# Ideation & Concepting — GreenBasket

*Stage 3 · Superlap UX pipeline · judge 0.89 · reach assumes ~8k weekly-active shoppers*

## Features (RICE-ranked)

| RICE | Feature | HMW | Reach | Impact | Conf | Effort |
|---|---|---|---|---|---|---|
| 9600.0 | Buy Again | How might we let a returning shopper recreate their usual order without hunting down each item? | 6000 | 3 | 0.8 | 1.5 |
| 8400.0 | Per-item substitution rules | How might we keep shoppers in control when something they wanted turns out to be unavailable? | 7000 | 3 | 0.8 | 2.0 |
| 6400.0 | Never-substitute default | How might we keep shoppers in control when something they wanted turns out to be unavailable? | 4000 | 1 | 0.8 | 0.5 |
| 6400.0 | AM/PM delivery windows | How might we make a delivery's timing predictable enough to plan a household around? | 8000 | 2 | 0.8 | 2.0 |
| 4800.0 | Proactive delay alerts | How might we make a delivery's timing predictable enough to plan a household around? | 3000 | 2 | 0.8 | 1.0 |
| 4266.7 | Per-order impact receipt | How might we help shoppers feel what their order achieved without asking them to interpret a score? | 8000 | 1 | 0.8 | 1.5 |
| 4000.0 | My Regulars list | How might we let a returning shopper recreate their usual order without hunting down each item? | 5000 | 2 | 0.8 | 2.0 |
| 3840.0 | Approve-the-swap notification | How might we keep shoppers in control when something they wanted turns out to be unavailable? | 6000 | 2 | 0.8 | 2.5 |
| 1250.0 | Your GreenBasket story | How might we help shoppers feel what their order achieved without asking them to interpret a score? | 5000 | 1 | 0.5 | 2.0 |
| 1000.0 | Seasonal picks module | How might we make browsing feel like discovering a market rather than scanning a list? | 4000 | 1 | 0.5 | 2.0 |
| 600.0 | Producer stories in browse | How might we make browsing feel like discovering a market rather than scanning a list? | 3000 | 1 | 0.5 | 2.5 |

### Feature descriptions

- **Buy Again** — A one-tap action on any past order that loads its full contents into the cart for editing.
- **My Regulars list** — A standing list of the shopper's core items they can tick into the cart in one screen instead of searching each week.
- **Per-item substitution rules** — Set once per product or category whether to allow a swap, choose from a shortlist, or refund if it's out of stock.
- **Approve-the-swap notification** — When an item goes out of stock at pick time, notify the shopper with a proposed alternative to accept or reject before dispatch.
- **Never-substitute default** — An account-level setting that removes any item that can't be fulfilled rather than swapping it, no per-item setup.
- **AM/PM delivery windows** — Let shoppers pick a morning or afternoon slot at checkout instead of a whole day, narrowing to a 2-hour window on the day.
- **Proactive delay alerts** — When an order will miss its slot, push a message with the reason and a new ETA rather than leaving the shopper to guess.
- **Per-order impact receipt** — Replace the bare score with a plain-language summary of what this order did: local farms supported, produce-waste prevented, average food miles.
- **Your GreenBasket story** — A running, shareable summary of cumulative impact over time — producers supported, total food miles, waste prevented since sign-up.
- **Seasonal picks module** — A curated 'what's good and new this week' section on the home screen that changes with the season and stock.
- **Producer stories in browse** — Surface the producer profile — photos, farm, why they started — inline while browsing a category, with a shareable producer page.

## Design directions

### Two Taps to Done

Bet that GreenBasket wins by being the fastest way to run a known weekly shop. Rebuild the home screen around the repeat order and remove every surprise; discovery is a secondary surface.

**Only this direction:** A reorder-first home built on your regulars and last order, substitution rules set once, and delivery windows tight enough to plan around — the whole shop in under two minutes.

**Trade-off:** Gives up the market-discovery feeling the values-driven shopper wants; risks reading as utilitarian as Ocado and losing the brand warmth that makes people evangelists.

HMWs addressed:
- How might we let a returning shopper recreate their usual order without hunting down each item?
- How might we keep shoppers in control when something they wanted turns out to be unavailable?
- How might we make a delivery's timing predictable enough to plan a household around?

### The Digital Market

Bet that GreenBasket wins on the one thing no competitor has — the feeling of a curated market with people and stories behind the food. Lead the experience with seasonal editorial, producer narratives, and impact framed as part of the story.

**Only this direction:** Producer stories and seasonal curation live in the browse flow, not a hidden blog; every product connects to a shareable human story, turning word-of-mouth into a built-in feature.

**Trade-off:** Does little for the Sunday-night efficiency shopper in the short term, needs an ongoing content operation, and may lose time-pressed users before the discovery investment pays back.

HMWs addressed:
- How might we make browsing feel like discovering a market rather than scanning a list?
- How might we help shoppers feel what their order achieved without asking them to interpret a score?

### Set It and Trust It

Bet that the winning move is to take the weekly shop off the user's plate entirely — a standing order the system maintains and adjusts for season and stock, with delivery and impact communicated to you rather than checked by you.

**Only this direction:** The system does the recurring work, not the user: a managed basket that proposes changes, handles stock-outs by your pre-set rules, and reports back — the shopper approves rather than assembles.

**Trade-off:** Demands high trust in GreenBasket's judgment from users who've been burned by silent substitutions, reduces hands-on control, and is irrelevant to shoppers who browse for enjoyment.

HMWs addressed:
- How might we let a returning shopper recreate their usual order without hunting down each item?
- How might we keep shoppers in control when something they wanted turns out to be unavailable?
- How might we make a delivery's timing predictable enough to plan a household around?
- How might we help shoppers feel what their order achieved without asking them to interpret a score?

