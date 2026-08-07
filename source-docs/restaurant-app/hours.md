# Hours & delivery zone — Restaurant app

Two related settings surfaces: **opening hours** (when the restaurant can take orders at all) and **delivery settings** (how far, how fast, and how much it costs) — both feed directly into what customers and drivers see elsewhere.

## What drives this

**Opening hours** (`Restaurant.openingTime` / `closingTime`, plus `is_closed`):

- Outside this window, the restaurant shows **closed** on the [customer restaurant page](../customer-app/restaurant-page.md) even if nothing else changed.
- `is_closed` is a manual override the restaurant can flip regardless of the clock (e.g. unplanned closure).

**Delivery settings** (`DeliverySetting`, one document per restaurant):

- **`maxDeliveryDistance`** (shown as "delivery radius" in this screen) — caps how far a customer's address can be and still order delivery from this restaurant; also the basis for [driver batch radius](../delivery-app/deliveries.md) if `autoAssignmentRadius` isn't set separately.
- **`deliveryPreparationTime`** (shown as "estimated time") — the prep-minutes floor used by [smart ETA](../customer-app/smart-eta.md); a restaurant that under-reports this will show ETAs that don't match reality.
- **`deliveryFeeType`** (`FIXED` / `DYNAMIC` / `FREE` / `RESTAURANT_DEFINED`), **`fixedDeliveryFee`**, **`dynamicDeliveryFee`** (base/per-km/min/max), and **`freeDeliveryThreshold`** — together they are the base fee that [surge pricing](../customer-app/delivery-fee.md) multiplies against; edit these to change what a non-surge delivery costs.
- **`autoAssignmentRadius`** and **`driverAssignmentMethod`** — how far and how automatically the platform offers this restaurant's `ready` orders to nearby drivers ([job board & batching](../delivery-app/deliveries.md)).

## Try it

1. Open **Opening Hours** — set weekly hours and save before service.
2. Open **Delivery Settings** — review delivery radius and estimated prep time; adjust the fee type/threshold if needed.
3. Confirm the [customer restaurant page](../customer-app/restaurant-page.md) shows matching open/closed state and a fee/ETA that reflects these numbers.
4. Shrink the delivery radius drastically and confirm addresses just outside it can no longer complete delivery checkout to this restaurant.

## Related

- [Incoming orders](./orders.md) · [Driver job board](../delivery-app/deliveries.md) · [Surge pricing](../customer-app/delivery-fee.md)
