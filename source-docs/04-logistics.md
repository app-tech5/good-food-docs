# Logistics & proof of delivery (developer)

Order batching, live map tracking, and multimedia POD (photo + signature).

## Batching

- Service: `my-backend/src/services/logisticsService.js`
  - `findBatchCandidates({ orderId, driverId, radiusKm })`
  - Radius from delivery settings (`autoAssignmentRadius`) with clamps
  - Helpers for dropoff / restaurant coordinates (GeoJSON or lat/lng)
- Constants: `my-backend/src/constants/logistics.js`
- Routes: `my-backend/src/routes/logisticsRoutes.js` → **`/api/logistics`**
- Mounted in `my-backend/src/server.js`

## Live map tracking

- Customer app: map / tracking screens and markers
- Driver app: active deliveries, navigation, location updates
- Shared order location fields on `Order` / user location

## Proof of delivery (POD)

- `delivery-app/components/ProofOfDeliveryModal.js` — capture / attach proof media
- `delivery-app/components/SignaturePad.js` — customer signature
- Wired via `delivery-app/hooks/useDeliveryActions.js` and driver order hooks (`useDriverOrders.js`)

## Related settings

- `DeliverySetting` (per restaurant) influences assignment radius and logistics behaviour
- Driver subscription tiers may gate access features (see monetization docs)
