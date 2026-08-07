# Incoming orders — Restaurant app

Accept/reject live tickets and advance status through prep → ready → pickup/driver handoff. This is the same order pipeline that feeds [Kitchen Display](./kitchen-display.md), the driver app, and customer tracking — accepting here is the hinge point for all of it.

## What drives this

- **Restaurant must be open** — `Restaurant.is_closed` and the `openingTime`/`closingTime` window ([hours & delivery zone](./hours.md)) gate whether new orders can even be placed against this restaurant; being "closed" doesn't hide existing tickets already in the pipeline.
- **Auto-accept** — per-user `UserSettings.restaurantSettings.autoAcceptOrders` (off by default) will accept incoming orders automatically instead of waiting for a manual tap; paired with `preparationTime`, a per-user default prep estimate distinct from the restaurant-wide `DeliverySetting.deliveryPreparationTime` used in [smart ETA](../customer-app/smart-eta.md).
- **Status advances** (`pending → preparing → ready → out_for_delivery/pickup`) are what [Kitchen Display](./kitchen-display.md) and the driver app read to know what to show — advancing status here is not cosmetic, it unlocks the next actor's screen (e.g. `ready` is what makes an order eligible for driver batching).
- **Reject reason** is recorded on the order for support/analytics, not silently discarded.

## Try it

1. Keep the restaurant **open**.
2. Watch the orders list — accept what you can cook; reject with a reason when you can't.
3. Advance status as food progresses; mark ready for courier/pickup and confirm it becomes assignable in the [driver job board](../delivery-app/deliveries.md).
4. Optionally run the same pipeline on [Kitchen Display](./kitchen-display.md) instead of this list — both read/write the same order.

## Related

- [Hours & delivery zone](./hours.md) · [Menu](./menu.md) · [Kitchen Display](./kitchen-display.md)
