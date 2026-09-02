# Acceptance criteria guide

Each story needs **2–6** criteria that a tester or reviewer could check without asking a
question. Aim for: the main success path, one or two important alternate/edge paths, and
any explicit rule from the source material.

## Preferred form — Given / When / Then

```
- Given <starting context / preconditions>, when <the user action>, then <observable result>.
```

Keep each criterion to a single scenario. If you need "and then ... and then ...", split it.

Good:
- Given I have items in my cart, when I click Checkout, then I am taken to the payment step.
- Given my card is declined, when I submit payment, then the order is not placed and I see the decline reason.

Weak (not testable / bundled):
- The checkout should work well.
- User can check out, pay, and get a receipt email and see order history.

## Checklist form (acceptable when scenarios don't fit Given/When/Then)

```
- [ ] <observable, specific condition>
```

Use for constraints and non-functional rules:
- [ ] Response returns within 500 ms for up to 1,000 rows.
- [ ] Files larger than 10 MB are rejected with a message naming the limit.

## Edge cases worth a criterion when the domain calls for it

- Empty / first-run state (no data yet)
- Invalid or missing input
- Permissions — actor is not allowed to do this
- Concurrency / offline / retry
- Limits and boundaries (max length, max count, timeout)
- Failure of a downstream step and how the user recovers

## Anti-patterns

- Restating the story sentence as a criterion.
- Criteria that describe implementation ("insert a row into the orders table").
- Vague adjectives: "fast", "intuitive", "robust" — quantify or drop them.
