# Live status sync — Backend API

What actually pushes an order/driver update to the right screens in real time — and the one thing that has to be true for it to work.

## How it actually works

There's nothing to "configure" here in the App Settings sense — it's wiring, not a flag. When an order or restaurant record is updated, the backend emits a Socket.io event straight from the database hook that saved the change:

| Event | Emitted to room | Fires when |
|---|---|---|
| `order-updated` | `orders-<customerUserId>` | Any order update (status, driver assignment, payment) |
| `order-updated` | `orders-<driverUserId>` | Same update, also sent to the assigned driver's room |
| `driver-location-updated` | `order-<orderId>` | A driver's location changes while they have that order active — see [logistics engine](./logistics-engine.md) |
| `restaurant-updated` | `restaurant-<id>` and `restaurants` | A restaurant profile changes (activation, hours, closed toggle) |

Clients (customer tracking screen, restaurant board, driver active-job screen) join the room for the order/restaurant/driver they care about when they open that screen, and just re-render on the event — no polling.

## What has to be true for this to work

1. **The API process must be the one holding the socket server** — `global.io` is set up once in `src/server.js`. If you run multiple API instances behind a load balancer without a shared socket adapter, a client connected to instance A won't see an update written by instance B.
2. **Clients must hit the same host/port as the socket connection** — the usual "apps look out of sync" bug is `EXPO_PUBLIC_API_URL` (or admin's `REACT_APP_API_URL`) pointing at a different `PORT` than the one you set in `.env`. See [getting started](./getting-started.md).
3. **`CORS_ORIGINS` must include any browser-based client** — the websocket handshake is subject to the same origin check as the REST API.
4. There is no toggle to disable realtime — if the socket layer is reachable, updates fan out; if a screen looks stale, it's a connectivity/room-join problem on the client, not a setting you forgot on the backend.

## Smoke test

1. Place an order; restaurant advances status.
2. Customer **Track order** timeline updates without force-killing the app.
3. Driver goes en route — customer delivery map / ETA updates (network permitting).
4. Restaurant KDS/orders and driver active job stay aligned with the same order in admin.
5. If updates are missing on one client only: check Wi-Fi, background location permissions (driver), and that its API base URL/port matches every other client.

## Related

- [Order lifecycle](./order-lifecycle.md)
- [Logistics engine](./logistics-engine.md)
- Driver: [active delivery](../delivery-app/active-delivery.md) · Customer: online Live tracking page
