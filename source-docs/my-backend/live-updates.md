# Live status sync — Backend API

How kitchen and courier progress reach customer tracking, restaurant boards, and driver jobs without a phone call.

## Prerequisites

- Order lifecycle working ([order lifecycle](./order-lifecycle.md))
- Customer tracking and driver location permissions granted on device

## What to verify

1. Place an order; restaurant advances status.
2. Customer **Track order** timeline updates without force-killing the app.
3. When a driver is en route, customer **delivery map** / ETA updates (network permitting).
4. Restaurant KDS / orders and driver active job stay aligned with admin order detail.

Realtime depends on the API process staying up and clients using the **same** `/api` host. Spotty updates → check Wi‑Fi, background location limits, and CORS / URL mismatch.

## Related

- [Order lifecycle](./order-lifecycle.md)
- [Logistics engine](./logistics-engine.md)
- Driver: [active delivery](../delivery-app/active-delivery.md) · Customer: online Live tracking page
