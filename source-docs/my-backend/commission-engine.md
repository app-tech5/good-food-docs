# Commission engine — Backend API

Platform vs restaurant splits on completed orders, including subscription benefit adjustments.

## Configure

1. Admin → **App Settings** — set default commission %.
2. Optionally set restaurant-level overrides if your forms expose them.
3. Attach an active **restaurant** subscription with commission relief to test benefits ([subscriptions engine](./subscriptions-engine.md)).

## Verify

1. Complete a full order (customer → accept → deliver).
2. Admin → **Earnings** — platform vs restaurant split matches rate ± plan benefits.
3. Repeat with an active restaurant plan that reduces commission — split should soften.

API / settings drive the math; admin Earnings is the audit view.

## Related

- [Payments & wallet](./payments-wallet.md)
- [Admin earnings HOW-TO](../admin-app/earnings.md)
