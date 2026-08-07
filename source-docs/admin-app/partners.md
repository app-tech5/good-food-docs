# Partners & users — Admin app

Three lists that cover everyone on the marketplace who isn't a customer placing an order: restaurants, drivers, and the underlying user accounts (which also include customers and admins). This is where you activate a partner, adjust their per-account settings, and suspend accounts that misbehave.

## What you configure

### Restaurants

| Field | Meaning | Effect when set |
|---|---|---|
| **Is Activated** (`isActivated`) | Whether the restaurant is live on the marketplace | Off = hidden from customer browse/search entirely, even if `is_closed` is false; flip on once onboarding (menu, hours, tax) is complete — the restaurant gets an activation notification |
| **Is Closed** (`is_closed`) | Manual "closed right now" flag | On = restaurant shows as temporarily closed to customers (separate from being activated) |
| **Is Available For Delivery** (`isAvailableForDelivery`) | Whether this restaurant offers delivery | Off = customers can only see it for pickup, if service mode allows |
| **Commission Rate** (`commission_rate`) | Per-restaurant override of the platform's [App Settings commission](./app-settings.md) | Set this when a restaurant negotiated a different cut than the marketplace baseline; leave unset to inherit the default |
| **Tax** | Which [tax rate](./currencies-taxes.md) applies to this restaurant's orders | Determines the tax line on every order from this restaurant |
| **Opening Time / Closing Time** | Daily service window | Orders outside this window shouldn't be accepted by checkout |
| **Categories** | Cuisine/category tags for browse and filtering | Drives which category filters surface this restaurant to customers |
| **Address / Latitude / Longitude** | Location used for distance and delivery-radius checks | Must be accurate for `maxDeliveryDistance` (App Settings) to work correctly |

### Drivers

| Field | Meaning | Effect when set |
|---|---|---|
| **Is Approved** (`isApproved`) | Background/document check gate | Off = driver **cannot** go online (`available`/`busy`/`on_delivery`) — the app blocks the status change until approved. Approve only after verifying license/documents |
| **Status** | `offline / available / busy / on_delivery` | Mostly driver-app controlled; use as a read signal for "why isn't this driver getting orders" |
| **Vehicle** (type, model, license plate) | What the driver is using | Shown to customers/restaurants for pickup identification |
| **Documents** | Uploaded license/ID files | Review before approving |
| **Rating / Total Deliveries** | Track record | Use alongside [partner reports](./partner-reports.md) before suspending |

### Users

| Field | Meaning | Effect when set |
|---|---|---|
| **Role** | `customer / restaurant / delivery / admin` | Determines which app/permissions the account can use — don't change casually, it changes what the account is allowed to do |
| **Is Active** (`isActive`) | Account enabled/disabled | Off = account is force-logged-out and blocked from signing back in (used for abuse suspension) |
| **Restaurant** | Link from a `restaurant`-role user to their Restaurant record | Needed for restaurant-role staff to see their own orders/menu |

## How to set it up

1. **Restaurants** — open a restaurant, fill in hours/address/categories/tax, then flip **Is Activated** on once it's ready to receive real orders.
2. **Drivers** — review uploaded documents, then set **Is Approved** on; only then can the driver go online in the delivery app.
3. **Users** — use for support edits or to set **Is Active** off when suspending an abusive account; pair with [orders](./orders.md) to see what triggered the suspension.
4. Need a different commission for one restaurant? Set **Commission Rate** on that restaurant record instead of changing the global one in [App Settings](./app-settings.md).

## Verify

| Check | Expect |
|---|---|
| Newly onboarded restaurant, `isActivated` off | Not visible in customer browse |
| Flip `isActivated` on | Appears in customer browse within a refresh; restaurant gets an activation notification |
| Unapproved driver tries to go online | Blocked with a "driver not approved" error |
| Approve driver, retry going online | Status change succeeds |
| Set a user `isActive` to false | User is signed out and can't log back in |

## Related

- [Catalog](./catalog.md) · [Orders](./orders.md) · [Partner reports](./partner-reports.md) · [Currencies & taxes](./currencies-taxes.md)
