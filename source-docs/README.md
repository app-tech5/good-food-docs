# Source documentation (CodeCanyon pack)

This folder is the **technical HOW-TO pack** that ships with the source ZIP. It is written for buyers who unzipped the suite and want to launch, configure, and use every app against a real local (or VPS) API.

## How this differs from the online HTML docs

| | Online HTML docs | This `source-docs/` pack |
|---|---|---|
| Audience | Shoppers & evaluators browsing the product page | Buyers who already have the ZIP |
| Tone | Feature stories, screenshots, marketing clarity | Step-by-step launch & configuration |
| Depth | What the platform can do | How to boot Mongo, migrate, point env vars, smoke-test an order |
| Format | Public site (pages under each app: customer / delivery / restaurant / admin / backend) | Markdown you can read offline next to the repos |

The online docs stay buyer-friendly on purpose. **These guides go one level deeper**: npm scripts, `.env` keys, admin entity names, useful API paths (for example `/api/subscriptions`), and migration commands. They still avoid dumping internal source-file inventories — you configure and *use* the product, not map every service file.

## Recommended read order

1. **[Launch the whole suite](./00-launch-suite.md)** — boot order, shared API URL, end-to-end smoke test.
2. **[Backend API](./getting-started-backend.md)** — MongoDB, `.env`, `migrate:up`, verify port `5000`.
3. **Mobile & admin getting started** (any order after the API is up):
   - [Customer app](./getting-started-customer.md)
   - [Driver app](./getting-started-driver.md)
   - [Restaurant app](./getting-started-restaurant.md)
   - [Admin web app](./getting-started-admin.md)
4. **[Environment & branding](./environment-config.md)** — reachability matrix, branding, i18n, FCM, maps, production checklist.
5. **Feature guides** once the suite is running:
   - [Monetization](./01-monetization.md)
   - [Market adaptability](./02-market-adaptability.md)
   - [Kitchen Display (KDS)](./03-kitchen-display.md)
   - [Logistics & proof of delivery](./04-logistics.md)
   - [AI / ops intelligence](./05-intelligence.md)

## Index

| Guide | File | What you will do |
|-------|------|------------------|
| Launch the suite | [00-launch-suite.md](./00-launch-suite.md) | Prerequisites, boot order, smoke checklist, demo vs live |
| Backend | [getting-started-backend.md](./getting-started-backend.md) | Install API, env keys, migrations, `npm start` / `npm run dev` |
| Customer | [getting-started-customer.md](./getting-started-customer.md) | `EXPO_PUBLIC_API_URL`, Expo, first login |
| Driver | [getting-started-driver.md](./getting-started-driver.md) | Driver account, maps/location, first job |
| Restaurant | [getting-started-restaurant.md](./getting-started-restaurant.md) | `start:demo` / `start:live`, accept orders, open KDS & monetization screens |
| Admin | [getting-started-admin.md](./getting-started-admin.md) | `REACT_APP_SERVER_URL` / API URL, login, configure the marketplace |
| Environment & branding | [environment-config.md](./environment-config.md) | Env tables, CORS, FCM, maps, production checklist |
| Monetization | [01-monetization.md](./01-monetization.md) | Commissions, subscriptions, sponsored listings, wallet, gateways |
| Market adaptability | [02-market-adaptability.md](./02-market-adaptability.md) | EN/FR/ES/AR, RTL, currency, channels, regional payments |
| Kitchen Display | [03-kitchen-display.md](./03-kitchen-display.md) | Open KDS, ticket lifecycle, tablet tips |
| Logistics & POD | [04-logistics.md](./04-logistics.md) | Assignment radius, batching, live tracking, photo + signature |
| Intelligence | [05-intelligence.md](./05-intelligence.md) | Recommendations, smart ETA, surge — how to demo |

## Conventions used in these guides

- **“The suite” / “the platform” / “this project”** means the full multi-app stack (backend API + customer + driver + restaurant + admin).
- **Commands** assume you are inside the relevant project folder (`my-backend`, `customer-app`, `delivery-app`, `restaurant-app`, `admin-app`).
- **Demo credentials** come from each app’s `.env.example` after migrations seed the database. Change them before any public deploy.
- Keep the **same API base URL** (including `/api`) across every client so login and sockets stay consistent.
