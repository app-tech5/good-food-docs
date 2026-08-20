# Browse & discover — Customer app

Home, search, and the nearby map — how customers find a restaurant before opening its page. What appears here is a direct read of restaurant/product data and a couple of Admin gates, not hardcoded demo content.

## What drives this

- **`Restaurant.isActivated`** must be `true` for a restaurant to appear anywhere in discovery (home, search, map). Newly onboarded restaurants stay invisible to customers until an admin activates them.
- **`Restaurant.isAvailableForDelivery`** and `serviceModes` (`delivery` / `pickup`) control which toggle state (Delivery vs Pickup) a restaurant shows under.
- **Promo / Special Offers cards** on home are populated from active Admin promotions/coupons and any live [sponsored listings](../restaurant-app/sponsored.md) placed in the `home_banner` slot.
- **Map pins** use `Restaurant.latitude` / `longitude`; a restaurant with unset coordinates won't render a pin even if it's activated.
- **Map provider** defaults to `MapLibre + OpenStreetMap` (`EXPO_PUBLIC_MAP_PROVIDER=osm`, zero map API fee). Buyers can switch to `maptiler`, `mapbox`, or `google` with env config (`EXPO_PUBLIC_MAP_PROVIDER` + matching key/token) without editing map screen code.
- **Search** matches restaurant name, category, and product name/description across activated restaurants.
- App Settings **`isMaintenance`** exists in Admin as a platform-wide flag; note that the current app builds don't read it directly, so treat it as a backend-only signal rather than a customer-facing kill switch unless you've wired it into your fork.

## Try it

1. Open home — the Delivery/Pickup toggle, categories, and promo cards should load from the API (empty ≠ broken if you have zero activated restaurants or zero live promos).
2. Open **Search** — type a restaurant or dish keyword and open a result.
3. Open the nearby **map** — pins plus a swipeable card per restaurant (this is not the post-checkout tracking map).
4. Tap a restaurant → continues to [restaurant details](./restaurant-page.md).

Empty home is almost always: API URL misconfigured, migrations not run, or every restaurant still has `isActivated: false`.

## Related

- [Restaurant details](./restaurant-page.md) · [AI recommendations](./recommendations.md)
