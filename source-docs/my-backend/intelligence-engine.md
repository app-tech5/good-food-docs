# AI & pricing brain — Backend API

Recommendations, smart ETA, and surge delivery fee — computed live from your marketplace data (plus optional weather/routing).

Intelligence provider abstraction:
- `AI_PROVIDER=builtin` (default) for deterministic local scoring
- `AI_PROVIDER=openai` or `AI_PROVIDER=gemini` for optional model-driven recommendations, ETA, and surge tuning
- optional feature-level overrides: `AI_RECOMMENDATION_PROVIDER`, `AI_ETA_PROVIDER`, `AI_SURGE_PROVIDER`
- automatic fallback to `builtin` if provider keys are missing or provider calls fail

## What operators configure

| Surface | Effect on intelligence |
|---|---|
| Restaurant **prep time** / delivery fee / free threshold / max distance (`DeliverySetting`) | Feeds ETA base prep and the delivery-fee base before surge |
| Driver **online** status | More online drivers → lower surge |
| Open kitchen load (`pending` / `preparing` / `ready`) | Busier kitchen → longer ETA |
| Order history + product tags/ratings | Powers “often bought together” recommendations |
| `.env` `OPEN_METEO_BASE_URL` / `OSRM_BASE_URL` / `INTELLIGENCE_HTTP_TIMEOUT_MS` | Optional self-hosted weather/routing and timeout |
| `.env` `AI_PROVIDER` / `OPENAI_API_KEY` / `GEMINI_API_KEY` (+ model vars) | Switch intelligence provider between built-in and external AI |
| `.env` `AI_RECOMMENDATION_PROVIDER` / `AI_ETA_PROVIDER` / `AI_SURGE_PROVIDER` | Override provider per feature when needed |

Surge thresholds, ETA padding, and scoring weights ship tuned in `src/constants/intelligence.js` so the feature works out of the box without an extra Admin panel.

## What customers see

- Recommendations ranked from pairs + ratings + time/weather tags (plus optional OpenAI/Gemini re-rank)
- Smart ETA with prep + kitchen + travel (+ weather when reachable)
- Surge multiplier on delivery fee when demand is high or drivers are scarce

## Verify

1. API up; customer app reaches intelligence endpoints.
2. Restaurant with products + a customer with order history → pair-based suggestions.
3. Several open delivery orders and few online drivers → surge multiplier > 1.
4. Offline weather/routing → ETA still returns via local heuristics.

## Related

- [Logistics engine](./logistics-engine.md)
- Customer: [recommendations](../customer-app/recommendations.md) · [smart ETA](../customer-app/smart-eta.md) · [delivery fee](../customer-app/delivery-fee.md)
