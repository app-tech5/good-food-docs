# Paystack — how to configure (Admin)

Technical HOW-TO. Online HTML: `admin-app/gateway-paystack.html`.

## What this gateway does

- Identifier: `paystack`
- Init: `POST /api/gateways/initialize` → `POST https://api.paystack.co/transaction/initialize`
- Auth: `Authorization: Bearer <secretKey>`
- Amount converted to **minor units** via shared helper (zero-decimal currencies handled)
- Returns `authorizationUrl`, `accessCode`

## Prerequisites

1. Paystack test keys, then live keys.
2. Callback URL registered consistently (Paystack dashboard + `callbackUrl` on initialize).
3. Seeded `paystack` gateway row.

## Admin steps

1. **Gateways** → **Paystack**.
2. Paste **public key** + **secret key**.
3. Capabilities (seed often enables refunds, withdrawals, webhooks, subscriptions).
4. **Active** → Save.

## Smoke test

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"paystack","amount":10,"currency":"NGN","email":"buyer@example.com","callbackUrl":"https://example.com/paystack/callback"}'
```

| Step | Expect |
|------|--------|
| Demo secret | `demo: true` hint |
| Real secret | `authorizationUrl` + `accessCode` |
| Customer pays on Paystack page | Reference settles; order/ledger updates |
| Wrong currency for merchant | Provider error — fix currency in app settings / checkout |

## Differs from others

- No environment dropdown — test vs live = which keys you paste.
- No encryption key field (unlike Flutterwave).

## Related

- [gateways.md](./gateways.md) · [gateway-flutterwave.md](./gateway-flutterwave.md)
