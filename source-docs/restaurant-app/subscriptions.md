# Partner plans — Restaurant app

Restaurant-targeted SaaS tiers — this is the one subscription surface in the suite where the benefit flags are fully wired into real money math, not just a display label.

## What operators set in Admin (Subscriptions, `target = restaurant`)

- **`price`**, **`billing_cycle`** — what the restaurant pays for the plan.
- **`benefits`** — plain-text bullets shown on the plan card (tools, visibility, support, etc.).
- **`benefitFlags.reducedCommissionPercent`** — shaves this many percentage points off the restaurant's normal commission rate on every order while the subscription is active.
- **`benefitFlags.waiveCommission`** or **`platformAccess`** — either flag drops the restaurant's commission to **0%** entirely (SaaS-access mode: the flat subscription fee replaces per-order commission).
- **`benefitFlags.prioritySupport`** — display-only perk (support routing/labeling on your side).

## What the restaurant actually sees

`commissionService.getEffectiveCommissionRate()` is called on every order split: it looks up the restaurant owner's active `restaurant`-target subscription and applies whichever of the rules above is active, before splitting the order total into platform vs. restaurant amounts. So a restaurant on a commission-relief plan will see a **larger payout on the very next order** — this is real, not cosmetic. Restaurants don't see the raw `benefitFlags` field, just the resulting lower commission line in their earnings.

## Try it

1. In Admin, confirm an active plan exists with `target = restaurant` and `benefitFlags.reducedCommissionPercent` (or `waiveCommission`) set ([admin subscriptions](../admin-app/subscriptions.md)).
2. Restaurant app → **Subscriptions** → Subscribe, complete payment.
3. Accept and complete a new order.
4. Compare the commission taken on that order against the restaurant's base `commission_rate` — it should be reduced (or zero) per the plan's flags.

## Related

- [Sponsored visibility](./sponsored.md) · [Backend subscriptions](../my-backend/subscriptions-engine.md) · [Backend commission engine](../my-backend/commission-engine.md)
