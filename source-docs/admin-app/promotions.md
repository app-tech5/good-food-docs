# Promotions — Admin app

Scheduled marketing campaigns that discount an order automatically at checkout — no code required from the customer (that's what [coupons](./coupons.md) are for). Promotions can target the whole platform, a category, specific restaurants, or specific items.

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Name / Description / Image** | Campaign display info | Shown on customer-facing promo surfaces (home banners, restaurant page) |
| **Promotion Type** | `percentage_discount`, `fixed_discount`, `free_delivery`, `buy_x_get_y`, `combo_deal`, `flash_sale`, `happy_hour` | Determines which other fields are required and how the discount is calculated |
| **Discount Value** | % off or fixed amount off | Required for `percentage_discount` / `fixed_discount`; ignored for other types |
| **Buy Quantity / Get Quantity** | e.g. buy 2 get 1 | Required for `buy_x_get_y` — free items = `floor(qty / buyQuantity) * getQuantity` |
| **Combo Items** | Item + discounted price pairs | Required for `combo_deal` — needs at least 2 items |
| **Scope** | `platform`, `category`, `restaurant`, `item` | Determines which of the "applicable" fields below is required and how wide the promo reaches |
| **Applicable Restaurants / Categories / Items** | The targets that match your **Scope** | Must have at least one entry matching the scope you picked, or saving fails |
| **Start Date / End Date** | Validity window | Promotion only applies to orders placed inside this window |
| **Happy Hours** (start/end time + days) | Optional recurring time-of-day/day-of-week restriction | If set, the promotion only applies during these windows even within the date range — good for `happy_hour` type |
| **Min Order Amount** | Cart subtotal floor | Order must reach this subtotal before the discount applies |
| **Max Discount Amount** | Cap on the discount for percentage types | Prevents a % discount from getting too large on big carts |
| **User Eligibility** | `all`, `new_users`, `existing_users`, `vip` | Narrows who can trigger the promotion beyond scope/schedule |
| **Max Usage / Current Usage** | Optional total redemption cap and running counter | Once `currentUsage` hits `maxUsage`, the promotion stops applying |
| **Is Active** | Master on/off switch | Off = promotion is fully disabled regardless of dates |
| **Priority** (1–10) | Tie-break order when multiple promotions could apply | Higher priority wins when more than one promotion matches the same order |

## How to set it up

1. Open **Promotions** → create a campaign.
2. Pick **Promotion Type** first — it determines which fields become required.
3. Pick **Scope**, then fill the matching **Applicable...** field (restaurants / categories / items) — required for anything except `platform` scope.
4. Set **Start Date** / **End Date** (and **Happy Hours** if it's time-boxed within the day).
5. Add guardrails: **Min Order Amount**, **Max Discount Amount**, **User Eligibility**, **Max Usage**.
6. Set **Is Active** on and save.
7. Place a customer test order that should qualify; confirm the discount lands and shows on the relevant customer/restaurant surfaces.

## Verify

| Check | Expect |
|---|---|
| Create a `platform` scope, active, in-date promotion | Applies automatically on a qualifying checkout, no code needed |
| Order below `minOrderAmount` | Promotion does not apply |
| Two active promotions match one order | Higher **Priority** one wins |
| `currentUsage` reaches `maxUsage` | Promotion stops applying to new orders |
| Set `isActive` off | Promotion stops applying immediately, even mid-date-range |

## Related

- [Coupons](./coupons.md) · [Customer checkout](../customer-app/checkout.md)
