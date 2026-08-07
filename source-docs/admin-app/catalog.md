# Menus & catalog — Admin app

Categories and products that make up what customers browse and order. Use this to seed a new city/restaurant's catalog or to fix a listing centrally instead of asking the restaurant to do it from their own app.

## What you configure

### Categories

| Field | Meaning | Effect when set |
|---|---|---|
| **Name** | Category label (e.g. "Pizza", "Desserts") | Shown as a browse/filter tag on the customer app |
| **Image** | Category tile artwork | Shown wherever the category is browsed as a tile |

### Products (menu items)

| Field | Meaning | Effect when set |
|---|---|---|
| **Name / Description / Image** | What the customer sees on the item card | Directly customer-facing — keep accurate, this is what they're buying |
| **Price** | Base price for the item | What gets charged per unit before extras/variants |
| **Category** | Which category this item is filed under | Controls where it shows up in category browse |
| **Restaurant** | Which restaurant owns this item | Items are always scoped to one restaurant — you can't share one product across restaurants |
| **Availability** | In-stock / orderable toggle | Off = item is visible but can't be added to cart (use for temporary 86'd items instead of deleting) |
| **Preparation Time** (`preparation_time`) | Minutes the kitchen expects it to take | Feeds ETA estimates shown to the customer |
| **Tags / Ingredients** | Free-form labels and ingredient list | Used for search/filtering and allergen visibility |
| **Discount** (`isActive`, `percentage`) | Item-level discount override | When **isActive** is on, the item shows a struck-through price and the percentage off — separate from marketplace-wide [promotions](./promotions.md) |
| **Variants** | Linked size/option variant group | Lets the customer pick a size/option that changes price on the item |

## How to set it up

1. Open **Categories** (as labelled in your sidebar) and create/edit the tags you need first — products need a category to file under.
2. Open **Products** and create or edit items: set name, description, image, price, category, and the restaurant it belongs to.
3. Toggle **Availability** off instead of deleting an item you expect to bring back.
4. Keep prices here aligned with anything the restaurant edits from their own app — whichever was saved last wins.
5. Refresh the customer app / browse screen to confirm the change picked up.

## Verify

| Check | Expect |
|---|---|
| Create a category with an image | Appears as a browse tile |
| Create a product under it | Shows on the restaurant's menu and in that category's filter |
| Turn Availability off | Item stays visible but can't be added to cart |
| Set an item-level discount active | Struck-through price shows on the item card |

## Related

- [Partners](./partners.md) · [Restaurant menu](../restaurant-app/menu.md) · [Backend catalog](../my-backend/catalog-api.md)
