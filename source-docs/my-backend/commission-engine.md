# Commission engine — Backend API

Platform vs restaurant (and delivery/tax) splits on completed orders, including subscription benefit adjustments. Soft product story + screenshots: online `my-backend/commission-engine.html`.

## Prerequisites

1. `migrate:up` — settings, restaurants, subscriptions, earnings seeds as needed.
2. Admin pointed at the API ([admin getting started](../admin-app/getting-started.md)).
3. Ability to complete a full order (customer → restaurant → delivery).

## Configure the rate stack

The API resolves an **effective commission** roughly as:

1. **Marketplace baseline** — Admin → **Settings → App Settings** → **Commission Rate** (e.g. `15`).
2. **Restaurant override** (optional) — Admin → **Restaurants** → View → **Commission Rate (%)** on that partner.
3. **Active restaurant plan benefits** (optional) — Admin → **Subscriptions** → restaurant-target plan → benefit flags:
   - `reducedCommissionPercent` / **Reduced commission %**
   - `waiveCommission` / **Waive commission**

See [subscriptions engine](./subscriptions-engine.md) for plan catalogue / enforcement.

## Verify

1. Note the rates you set (baseline / override / plan benefits).
2. Complete a full paid order for that restaurant.
3. Admin → **Earnings** → list row → **View** detail:
   - Summary cards: platform commission, restaurant earnings, delivery earnings, taxes
   - Transactions: per-order **Commission** column
   - Payouts when restaurant share is owed out
4. Attach (or activate) a restaurant plan with reduced/waive commission and place another order — platform commission on the new earning lines should soften (or zero if waived).

## Smoke test

| Step | Expect |
|------|--------|
| App Settings Commission Rate = 15, no override/plan | ~15% platform commission on new completed orders |
| Restaurant Commission Rate (%) set differently | That restaurant’s new earnings use the override |
| Plan Reduced commission % / Waive | Softened or zero platform cut while plan active |
| Earnings detail | Split cards + transaction commission lines match the rules above |

## Related

- [Payments & wallet](./payments-wallet.md)
- [Subscriptions engine](./subscriptions-engine.md)
- [Admin earnings HOW-TO](../admin-app/earnings.md)
