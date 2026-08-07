# Monetization — index

Everything that touches marketplace money, split to match the online admin menu:

| Guide | What you configure there |
|---|---|
| [App Settings](./app-settings.md) | Baseline commission, wallet cashback, Stripe & COD switches, delivery defaults, channels |
| [Gateways](./gateways.md) | Which payment providers are active and their credentials/fees |
| [Earnings](./earnings.md) | Review platform/restaurant/delivery/tax splits by period (read-only) |
| [Subscriptions](./subscriptions.md) | SaaS tiers for customer/restaurant/driver — free delivery, discount %, commission waiver, priority support |
| [Sponsored listings](./sponsored.md) | Oversight of restaurant-run paid placement campaigns (placement, status, bid, schedule) |
| [Promotions](./promotions.md) | Automatic checkout-time discount campaigns (type, scope, schedule, eligibility) |
| [Coupons](./coupons.md) | Redeemable codes with limits, targeting, and expiry |
| [Transactions](./transactions.md) | The full money ledger — payments, payouts, refunds, tips, commission (read-only) |
| [Customer wallet](../customer-app/wallet.md) | Customer-side wallet balance, top-ups, cashback display |

Backend internals: [payments & wallet](../my-backend/payments-wallet.md), [commission engine](../my-backend/commission-engine.md), [subscriptions engine](../my-backend/subscriptions-engine.md).

After `migrate:up` you usually already have commission defaults, sample subscription tiers, and sample sponsored listings seeded — review them against the tables above before changing anything for real.

## Related

- [Market index](./market.md) · [Getting started](./getting-started.md)
