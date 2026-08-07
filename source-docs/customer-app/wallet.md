# Wallet & cashback — Customer app

In-app balance, top-up, pay at checkout; cashback / instant refund when flags allow.

## Prerequisites

- Gateways / wallet flags configured ([payments & wallet](../my-backend/payments-wallet.md))

## Steps

1. Customer → **Wallet** — note balance and saved methods.
2. **Add Money** — amount chips, pay, confirm balance.
3. Checkout using wallet when balance covers the order.
4. If cashback / instant-refund flags are on, trigger an eligible delivered order or cancel and confirm ledger movement.

## Related

- [Checkout](./checkout.md) · Admin [gateways](../admin-app/gateways.md)
