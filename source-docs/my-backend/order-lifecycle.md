# Order lifecycle — Backend API

How one shared order record moves from checkout to delivered across customer, restaurant, driver, and admin.

## Prerequisites

- API migrated and running ([getting started](./getting-started.md))
- At least one customer, restaurant, and (for delivery) driver account from seed or admin

## What the API owns

The order document is the **source of truth**: line items, payment state, restaurant, optional driver, and fulfillment status. Mobile and admin UIs only display and advance that record — they do not keep a private copy.

Useful surfaces: **`/api/orders`** (and related restaurant / driver order routes).

## Smoke test

1. Customer places a delivery order and pays with an enabled method.
2. Restaurant accepts (orders list or KDS).
3. Driver is assigned / accepts; advances toward delivered.
4. Customer opens tracking — status matches restaurant and driver.
5. Admin → **Orders** → open the same id — payment + fulfillment coherent.

If one app shows a different status, refresh and confirm API URL / auth on that client. The bug is almost never “three databases.”

## Related

- [Live status sync](./live-updates.md)
- [Logistics engine](./logistics-engine.md)
- Online: `my-backend/order-lifecycle.html`
