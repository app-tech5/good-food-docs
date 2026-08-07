# On the road — Driver app

Active job controls and customer/address details while a delivery (or batch of deliveries) is in progress. This screen is a view over the same `Order` documents the customer and restaurant apps see — there's no separate driver-only order state.

## What drives this

- **Which orders show here** — orders assigned to this driver with status `ready` or `out_for_delivery` (the same statuses used for batching eligibility).
- **Batch grouping** — if the driver accepted a [batch](./deliveries.md), all orders in the batch share a `batchId` and appear together.
- **Live customer tracking** — while this screen is open and the driver's location permission stays granted, the app streams location updates into the order's socket room (`order-<id>`), which is what powers the customer's [live tracking](../customer-app/order-tracking.md) map. Backgrounding the app or revoking location permission stalls the customer's map, not just the driver's.
- **Completion** requires [proof of delivery](./proof-of-delivery.md) — this screen hands off to that flow rather than allowing a bare "mark delivered."

## Try it

1. From [deliveries](./deliveries.md), open the active job (or batch).
2. Confirm status actions (navigate, arrived, complete) match the order's real status.
3. Open details — customer phone, address notes, order lines — all sourced from the order document.
4. Keep location permission granted and the app foregrounded; check the customer app's tracking map updates in near real time.
5. Finish with [proof of delivery](./proof-of-delivery.md).

## Related

- [Shift earnings](./earnings.md) · [Job board & batching](./deliveries.md)
