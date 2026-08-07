# Payments & wallet — Backend API

Gateways, checkout initialize, wallet ledger, cashback, and instant refund behaviour.

## Prerequisites

- `migrate:up` applied (wallet / gateway seeds)
- Admin can open **Gateways** and **App Settings**

## Operator steps

1. Admin → **Gateways** — enable only methods you have credentials for (`/api/gateways`).
2. Set Stripe (and regional PSP) secrets in backend `.env` when leaving demo keys — see [getting started](./getting-started.md).
3. App Settings — review wallet flags (cashback / instant refund to wallet).
4. Customer app — top up wallet, pay an order from balance ([customer wallet](../customer-app/wallet.md)).
5. Cancel a paid test order if instant-refund is on — confirm wallet credit.

## Smoke test

| Step | Expect |
|------|--------|
| Gateway disabled | Checkout with that method fails clearly |
| Wallet top-up | Balance increases |
| Pay from wallet | Order paid; ledger entry exists |
| Refund / cashback flags | Matching ledger movement after eligible event |

## Related

- [Commission engine](./commission-engine.md)
- Admin HTML: Payment gateways · Customer: Wallet & cashback
