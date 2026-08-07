# Subscription plans — Admin app

SaaS-style plans that customers, restaurants, or drivers can subscribe to for perks (free delivery, reduced commission, priority support, etc.). Plans are role-specific — a plan targets exactly one of the three audiences.

## What you configure

| Field | Meaning | Effect when set |
|---|---|---|
| **Name** | Plan name shown to the subscriber | Must be unique across all plans |
| **Target** | `customer`, `restaurant`, or `driver` | Determines which mobile app's subscribe screen lists this plan — a plan never shows to the wrong audience |
| **Price / Currency / Billing Cycle** | What they pay and how often (`daily`, `weekly`, `monthly`, `yearly`) | Drives the billing amount and renewal cadence |
| **Benefits** | Free-form display tags (e.g. "Free delivery", "10% off commission") | Purely cosmetic list shown on the plan card — keep it in sync with the actual **Benefit Flags** below, or subscribers will see perks that don't actually apply |
| **Is Active** | Whether the plan is purchasable | Off = existing subscribers keep it, but it disappears from the "subscribe" list for new sign-ups |
| **Service Modes** | Which service modes (`delivery`, `pickup`, `dinein`) the plan's perks apply to | Scopes benefits like free delivery to the modes you list |
| **Max Usage / Start Date / End Date** | Optional caps and validity window | Use for limited-run promotional plans |

### Benefit flags (the part that actually changes behavior)

| Flag | Meaning | Effect when on |
|---|---|---|
| **Reduced Commission Percent** (`reducedCommissionPercent`, 0–100) | Lowers marketplace commission for a **restaurant** subscriber | Applied on completed orders for that restaurant |
| **Waive Commission** (`waiveCommission`) | Flat plan fee instead of % per order (restaurant SaaS) | Platform commission becomes 0% while the plan is active |
| **Platform Access** (`platformAccess`) | Marks the plan as platform-access SaaS (with waive) | Set together with `waiveCommission` for a true flat-fee access plan |
| **Free Delivery** (`freeDelivery`) | Waives delivery fee for the subscriber | Checkout forces delivery fee to **0** for active customer members |
| **Discount Percent** (`discountPercent`, 0–100) | Percent off cart subtotal (customer plans) | Applied at checkout (before tax) for active customer members |
| **Priority Support** (`prioritySupport`) | Priority handling for the member | Drivers: first look at new jobs + wider batch radius. Others: priority support badge |

## How to set it up

1. Open **Subscriptions**.
2. Decide the **Target** first (customer / restaurant / driver) — this can't be split across audiences on one plan.
3. Set **Price**, **Currency**, **Billing Cycle**.
4. Turn on the **Benefit Flags** that should actually apply (Free Delivery, Discount %, Reduced/Waived Commission, Platform Access, Priority Support).
5. Add matching **Benefits** display tags so the plan card doesn't undersell or oversell what the flags do.
6. Set **Is Active** on when ready to sell; leave off while still drafting.
7. Verify the plan on the matching mobile role's subscribe screen.

## Verify

| Check | Expect |
|---|---|
| Create a plan, `is_active` on | Appears on the matching role's subscribe screen (customer/driver/restaurant app) |
| Subscribe a test restaurant with `waiveCommission` on | That restaurant's new completed orders show **0%** platform commission on Earnings |
| Subscribe a test restaurant with `reducedCommissionPercent` | Platform cut softens by that % vs App Settings baseline |
| Customer plan with `freeDelivery` | Next checkout shows **$0** delivery fee |
| Customer plan with `discountPercent` | Checkout subtotal is reduced by that % before tax |
| Set `is_active` off | Plan disappears from new sign-ups; existing subscribers unaffected |

## Related

- [Monetization index](./monetization.md) · [App Settings](./app-settings.md) (baseline commission) · [Backend subscriptions](../my-backend/subscriptions-engine.md)
