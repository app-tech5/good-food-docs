# Payment gateways — how to configure them (Admin)

Technical HOW-TO for buyers with the ZIP. Soft product copy lives in the **online HTML** docs (`admin-app/gateways.html` + per-gateway pages). Here you get routes, credential fields, env keys, and smoke tests.

Each PSP has a different admin form and API initialize shape. Do **not** paste Stripe keys into Paystack (or any other row).

## Per-provider guides

| Gateway | Identifier | Guide |
|---------|------------|-------|
| Stripe | `stripe` | [gateway-stripe.md](./gateway-stripe.md) |
| PayPal | `paypal` | [gateway-paypal.md](./gateway-paypal.md) |
| Flutterwave | `flutterwave` | [gateway-flutterwave.md](./gateway-flutterwave.md) |
| Paystack | `paystack` | [gateway-paystack.md](./gateway-paystack.md) |
| OrangePay | `orange-pay` | [gateway-orangepay.md](./gateway-orangepay.md) |
| Razorpay | `razorpay` | [gateway-razorpay.md](./gateway-razorpay.md) |
| Cash on Delivery | `cash-on-delivery` | [gateway-cod.md](./gateway-cod.md) |
| Internal Wallet | `internal-wallet` | [gateway-wallet.md](./gateway-wallet.md) |
| Crypto (Commerce) | `crypto` / commerce slot | [gateway-crypto.md](./gateway-crypto.md) |

## Prerequisites

1. Backend up with migrations (`cd my-backend && npm run migrate:up`) — seed creates the gateway rows (`migrations/12-3-gateways-seed.js`).
2. Admin app pointed at the same API (`REACT_APP_API_URL=…/api`) — [admin getting started](./getting-started.md).
3. Sign in as an **admin** user (seed / demo credentials from backend getting started).

## Shared operator path (all gateways)

1. Admin UI → **Gateways** (`/gateways`) — list from `/api/gateways`.
2. **View** the row you care about (or use **+ Add Gateway** only when you intentionally create a new identifier).
3. Fill **that** provider’s credential map, fees, and capabilities; tick **Active** only when ready.
4. Save (**Send**).
5. Confirm active providers via API if useful:

```bash
# after login — use your admin JWT
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/gateways/providers
```

6. Hosted PSP init (Paystack / Flutterwave / Razorpay / PayPal / crypto slot):

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"paystack","amount":10,"currency":"NGN","email":"buyer@example.com"}'
```

Stripe card intents use dedicated routes under `/api/payments/stripe/…` (see [gateway-stripe.md](./gateway-stripe.md)), not only `/api/gateways/initialize`.

## Rules that bite in production

- **Active + demo keys** → many providers return a `demo: true` init payload with a configure hint instead of a real authorization URL/order id. Replace secrets before go-live.
- Disable unused gateways so checkout cannot pick a half-configured method.
- Wallet **top-ups** need a real external PSP; **Internal Wallet** only spends balance ([gateway-wallet.md](./gateway-wallet.md)).

## Related

- Backend money path: [payments-wallet.md](../my-backend/payments-wallet.md)
- Customer checkout / wallet: [checkout.md](../customer-app/checkout.md), [wallet.md](../customer-app/wallet.md)
- Stripe Connect (driver payouts): backend `/api/connect` + `STRIPE_*` in `my-backend/.env.example`
