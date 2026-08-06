# Logistics & proof of delivery — how to run last mile

This guide walks operators through assignment radius / delivery settings, driver batching, live map tracking, and completing a delivery with **photo + signature** proof. Useful API paths live under **`/api/logistics`** (batch suggestions, accept-batch, complete-with-proof).

## Prerequisites

- API migrated and running
- Customer, restaurant, and driver apps pointed at the same `/api` base
- Driver location permissions granted

## 1. Assignment radius & delivery settings

Couriers get work that fits your geography. Delivery settings (including **`autoAssignmentRadius`**) influence how far the platform looks when suggesting nearby compatible jobs. Values are clamped to safe defaults in the API so an extreme setting does not melt the matcher.

### What to do

1. In **admin** (or restaurant delivery-settings UI if exposed for that partner), review delivery / assignment radius for the restaurants you test with.
2. Start with a modest city radius (a few kilometres) for demos so batch suggestions actually find neighbours.
3. Place two orders to nearby drop-offs if you want to demonstrate batching.
4. If drivers never see jobs, widen radius slightly and confirm restaurants are marking orders ready for assignment.

Driver subscription tiers may gate some logistics features — configure plans under [monetization](./01-monetization.md) if access seems plan-locked.

## 2. Batching (concept & how to demo)

**Batching** lets a driver take compatible deliveries that sit close together — fewer empty miles, more completes per shift.

### Demo steps

1. Create two (or more) assignable orders with drop-offs in the same neighbourhood.
2. Sign in as a **driver**, go online, and open an active job.
3. When the app offers **batch suggestions**, review the candidates and **accept the batch** if it looks sane.
4. Complete stops in a sensible order; confirm both orders progress.

Under the hood the client uses logistics routes such as batch-suggestions and accept-batch on **`/api/logistics`**. You do not need to call them manually for a normal demo.

## 3. Live tracking

1. Customer places an order; restaurant accepts; driver is assigned and moving.
2. On the **customer** app, open order tracking / map and confirm the driver marker updates.
3. On the **driver** app, keep location on and the delivery active so updates keep flowing.
4. Spotty tracking is almost always permissions, background limits, or API URL / network — not “the map library is missing.”

## 4. Complete with proof of delivery (photo + signature)

At the door, drivers can capture multimedia proof — important for cash-on-delivery, high-value orders, and “I never got it” disputes.

### Driver steps

1. Arrive at drop-off (stay within any geofence the app enforces).
2. Choose complete / deliver on the active job.
3. When **Proof of delivery** opens:
   - Capture a **photo** of the drop-off when required (contactless flows often require a photo).
   - Capture a **customer signature** on the signature pad when required.
4. Submit. The order should move to delivered for customer, restaurant, and admin.

If the API rejects completion, read the on-screen error: common causes are missing photo/signature when policy requires proof, or standing too far from the drop-off coordinates.

## 5. Full logistics smoke test

1. Customer orders delivery.
2. Restaurant accepts and advances kitchen status ([KDS](./03-kitchen-display.md) optional).
3. Driver accepts job (and a batch if offered).
4. Customer watches live tracking.
5. Driver completes with **photo + signature**.
6. Admin opens the order — status delivered, earnings sensible.

## Related

- [Driver getting started](./getting-started-driver.md)  
- [Launch suite checklist](./00-launch-suite.md)  
- [Intelligence](./05-intelligence.md) — ETA / surge that customers see beside tracking
