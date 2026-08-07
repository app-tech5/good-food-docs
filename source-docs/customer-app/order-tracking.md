# Live tracking — Customer app

Status timeline and delivery map while the courier is en route.

## Smoke test

1. Place delivery order; restaurant accepts; driver assigned and moving.
2. Open **Track order** — timeline advances (pending → preparing → out for delivery → delivered).
3. When out for delivery, confirm **map** (destination, courier, route/ETA) — not the discovery map.
4. Driver completes with POD ([proof of delivery](../delivery-app/proof-of-delivery.md)).

Broken map → location permissions, API host, or driver not updating location.

## Related

- [Backend live updates](../my-backend/live-updates.md)
- [Driver logistics](../delivery-app/logistics.md)
