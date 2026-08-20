# AI intelligence — index

Customer-facing intelligence is split into three HOW-TOs. All three are served by the same backend engine (`src/services/intelligenceService.js`) and share the same weather/routing fallbacks.

| Guide | What you configure |
|-------|---------------------|
| [AI recommendations](./recommendations.md) | Nothing to toggle — always on; quality depends on product tags/discounts, ratings, and real order history. |
| [Smart delivery ETA](./smart-eta.md) | Per-restaurant `deliveryPreparationTime` (prep minutes) drives the floor of the range; live kitchen load and travel distance drive the rest. |
| [Surge pricing](./delivery-fee.md) | Per-restaurant delivery fee type/thresholds set the base; the surge multiplier itself reacts to live order/driver demand and weather, not an Admin dial. |

Backend overview: [AI & pricing brain](../my-backend/intelligence-engine.md).

Offline fallbacks (Open-Meteo weather → heuristic; OSRM routing → haversine heuristic) keep all three features working without external network access — each linked page documents its own fallback behaviour.
