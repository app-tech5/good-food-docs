# AI recommendations — Customer app

"Recommended for you" / cross-sell rails on the menu and other surfaces, served live from **`GET /api/intelligence/recommendations`**. This is real personalization, not a static merchandising list — there is no Admin on/off switch, it always runs, but the *inputs* are real data you control.

The engine ships with a **built-in provider** (`AI_PROVIDER=builtin`) and can optionally switch recommendations to **OpenAI** or **Gemini** (`AI_PROVIDER=openai|gemini`) via environment variables. If external keys are missing or an API call fails, the backend automatically falls back to built-in scoring so the customer rail never disappears.

## What drives this

- **Order pairing** — the engine looks at the restaurant's last ~120 delivered/active orders and scores products that are frequently bought together with what's already in the customer's cart.
- **Customer history** — if the customer is logged in, their last 40 delivered orders bias results toward items they've ordered before.
- **Time of day** — breakfast / lunch / snack / dinner / late windows boost items tagged accordingly (`tags` field on `Product`, e.g. `breakfast`, `dinner`, `comfort`).
- **Weather** — live conditions from Open-Meteo (no key required) at the customer's coordinates boost `rain` / `hot` / `cold` tagged items; if Open-Meteo is unreachable the engine falls back to a neutral "fair" heuristic so the rail never breaks.
- **Provider strategy** — built-in scoring is always available; OpenAI/Gemini mode can reorder candidates and return short AI reasons. External AI is optional and usage-billed by the provider.
- **Catalog signals** — product `rating.average`, review count, and an active `discount` all add score. Restaurants that keep ratings and discounts current show up more.
- **Availability** — only `Product.availability: true` items for the current restaurant (or a mixed set if no restaurant is specified) are eligible.

Nothing here is a demo stub: turning off network access to the weather host doesn't break the feature, it just falls back to heuristics — that's the fallback behaviour to demo if you want to show resilience.

## Try it

1. Give a customer some order history (place 2+ related orders if the account is new), or add 2 items from the same restaurant to the cart.
2. Open the restaurant menu / any surface that renders recommendations.
3. Confirm each card shows a **reason** ("often ordered together", weather- or time-based) and add one to the cart.
4. Optionally block the weather host — recommendations should still appear via the heuristic fallback.

## Related

- [Smart ETA](./smart-eta.md) · [Surge pricing](./delivery-fee.md)
- [Intelligence hub](./intelligence.md) · [Backend AI brain](../my-backend/intelligence-engine.md)
