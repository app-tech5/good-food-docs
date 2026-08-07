# Catalog & partners — Backend API

Restaurants, menus, products, variants, and user accounts every discovery screen depends on.

## Operator steps

1. Admin → **Restaurants / Users / Drivers** — activate partners ([partners](../admin-app/partners.md)).
2. Seed or edit **Menus / Products** centrally ([catalog](../admin-app/catalog.md)).
3. Restaurant app → **Menu** for partner self-serve edits ([menu](../restaurant-app/menu.md)).
4. Customer discovery — closed restaurants / 86’d items must disappear after refresh.

## Smoke test

Create or edit one dish in restaurant app → customer menu shows new price → admin catalog matches.

## Related

- [Order lifecycle](./order-lifecycle.md)
- Online: Catalog & partners
