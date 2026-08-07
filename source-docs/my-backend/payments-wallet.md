# Payments & wallet — Backend API

Gateways, checkout initialize, wallet ledger, cashback, and instant refund behaviour.

Admin UI field-by-field HOW-TOs (ZIP docs): [gateways index](../admin-app/gateways.md) and per-provider pages under `source-docs/admin-app/gateway-*.md`. Online HTML stays the soft product explanation.

## Prerequisites

- `migrate:up` applied (wallet / gateway seeds)
- Admin can open **Gateways** and **App Settings**
- For Stripe beyond demo: `STRIPE_SECRET_KEY` (and Connect URLs if used) in `my-backend/.env` — see `.env.example`

## Operator steps

1. Admin → **Gateways** — enable only methods you have credentials for (`/api/gateways`). Use the matching [per-gateway HOW-TO](../admin-app/gateways.md).
2. Set Stripe secrets in backend `.env` when leaving demo keys — see [getting started](./getting-started.md) and [gateway-stripe.md](../admin-app/gateway-stripe.md).
3. App Settings — review wallet flags (cashback / instant refund to wallet).
4. Customer app — top up wallet, pay an order from balance ([customer wallet](../customer-app/wallet.md)).
5. Cancel a paid test order if instant-refund is on — confirm wallet credit.

## API smoke (hosted PSPs)

```bash
# List active providers (shape may omit secrets)
curl -s -H "Authorization: Bearer $TOKEN" \\
  http://localhost:5000/api/gateways/providers

# Initialize (paystack | flutterwave | razorpay | paypal | crypto/…)
curl -s -X POST http://localhost:5000/api/gateways/initialize \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"provider":"paystack","amount":10,"currency":"NGN","email":"buyer@example.com"}'
```

Stripe card intents: `/api/payments/stripe/payment-intent` (not only `/initialize`).

## Smoke test

| Step | Expect |
|------|--------|
| Gateway disabled | Checkout with that method fails clearly |
| Demo secrets on Active gateway | `demo: true` init (or Stripe failure) until real keys |
| Wallet top-up | Balance increases |
| Pay from wallet | Order paid; ledger entry exists |
| Refund / cashback flags | Matching ledger movement after eligible event |

## Related

- [Commission engine](./commission-engine.md)
- Admin HOW-TOs: [gateways.md](../admin-app/gateways.md)
- Customer: [wallet.md](../customer-app/wallet.md)
