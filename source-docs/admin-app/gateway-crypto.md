# Crypto (Commerce) — how to configure (Admin)

## What this gateway does

- Commerce / crypto checkout slot (e.g. Coinbase Commerce–style integrations)
- Identifiers treated by initializer include `crypto` / `coinbase-commerce` (demo path until real keys)
- Admin credentials typically: **API key** + **webhook signing secret**
- Capabilities often emphasize webhooks; classic card refunds/payouts/subscriptions may be off until you wire them
- Init via `POST /api/gateways/initialize` returns demo payload until non-demo keys are configured

## Prerequisites

1. Account with your chosen crypto commerce provider.
2. Public HTTPS webhook URL to your API.
3. Compliance/support ready for delayed confirmations and refund limits.

## Admin steps

1. **Gateways** → **Crypto (Commerce)** (or your seeded crypto-named row).
2. Paste API key + webhook signing secret from the provider.
3. Enable webhook capability; set **Active** only when the webhook endpoint is verified.
4. Save.
5. Confirm checkout only advances order status **after** webhook confirmation (not on “invoice shown”).

## Smoke test

```bash
curl -s -X POST http://localhost:5000/api/gateways/initialize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"provider":"crypto","amount":25,"currency":"USD","email":"buyer@example.com"}'
```

| Step | Expect |
|------|--------|
| Demo keys | `demo: true` + configure hint |
| Real keys + webhook | Invoice/session created; order waits for webhook |
| Premature “paid” in UI before webhook | Bug — fix client to wait for confirmed status |
| Refund request | Follow provider policy — may not mirror Stripe refunds |

## Differs from others

- On-chain / commerce confirmation latency. Not a substitute for COD or Internal Wallet.

## Related

- [gateways.md](./gateways.md) · [payments-wallet.md](../my-backend/payments-wallet.md)
