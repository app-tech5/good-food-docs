# Live tracking — Customer app

Status timeline and delivery map while the courier is en route, driven by real-time socket events on the order's room, not polling.

## What drives this

- **Timeline steps** mirror `Order.status`: `pending → preparing → ready → out_for_delivery → delivered`. Each step only advances when the restaurant or driver app actually calls the corresponding action — this screen never simulates progress.
- **Map + driver marker** appears once a driver is assigned and the order is `out_for_delivery`; the driver's device emits location updates that fan out to everyone subscribed to that order's room (`order-<id>`), which is why keeping the driver app foregrounded/online matters.
- **Route/ETA** on the tracking map reuses the same [smart ETA](./smart-eta.md) engine (OSRM when reachable, heuristic otherwise).
- **Delivery completion** requires the driver to submit [proof of delivery](../delivery-app/proof-of-delivery.md) — the timeline only reaches "delivered" after that succeeds (photo/signature and, if enforced, within the geofence).

## Try it

1. Place a delivery order; have the restaurant accept it; have a driver go online and accept/be assigned.
2. Open **Track order** — the timeline should advance as the restaurant/driver apps change status.
3. Once out for delivery, confirm the **map** shows destination, courier position, and route/ETA — this is a different map from the pre-checkout [discovery](./discovery.md) map.
4. Have the driver complete with proof of delivery — the order should flip to delivered here within a few seconds.

Broken map is almost always: location permission denied on the driver's device, a stale API URL, or the driver app not actually online.

## Related

- [Backend live updates](../my-backend/live-updates.md) · [Driver logistics](../delivery-app/logistics.md) · [Proof of delivery](../delivery-app/proof-of-delivery.md)
