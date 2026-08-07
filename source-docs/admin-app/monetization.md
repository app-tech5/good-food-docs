# Monetization — how to turn it on and use it

This guide is for buyers who already ran `npm run migrate:up` on the backend and want to **operate** commissions, subscription tiers, sponsored listings, wallet behaviour, and payment gateways — not read an inventory of source files.

Money features are configured mainly in the **admin** app and consumed in the **customer**, **driver**, and **restaurant** apps. Useful API surfaces include `/api/subscriptions`, `/api/sponsored`, and `/api/gateways`.

## After migrations — what you already have

A fresh `migrate:up` typically seeds:

- Default **commission** behaviour via app settings (commonly around a 15% baseline unless you change it)
- **Subscription** plan tiers for customers, drivers, and restaurants
- Sample **sponsored listing** campaigns
- **Monetization demo** fill so admin lists and partner screens are not empty
- Wallet-related defaults that pair with market-adaptability seeds

Your job is to review those defaults, adjust them for your market, then walk each app’s UI.

## 1. Commissions (platform cut per order)

### Configure

1. Open the **admin** app → **App Settings**.
2. Set the platform **commission rate** (percent the marketplace keeps before subscription benefits apply).
3. Optionally adjust per-restaurant overrides if your workflow exposes restaurant-level commission fields.
4. Save, then place a test order and inspect **earnings** / order money views in admin.

### How benefits interact

Restaurant **subscription** benefits can soften the cut — for example reduced commission percent or waived commission — when an active restaurant plan says so. That is intentional: tiers become an incentive, not only an invoice.

### Verify

1. Customer places an order.
2. Restaurant accepts; order completes.
3. Admin earnings show a clear **platform vs restaurant** split that matches your rate (and any active plan benefits).

## 2. Subscription tiers (SaaS)

Plans are managed as **Subscriptions** (and related user-subscription records) in admin. Targets cover three audiences: **customer**, **driver**, **restaurant**.

Typical benefit ideas you will see in seeded plans:

- Customers — free delivery, member discounts
- Drivers — access / support style perks
- Restaurants — commission relief, visibility, partner tools

### Operator steps

1. In admin, open **Subscriptions**.
2. Review seeded plans: price, currency, billing cycle, benefits / flags.
3. Edit or create plans that match your pricing story.
4. Ensure currencies align with your main market currency ([market adaptability](./market.md)).

### App steps (buyers / partners)

1. **Customer app** — open the subscriptions / membership screen, pick a plan, complete the purchase path your gateways allow.
2. **Driver app** — open driver subscriptions and subscribe with a driver account.
3. **Restaurant app** — open **Subscriptions**, choose a restaurant tier, confirm benefits show after activation.

API consumers talk to **`/api/subscriptions`**. If lists are empty, re-check `migrate:status` and admin CRUD permissions.

## 3. Sponsored listings (restaurants buy attention)

Restaurants create campaigns (headline, schedule, budget) and activate them; the customer experience shows paid placement without looking bolted-on. Admin can review campaigns under **Sponsored listings**.

### Restaurant flow

1. Sign in to the **restaurant** app (`start:live` recommended for real API).
2. Open **Sponsored listings**.
3. Create a campaign (copy, schedule, budget as the form requires).
4. **Activate** the campaign.
5. Optionally confirm impressions / clicks reporting if the UI exposes tracking.

### Customer / admin check

1. Refresh the **customer** home / search surfaces — active sponsored creatives should appear among organic results when placement rules match.
2. In **admin → Sponsored listings**, confirm the campaign is visible and in the expected state.

API surface: **`/api/sponsored`** (active feed, restaurant “mine” CRUD/activate, and track endpoints).

## 4. Wallet

The customer wallet turns checkout into a balance relationship: top-ups, spending, and smoother refunds when you enable the related flags.

### Operator steps

1. In **App Settings**, review wallet-related toggles (cashback-style rewards, instant refund behaviour — seeded with market-adaptability defaults).
2. Ensure a payment path exists for top-ups (gateway / Stripe as you configure below).

### Customer steps

1. Open wallet / add-money screens in the customer app.
2. Top up with a test method (demo or Stripe test mode).
3. Pay an order from wallet balance.
4. If cashback is enabled, confirm a cashback-style ledger entry after eligible activity.

## 5. Payment gateways & Stripe

### Admin / API

1. Open **Gateways** in admin (or call **`/api/gateways`** providers / initialize as your integration expects).
2. Enable the providers you need for the regions you serve (Stripe plus regional PSP slots such as Paystack, Flutterwave, Razorpay depending on what the build exposes).
3. Keep admin and mobile publishable/secret configuration in sync.

### Backend env (Stripe)

In the API `.env`:

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_CONNECT_COUNTRY=FR
STRIPE_CONNECT_RETURN_URL=goodfooddriver://stripe-connect/return
STRIPE_CONNECT_REFRESH_URL=goodfooddriver://stripe-connect/refresh
```

### Customer env

```env
EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Restart API and Metro after changes. Use Stripe **test** keys until you are ready for live charges. Connect return URLs matter when drivers onboard for marketplace payouts.

## Suggested day-one monetization checklist

1. `npm run migrate:up` + `migrate:status` clean.
2. Admin: set **commission rate** + main **currency**.
3. Admin: review **Subscriptions** for all three audiences.
4. Restaurant: activate one **Sponsored** campaign; confirm on customer home.
5. Customer: subscribe to a plan **or** top up **wallet** and pay once.
6. Complete an order and read the **earnings** split in admin.
7. Only then switch Stripe from test to live keys.

## Related guides

- [Market adaptability](./market.md) — currency, languages, regional wallet/payment flags  
- [Restaurant getting started](../restaurant-app/getting-started.md) — where partner screens live  
- [Environment config](./environment-config.md) — secrets and production checklist
