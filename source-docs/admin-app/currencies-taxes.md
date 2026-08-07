# Currencies & taxes — Admin app

Two small catalogues that feed money display everywhere (menus, cart, wallet, earnings) and the tax line applied to orders.

## What you configure

### Currencies

| Field | Meaning | Effect when set |
|---|---|---|
| **Code** | Currency code (e.g. `USD`, `EUR`, `XOF`) | Referenced by name, not by row order — must be unique |
| **Symbol** | Display symbol (e.g. `$`, `€`) | What actually renders next to amounts across every client |
| **Name** | Human-readable currency name | Shown in currency pickers/admin lists |
| **Exchange Rate** (`exchangeRate`) | Rate relative to your base currency | Used anywhere the app needs to convert between currencies — keep it current if you operate multi-currency |

The **main currency** for the marketplace isn't set here — it's chosen in [App Settings](./app-settings.md) (or the relevant setting field your build exposes); this screen just maintains the list of currencies that can be picked from.

### Taxes

| Field | Meaning | Effect when set |
|---|---|---|
| **Location** | Region/jurisdiction the rate applies to | Lets you keep multiple rates for different regions |
| **Name** | Tax label (e.g. "VAT", "GST", "Sales Tax") | Shown on the order's tax line |
| **Rate** | Tax rate applied to the order subtotal | Multiplied against the subtotal to compute the tax amount added to the order total |

Each restaurant is assigned one tax rate (see [Partners](./partners.md) → restaurant **Tax** field) — new restaurants default to the earliest-created tax row until you assign one explicitly.

## How to set it up

1. **Currencies** — open **Currencies** → create code, symbol, name, exchange rate (see the Admin UI walkthrough online).
2. Set the marketplace **main currency** in [App Settings](./app-settings.md) / general settings so every client displays that symbol.
3. **Taxes** — create rate rows per location/jurisdiction you operate in.
4. Assign the right tax row to each restaurant in [Partners](./partners.md).
5. Force clients to reload settings (restart the app or wait for their next settings fetch).
6. Verify symbols on menu, cart, wallet, and earnings, and confirm checkout tax lines match finance.

## Verify

| Check | Expect |
|---|---|
| Add a currency | Appears in currency pickers across clients after reload |
| Change main currency in App Settings | Prices reformat with the new symbol/rate everywhere |
| Add a tax row and assign it to a restaurant | That restaurant's orders show the new tax name/rate on the tax line |
| Place a test order | Tax amount = subtotal × assigned rate |

## Related

- [Market index](./market.md) · [App Settings](./app-settings.md) · [Partners](./partners.md)
