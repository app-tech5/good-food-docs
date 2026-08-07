# Membership plans — Customer app

Customer-facing subscription tiers (e.g. Good Food+). Plans are created in Admin (`target = customer`) and enrolled from the app.

## What you configure (Admin → Subscriptions)

| Field / flag | Effect for the member |
|---|---|
| **Price / currency / billing cycle** | What they pay and how often |
| **Benefits** (display tags) | Copy on the plan card |
| **`freeDelivery`** | Delivery fee is **0** at checkout |
| **`discountPercent`** | That % off cart subtotal (before tax) at checkout |
| **`prioritySupport`** | Priority support badge / routing |
| **`is_active`** | Plan purchasable or hidden from new sign-ups |

## Try it

1. Admin: active plan with `target = customer`, turn on `freeDelivery` and/or set `discountPercent`.
2. Customer app → **Subscriptions** → subscribe.
3. Place an order — confirm free delivery and/or discounted subtotal on checkout and on the order total.

## Related

- [Checkout](./checkout.md) · [Wallet](./wallet.md)
- [Backend subscriptions](../my-backend/subscriptions-engine.md) · Admin [subscriptions](../admin-app/subscriptions.md)
