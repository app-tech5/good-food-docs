# Source documentation

Technical HOW-TO guides that ship with the source ZIP. Same **app split and feature topics** as the online HTML docs — written for buyers who already unzipped the suite and need commands, `.env`, and smoke tests.

| | Online HTML docs | This `source-docs/` pack |
|---|---|---|
| Audience | Shoppers & evaluators | Buyers with the ZIP |
| Tone | Soft product stories | Step-by-step launch & configuration |
| Layout | Pages under each app | **Same folders & topics by app** |

## Folder map (mirrors the online site)

```
source-docs/
  README.md
  00-launch-suite.md
  environment-config.md
  my-backend/
    getting-started.md
    order-lifecycle.md · live-updates.md
    payments-wallet.md · commission-engine.md · subscriptions-engine.md
    intelligence-engine.md · logistics-engine.md
    channels-api.md · market-data.md · catalog-api.md
  customer-app/
    getting-started.md
    discovery.md · restaurant-page.md · menu-cart.md · checkout.md
    order-history.md · order-tracking.md
    wallet.md · subscriptions.md
    recommendations.md · smart-eta.md · delivery-fee.md
    languages-rtl.md
    intelligence.md          ← index → reco / ETA / surge
  delivery-app/
    getting-started.md
    deliveries.md · active-delivery.md · proof-of-delivery.md
    earnings.md · transactions-payouts.md
    subscriptions.md · languages.md
    logistics.md             ← index → jobs / road / POD
  restaurant-app/
    getting-started.md
    orders.md · menu.md · hours.md · analytics.md
    kitchen-display.md
    subscriptions.md · sponsored.md · languages.md
  admin-app/
    getting-started.md
    orders.md · partners.md · catalog.md
    earnings.md · subscriptions.md · gateways.md
    gateway-stripe.md · gateway-paypal.md · gateway-flutterwave.md
    gateway-paystack.md · gateway-orangepay.md · gateway-razorpay.md
    gateway-cod.md · gateway-wallet.md · gateway-crypto.md
    promotions.md · coupons.md
    languages.md · currencies-taxes.md · app-settings.md · order-channels.md
    sponsored.md
    sales-reports.md · partner-reports.md · transactions.md
    monetization.md · market.md   ← indexes into the money / market splits
```

## Recommended read order

1. **[Launch the whole suite](./00-launch-suite.md)**
2. **[Backend getting started](./my-backend/getting-started.md)** then backend feature guides as needed
3. Per app getting started (any order after the API is up)
4. **[Environment & branding](./environment-config.md)**
5. Feature HOW-TOs under the owning app (same names as the online sidebar)

## Index by app

### Shared
| Guide | Path |
|-------|------|
| Launch the suite | [00-launch-suite.md](./00-launch-suite.md) |
| Environment & branding | [environment-config.md](./environment-config.md) |

### Backend (API)
| Guide | Path |
|-------|------|
| Getting started | [getting-started.md](./my-backend/getting-started.md) |
| Order lifecycle | [order-lifecycle.md](./my-backend/order-lifecycle.md) |
| Live status sync | [live-updates.md](./my-backend/live-updates.md) |
| Payments & wallet | [payments-wallet.md](./my-backend/payments-wallet.md) |
| Commission engine | [commission-engine.md](./my-backend/commission-engine.md) |
| Subscriptions engine | [subscriptions-engine.md](./my-backend/subscriptions-engine.md) |
| AI & pricing brain | [intelligence-engine.md](./my-backend/intelligence-engine.md) |
| Logistics engine | [logistics-engine.md](./my-backend/logistics-engine.md) |
| Hybrid channels | [channels-api.md](./my-backend/channels-api.md) |
| Languages & market data | [market-data.md](./my-backend/market-data.md) |
| Catalog & partners | [catalog-api.md](./my-backend/catalog-api.md) |

### Customer app
| Guide | Path |
|-------|------|
| Getting started | [getting-started.md](./customer-app/getting-started.md) |
| Browse & discover | [discovery.md](./customer-app/discovery.md) |
| Restaurant details | [restaurant-page.md](./customer-app/restaurant-page.md) |
| Menu & basket | [menu-cart.md](./customer-app/menu-cart.md) |
| Checkout & vouchers | [checkout.md](./customer-app/checkout.md) |
| Order history | [order-history.md](./customer-app/order-history.md) |
| Live tracking | [order-tracking.md](./customer-app/order-tracking.md) |
| Wallet & cashback | [wallet.md](./customer-app/wallet.md) |
| Membership plans | [subscriptions.md](./customer-app/subscriptions.md) |
| AI recommendations | [recommendations.md](./customer-app/recommendations.md) |
| Smart delivery ETA | [smart-eta.md](./customer-app/smart-eta.md) |
| Surge pricing | [delivery-fee.md](./customer-app/delivery-fee.md) |
| Languages & RTL | [languages-rtl.md](./customer-app/languages-rtl.md) |
| AI index (legacy) | [intelligence.md](./customer-app/intelligence.md) |

