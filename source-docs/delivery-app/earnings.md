# Shift earnings — Driver app

Period/shift totals for completed jobs — a rollup of this driver's `delivery_fee` transactions and completed-order count, not a separate manually-maintained ledger.

## What drives this

- **`Driver.totalDeliveries`** increments by one every time [proof of delivery](./proof-of-delivery.md) is successfully completed for an order assigned to this driver.
- **Per-order earnings** come from the `delivery_fee` amount charged on that order, which is itself driven by [surge pricing](./delivery-fee.md) — a surge order genuinely pays the driver more, this isn't cosmetic.
- **Marketplace commission** (`AppSetting.commissionRate`, or a restaurant's own `commission_rate`, adjusted by any active restaurant subscription relief) applies to the *restaurant's* cut, not the driver's delivery fee — driver earnings and platform commission are computed independently on the same order.
- **Batched deliveries** ([job board & batching](./deliveries.md)) each retain their own `delivery_fee`, so a 2-order batch pays out as two separate line items, not a single combined fee.

## Try it

1. Complete a few deliveries for the shift (via [proof of delivery](./proof-of-delivery.md)).
2. Open **Earnings** — confirm the totals match the number and fee amounts of the jobs just completed.
3. Push demand up (surge active) for one delivery and confirm that job's line item pays more than a standard-fee job.
4. For line-by-line detail / payout setup, see [payouts & history](./transactions-payouts.md).

## Related

- [Backend commission engine](../my-backend/commission-engine.md) (marketplace side) · [Surge pricing](../customer-app/delivery-fee.md)
