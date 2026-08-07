# Logistics engine — Backend API

What the per-restaurant delivery settings actually control once an order is ready for a driver — not a route list.

## Where the numbers come from

Almost everything logistics does reads from **`DeliverySetting`**, one document per restaurant (Admin or restaurant app → delivery settings). This is the real configuration surface — there's no separate "logistics settings" screen:

| `DeliverySetting` field | Drives |
|---|---|
| `isDeliveryEnabled` / `isPickupEnabled` | Whether the restaurant offers each service mode at all. |
| `deliveryFeeType` (`FIXED` / `DYNAMIC` / `FREE` / `RESTAURANT_DEFINED`) + `fixedDeliveryFee` / `dynamicDeliveryFee` (`baseFee`, `perKmFee`, `minFee`, `maxFee`) | The base delivery fee before any surge multiplier is applied — see [AI & pricing brain](./intelligence-engine.md). |
| `freeDeliveryEnabled` / `freeDeliveryThreshold` | Forces the fee to zero outright, or once the cart subtotal clears the threshold. |
| `deliveryPreparationTime` | Feeds the smart-ETA base prep estimate. |
| `autoAssignmentRadius` | How far the batching engine looks for nearby orders to bundle with a driver's accepted job (clamped to 0.5–15 km server-side no matter what's typed in). |
| `maxDeliveryDistance`, `deliveryZones`, `deliveryHours`, `blackoutDays`, `allowScheduledDelivery`, `schedulingLeadTime`, `timeSlotDuration` | Availability/eligibility checks around when and where delivery can be offered. |
| `driverAssignmentMethod` (`AUTO` / `MANUAL` / `HYBRID`) | Documents the intended assignment mode for that restaurant (operational convention — batching itself runs the same way regardless). |

Change these per restaurant in Admin (or let the restaurant self-serve if your build exposes it), not in App Settings — App Settings only has a **global** fallback (`deliveryFee`, `freeDeliveryThreshold`, `maxDeliveryDistance`) used when a restaurant has no `DeliverySetting` document at all.

## Batching — what actually gets bundled

When a driver accepts an order, the backend looks for **other unassigned delivery orders** within that restaurant's `autoAssignmentRadius` of the drop-off point (falling back to the restaurant location if the customer has no saved coordinates), preferring same-restaurant orders and shorter distance first, capped at a max batch size. Everything in the batch gets the same `batchId` and moves to `out_for_delivery` together. Pickup orders are never batched.

## Proof of delivery & geofence

Completing a delivery requires either a signature or a photo (a photo is mandatory for contactless drop-offs). If the customer's saved location is known, the backend measures the driver's completion coordinates against it: outside a default **150 m** geofence, the delivery is flagged `geofenceOk: false` on the order but still allowed to complete (soft-fail) unless that behavior is turned off via env (`LOGISTICS_POD_GEOFENCE_SOFT`), in which case it's hard-rejected. Geofence radius and batch limits (`LOGISTICS_POD_GEOFENCE_M`, `LOGISTICS_BATCH_RADIUS_KM`, `LOGISTICS_MAX_BATCH_SIZE`) are `.env` values, not Admin UI fields — set them once at deploy time if the defaults don't fit your delivery radius.

## End-to-end

Customer orders → restaurant marks ready → driver accepts (batching runs) → customer sees live map/ETA → driver completes with proof of delivery → admin shows the order delivered.

## Smoke test

1. Set a restaurant's `DeliverySetting` to `DYNAMIC` fees with a small `autoAssignmentRadius` and place two nearby delivery orders.
2. Driver accepts one — confirm the nearby order gets pulled into the same batch (`batchId` matches, both move to `out_for_delivery`).
3. Complete delivery with a photo, away from the customer's saved address — confirm the order still completes but shows `geofenceOk: false`.
4. Complete a normal in-range delivery — confirm `geofenceOk: true` and driver becomes `available` again once their batch is empty.

## Related

- [Live status sync](./live-updates.md)
- [Order lifecycle](./order-lifecycle.md)
- [AI & pricing brain](./intelligence-engine.md)
- Driver HOW-TOs: [job board & batching](../delivery-app/deliveries.md) · [on the road](../delivery-app/active-delivery.md) · [photo & signature POD](../delivery-app/proof-of-delivery.md)
