# Smart delivery ETA — Customer app

The ETA chip on the restaurant page and checkout is a real min–max range computed per request from kitchen load, prep time, and travel — it is not a fixed label.

## What drives this

- **Prep time floor** — each restaurant's `DeliverySetting.deliveryPreparationTime` (default 30 min) is the base; there's no Admin App Settings equivalent, it's set per restaurant.
- **Kitchen load** — the number of that restaurant's orders currently `pending`/`preparing`/`ready` adds extra minutes (capped at 45 extra minutes) — a busy kitchen genuinely widens the ETA shown to customers.
- **Travel time** — uses live **OSRM** driving-time routing between the restaurant and customer coordinates when reachable; falls back to a distance-based heuristic (faster in normal hours, slower during rush windows) when OSRM is unreachable.
- **Rush hour** — 7–9, 12–14, and 17–20 apply a travel-time multiplier on top of the routed or heuristic time.
- **Weather** — rain adds ~6 minutes, cold adds ~3 minutes to the top of the range (via the same Open-Meteo/heuristic weather lookup used by recommendations and surge).

None of this is Admin-configurable beyond the restaurant's prep time — the rest reacts to real order volume, distance, and weather at request time.

## Try it

1. Build up kitchen load for a restaurant (several accepted/preparing orders), or use seeded demo activity.
2. Open that restaurant's detail page / checkout — note the ETA range (e.g. "26–36 min").
3. Clear the kitchen queue (advance/deliver those orders) and reload — the range should tighten back toward the base prep + travel time.
4. Explain to the client: OSRM routing when online, heuristic distance × time-per-km when offline — both are visible in the API response's `factors.routingSource`.

## Related

- [Restaurant details](./restaurant-page.md) · [Recommendations](./recommendations.md) · [Surge pricing](./delivery-fee.md)
