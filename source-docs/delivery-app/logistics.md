# Logistics & POD — index

Driver logistics HOW-TOs, split like the online docs. All three share the same backend `logisticsService.js` and the same `Order` status pipeline the customer and restaurant apps use.

| Guide | What you configure |
|-------|---------------------|
| [Job board & batching](./deliveries.md) | Per-restaurant `autoAssignmentRadius` (batch distance) and `driverAssignmentMethod` (AUTO/MANUAL/HYBRID) in Delivery Settings. |
| [On the road](./active-delivery.md) | Nothing new to configure — it's a live view of the assigned order(s); depends on location permission staying granted. |
| [Photo & signature POD](./proof-of-delivery.md) | Backend env vars `LOGISTICS_POD_GEOFENCE_M` (default 150m) and `LOGISTICS_POD_GEOFENCE_SOFT` (default true = warn, not block) — not Admin UI fields. |

Backend: [Logistics engine](../my-backend/logistics-engine.md).

### Full smoke checklist

1. Customer orders delivery.
2. Restaurant accepts / marks ready.
3. Driver goes online → accepts the job (batch if offered based on `autoAssignmentRadius`).
4. Customer watches live tracking while the driver's location streams in.
5. Driver completes with photo + signature (subject to the geofence check above).
6. Admin/customer/restaurant all see the same order marked delivered.
