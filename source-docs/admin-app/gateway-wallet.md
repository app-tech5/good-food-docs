# Internal Wallet — how to configure (Admin)

Technical HOW-TO. Online HTML: `admin-app/gateway-wallet.html`.

## What this gateway does

- Identifier: `internal-wallet`
- Spends the customer’s **in-app balance** (ledger debit) — not an external authorize URL
- Seed credential: **platformSecret** (server-side only)
- Capabilities often: refunds to wallet on; withdrawals off; no provider webhooks
- **Top-ups** still require an external PSP (Stripe / Paystack / …)

## Prerequisites

1. At least one external gateway configured for top-up.
2. Wallet / cashback flags understood in App Settings ([app-settings.md](./app-settings.md)).
3. Backend wallet ledger services healthy ([payments-wallet.md](../my-backend/payments-wallet.md)).

## Admin steps

1. **Gateways** → **Internal Wallet**.
2. Set/rotate **platform secret** per your deploy practice — never ship it in mobile apps or public repos.
3. Tick **Active** if checkout should offer “pay with wallet”.
4. Align refund-to-wallet / cashback behaviour in App Settings.
5. Save.

## Smoke test

| Step | Expect |
|------|--------|
| Top up via external PSP | Wallet balance increases ([customer wallet](../customer-app/wallet.md)) |
| Pay order with wallet | Order paid; ledger debit exists |
| Insufficient balance | Clear failure — not a card decline |
| Instant refund to wallet (if enabled) | Credit appears after eligible cancel/refund |
| Platform secret in client bundle | **Fail security review** — keep server-only |

## Differs from others

- Ledger method. Combine with a card/mobile-money gateway for funding the wallet.

## Related

- [gateways.md](./gateways.md) · [wallet.md](../customer-app/wallet.md) · [payments-wallet.md](../my-backend/payments-wallet.md)
