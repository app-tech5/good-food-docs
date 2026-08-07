# Transactions — Admin app

The full money ledger: every payment, payout, refund, tip, cashback, top-up, and platform-commission line in one list. This is the record to check when a payment, payout, or wallet balance is disputed.

## What you're looking at

| Field | Meaning | Effect when set |
|---|---|---|
| **Transaction Type** | `customer_payment`, `restaurant_payout`, `driver_payout`, `platform_commission`, `service_fee`, `delivery_fee`, `tip`, `refund`, `adjustment`, `customer_top_up`, `cashback` | What kind of money movement this row represents — always check this first when reading a ledger entry |
| **Amount / Currency** | The money moved | |
| **Status** | `pending`, `completed`, `failed`, `canceled`, `disputed`, `refunded` | Only `completed` transactions count toward wallet balances and payout totals — a `pending` refund hasn't landed yet |
| **Payment Method** | Required for `customer_payment` rows (`credit_card`, `paypal`, `apple_pay`, `google_pay`, `platform_credit`, `cash`, etc.) | Tells you which gateway to check in [Gateways](./gateways.md) if a payment looks wrong |
| **Payout Method** | Required for `restaurant_payout` / `driver_payout` rows (`ach_deposit`, `instant_pay`, `check`, `paypal`, `platform_balance`) | How the partner actually receives their money |
| **Related Order** | Order this transaction is tied to, if any | Cross-reference into [Orders](./orders.md) |
| **User** | Who the transaction belongs to | Cross-reference into [Partners](./partners.md) |
| **Platform Fee** (amount/percentage) | The commission portion of a payment, itemized | Explains the gap between what a customer paid and what a restaurant/driver nets |
| **Processor Fee** | The gateway's own cut, itemized | Explains the gap between platform fee and what actually lands after gateway costs |
| **Tax** | Tax portion of the transaction, itemized | Should reconcile against the order's tax line |

## How to set it up

There's nothing to configure to make transactions appear — they're generated automatically by orders, payouts, refunds, and wallet activity. Your job here is investigation:

1. Open **Transactions**.
2. Filter/search to the disputed payout, refund, or wallet top-up.
3. Check **Status** first — a `pending`/`failed` row explains "money hasn't shown up yet" without anything being broken.
4. Follow **Related Order** into [Orders](./orders.md) if the dispute is order-specific.
5. Pair with [Earnings](./earnings.md) for the aggregated commission view, and [Gateways](./gateways.md) if a specific provider's payments look off.

## Verify

| Check | Expect |
|---|---|
| Complete a test order (card or wallet) | A `customer_payment` transaction appears, status `completed` once payment confirms |
| Cancel that order with wallet instant refund on | A `refund` transaction appears and the customer's wallet balance updates |
| Restaurant earns from a delivered order | A `platform_commission` row (and eventually a `restaurant_payout`) appears tied to that order |
| Search by `related_order` | Finds every transaction tied to one order (payment, commission, any refund) |

## Related

- [Earnings](./earnings.md) · [Gateways](./gateways.md) · [Backend payments & wallet](../my-backend/payments-wallet.md)
