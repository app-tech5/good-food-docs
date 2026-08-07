# Order history — Customer app

Past and live orders, pulled from the customer's own `Order` documents (`GET /api/orders` filtered by `user`). There is nothing to configure here beyond what already drives the order pipeline elsewhere — this page is a read view of that pipeline.

## What drives this

- **Status labels** mirror the real order lifecycle set by the restaurant/driver apps: `pending → preparing → ready → out_for_delivery → delivered`, or `cancelled`. A row's status only changes when the restaurant or driver actually advances the order — this list never fakes progress.
- **Amount** shown is `totalPrice` (items + delivery fee + tax) as computed at checkout, including any surge fee or free-delivery discount that applied at the time.
- **Cancelled + paid** orders trigger an instant wallet refund if App Settings **`walletInstantRefundEnabled`** is on ([wallet](./wallet.md)) — you'll see the refunded order's total reflected in the customer's wallet, not in this list.
- **Reorder / repeat** flows (if exposed in your build) reuse the same restaurant + items, subject to that restaurant's current availability.

## Try it

1. Place and complete a checkout, then open **Orders** / history.
2. Confirm the restaurant name, total, and status on the new row match what you just did.
3. Open an active (non-delivered, non-cancelled) order → continues to [Track order](./order-tracking.md).
4. Cancel a paid order and confirm the wallet reflects the refund per the setting above.

## Related

- [Checkout](./checkout.md) · [Wallet](./wallet.md) · [Order tracking](./order-tracking.md)
