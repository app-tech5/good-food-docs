# Catalog & partners — Backend API

What has to be true on a restaurant/menu/product for it to actually show up in discovery — not a route list.

## The flags that gate discovery

A restaurant isn't visible or orderable just because it exists in the database. Three fields on `Restaurant` matter:

| Field | Meaning | Effect |
|---|---|---|
| `isActivated` | Partner has been approved/onboarded. | Gates whether the restaurant gets **new-order notifications** at all (an order to a non-activated restaurant is created but the restaurant isn't notified) and whether a [sponsored listing](../admin-app/sponsored.md) for it is shown. Flipping this from off→on also fires a "restaurant activated" notification to that restaurant's staff. |
| `is_closed` | Manual closed toggle (restaurant or admin). | Intended to hide the restaurant from active ordering — enforce this in your discovery query if your client list endpoint doesn't already filter on it. |
| `isAvailableForDelivery` | Restaurant currently accepts delivery orders. | Same idea — a discovery/filter flag your client-facing list should respect alongside `DeliverySetting.isDeliveryEnabled`. |

Because the generic list endpoints in this backend let the caller pass filters, whether closed/inactive restaurants actually disappear from a given screen depends on that screen querying with the right filter — this is worth testing per client, not assuming.

At the item level, `Product.availability` and `Menu.availability` are simple on/off switches — 86'd items should flip `availability: false` (restaurant app has a dedicated toggle route for this) rather than being deleted, so order history keeps working.

## What must be set for a restaurant to be orderable

1. `Restaurant` document exists with `isActivated: true`, correct `latitude`/`longitude` (used by ETA/surge and driver routing — see [logistics engine](./logistics-engine.md)), and a `tax` reference (auto-assigned from the oldest seeded `Tax` if you don't set one — see [market data](./market-data.md)).
2. At least one `Category`, and `Product`/`Menu` documents pointing at that restaurant with `availability: true` and a real `price`.
3. A `DeliverySetting` document for the restaurant if you want delivery-specific fees/prep time/radius rather than the platform-wide App Settings fallback — see [logistics engine](./logistics-engine.md).
4. Optionally a `commission_rate` override on the restaurant (see [commission engine](./commission-engine.md)) and a `RestaurantPaymentSetting` if it should not accept every globally-active gateway (see [payments & wallet](./payments-wallet.md)).

## Configure catalog data

1. Admin → **Restaurants / Users / Drivers** — activate partners, edit profile fields (hours, address, commission override, categories, activation) ([partners](../admin-app/partners.md)).
2. Seed or edit **Menus / Products** centrally ([catalog](../admin-app/catalog.md)), or let restaurants self-serve via the restaurant app's **Menu** screen — both write to the same `Menu`/`Product` collections.
3. Customer discovery should drop closed restaurants and 86'd items after a refresh — if it doesn't, that screen's query needs the `isActivated`/`is_closed`/`availability` filters above.

## Smoke test

1. Create or edit one dish in the restaurant app → toggle its availability off → confirm it disappears from customer menu after refresh, but still appears (greyed out or omitted, per your client) rather than erroring.
2. Flip a restaurant's `isActivated` off → confirm new orders to it no longer trigger the "new order received" notification.
3. Admin catalog view matches what the restaurant app shows for the same item.

## Related

- [Order lifecycle](./order-lifecycle.md)
- [Logistics engine](./logistics-engine.md)
- [Commission engine](./commission-engine.md)
- Admin: [partners](../admin-app/partners.md) · [catalog](../admin-app/catalog.md)
