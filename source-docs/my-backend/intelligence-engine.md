# AI & pricing brain — Backend API

Recommendations, smart ETA, and surge fees via **`/api/intelligence`**. Weather (Open-Meteo) and routing (OSRM) when reachable; local heuristics offline.

## Demo script

Follow the practical steps in the customer guides (same API, UI-facing checklists):

- [Recommendations](../customer-app/recommendations.md)
- [Smart delivery ETA](../customer-app/smart-eta.md)
- [Surge pricing](../customer-app/delivery-fee.md)

Hub overview (older path): [intelligence.md](../customer-app/intelligence.md).

## Operator checklist

1. API up; customer app can reach `/api/intelligence`.
2. Restaurant with products + a customer with some order history.
3. For surge: few online drivers + several open delivery orders.
4. Confirm offline fallbacks still return ETA / suggestions without external hosts.

## Related

- [Order lifecycle](./order-lifecycle.md)
- [Logistics engine](./logistics-engine.md)
