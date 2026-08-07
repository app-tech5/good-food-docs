# Getting started — Admin web app

Goal: run the React operator console against your API, sign in as an administrator, and find the screens where you configure subscriptions, currencies, languages, payment gateways, and general app settings.

## Before you start

The dashboard talks to the backend immediately after login. Start **`my-backend`** first ([backend guide](./getting-started-backend.md)) and confirm migrations ran.

## 1. Install

```bash
cd admin-app
npm install
```

There is no database inside this repo — Mongo lives behind the API.

## 2. Point the UI at the API

Create a `.env` (or `.env.local`) in the admin project root if you are not using the built-in localhost defaults.

| Variable | Purpose | Local default behaviour |
|----------|---------|-------------------------|
| `REACT_APP_API_URL` | REST base ending in `/api` | Falls back to `http://localhost:5000/api` in development |
| `REACT_APP_SERVER_URL` | API origin for sockets / server root (trailing slash) | Falls back to `http://localhost:5000/` in development |

Example for a LAN or custom port:

```env
REACT_APP_API_URL=http://192.168.1.20:5000/api
REACT_APP_SERVER_URL=http://192.168.1.20:5000/
```

Restart `npm start` after changing these. Also add the admin origin (usually `http://localhost:3000`) to the backend’s `CORS_ORIGINS`.

## 3. Start the dashboard

```bash
npm start
```

Create React App serves the UI (typically **http://localhost:3000**). For production you would `npm run build` and host the static output behind HTTPS.

## 4. Login

Use an account the API recognises as privileged (admin / manager). After a normal `migrate:up`, demo presets often match:

- Email: `admin@example.com`
- Password: `admin123`

Replace these before any shared or production deploy. If you can sign in but lists look empty, you may be on a limited role — try a true admin user rather than assuming the install is broken.

## 5. Where to configure the marketplace

After login, use the sidebar entities (names may be translated, but the concepts are stable):

| Area | What you configure |
|------|--------------------|
| **App Settings** | Platform defaults: commission rate, main currency selection, wallet-related flags, and other operator toggles |
| **Currencies** | Add codes/symbols/rates; then set the main currency in App Settings |
| **Languages** | Enable EN / FR / ES / AR (and defaults / RTL metadata as stored in the API) |
| **Subscriptions** | SaaS plans for customer, driver, and restaurant audiences |
| **Sponsored listings** | Review / manage paid placement campaigns |
| **Gateways** | Payment providers available to initialize for your markets |
| **Restaurants / Orders / Users** | Day-to-day operations, verification, and support |

Deeper money setup: [01-monetization.md](./01-monetization.md).  
Languages, currency, channels: [02-market-adaptability.md](./02-market-adaptability.md).

## 6. Quick verification

1. Open **App Settings** and save a harmless change (or simply confirm values load).
2. Open **Currencies** and **Languages** — seeded rows should appear after migrations.
3. Open **Subscriptions** — customer / driver / restaurant tiers from seed migrations should be listed.
4. Open an **Orders** (or earnings) view after you complete the suite smoke test.

## Branding (short)

Browser tab title and PWA labels live under `public/` (`index.html`, `manifest.json`). Logo assets follow the project’s public logo path. Full branding notes: [environment-config.md](./environment-config.md).


## Stack & where things live (for launch)

The admin app is a **React** web dashboard (Create React App–style). Deploy the built static assets to any static host; day-to-day work is desktop-first (wide tables).

| You want to… | Look here |
|--------------|-----------|
| Point at your API | `.env` → `REACT_APP_API_URL` / `REACT_APP_SERVER_URL` (exact names in `.env.example`) |
| Sign-in & roles | Login page; use an **admin**-capable account from migrations / seed |
| List / create / edit entities | Sidebar modules (orders, restaurants, users, drivers, settings, …) |
| Forms & tables | Shared list / detail / new patterns under `src/pages/` |
| Branding (tab title, icons) | `public/` (`index.html`, `manifest.json`, logos) |
| Languages in the UI | `src/locales/` |

Package version may read `0.1.0` / `1.0.0` depending on the pack — bump it when you publish your own release.

## Next

- [00-launch-suite.md](./00-launch-suite.md) — end-to-end smoke test  
- Mobile apps — customer / driver / restaurant getting-started pages
