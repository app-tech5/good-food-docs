# Sponsored visibility — Restaurant app

Paid search/home-banner placement campaigns, launched by the restaurant, ranked and served live to customers — this is a real ranking query against `SponsoredListing`, not a mock ad unit.

## What the restaurant sets when creating a campaign

- **`headline`** — the promo text shown on the card.
- **`placement`** — `search`, `home_banner`, or `both`; determines which customer-app surfaces can show this listing.
- **`bidAmount`** and **`dailyBudget`** — bid used for ranking (higher bids sort first alongside `priority`); budget capping isn't automatically enforced by a spend-tracker in this build, so don't promise buyers hard budget cutoffs without checking your fork.
- **`startAt` / `endAt`** — the campaign's active window.
- **Launching** moves the listing from `draft`/`pending_payment` to **`active`** — only `active` listings inside their date window are eligible to be served.

## What actually makes a listing appear to customers

`getActiveListings()` only returns listings where `status: 'active'`, the current time is between `startAt` and `endAt`, the placement matches the requested slot, and — critically — the listing's restaurant still has **`isActivated: true`**. Results are sorted by `priority` then `bidAmount` descending. A restaurant that gets deactivated in Admin stops showing sponsored placements immediately, even mid-campaign.

## Try it

1. Prefer **live** API mode for a real campaign test.
2. Open **Sponsored listings** in the restaurant app.
3. Create a new campaign — headline, daily bid, placement (search / home banner / both), and a date range that includes now.
4. **Launch** it; confirm it appears under **My campaigns** with status `active`.
5. Check the customer app's home/search for that placement, and check Admin's [sponsored inventory](../admin-app/sponsored.md) to confirm impressions/clicks tick up as customers see/tap it.

## Related

- [Partner plans](./subscriptions.md) · Backend: `sponsoredListingService.js`
