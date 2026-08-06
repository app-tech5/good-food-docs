# AI / ops intelligence (developer)

Recommendations (cross-sell), smart ETA, and surge delivery fee multipliers.

## Service

- `my-backend/src/services/intelligenceService.js`
- Constants: `my-backend/src/constants/intelligence.js`
- Routes: `my-backend/src/routes/intelligenceRoutes.js` → **`/api/intelligence`**
- Mounted in `my-backend/src/server.js`

## Capabilities

### Recommendations

Complementary products from:

- Order history pairs
- Time-of-day buckets (breakfast / lunch / snack / dinner)
- Weather tags (Open-Meteo when reachable)

### Smart ETA

Combines:

- Kitchen load (active / kitchen order statuses)
- Travel estimates (OSRM when reachable, haversine / heuristic fallback)
- Rush-hour windows

### Surge fee

Multiplier from demand vs online drivers (+ optional weather pressure), applied to delivery fee server-side.

## External inputs

| Signal | Source |
|--------|--------|
| Weather | Open-Meteo (no API key) |
| Routing | OSRM |
| Fallback | Local heuristics when offline |

## Client usage

Customer app consumes intelligence endpoints for reco / ETA / surge presentation at browse and checkout (see customer API / demo handlers as applicable).
