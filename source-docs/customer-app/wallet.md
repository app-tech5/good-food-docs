# Wallet & cashback — Customer app

In-app balance the customer can top up and pay checkout with, plus platform-funded cashback and instant refunds. The balance itself is not a stored number — it is computed live from the customer's `Transaction` ledger: completed credits (`customer_top_up`, `refund`, `adjustment`, `cashback`) minus completed debits (`customer_payment` paid with `platform_credit`).

## What drives this (Admin → App Settings → Wallet)

- **`walletCashbackEnabled`** — when true (default), every order that reaches `delivered` status automatically credits cashback to the customer's wallet. Turn it off and no cashback transactions are created, but existing balance/history stays.
- **`walletCashbackPercent`** — the percent (default 2%) applied to the order's `subtotal` to compute the cashback amount. The system won't cashback the same order twice.
- **`walletInstantRefundEnabled`** — when true (default), cancelling a **paid** order (card, wallet, gateway — not unpaid cash-on-delivery) immediately credits the full order total back to the customer's wallet instead of waiting for a manual refund.
- **Top-up / pay-with-wallet at checkout** still depends on which gateways are marked **Active** in Admin ([gateways](../admin-app/gateways.md)) — the wallet itself has no separate "enabled" switch; it's always available as a payment method once a customer has a balance.

## Try it

1. Customer → **Wallet** — note the balance and recent transactions.
2. **Add Money** — pick an amount chip, pay with an active gateway, confirm the balance increases.
3. Checkout an order using the wallet when the balance covers it.
4. To see cashback: place an order and advance it to **delivered** (restaurant + driver apps) — confirm a `cashback` line appears in **Wallet → Transactions** at `walletCashbackPercent` of the subtotal.
5. To see instant refund: cancel a **paid** order and confirm a `refund` transaction lands in the wallet immediately (cancelling an unpaid cash-on-delivery order does not create a refund — there was nothing charged).

## Related

- [Checkout](./checkout.md) · Admin [gateways](../admin-app/gateways.md) · Backend [payments & wallet](../my-backend/payments-wallet.md)
