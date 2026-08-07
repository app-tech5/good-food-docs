# Kitchen Display (KDS) — how to use it

The Kitchen Display turns accepted restaurant orders into a paperless prep board your kitchen staff can read at a glance. It lives inside the **restaurant app** — same login, same order pipeline as accept / ready / pickup — so cooks, couriers, and admin all share one order story.

## Prerequisites

1. Backend migrated (`npm run migrate:up`) — kitchen **demo tickets** are seeded so the board can look alive even before your first real order.
2. Restaurant app running, preferably **`npm run start:live`** when you want real API tickets ([restaurant getting started](./getting-started.md)).
3. A restaurant user that can see that restaurant’s orders.

## 1. Open Kitchen Display

1. Sign in to the restaurant app.
2. From the drawer / navigation, open **Kitchen Display** (labelled from the `kds` / “Kitchen Display” strings).
3. Prefer a **tablet or large phone in landscape** mounted where the line can see it (see tips below).

If the board is empty on a fresh demo database, either wait for migrations’ KDS demo tickets or accept a new customer order.

## 2. Happy path — ticket lifecycle

Follow this once end-to-end so the team knows what “done” means:

1. **Customer** places a delivery (or pickup) order.
2. **Restaurant** accepts the order on the normal orders UI (or auto-accept if you configured that).
3. The ticket appears on **Kitchen Display** in a kitchen-oriented layout (items, modifiers, timing cues).
4. Kitchen staff **advance** the ticket through prep states your build exposes (for example preparing → ready).
5. When food is ready, the **driver** (or customer for pickup) completes the handoff.
6. **Admin** still sees the same order for earnings and support — KDS does not fork a second database of truth.

Status changes on the KDS should stay consistent with what drivers and customers see. If something looks stuck, refresh the board and confirm the order status in the main restaurant orders list.

## 3. Using demo tickets on day one

Migrations include kitchen-oriented demo tickets so you can:

- Screenshot the board for investors or CodeCanyon previews
- Train staff before lunch rush
- Verify tablet layout without placing ten real orders

After you are comfortable, switch to live orders only and clear or ignore seed tickets as appropriate for your database hygiene.

## 4. Tablet & station tips

1. **Mount at eye level** for the pass — avoid forcing cooks to unlock a phone in a pocket.
2. Use **landscape**, keep brightness high, disable auto-lock during service (or use a kiosk-style device policy).
3. Stay on a **stable Wi‑Fi** path to the API; a flaky LAN makes tickets lag and looks like “KDS is broken.”
4. One board per station is fine; multiple devices can sign in as the same restaurant if your seats allow it — agree who advances which ticket to avoid double updates.
5. Combine with **Subscriptions** / **Sponsored listings** demos when pitching restaurants: orders + ads + membership + KDS in one partner app.

## 5. Quick troubleshooting

| Issue | What to try |
|-------|-------------|
| Empty board | Accept an order; confirm `migrate:up`; use live mode |
| Ticket missing after accept | Pull to refresh; verify restaurant account matches the order’s restaurant |
| Status not moving | Check API reachability; retry; confirm user permissions |
| Demo-only data | Restart with `npm run start:live` |

## Related

- [Restaurant getting started](./getting-started.md)  
- [Logistics & POD](../delivery-app/logistics.md) — what happens after food is ready  
- [Monetization](../admin-app/monetization.md) — partner subscriptions alongside KDS
