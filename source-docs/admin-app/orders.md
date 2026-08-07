# Orders — Admin app

One list of every order placed across the marketplace, regardless of which channel it came in on (app, WhatsApp, USSD, web, or admin-created). Use it to investigate a specific order, confirm status, and see how it was paid and delivered.

## What you configure (per order)

Orders aren't a form you fill in from scratch — you're reviewing and, when needed, correcting a record created by checkout. The fields worth understanding:

| Field | Meaning | Effect when set |
|---|---|---|
| **Status** | `pending → preparing → ready → out_for_delivery → delivered`, or `cancelled` | Changing status here pushes the same update the restaurant/driver apps would send — it fires customer notifications and (if cancelled) can trigger an instant wallet refund when that setting is on |
| **Payment → Method** | How the customer paid (`credit_card`, `cash_on_delivery`, `wallet`, `paystack`, `flutterwave`, `razorpay`, `paypal`, `crypto`, `mobile_money`, `google_pay`, `apple_pay`) | Read-only context — tells you which gateway page to check if payment looks wrong |
| **Payment → Status** | `pending / paid / failed / refunded` | If an order is `delivered` but payment is still `pending`/`failed`, that's the first thing to fix before anything else |
| **Order Source** (`orderSource`) | Which channel created the order: `app`, `whatsapp`, `ussd`, `web`, `admin` | Tells you which channel to check in [order channels](./order-channels.md) if something about intake looks wrong |
| **Delivery → Type** | `delivery` or `pickup` | Pickup orders won't have a driver assigned; don't chase a "missing driver" on those |
| **Delivery → Proof of Delivery** | Photo, signature, contactless flag, geofence check captured at drop-off | Present only once a driver completes delivery — useful for "where's my order" disputes |
| **Driver** | Assigned courier (delivery orders only) | Blank until a driver accepts; reassignable if a driver goes dark on an active order |
| **Items / Extras / Variants** | Snapshot of what was ordered, at the price charged at order time | This is the source of truth for "what did the customer actually pay for" — it won't change even if the menu changes later |

## How to set it up

1. Open **Orders** on an incident, support ticket, or spot-check.
2. Search/filter by customer, restaurant, or order id.
3. **View** the full detail — line items, payment, driver, timeline — before changing anything.
4. Only change **Status** when you're intentionally overriding the normal restaurant/driver flow (e.g. manually completing a stuck order). Prefer letting the restaurant/driver apps drive status in normal operation.
5. If payment looks wrong, cross-check the specific gateway in [Gateways](./gateways.md) or the [money ledger](./transactions.md) before editing the order.
6. Only look at the customer/restaurant/driver mobile apps once the API record here looks wrong — most "bugs" turn out to be a stale client view of a correct order.

## Verify

| Check | Expect |
|---|---|
| Open an order by id | Full detail: items, totals, payment, delivery, driver, timeline |
| Filter by `orderSource` | Orders from WhatsApp/USSD/web show up alongside app orders |
| Move status forward on a test order | Customer gets a notification; earnings/transactions reflect it once `delivered` |
| Cancel a test order | Payment status flips to `refunded` (if wallet instant refund is on, the customer wallet updates immediately) |

## Related

- [Order channels](./order-channels.md) · [Partners](./partners.md) · [Transactions](./transactions.md) · [Earnings](./earnings.md)
- [Backend order lifecycle](../my-backend/order-lifecycle.md)
