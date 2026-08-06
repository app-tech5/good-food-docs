# Market adaptability (developer)

Languages, currencies, hybrid channels, wallet defaults, and regional payment gateway slots.

## Overview

Seed / defaults: `my-backend/migrations/44-market-adaptability.js`

- Upserts languages `es` (Spanish) and `ar` (Arabic, `rtl: true`); sets `rtl: false` on `en` / `fr`
- App settings: wallet cashback / instant refund flags and related defaults
- Prepares channel / gateway hooks for regional markets

## Languages

| Surface | Locale files |
|---------|----------------|
| Customer | `lang/en.json`, `fr.json`, `es.json`, `ar.json` + `lang/i18n.js` |
| Driver | `lang/*.json` + root `i18n.js` |
| Restaurant | `lang/*.json` + root `i18n.js` |
| Admin | `src/locales/{en,fr,es,ar}.json` |
| Backend | `src/locales/` + `src/config/i18n.js` |

MongoDB: `languages` collection (`code`, `name`, `isDefault`, `rtl`).

Online setup guide: public docs → Environment setup → Languages.

## Currencies

- Runtime currency via app settings (see public Environment setup → Change app currency)
- Admin currency entities for multi-market dashboards
- Routes: `my-backend/src/routes/currencyRoutes.js` (as used by the suite)

## Hybrid channels

- Service: `my-backend/src/services/channelService.js`
- Routes: `my-backend/src/routes/channelRoutes.js`
  - Mounted at **`/api/channels`** (public + protected routers in `server.js`)
- Admin: channel-related fields / entities for configuration
- Orders still land in the shared MongoDB order pipeline

## Regional payments & wallet

- Gateway API: **`/api/gateways`** (`paymentGatewayService`) — Stripe + regional PSPs (e.g. Paystack, Flutterwave, Razorpay)
- Stripe Connect for marketplace payouts where applicable
- Wallet cashback / instant-refund toggles from migration 44 + `walletLedgerService`
