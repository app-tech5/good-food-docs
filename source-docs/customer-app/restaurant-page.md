# Restaurant details — Customer app

Open/closed state, ETA chip, delivery fee/surge chip, restaurant-scoped offers, and reviews for a single restaurant — everything here is computed against that restaurant's own settings, not global defaults.

## What drives this

- **Open/closed** — `Restaurant.is_closed` plus `openingTime`/`closingTime` ([restaurant hours](../restaurant-app/hours.md)); a restaurant outside its own opening window shows closed even if `is_closed` is `false`.
- **ETA chip** — [smart ETA](./smart-eta.md): that restaurant's prep time + current kitchen load + travel distance/time.
- **Fee / surge chip** — [surge pricing](./delivery-fee.md): that restaurant's `DeliverySetting` base fee/threshold, multiplied by the live demand/weather surge factor.
- **Available Offers** on this page are restaurant-scoped promotions/sponsored placements — distinct from the global **Offers** tab in [checkout](./checkout.md).
- **Reviews / rating** roll up from delivered orders' review data tied to this restaurant.

## Try it

1. From [discovery](./discovery.md), open a restaurant.
2. Confirm **open/closed** matches that restaurant's configured hours.
3. Note the **ETA** chip and cross-check against current kitchen load.
4. Note the **fee/surge** chip and cross-check against active orders/drivers near that restaurant.
5. Scroll **Available Offers** / reviews for that restaurant specifically (not the global Offers tab).

## Related

- [Menu & basket](./menu-cart.md) · [Restaurant hours & delivery zone](../restaurant-app/hours.md)
