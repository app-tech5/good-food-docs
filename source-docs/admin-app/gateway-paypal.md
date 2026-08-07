# PayPal — how to configure (Admin)

Technical HOW-TO. Online HTML: `admin-app/gateway-paypal.html`.

## What this gateway does

- Identifier: `paypal`
- Init path: `POST /api/gateways/initialize` with `"provider":"paypal"`
- Server flow: OAuth token (`sandbox` or `live` API host) → create Checkout Order (`intent: CAPTURE`) → return **approve** URL
- Credentials: **clientId**, **clientSecret**, **mode** (`sandbox` | `live`)

## Prerequisites

1. PayPal Developer Dashboard REST app (sandbox first).
2. Backend + admin running; PayPal row seeded Active/inactive as you choose.
3. Public/callback URLs reachable for return/cancel (see `PUBLIC_APP_URL` / callback passed into initialize).

## Admin steps

1. **Gateways** → **PayPal**.
2. Paste:

| Field | Source |
|-------|--------|
| Client ID | PayPal app → Client ID |
| Client secret | PayPal app → Secret |
| Environment mode | `Sandbox` while testing; `Live` only with live credentials |

3. Align capabilities (refunds / payouts / webhooks / subscriptions) with what you will wire in PayPal webhooks.
4. **Active** → Save.

## Smoke test

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"paypal","amount":12.5,"currency":"USD","email":"buyer@example.com","callbackUrl":"https://example.com/paypal/return"}'
```

| Step | Expect |
|------|--------|
| Demo / placeholder client id | JSON with `demo: true` and configure hint |
| Real sandbox credentials | `authorizationUrl` (approve link), `orderId` |
| Customer completes approval | Order capture / status update per your webhook + order flow |
| Mode `live` with sandbox keys | Auth failure — keep mode and keys matched |

## Differs from others

- OAuth client credentials + mode dropdown (not Stripe key prefixes, not Paystack Bearer-only).
- Amount sent as decimal string in purchase units (not always minor units like Paystack).

## Related

- [gateways.md](./gateways.md) · [payments-wallet.md](../my-backend/payments-wallet.md)
