# Razorpay — how to configure (Admin)

Technical HOW-TO. Online HTML: `admin-app/gateway-razorpay.html`.

## What this gateway does

- Identifier: `razorpay`
- Init: `POST /api/gateways/initialize` → `POST https://api.razorpay.com/v1/orders` (Basic auth `keyId:keySecret`)
- Returns **`orderId`**, **`keyId`**, amount, currency for the **client SDK** (not primarily an authorization URL)
- Credentials: **keyId** (or publicKey alias), **keySecret** (or secretKey alias)

## Prerequisites

1. Razorpay test Key Id / Key Secret.
2. Customer app build that opens Razorpay Checkout with `orderId` + `keyId`.
3. Seeded `razorpay` row.

## Admin steps

1. **Gateways** → **Razorpay**.
2. Paste key id + key secret.
3. Capabilities (seed often enables refunds, withdrawals, webhooks, subscriptions).
4. **Active** → Save.
5. Confirm mobile/web never embeds the **key secret**.

## Smoke test

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"razorpay","amount":100,"currency":"INR","email":"buyer@example.com"}'
```

| Step | Expect |
|------|--------|
| Demo key secret | `demo: true` hint |
| Real keys | `orderId` + `keyId` in JSON |
| SDK payment completes | Signature/webhook verification path updates order |
| Looking for `authorizationUrl` like Paystack | Wrong expectation — use orderId/keyId |

## Differs from others

- SDK/order model vs Paystack/Flutterwave/PayPal redirect approve links.

## Related

- [gateways.md](./gateways.md) · [customer checkout](../customer-app/checkout.md)
