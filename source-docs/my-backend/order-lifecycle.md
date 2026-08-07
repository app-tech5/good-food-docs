# Order lifecycle — Backend API

What actually drives an order from checkout to delivered, and which settings hook into that transition — not a route list.

## The one document

Every order is a single `Order` record — line items, payment state, restaurant, optional driver, delivery/pickup details, and a `status`. Customer, restaurant, driver, and admin apps all read and advance that **same** record; none of them keeps a private copy. If two apps disagree, it's a refresh/auth/API-URL problem, not a sync bug.

## The status machine

```
pending → preparing → ready → out_for_delivery → delivered
                                                 ↘ cancelled (from most states)
```

Who is allowed to move the needle:

- **Restaurant** — `pending → preparing → ready` (accept, start prep, mark ready). Configured nowhere except who owns the restaurant account; any authenticated user tied to that restaurant can do this.
- **Driver** — `ready → out_for_delivery → delivered`. Assignment and batching rules live in [logistics engine](./logistics-engine.md); proof-of-delivery is required to reach `delivered` when the delivery type is `delivery`.
- **Customer / Admin** — can cancel while an order is still active. In `DEMO_MODE=true` deployments, cancellation is blocked outright (used for public demo builds so testers can't wipe seeded orders).
- `orderSource` (`app` / `whatsapp` / `ussd` / `web` / `admin`) never changes who can advance the order or which pipeline it enters — see [channels API](./channels-api.md).

## Settings that react to a status change

A status update is not just a field write — the backend runs side effects off it, controlled by the **same** App Settings you'd configure elsewhere in this suite:

| On this transition | If this App Settings flag is on | Effect |
|---|---|---|
| → `cancelled` | `walletInstantRefundEnabled` (default **on**) | The order total is credited back to the customer's internal wallet automatically — see [payments & wallet](./payments-wallet.md). Skipped for unpaid cash-on-delivery orders. |
| → `delivered` | `walletCashbackEnabled` + `walletCashbackPercent` | Cashback is credited to the customer's wallet based on the order subtotal. |
| any status change | `whatsappNotifyOnStatus` | The customer gets a WhatsApp message with the new status, if they have a phone on file and WhatsApp is configured — see [channels API](./channels-api.md). |

None of this needs separate configuration in this doc — it's the same flags described in payments-wallet.md and channels-api.md, just triggered by the order's own status field. That's the point: one lever, several effects, all enforced server-side regardless of which client changed the status.

## Smoke test

1. Customer places a delivery order and pays with an enabled method.
2. Restaurant accepts (orders list or KDS) → `preparing` → `ready`.
3. Driver accepts / is assigned → `out_for_delivery` → `delivered` (with proof of delivery).
4. Customer tracking, restaurant board, and driver job all show the same status at each step.
5. Cancel a paid test order (while still active) — wallet should show an instant refund if `walletInstantRefundEnabled` is on.
6. Admin → **Orders** → open the same id — payment + fulfillment coherent with what the other three apps showed.

## Related

- [Live status sync](./live-updates.md)
- [Logistics engine](./logistics-engine.md)
- [Payments & wallet](./payments-wallet.md)
- [Hybrid order channels](./channels-api.md)
