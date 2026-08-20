# Stripe — how to configure (Admin)

## What this gateway does in the suite

- **Checkout / saved cards / payment intents** via `/api/payments/stripe/…`
- **Driver payouts (Connect)** via `/api/connect` when Connect is enabled
- Admin row identifier: `stripe`
- Credential shape: publishable key, secret key, webhook signing secret (plus capabilities / fees on the Gateway document)

This is **not** the same code path as Paystack/Flutterwave (`POST /api/gateways/initialize`).

## Prerequisites

1. `my-backend` running; migrations applied (Stripe row seeded).
2. For live Stripe calls beyond admin storage, set backend env (see `my-backend/.env.example`):

```env
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_CONNECT_COUNTRY=FR
STRIPE_CONNECT_RETURN_URL=goodfooddriver://stripe-connect/return
STRIPE_CONNECT_REFRESH_URL=goodfooddriver://stripe-connect/refresh
```

3. Admin open on the same API base URL.

## Admin steps

1. Open **Gateways** → **View** on **Stripe**.
2. Set capabilities to match what you operate:
   - `canRefund` / Refunds supported
   - `canWithdraw` / Payouts
   - `hasWebhook` / Webhooks
   - `isSubscriptionReady` / Subscriptions
3. Paste credentials from Stripe Dashboard → Developers → API keys / Webhooks:

| Admin field (typical) | Stripe Dashboard |
|----------------------|------------------|
| Publishable key | `pk_test_…` / `pk_live_…` |
| Secret key | `sk_test_…` / `sk_live_…` |
| Webhook signing secret | `whsec_…` from your webhook endpoint |

4. Tick **Active** only when keys are valid for the environment you are testing.
5. Save (**Send**).
6. Configure a Stripe webhook endpoint that hits your deployed API Stripe webhook handler; use that endpoint’s signing secret in admin (and keep server `STRIPE_SECRET_KEY` in sync with the same mode — test vs live).

## Smoke test

| Step | Expect |
|------|--------|
| Gateway Active with demo/placeholder keys only | Card flows fail or stay in demo — replace keys |
| `POST /api/payments/stripe/payment-intent` with auth | Intent created when `STRIPE_SECRET_KEY` is real |
| Customer checkout pays with card | Order paid; transaction/ledger row exists |
| Connect onboarding (driver app) | Account link opens when Connect env URLs are set |
| Deactivate Stripe in admin while apps still offer card | Init/checkout should fail clearly — do not leave stale Active+demo |

## Differs from other gateways (ops checklist)

- No sandbox/live dropdown — mode is encoded in the key prefix.
- Do not use `/api/gateways/initialize` as your only Stripe check; exercise `/api/payments/stripe/…`.
- Subscriptions / Connect are Stripe-specific concerns in this suite.

## Related

- [gateways.md](./gateways.md) · [payments-wallet.md](../my-backend/payments-wallet.md) · [backend getting started](../my-backend/getting-started.md)
