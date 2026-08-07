# Coupons — Admin app

Redeemable codes the customer has to type in at checkout — unlike [promotions](./promotions.md), which apply automatically. Use coupons for targeted, opt-in, or one-time-use discounts.

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Code** | The string customers type in (5–20 chars, stored uppercase) | Must be unique; this is what the customer enters at checkout |
| **Description** | Internal/customer-facing note about the offer | Context for support and the customer-facing coupon list |
| **Discount Type** | `percentage`, `fixed`, or `free_delivery` | Determines how the discount is calculated at redemption |
| **Discount Value** | % or fixed amount off | Required unless type is `free_delivery` |
| **Min Order Amount** | Cart subtotal floor to redeem | Redemption fails below this subtotal |
| **Applicable Restaurants / Categories** | Optional scoping | Leave empty for platform-wide; fill in to restrict the code to specific restaurants or categories |
| **Start Date / End Date** | Validity window | Code is rejected as invalid outside this window |
| **Max Uses** (`maxUses`) / **Current Uses** (`currentUses`) | Optional total redemption cap and running counter | Once `currentUses` reaches `maxUses`, the code stops working for everyone |
| **User Usage Limit** (`userUsageLimit`, default 1) | Redemptions allowed per individual customer | Stops one customer from reusing the same code repeatedly |
| **Is Public** (`isPublic`) | Whether the code can be discovered/listed, vs. targeted only | Off + **Targeted Users** set = the code only works for the specific customers you list |
| **Targeted Users** | Explicit allow-list of customers | Only meaningful when **Is Public** is off |
| **First Order Only** (`firstOrderOnly`) | Restricts redemption to a customer's first order | Good for acquisition codes — existing customers can't apply it |
| **Is Active** | Master on/off switch | Off = code is rejected at checkout even if still within its date range |

## How to set it up

1. Open **Coupons** → create a code.
2. Set **Discount Type** and **Discount Value** (skip value for `free_delivery`).
3. Add guardrails: **Min Order Amount**, **Max Uses**, **User Usage Limit**, **First Order Only** as needed.
4. Decide visibility: leave **Is Public** on for a code you'll advertise, or turn it off and add specific **Targeted Users** for a private code.
5. Set **Start Date** / **End Date**, then **Is Active** on.
6. Apply the code on a test customer's cart/checkout to confirm it discounts correctly.
7. Retire (**Is Active** off) codes that are no longer funded — don't delete if you need the usage history.

## Verify

| Check | Expect |
|---|---|
| Redeem a valid, active, in-date code | Discount applies at checkout per its type |
| Redeem below `minOrderAmount` | Rejected with a minimum-order message |
| Redeem past `maxUses` | Rejected as fully used |
| Redeem a `firstOrderOnly` code on a repeat customer | Rejected |
| Turn `isActive` off | Code stops working immediately |

## Related

- [Promotions](./promotions.md)
