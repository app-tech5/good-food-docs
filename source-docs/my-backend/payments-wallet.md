# Payments & wallet — Backend API

How marketplace payment switches and wallet cashback/refunds are configured — and how the API applies them at checkout.

## Turning payment methods on / off

Two Admin surfaces stay **in sync**:

| Surface | What you set | Effect |
|---|---|---|
| **App Settings → Stripe Enabled** | Marketplace-wide card switch | On → Stripe payment intents work and the Stripe **Gateway** row is set **Active**. Off → card checkout is refused |
| **App Settings → Cash On Delivery Enabled** | Marketplace-wide COD switch | On → COD orders/methods allowed and COD **Gateway** set **Active**. Off → COD refused |
| **Gateways → Active** (per provider) | Paystack, Flutterwave, Razorpay, PayPal, Crypto, Wallet, … | Each PSP must be **Active** (with real credentials when you leave demo) to initialize that method |

Toggling Stripe/COD in either App Settings **or** the matching Gateway row updates the other, so operators never fight two conflicting switches.

Wallet (`platform_credit`) stays available whenever the customer has a balance — it is not gated by those two App Settings flags.

## Demo credentials vs. real credentials

Each gateway stores its own `credentials` map. Seeded rows ship with `demo_` placeholders. Until you replace them, initialize returns a clear “configure in Admin → Gateways” demo response (Stripe needs a real `STRIPE_SECRET_KEY` in `.env`). Nothing charges for real until credentials are live.

Per-provider fields: [gateways](../admin-app/gateways.md) and `gateway-*.md`.

## Wallet: cashback & instant refund

Balance = ledger of `Transaction` rows (credits minus wallet debits). App Settings:

| Flag | Default | Effect |
|---|---|---|
| `walletCashbackEnabled` + `walletCashbackPercent` | on, 2% | On `delivered`, credit cashback % of subtotal (once per order) |
| `walletInstantRefundEnabled` | on | On `cancelled` of a **paid** order, credit full total to wallet (skipped for unpaid COD) |

## Restaurant-level payment acceptance

`RestaurantPaymentSetting` can further restrict cash/card/online per partner under the global switches above.

## Verify

| Step | Expect |
|------|--------|
| App Settings Stripe **off** | Card payment intent refused |
| App Settings COD **off** | New COD order refused |
| Gateway Paystack **Active** + real key | Init returns provider authorization URL |
| Delivered order + cashback on | `cashback` credit on wallet |
| Cancel paid order + instant refund on | `refund` credit on wallet |

## Related

- [Order lifecycle](./order-lifecycle.md) · [Commission engine](./commission-engine.md)
- Admin: [gateways](../admin-app/gateways.md) · [app settings](../admin-app/app-settings.md)
- Customer: [wallet](../customer-app/wallet.md)
