# Monetization (developer)

How the platform earns: commissions, SaaS subscriptions, sponsored listings, wallet ledger, and multi-PSP gateways.

## Overview

Revenue levers are implemented in `my-backend` and surfaced in Customer / Driver / Restaurant / Admin apps.

## Commissions

- Service: `my-backend/src/services/commissionService.js`
  - `getEffectiveCommissionRate(restaurantOrId)` — base restaurant or app-setting rate, then applies active **restaurant** subscription benefits (`waiveCommission`, `reducedCommissionPercent`, `platformAccess`).
  - `splitOrderAmounts(orderTotal, commissionRatePercent)` — platform vs restaurant shares.
- Admin earnings UIs consume these splits for ops and payouts.

## Subscriptions (SaaS tiers)

- Model: `Subscription` / `UserSubscription`
- Service: `my-backend/src/services/subscriptionService.js`
  - Targets: `customer` | `driver` | `restaurant`
  - Fields: price, currency, `billing_cycle`, `benefits[]`, `benefitFlags` (freeDelivery, discountPercent, reducedCommissionPercent, waiveCommission, prioritySupport, …)
- Routes: `my-backend/src/routes/subscriptionRoutes.js` → **`/api/subscriptions`**
- Apps: Subscriptions screens (customer, driver, restaurant)
- Admin: subscription / user-subscription entities
- Seeds:
  - `migrations/37-subscriptions-seed-plans.js`
  - `migrations/42-driver-subscription-tiers.js`
  - `migrations/43-customer-subscription-tiers.js`

## Sponsored listings

- Model: `SponsoredListing`
- Service: `my-backend/src/services/sponsoredListingService.js`
- Routes: `my-backend/src/routes/sponsoredListingRoutes.js` → **`/api/sponsored`**
  - `GET /active`, `GET|POST /mine`, `POST /mine/:id/activate`, `POST /:id/track`, `GET /:id`
- Restaurant UI: `restaurant-app/screens/SponsoredListingsScreen.js` (+ demo handlers if demo mode)
- Seed: `migrations/39-saas-sponsored-seed.js`

## Wallet ledger

- Service: `my-backend/src/services/walletLedgerService.js`
- App settings flags (cashback %, instant refund) from market-adaptability migration
- Customer app: wallet / add-money screens

## Payment gateways

- Service: `my-backend/src/services/paymentGatewayService.js`
- Routes: `my-backend/src/routes/paymentGatewayRoutes.js` → **`/api/gateways`**
  - `GET /providers`, `POST /initialize`
- Also: Stripe Connect / Stripe customer services and routes for marketplace card payouts
- Demo fill: `migrations/40-monetization-demo-fill.js`

## Related UI

- `restaurant-app/screens/SubscriptionsScreen.js`
- `restaurant-app/screens/SponsoredListingsScreen.js`
- Admin entities for subscriptions, sponsored listings, gateways, earnings
