# Menu & basket — Customer app

Categories, items, variants, and the running cart for a single restaurant. What's orderable here is a live reflection of that restaurant's catalog — nothing is cached into the app at build time.

## What drives this

- **`Product.availability`** — the restaurant's 86 toggle ([restaurant menu](../restaurant-app/menu.md)). Set to `false` and the item disappears from the customer menu on next refresh; it cannot be added to cart even if it's still in an old cart screenshot.
- **Categories, prices, photos, variants/extras** all come straight from the restaurant's (or Admin's centrally-curated [catalog](../admin-app/catalog.md)) product documents — editing there is what changes what the customer sees, there is no separate customer-app copy of the menu.
- **Cross-sell rail** on the menu is the same [AI recommendations](./recommendations.md) engine used elsewhere — driven by order pairing, time of day, and weather, not manual merchandising.
- **Restaurant open/closed state** ([restaurant page](./restaurant-page.md)) doesn't hide the menu, but checkout will reject placing an order against a closed restaurant.

## Try it

1. On a restaurant menu, add 2+ items (use variants if the build exposes them).
2. Confirm quantity steppers and the **View Cart** badge update.
3. Open the cart — change a quantity, remove a line, confirm totals recompute (tax + delivery fee are added at checkout, not shown in the basket subtotal).
4. From the restaurant app, 86 one of the items in the cart and refresh the customer menu — it should no longer be orderable.
5. Continue to [checkout](./checkout.md).

## Related

- [Recommendations](./recommendations.md) · [Restaurant menu management](../restaurant-app/menu.md)
