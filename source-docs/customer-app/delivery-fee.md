# Surge pricing — Customer app

The delivery fee chip on the restaurant page and checkout shows a **base fee** (set per restaurant, or a platform default) multiplied by a **live surge multiplier** computed by the intelligence engine — not a manual Admin toggle.

## What drives this

**Base fee** — per-restaurant delivery config wins over the platform default:

- Each restaurant's `DeliverySetting.deliveryFeeType` is `FIXED`, `DYNAMIC`, `FREE`, or `RESTAURANT_DEFINED`. `FIXED` uses `fixedDeliveryFee`; `DYNAMIC`/`RESTAURANT_DEFINED` computes `baseFee + distanceKm × perKmFee`, clamped between `minFee` and `maxFee`.
- `DeliverySetting.freeDeliveryThreshold` (or `freeDeliveryEnabled`) zeroes the fee once the cart subtotal clears it, at the restaurant level.
- If a restaurant has no `DeliverySetting`, the platform falls back to App Settings **`deliveryFee`** and **`freeDeliveryThreshold`**.
- **`maxDeliveryDistance`** (per restaurant, or the App Settings default) caps how far the order can be from the restaurant before delivery isn't offered at all.

**Surge multiplier** — recomputed on every quote from live signals (demand vs online drivers, weather, rush hours), capped at 2×. Membership `freeDelivery` still forces the fee to **0** after surge.

## Try it

1. Get a few drivers online and create several open delivery orders for one restaurant.
2. Open that restaurant / checkout — the fee chip should show an elevated amount or a surge label when demand is high.
3. Bring more drivers online — the fee should drop back toward the base.
4. Free delivery: cart above `freeDeliveryThreshold`, or an active membership with `freeDelivery`.
5. Member discount: active plan with `discountPercent` reduces subtotal before tax.

## Related

- [Smart ETA](./smart-eta.md) (time ≠ fee — they share inputs but compute separately)
- [Intelligence hub](./intelligence.md) · [Backend AI brain](../my-backend/intelligence-engine.md)
