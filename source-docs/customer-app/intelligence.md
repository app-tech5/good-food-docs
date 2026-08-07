# AI / ops intelligence — recommendations, ETA, surge

The platform includes operator-friendly intelligence that makes carts smarter, arrival times clearer, and delivery fees responsive to demand. Clients talk to **`/api/intelligence`**. External weather (Open-Meteo) and routing (OSRM) are used when reachable; **local heuristics keep demos working offline**.

This page explains what each capability does, how customers see it, and how you can demonstrate it after the suite is running.

## What operators get

| Capability | Business effect |
|------------|-----------------|
| **Recommendations** | Suggest sides, drinks, and complements → higher average order value and more commission without a merchandising team |
| **Smart ETA** | Combine kitchen load + travel estimates + rush windows → fewer “where is my food?” tickets |
| **Surge fee** | Multiply delivery fee when demand outpaces online drivers (and optional weather pressure) → protect SLA and capture peak value |

You do not need a separate ML vendor to show a modern marketplace story on day one.

## How the customer sees it

1. **Browse / product flows** — recommendation chips or “recommended for you” style suggestions based on prior pairs, time-of-day buckets (breakfast / lunch / snack / dinner), and weather tags when weather data is available.
2. **Checkout / fee line** — ETA ranges (for example a min–max minute label) and, when surge applies, a clearer delivery fee (multiplier or “high demand” style messaging).
3. **Honesty in copy** — when surge is idle, customers still see a standard fee; when it spikes, reasons can include high demand vs drivers, rush hour, or weather.

Restaurant and admin users benefit indirectly: larger baskets, calmer support, and fees that track city stress.

## Offline / fallback behaviour

| Signal | Preferred source | If unreachable |
|--------|------------------|----------------|
| Weather | Open-Meteo (no API key) | Recommendations / surge continue with non-weather heuristics |
| Road travel | OSRM | Haversine / heuristic travel estimates for ETA |
| Demand | Live orders vs online drivers | Surge logic still runs on available counts |

For CodeCanyon and laptop demos, **fallbacks matter**: you can pitch intelligence without guaranteeing outbound network access to every third-party host.

## How to demo (practical script)

### Recommendations

1. Start API + customer app with migrated data.
2. Sign in as a customer who already has some order history (place two related orders if the account is new).
3. Open a restaurant menu / cart path where recommendations render.
4. Point out time-of-day relevance (demo at lunch vs evening if you can).
5. Optionally disconnect weather access and show that suggestions still appear via fallbacks.

### Smart ETA

1. Create kitchen load: accept several orders in the restaurant app (or use seeded activity).
2. As a customer, open checkout or the ETA display on a store / cart screen.
3. Explain that the window reflects kitchen queue + travel, not a static “30 minutes” guess.
4. Mention OSRM when online; heuristics when not.

### Surge

1. Put few drivers online (or busy) while generating several open delivery orders.
2. Open customer checkout and show an elevated delivery fee / surge label when the multiplier kicks in.
3. Bring more drivers online or let demand fall; show the fee returning toward standard.
4. If weather pressure is active in your build, call it out as an optional signal — not a hard dependency.

## Operator checklist

1. API running; `/api/intelligence` reachable from the customer app’s host.
2. At least one restaurant with products and a customer session.
3. Demo script above rehearsed before investor calls.
4. Pair with [logistics](../delivery-app/logistics.md) so ETA stories continue into live tracking after checkout.

## Related

- [Launch suite](./00-launch-suite.md)  
- [Monetization](../admin-app/monetization.md) — commission on larger baskets  
- [Environment config](./environment-config.md) — network assumptions for production
