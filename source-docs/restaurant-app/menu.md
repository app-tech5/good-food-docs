# Menu management — Restaurant app

Categories, dishes, prices, photos, variants, and the 86 (availability) toggle — this is the same `Product` collection the customer app reads from directly, so changes here are live, not published on a delay.

## What drives this

- **`Product.availability`** is the 86 switch — flip it off and the item is immediately unorderable in the [customer menu](../customer-app/menu-cart.md), even mid-service, without deleting the item or its history.
- **Price, photo, description, variants/extras** edited here are exactly what the customer sees — there is no separate "draft" copy.
- **`discount`** on a product (if set) feeds directly into [AI recommendations](../customer-app/recommendations.md) scoring — discounted items get a small ranking boost on the customer's cross-sell rail.
- **Categories** organize the menu and also drive customer-app category browsing/search matching.
- Admin can also curate menus centrally across restaurants via the [catalog](../admin-app/catalog.md) tool — both paths write to the same `Product` documents.

## Try it

1. Drawer → **Menu**.
2. Add or edit categories and items; set price and photo.
3. Toggle availability off on one item (86 it).
4. Refresh the [customer menu](../customer-app/menu-cart.md) for the same restaurant and confirm that item is gone/greyed and cannot be added to cart.
5. Turn availability back on and confirm it reappears.

## Related

- [Analytics](./analytics.md) · [Admin catalog](../admin-app/catalog.md)
