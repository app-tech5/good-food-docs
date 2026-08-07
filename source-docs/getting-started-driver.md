# Getting started — Driver (delivery) app

Goal: run the courier app against your API, grant location permissions, and complete a first delivery job — including proof of delivery when prompted.

## Before you start

1. Backend is running with `migrate:up` applied ([backend guide](./getting-started-backend.md)).
2. Prefer having at least one **accepted restaurant order** waiting for a driver (customer + restaurant apps), or use seeded demo jobs if present.
3. Use a **development build** (`npm run android` / `npm run ios`) — Expo Go is not supported.

## 1. Install

```bash
cd delivery-app
npm install
```

## 2. Configure env

```bash
cp .env.example .env
```

### API URL

```env
EXPO_PUBLIC_API_URL=http://localhost:5000/api
```

Use the same host rules as the customer app:

- Physical phone → LAN IP, not `localhost`
- Android emulator → often `http://10.0.2.2:5000/api`
- Restart Metro after changes

### Demo account helpers

```env
EXPO_PUBLIC_DEMO_MODE=true
EXPO_PUBLIC_DEMO_EMAIL=driver@demo.com
EXPO_PUBLIC_DEMO_PASSWORD=driver123
```

Those credentials must exist as a **driver-role** user in Mongo (seeded by migrations in a typical install).

### Maps key (optional / production)

```env
EXPO_PUBLIC_GOOGLE_MAPS_API_KEY=
```

The driver experience is MapLibre-oriented by default; you may still need Google Maps configuration for certain production Android builds. See [environment-config.md](./environment-config.md) for Google Cloud / `app.json` notes.

## 3. Start the app

```bash
npm run android
# or
npm run ios
```

Later:

```bash
npm start
```

## 4. Maps, location, and online status

1. Sign in as the driver.
2. Allow **location** (and related) permissions when the OS prompts — assignment, navigation, and some completion geofence checks depend on them.
3. Go **online** / available so the platform can offer jobs.
4. Keep the device awake during an active delivery so location updates continue for customer live tracking.

If jobs never appear: confirm the API URL, that the user is actually a driver, that restaurant orders are in a ready-for-pickup / assignable state, and that delivery settings / radius are not impossibly small (see [logistics](./04-logistics.md)).

## 5. First job smoke test

1. From the customer app, place an order; from the restaurant app, **accept** it and advance prep if needed.
2. In the driver app, accept the offered delivery (or a **batch** of nearby compatible jobs if the UI suggests one).
3. Navigate restaurant → customer.
4. At the door, complete with **proof of delivery**: capture a **photo** and/or **customer signature** when required.
5. Confirm the order shows delivered for customer and admin.

This single path exercises logistics assignment, live tracking, and POD — the features buyers care about most in the courier app.

## Subscriptions note

Drivers may see a **Subscriptions** screen for courier tiers (access / support style benefits). Configure plans in admin first — [01-monetization.md](./01-monetization.md).


## Stack & where things live (for launch)

The driver app is **React Native + Expo**, same family as the customer and restaurant apps. Configuration sits at the **project root** (not under a nested `config/` folder in every build — check `config.js` / `.env` as shipped).

| You want to… | Look here |
|--------------|-----------|
| Point at your API | Root config / `.env` → API base URL ending in `/api` |
| Demo login shortcuts | Demo flags in the same config / `.env` |
| Maps & location | Maps key + OS location permission prompts |
| Day-to-day courier screens | `screens/` (home, deliveries, details, earnings, …) |
| POD UI (photo / signature) | Components used from the complete-delivery flow |
| Translations | `lang/` + `i18n.js` |

Login requires a **driver** account on the API (a pure customer user will be rejected). Version baseline is usually `1.0.0` in `package.json`.

## Next

- Suite boot order & checklist: [00-launch-suite.md](./00-launch-suite.md)
- Batching, radius, POD detail: [04-logistics.md](./04-logistics.md)