### Delivery app (driver)
| Guide | Path |
|-------|------|
| Getting started | [getting-started.md](./delivery-app/getting-started.md) |
| Job board & batching | [deliveries.md](./delivery-app/deliveries.md) |
| On the road | [active-delivery.md](./delivery-app/active-delivery.md) |
| Photo & signature POD | [proof-of-delivery.md](./delivery-app/proof-of-delivery.md) |
| Shift earnings | [earnings.md](./delivery-app/earnings.md) |
| Payouts & history | [transactions-payouts.md](./delivery-app/transactions-payouts.md) |
| Priority plans | [subscriptions.md](./delivery-app/subscriptions.md) |
| Languages & RTL | [languages.md](./delivery-app/languages.md) |
| Logistics index (legacy) | [logistics.md](./delivery-app/logistics.md) |

### Restaurant app
| Guide | Path |
|-------|------|
| Getting started | [getting-started.md](./restaurant-app/getting-started.md) |
| Incoming orders | [orders.md](./restaurant-app/orders.md) |
| Menu management | [menu.md](./restaurant-app/menu.md) |
| Hours & delivery zone | [hours.md](./restaurant-app/hours.md) |
| Performance | [analytics.md](./restaurant-app/analytics.md) |
| Kitchen Display | [kitchen-display.md](./restaurant-app/kitchen-display.md) |
| Partner plans | [subscriptions.md](./restaurant-app/subscriptions.md) |
| Sponsored visibility | [sponsored.md](./restaurant-app/sponsored.md) |
| Languages & RTL | [languages.md](./restaurant-app/languages.md) |

### Admin app
| Guide | Path |
|-------|------|
| Getting started | [getting-started.md](./admin-app/getting-started.md) |
| Orders & support | [orders.md](./admin-app/orders.md) |
| Partners & users | [partners.md](./admin-app/partners.md) |
| Menus & catalog | [catalog.md](./admin-app/catalog.md) |
| Commissions & earnings | [earnings.md](./admin-app/earnings.md) |
| Subscription plans | [subscriptions.md](./admin-app/subscriptions.md) |
| Payment gateways (index) | [gateways.md](./admin-app/gateways.md) |
| → Stripe | [gateway-stripe.md](./admin-app/gateway-stripe.md) |
| → PayPal | [gateway-paypal.md](./admin-app/gateway-paypal.md) |
| → Flutterwave | [gateway-flutterwave.md](./admin-app/gateway-flutterwave.md) |
| → Paystack | [gateway-paystack.md](./admin-app/gateway-paystack.md) |
| → OrangePay | [gateway-orangepay.md](./admin-app/gateway-orangepay.md) |
| → Razorpay | [gateway-razorpay.md](./admin-app/gateway-razorpay.md) |
| → Cash on Delivery | [gateway-cod.md](./admin-app/gateway-cod.md) |
| → Internal Wallet | [gateway-wallet.md](./admin-app/gateway-wallet.md) |
| → Crypto (Commerce) | [gateway-crypto.md](./admin-app/gateway-crypto.md) |
| Promo campaigns | [promotions.md](./admin-app/promotions.md) |
| Coupon codes | [coupons.md](./admin-app/coupons.md) |
| Languages & RTL | [languages.md](./admin-app/languages.md) |
| Currencies & taxes | [currencies-taxes.md](./admin-app/currencies-taxes.md) |
| Marketplace settings | [app-settings.md](./admin-app/app-settings.md) |
| Order channels | [order-channels.md](./admin-app/order-channels.md) |
| Sponsored inventory | [sponsored.md](./admin-app/sponsored.md) |
| Sales analytics | [sales-reports.md](./admin-app/sales-reports.md) |
| Partner scorecards | [partner-reports.md](./admin-app/partner-reports.md) |
| Money ledger | [transactions.md](./admin-app/transactions.md) |
| Monetization index | [monetization.md](./admin-app/monetization.md) |
| Market index | [market.md](./admin-app/market.md) |

## Conventions

- **“The suite”** = backend API + customer + driver + restaurant + admin.
- Commands assume you are inside the matching project folder (`my-backend`, `customer-app`, `delivery-app`, `restaurant-app`, `admin-app`).
- Demo credentials come from each app’s `.env.example` after migrations. Change them before any public deploy.
- Keep the **same API base URL** (including `/api`) across every client.
- Legacy index files (`intelligence.md`, `logistics.md`, `monetization.md`, `market.md`) stay as entry points that link to the split guides.
