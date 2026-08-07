# Performance — Restaurant app

Revenue, average order value, trends, and bestsellers for a selected period — computed from this restaurant's real completed orders, not sample/mock data. An empty chart on day one is the correct behaviour, not a bug.

## What drives this

- **Period selector** re-queries orders for that window (day/week/month depending on your build) and recomputes every metric — nothing here is cached beyond the current period.
- **Revenue / average order value / trend** are aggregated from this restaurant's own `Order` totals (`totalPrice`, including delivery fee and tax as charged) — orders still `pending`/`cancelled` don't count as revenue.
- **Bestsellers** come from actual item quantities across completed orders — a menu item with zero real orders will never appear here regardless of how it's priced or photographed.
- Numbers here are restaurant-scoped; platform-wide equivalents live in Admin ([reports](../admin-app/reports.md), [sales reports](../admin-app/sales-reports.md)).

## Try it

1. Complete several live orders over a day or two (empty charts on day one are expected).
2. Open **Analytics** and switch the period selector — confirm totals change with the window.
3. Use bestsellers and quiet time slots to adjust the [menu](./menu.md) (feature or 86 items) and staffing.

## Related

- [Incoming orders](./orders.md) · [Menu](./menu.md)
