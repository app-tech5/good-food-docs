# Flutterwave — how to configure (Admin)

## What this gateway does

- Identifier: `flutterwave`
- Init: `POST /api/gateways/initialize` → Flutterwave **v3** `POST /v3/payments`
- Returns `authorizationUrl` from `data.link` (hosted redirect)
- Credentials: **publicKey**, **secretKey**, **encryptionKey**

## Prerequisites

1. Flutterwave dashboard keys for your country/currency mix.
2. Backend can reach `https://api.flutterwave.com`.
3. Admin gateway row `flutterwave` present (seed).

## Admin steps

1. **Gateways** → **Flutterwave**.
2. Paste public, secret, and encryption keys.
3. Set capabilities; note seed often has `isSubscriptionReady: false`.
4. **Active** → Save.
5. Ensure checkout passes a **currency Flutterwave supports** for that merchant.

## Smoke test

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"flutterwave","amount":5000,"currency":"NGN","email":"buyer@example.com","callbackUrl":"https://example.com/flw/return"}'
```

| Step | Expect |
|------|--------|
| Secret contains `demo_` | `demo: true` + configure hint |
| Real secret | `authorizationUrl` set |
| Complete hosted pay + redirect | Order advances after callback/webhook handling |

## Differs from others

- Extra **encryption key** vs Paystack.
- Redirect-first (unlike Razorpay orderId + SDK).

## Related

- [gateways.md](./gateways.md) · [gateway-paystack.md](./gateway-paystack.md)
