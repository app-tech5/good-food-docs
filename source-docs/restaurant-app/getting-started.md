# Getting started — Restaurant app

Goal: run the partner app, sign in as a restaurant, accept a live (or demo) order, then open the screens that sell the full partner toolkit — Kitchen Display, Sponsored listings, and Subscriptions.

## Before you start

1. API is up and migrated ([backend guide](../my-backend/getting-started.md)).
2. Development build tooling ready (Expo Go is not supported).
3. Know whether you want **demo** or **live** mode for this session.

## 1. Install

```bash
cd restaurant-app
npm install
```

## 2. Configure `.env`

```bash
cp .env.example .env
```

Set the shared API base:

```env
EXPO_PUBLIC_API_URL=http://localhost:5000/api
EXPO_PUBLIC_DEMO_EMAIL=demo@restaurant.com
EXPO_PUBLIC_DEMO_PASSWORD=password123
```

Use LAN IP / `10.0.2.2` rules from the customer guide when not on simulator localhost.

**Important:** do **not** set `EXPO_PUBLIC_DEMO_MODE` manually in `.env`. The start scripts write the correct mode (they update a local env overlay). Restarting with the wrong script is how people accidentally stay in demo forever.

## 3. Start: demo vs live

| Command | Mode | Use when |
|---------|------|----------|
| `npm run start:demo` | Demo ON | Walkthroughs, seeded UI, offline-friendly demos |
| `npm run start:live` | Demo OFF | Real API accept / KDS / monetization flows |
| `npm run start:demo:localhost` | Demo + Metro `--localhost` | Same machine / tighter networking |
| `npm run start:live:localhost` | Live + `--localhost` | Real API with localhost Metro binding |
| `npm start` | Plain Expo start | Only if you already understand current env mode |

First native install:

```bash
npm run android
# or
npm run ios
```

Then prefer `start:demo` or `start:live` for day-to-day work.

## 4. First restaurant login

1. Sign in with the restaurant demo user (`demo@restaurant.com` / `password123`) or your own restaurant account.
2. Confirm the home / orders surface loads from the API (in live mode).
3. Keep the app in the foreground when waiting for a customer order.

## 5. Accept an order

1. Place an order from the **customer** app to this restaurant.
2. In the restaurant app, open the incoming order and **accept** it.
3. Advance status as your kitchen workflow requires so the driver can pick up.

That accept step is the hinge for KDS tickets, driver assignment, and admin earnings.

## 6. Screens to open after your first accept

Once accepting works, explore the partner features (they are part of what you bought — not separate products):

1. **Kitchen Display** — paperless prep board for accepted tickets. Full walkthrough: [Kitchen Display](./kitchen-display.md). Migrations can seed demo kitchen tickets so the board is not empty on day one.
2. **Sponsored listings** — create / activate campaigns for home and search placement. Flow: [Monetization](../admin-app/monetization.md).
3. **Subscriptions** — restaurant SaaS tiers (commission relief, tools, visibility). Configure plans in admin, then open the screen here.

Also verify language switching and currency formatting after you change market settings in admin ([Market adaptability](../admin-app/market.md)).

## Troubleshooting

| Symptom | Likely fix |
|---------|------------|
| Login / empty orders | API URL + `migrate:up` + live mode |
| Still seeing demo-only behaviour | Restart with `npm run start:live` |
| Orders never arrive | Customer pointed at same API; restaurant user tied to the correct restaurant document |
| KDS empty | Accept an order, or rely on KDS demo seed from migrations |


## Stack & where things live (for launch)

The restaurant app is **React Native + Expo**. Use **live** mode against your API for real orders (`npm run start:live` / equivalent in the package scripts).

| You want to… | Look here |
|--------------|-----------|
| Point at your API | Root `config.js` / `.env` → API base URL |
| Demo vs live behaviour | Package scripts and demo flags (turn demo off before production) |
| Accept / reject orders | Orders screens under `screens/` |
| Menu edits | Menu screens + item form |
| Kitchen Display | KDS screen in navigation / drawer |
| Sponsored + subscriptions | Partner monetization screens in the drawer |

Staff accounts must be tied to the correct **restaurant** document on the API. See also [Kitchen Display](./kitchen-display.md) and [Monetization](../admin-app/monetization.md).

## Branding & personalization

Use `.env` for `EXPO_PUBLIC_API_URL` and demo credentials; root `config.js` may mirror `APP_NAME`, subtitle, and timeouts.

### Change the public app name

1. `app.json` → Expo `name` / `slug` / identifiers.
2. `config.js` → `APP_NAME` and subtitle used on splash / login.
3. Optional: `DEFAULT_APP_NAME` fallback if your pack exposes one.
4. Restart Metro after changes.

### Logo

Replace under `assets/images`, keep the **same filename**, restart.

### Push / Firebase (Android)

The repo may ship a placeholder `android/app/google-services.json`. Replace it with your Firebase Android config for your package id before expecting push notifications.

### Auth note

Restaurant login uses `POST /auth/restaurant-login`. The account must be linked to the correct restaurant document on the API.

## Next

- [00-launch-suite.md](../00-launch-suite.md) for the full order → deliver path
- [Kitchen Display](./kitchen-display.md) · [Monetization](../admin-app/monetization.md)
