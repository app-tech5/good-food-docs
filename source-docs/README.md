# Source documentation

HOW-TO guides that ship with the source ZIP: commands, `.env`, configuration fields, and smoke tests for the full suite (API + customer + driver + restaurant + admin).

## Recommended read order

1. **[Launch the whole suite](./00-launch-suite.md)**
2. **[Backend getting started](./my-backend/getting-started.md)** then backend feature guides as needed
3. Per app getting started (any order after the API is up)
4. **[Environment & branding](./environment-config.md)**
5. Feature HOW-TOs under the owning app folder

## Conventions

- **“The suite”** = backend API + customer + driver + restaurant + admin.
- Commands assume you are inside the matching project folder (`my-backend`, `customer-app`, `delivery-app`, `restaurant-app`, `admin-app`).
- Demo credentials come from each app’s `.env.example` after migrations. Change them before any public deploy.
- Keep the **same API base URL** (including `/api`) across every client.
- Index files (`intelligence.md`, `logistics.md`, `monetization.md`, `market.md`) link out to the split feature guides.
