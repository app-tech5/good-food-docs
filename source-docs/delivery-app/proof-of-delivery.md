# Photo & signature POD — Driver app

Completing a delivery requires real multimedia proof — the backend actively rejects a completion call that doesn't satisfy the rules below, this isn't just a UI form.

## What drives this

- **Contactless toggle (on by default in this app)** — when on, a **photo is required**; the app blocks submission client-side and the backend also rejects it server-side if missing.
- **Signature or photo, always** — regardless of contactless, the backend requires at least one of `signatureData` or `photoUrl` to be present (`assertPodPayload`); this app's UI is slightly stricter and always asks for a signature too.
- **Geofence** — the backend compares the driver's submitted GPS coordinates against the order's drop-off location. The allowed radius defaults to **150 meters** (`LOGISTICS_POD_GEOFENCE_M` env var — not an Admin UI field). By default the geofence check is **soft-fail**: being outside it is recorded (`geofenceOk: false`, with the measured `distanceMeters`) but doesn't block completion, unless the backend operator has set `LOGISTICS_POD_GEOFENCE_SOFT=false`.
- **What each artifact means downstream**: the photo and/or signature are stored on `Order.delivery.proofOfDelivery` and are visible to Admin/support for dispute resolution; they are not shown back to the customer in this build.

## Try it

1. Arrive at (or near) the drop-off — geofence is soft-fail by default, so testing from across town will still succeed but be flagged.
2. Tap **Mark as Delivered** / complete.
3. With contactless on, capture a **photo**; sign on the **signature pad** (use **Clear** to retry).
4. Submit — confirm the order flips to delivered for the customer, restaurant, and admin simultaneously.
5. To see a rejection: turn contactless on and submit without a photo, or clear the signature and submit without one — the API should return the corresponding proof-required error.

## Related

- [Deliveries](./deliveries.md) · Full flow in [logistics.md](./logistics.md) · [Backend logistics engine](../my-backend/logistics-engine.md)
