# Job board & batching — Driver app

Go online, work today's list, and accept nearby batch suggestions. Batching is a real backend feature (`POST /api/logistics/batch-suggestions`, `.../accept-batch`) that groups genuinely nearby orders, not a UI gimmick.

## What drives this

- **Which orders are batchable** — only orders in `ready` or `out_for_delivery` status with no driver assigned yet (or already assigned to this driver) are candidates.
- **Batch radius** — each restaurant's `DeliverySetting.autoAssignmentRadius` (km), clamped between 0.5 and 15 km; if a restaurant has no explicit setting the platform falls back to an environment default (~2.5 km). Set this too small in Admin and drivers will rarely see batch suggestions for that restaurant.
- **Batch size** — capped at 3 orders per batch by default (server-side constant, not an Admin field).
- **Driver assignment method** — `DeliverySetting.driverAssignmentMethod` (`AUTO` / `MANUAL` / `HYBRID`) is the restaurant-level dial for how much the platform auto-offers vs. requires manual dispatch; it affects whether jobs appear on this board automatically at all.
- **Going online** flips the driver's own `status` to `available`, which is what makes them eligible to receive offers/batches in the first place.

## Try it

1. Driver goes **online**.
2. Open **Deliveries** — pending / on the way / completed lists.
3. Accept or start the next job.
4. For batching: with two nearby `ready` orders from restaurants whose `autoAssignmentRadius` covers the distance between them, open **batch suggestions** and accept the batch — confirm both orders now share the same driver and move together.
5. Continue to [on the road](./active-delivery.md).

## Related

- [Logistics index](./logistics.md) · [Restaurant delivery settings](../restaurant-app/hours.md) · [Backend logistics engine](../my-backend/logistics-engine.md)
