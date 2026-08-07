# Checkout & vouchers — Customer app

Delivery vs pickup, address, payment method, membership perks, vouchers, and order placement — where Admin settings become one price.

## What drives the total

| Setting | Where | Effect |
|---|---|---|
| Active gateways + Stripe / COD App Settings | Gateways + App Settings | Which payment methods appear and are accepted |
| Restaurant / platform delivery fee, free threshold, max distance | Delivery settings / App Settings | Delivery fee and distance eligibility |
| Member `freeDelivery` / `discountPercent` | Active customer subscription | Fee waived and/or % off subtotal |
| Tax | Restaurant / default tax | Applied after membership discount |
| Coupons / promos | Admin promotions & coupons | Applied when claimed and still valid |
| Wallet balance | Ledger | Pay with platform credit when balance covers the total |
| Address autocomplete | Google Places key on the customer build | Suggestions appear while typing a delivery address |

## Try it

1. From cart, open **Offers** if vouchers are seeded — claim/apply.
2. Checkout — delivery vs pickup, address (with Places suggestions when configured), payment method.
3. With an active membership, confirm free delivery and/or discount on the totals.
4. Place the order → [history](./order-history.md) / [tracking](./order-tracking.md).
5. Turn off COD or Stripe in App Settings and confirm that method can no longer complete checkout.

### Places (address autocomplete)

1. Google Cloud → enable **Places API** → create an API key → attach billing.
2. Put the key where this customer app expects it (see [getting started](./getting-started.md) / env example).
3. At checkout, type an address and confirm suggestions return.

## Related

- [Wallet](./wallet.md) · [Subscriptions](./subscriptions.md) · [Surge / delivery fee](./delivery-fee.md)
- [Payments API](../my-backend/payments-wallet.md)
