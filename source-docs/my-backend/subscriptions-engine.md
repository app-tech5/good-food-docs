# Subscriptions engine — Backend API

What each plan benefit does once a customer, driver, or restaurant is enrolled.

## Plan shape

A `Subscription` is a template: `target` (`customer` / `restaurant` / `driver`), `price`, `currency`, `billing_cycle`, display `benefits` tags, and `benefitFlags` (the flags that change money and checkout).

Enrollment creates a `UserSubscription` (active + period end). Other services resolve perks via the member’s active plan for their role.

## Benefit flags — what they do

| Flag | Audience | Effect |
|---|---|---|
| `reducedCommissionPercent` | Restaurant | Lowers platform commission on completed orders |
| `waiveCommission` / `platformAccess` | Restaurant | Platform commission **0%** while enrolled (flat SaaS fee instead) |
| `freeDelivery` | Customer | Checkout sets delivery fee to **0** |
| `discountPercent` | Customer | Checkout takes that % off subtotal (before tax) |
| `prioritySupport` | Driver (also customer/restaurant display) | Drivers get first look at new pending jobs and a wider batch radius |

Restaurant commission math: [commission engine](./commission-engine.md).  
Customer pricing is applied when the order is created (app checkout and channel intake), so totals cannot be bypassed by the client.

## Configure a plan

1. Admin → **Subscriptions** — set `target`, price, cycle, and the benefit flags above.
2. Restaurant SaaS: prefer `waiveCommission` + `platformAccess`; or use `reducedCommissionPercent` for a softer cut.
3. Customer perks: turn on `freeDelivery` and/or set `discountPercent`.
4. `is_active: false` hides the plan from new sign-ups without wiping existing members.

## Verify

| Check | Expect |
|---|---|
| Restaurant + `waiveCommission` | Earnings show 0% platform cut on new orders |
| Restaurant + `reducedCommissionPercent` | Platform cut softens by that % |
| Customer + `freeDelivery` | Checkout delivery fee is 0 |
| Customer + `discountPercent` | Checkout subtotal reduced before tax |

## Related

- [Commission engine](./commission-engine.md)
- Admin: [subscriptions](../admin-app/subscriptions.md)
- Apps: [customer](../customer-app/subscriptions.md) · [driver](../delivery-app/subscriptions.md) · [restaurant](../restaurant-app/subscriptions.md)
