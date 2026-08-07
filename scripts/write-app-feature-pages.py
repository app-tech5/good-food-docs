#!/usr/bin/env python3
"""Write feature pages under each app — real documentation, not caption+screenshot cards."""
from __future__ import annotations

import html
import subprocess
from pathlib import Path

ROOT = Path("/Users/nass/Documents/good-food-docs")
A = "assets/images"
SS = Path("/Users/nass/Documents/good-foods-description/img/pro/screenshots")


def esc(s: str) -> str:
    """Escape unless the string already contains intentional HTML tags we author."""
    if "<a " in s or "<code>" in s or "<strong>" in s or "<em>" in s:
        return s
    return html.escape(s)


def render_shot(shot, img_prefix: str) -> str:
    """One screenshot under its own text — never packed in a multi-column grid."""
    kind, src, alt, cap = shot
    cls = "phone" if kind == "phone" else "wide"
    return f"""            <figure class="doc-shot {cls}">
              <img src="{img_prefix}{src}" alt="{html.escape(alt)}" />
              <figcaption>{html.escape(cap)}</figcaption>
            </figure>"""


def render_shots(shots, img_prefix: str) -> str:
    if not shots:
        return ""
    return "\n".join(render_shot(s, img_prefix) for s in shots)


def render_section(sec: dict, img_prefix: str) -> str:
    """
    sec keys:
      h2: str
      paras: list[str]  (optional lead paragraphs)
      shot / shots: optional figure(s) right after lead paras
      blocks: list[{h3, paras?, steps?, shot?, shots?}]
      after: list[str] optional closing paras
    Prefer one shot per block so each capture sits under its own text.
    """
    lines = [f'          <section class="section-block">', f"            <h2>{esc(sec['h2'])}</h2>"]
    for i, p in enumerate(sec.get("paras") or []):
        cls = "" if i == 0 else ' class="section-subtext"'
        lines.append(f"            <p{cls}>\n              {esc(p)}\n            </p>")
    if sec.get("shot"):
        lines.append(render_shot(sec["shot"], img_prefix))
    if sec.get("shots"):
        lines.append(render_shots(sec["shots"], img_prefix))
    for block in sec.get("blocks") or []:
        if block.get("h3"):
            lines.append(f"            <h3>{esc(block['h3'])}</h3>")
        for p in block.get("paras") or []:
            lines.append(f'            <p class="section-subtext">\n              {esc(p)}\n            </p>')
        steps = block.get("steps") or []
        if steps:
            lines.append('            <ol class="doc-steps">')
            for step in steps:
                lines.append(f"              <li>{esc(step)}</li>")
            lines.append("            </ol>")
        if block.get("shot"):
            lines.append(render_shot(block["shot"], img_prefix))
        if block.get("shots"):
            lines.append(render_shots(block["shots"], img_prefix))
    for p in sec.get("after") or []:
        lines.append(f'            <p class="section-subtext">\n              {esc(p)}\n            </p>')
    lines.append("          </section>")
    return "\n".join(lines)


def page(title, h1, subtitle, pills, sections, css_href, js_href, img_prefix):
    pills_html = "\n".join(f'            <span class="meta-pill">{html.escape(p)}</span>' for p in pills)
    body = "\n".join(render_section(s, img_prefix) for s in sections)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="{css_href}" />
  </head>
  <body>
    <script src="{js_href}"></script>
    <main class="layout">
      <aside class="sidebar" data-docs-sidebar></aside>
      <section class="content">
        <header id="top" class="hero">
          <h1>{html.escape(h1)}</h1>
          <p class="subtitle">
            {esc(subtitle)}
          </p>
          <div class="meta-strip">
{pills_html}
          </div>
        </header>

        <section class="overview">
{body}
        </section>
      </section>
    </main>
  </body>
</html>
"""


def ensure_admin_sponsored():
    dest = ROOT / "assets/images/features/admin-sponsored.jpg"
    src = SS / "admin/46-sponsored-listings.jpg"
    if dest.exists() and dest.stat().st_size > 2000:
        return
    if src.exists():
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", str(src), "--out", str(dest)],
            check=False,
            capture_output=True,
        )
        subprocess.run(["sips", "-Z", "1400", str(dest)], check=False, capture_output=True)


# Appended as main() body for write-app-feature-pages.py — do not run alone.
def redirect_page(title: str, dest_href: str, dest_label: str, css_href: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="refresh" content="0; url={dest_href}" />
    <link rel="canonical" href="{dest_href}" />
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="{css_href}" />
  </head>
  <body>
    <main class="layout">
      <aside class="sidebar" data-docs-sidebar></aside>
      <section class="content">
        <header class="hero">
          <h1>{html.escape(title)}</h1>
          <p class="subtitle">This topic moved. <a href="{dest_href}">{html.escape(dest_label)}</a>.</p>
        </header>
      </section>
    </main>
  </body>
</html>
"""


def main():
    ensure_admin_sponsored()
    C = "./site.css"
    CJ = "./js/sidebar-scroll.js"
    CP = "./"
    D = "../site.css"
    DJ = "../js/sidebar-scroll.js"
    DP = "../"

    def w(path: str, *args):
        ROOT.joinpath(path).write_text(page(*args), encoding="utf-8")

    def r(path: str, title: str, dest: str, label: str, css: str):
        ROOT.joinpath(path).write_text(redirect_page(title, dest, label, css), encoding="utf-8")

    # --- Customer ---
    w(
        "discovery.html",
        "Browse & discover — Customer app",
        "Browse & discover",
        "How customers find restaurants: home, search, and the nearby map — before opening a place.",
        ["Home", "Search", "Map"],
        [
            {
                "h2": "Find food in a multi-restaurant marketplace",
                "paras": [
                    "The customer app is a multi-store marketplace: one install, many restaurants. Discovery is the browse layer — home, search, and map — before the restaurant page, menu, or checkout.",
                ],
                "blocks": [
                    {
                        "h3": "Homepage — delivery / pickup, categories, banners",
                        "paras": [
                            "Home starts with the Delivery / Pickup toggle, a search field, a horizontal category row, and a promo carousel (for example “15% off” with Browse Offers). Below that, Special Offers lists restaurant cards with rating, distance / prep cues, and offer badges.",
                        ],
                        "steps": [
                            "Open the app and choose <strong>Delivery</strong> or <strong>Pickup</strong>.",
                            "Browse categories or the promo carousel, or jump into Special Offers cards.",
                            "Tap a restaurant card when you are ready to open that place.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-home.jpg", "Home", "Delivery/Pickup, categories, promo carousel, Special Offers cards"),
                    },
                    {
                        "h3": "Search",
                        "paras": [
                            "Search is for intent: type a restaurant or dish keyword and open a matching result. It is a separate tab / entry from scrolling home.",
                        ],
                        "steps": [
                            "Open <strong>Search</strong> from the tab bar or the home search field.",
                            "Type a keyword and pick a restaurant or dish result.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-search.jpg", "Search", "Keyword search results"),
                    },
                    {
                        "h3": "Nearby map",
                        "paras": [
                            "The nearby map is geographic discovery: restaurant pins and a swipeable restaurant card. Use it for “what’s close” — not for live courier tracking after checkout.",
                        ],
                        "shot": ("phone", f"{A}/features/map-nearby.jpg", "Nearby map", "Map pins with swipeable restaurant card"),
                    },
                ],
                "after": [
                    'Next: open a place on <a href="./restaurant-page.html">Restaurant details</a>, then <a href="./menu-cart.html">Menu &amp; basket</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "restaurant-page.html",
        "Restaurant details — Customer app",
        "Restaurant details",
        "What customers see on a restaurant header: open/closed, ETA, delivery fee, and that restaurant’s offers and reviews.",
        ["Open/closed", "ETA", "Fee", "Offers"],
        [
            {
                "h2": "Decide before browsing the menu",
                "paras": [
                    "The restaurant page answers “can I order, how long, how much delivery, and what’s on offer?” before the customer digs into the catalog. Each cue below is its own chip or block — not one combined banner.",
                ],
                "blocks": [
                    {
                        "h3": "Open / closed status",
                        "paras": [
                            "The status line tells customers whether they can order now — for example a green “Open until 11:00 PM” or a closed state with the next opening time. This is only the open/closed cue (plus name / rating / address), not the ETA or fee chips.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-restaurant-open.jpg", "Open / closed", "Open until … (or closed) on the restaurant page"),
                    },
                    {
                        "h3": "Smart ETA",
                        "paras": [
                            'The ETA chip (for example “ETA 26–36 min”) estimates how long food will take. It is separate from open/closed and from the fee chip. More detail: <a href="./smart-eta.html">Smart delivery ETA</a>.',
                        ],
                        "shot": ("phone", f"{A}/features/ordering-restaurant-eta.jpg", "ETA", "ETA chip on the restaurant page"),
                    },
                    {
                        "h3": "Delivery fee (standard or surge)",
                        "paras": [
                            'The fee chip shows what delivery costs now — “Standard fee” or a surge multiplier. Separate from ETA. Details: <a href="./delivery-fee.html">Surge pricing</a>.',
                        ],
                        "shot": ("phone", f"{A}/features/ordering-restaurant-fee.jpg", "Delivery fee", "Fee / surge chip on the restaurant page"),
                    },
                    {
                        "h3": "Offers and reviews on the restaurant",
                        "paras": [
                            "Scrolling reaches Available Offers (discount / free-delivery cards) and Recent Reviews. This is not the global Offers tab — it is the block attached to that restaurant.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-restaurant-offers.jpg", "Restaurant offers", "Available Offers cards and Recent Reviews"),
                    },
                ],
                "after": [
                    'Continue with <a href="./menu-cart.html">Menu &amp; basket</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "menu-cart.html",
        "Menu & basket — Customer app",
        "Menu & basket",
        "Browse the catalog, add items with quantities, then review the cart before checkout.",
        ["Menu", "Add to cart", "Cart"],
        [
            {
                "h2": "Build the basket",
                "paras": [
                    "Once a restaurant is open, conversion is catalog → add → cart. Each screen below is a distinct moment.",
                ],
                "blocks": [
                    {
                        "h3": "Menu — categories and items",
                        "paras": [
                            "The menu lists categories with dish name, short description, price, and a + control. This capture is the catalog itself — not status chips or the cart banner.",
                        ],
                        "steps": [
                            "Scroll categories until you find the dish.",
                            "Tap + on an item (or open the item if your flow uses a detail sheet).",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-menu.jpg", "Menu", "Category sections with priced items and +"),
                    },
                    {
                        "h3": "Add to cart — quantities and View Cart",
                        "paras": [
                            "After an item is added, the menu shows quantity steppers (− / +) and a floating <strong>View Cart</strong> bar (item count + total). The tab-bar cart badge increments too.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-add-to-cart.jpg", "Add to cart", "Quantity steppers and View Cart bar on the menu"),
                    },
                    {
                        "h3": "Cart — line items and totals",
                        "paras": [
                            "The cart lists quantities, extras, and a running total. Change amounts or remove lines here before checkout.",
                        ],
                        "steps": [
                            "Open the cart from the tab bar or the View Cart bar.",
                            "Review quantities, extras, and totals.",
                            "Continue to checkout when the basket looks right.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-cart.jpg", "Cart", "Line items, quantities, and totals"),
                    },
                ],
                "after": [
                    'Next: <a href="./checkout.html">Checkout &amp; vouchers</a>. AI cross-sell: <a href="./recommendations.html">AI recommendations</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "checkout.html",
        "Checkout & vouchers — Customer app",
        "Checkout & vouchers",
        "Claim vouchers on the Offers surface, then confirm address and payment to place the order.",
        ["Offers", "Checkout"],
        [
            {
                "h2": "Convert the cart",
                "paras": [
                    "After the cart looks right, customers either claim a voucher on the Offers surface or go straight to checkout.",
                ],
                "blocks": [
                    {
                        "h3": "Offers tab — vouchers to claim",
                        "paras": [
                            'The Offers surface lists claimable vouchers / campaigns (separate from the small offers block on a restaurant page). Coupon codes and campaign rules are configured in admin — see <a href="./admin-app/promotions.html">Promotions</a> and <a href="./admin-app/coupons.html">Coupons</a>.',
                        ],
                        "shot": ("phone", f"{A}/features/ordering-offers.jpg", "Offers", "Offers / vouchers list to claim"),
                    },
                    {
                        "h3": "Checkout — address, payment, place order",
                        "paras": [
                            'Checkout confirms fulfillment (delivery vs pickup), the address, and the payment method (card, cash on delivery, wallet, or other gateways you activate). After place order, follow progress in <a href="./order-history.html">order history</a> / <a href="./order-tracking.html">live tracking</a>.',
                        ],
                        "steps": [
                            "Confirm delivery or pickup, address, and payment method.",
                            "Place the order.",
                            "Open order history / tracking to follow status.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-checkout.jpg", "Checkout", "Summary, payment method, place order"),
                    },
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "order-history.html",
        "Order history — Customer app",
        "Order history",
        "Where past and live orders live so customers can reopen tracking, contact the restaurant, or leave a review.",
        ["Orders", "Status", "History"],
        [
            {
                "h2": "Every order in one list",
                "paras": [
                    "After checkout, every order lands in the order list with status and a way into detail. From here customers reopen tracking, contact the restaurant when needed, and later leave reviews when your flow enables them.",
                ],
                "blocks": [
                    {
                        "h3": "What the list shows",
                        "paras": [
                            "Each row summarizes restaurant, amount, and fulfillment status so the customer can reopen Track Order or dig into line items.",
                        ],
                        "shot": ("phone", f"{A}/features/ordering-history.jpg", "Orders", "Order history list with status"),
                    },
                ],
                "after": [
                    'Live progress: <a href="./order-tracking.html">Live tracking</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "recommendations.html",
        "AI recommendations — Customer app",
        "AI recommendations",
        "Dynamic AI picks that cross-sell sides, drinks, and extras that grow the basket without a separate upsell screen.",
        ["Recommended", "Upsell", "AOV"],
        [
            {
                "h2": "AI recommendations that grow the basket",
                "paras": [
                    "This is the conversion layer buyers expect: a <strong>Recommended for you</strong> block that cross-sells complementary items from the customer’s history, time of day, and context such as weather. Each card shows a short reason line so the suggestion feels explained rather than random.",
                    "The goal is a natural add-to-cart moment (sides, drinks, extras) that raises average order value.",
                ],
                "blocks": [
                    {
                        "h3": "What the customer sees",
                        "paras": [
                            "A horizontal row of recommended items with title, price, and a short match reason. Tapping a card follows your normal product / add-to-cart path.",
                        ],
                        "shot": ("phone", f"{A}/features/ai-reco.jpg", "Recommendations", "Recommended for you with reason lines on the restaurant screen"),
                    },
                ],
                "after": [
                    'Related header cues: <a href="./smart-eta.html">Smart delivery ETA</a>, <a href="./delivery-fee.html">Surge pricing</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "smart-eta.html",
        "Smart delivery ETA — Customer app",
        "Smart delivery ETA",
        "How arrival-time estimates appear on the restaurant page so customers commit with clear expectations.",
        ["ETA chip", "Kitchen load", "Travel"],
        [
            {
                "h2": "Arrival times customers can trust",
                "paras": [
                    "Smart ETA estimates how long food will take, using kitchen load and travel time where your backend intelligence stack is enabled. On the restaurant page the estimate appears as its own chip (for example “ETA 26–36 min”).",
                    "Clearer arrivals reduce “where is my food?” support load before checkout.",
                ],
                "blocks": [
                    {
                        "h3": "The ETA chip",
                        "paras": [
                            "Look for the pink/clock ETA chip on restaurant detail. That chip is only about time — open/closed status and the delivery-fee chip are separate cues on the same header.",
                        ],
                        "shot": ("phone", f"{A}/features/ai-eta.jpg", "ETA badge", "ETA 26–36 min chip on restaurant detail"),
                    },
                ],
                "after": [
                    'See the same cue in context on <a href="./restaurant-page.html">Restaurant details</a>. Fee / surge is separate: <a href="./delivery-fee.html">Surge pricing</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "delivery-fee.html",
        "Surge pricing — Customer app",
        "Surge pricing",
        "How the fee chip shows a standard delivery price or a surge multiplier when the city is busy.",
        ["Standard fee", "Surge", "Reliability"],
        [
            {
                "h2": "Surge pricing when the city is busy",
                "paras": [
                    "When demand is high and courier capacity is tight, the delivery-fee chip can show a surge multiplier (for example “Surge 1.45x”). Quiet periods keep a standard fee; peaks stay explicit so the customer understands the cost before paying.",
                    "Fee / surge is a marketplace lever for reliability — separate from the ETA chip, which only answers “how long?”.",
                ],
                "blocks": [
                    {
                        "h3": "The fee / surge chip",
                        "paras": [
                            "On restaurant detail, read the fee chip for what delivery costs now. Surge replaces the standard fee when your rules say demand is elevated.",
                        ],
                        "shot": ("phone", f"{A}/features/ai-surge.jpg", "Fee / surge", "Surge (or standard) fee chip on restaurant detail"),
                    },
                ],
                "after": [
                    'Header context: <a href="./restaurant-page.html">Restaurant details</a>. Timing: <a href="./smart-eta.html">Smart delivery ETA</a>.',
                ],
            },
        ],
        C, CJ, CP,
    )

    # wallet + subscriptions + tracking (kept, links updated)
    w(
        "wallet.html",
        "Wallet & cashback — Customer app",
        "Wallet & cashback",
        "How the in-app balance works for customers, how they top up, and what you configure so checkout and refunds stay coherent.",
        ["Balance", "Top up", "Payment methods"],
        [
            {
                "h2": "What the wallet is for",
                "paras": [
                    "The wallet is a prepaid balance inside the customer app. Instead of entering a card on every order, the customer can pay from money already on the account. That shortens checkout, reduces failed payments at the door of the kitchen, and gives you a place to land refunds or promotions as credit — including cashback on delivered orders and instant refund to wallet when a paid order is cancelled.",
                ],
                "blocks": [
                    {
                        "h3": "What the customer sees on Wallet",
                        "paras": [
                            "The Wallet screen shows the current balance at the top, then actions to add (and optionally send) money, then the list of saved payment methods — card brands, Google Pay, PayPal, cash, and similar options you enable.",
                        ],
                        "shot": ("phone", f"{A}/features/wallet.jpg", "Customer wallet", "Balance, actions, and saved payment methods"),
                    },
                    {
                        "h3": "How a customer tops up",
                        "paras": [
                            "Add Money opens a focused top-up flow: pick an amount (or a quick chip such as $10 / $20 / $50), choose how to pay, then confirm.",
                        ],
                        "steps": [
                            "Open the drawer or account area and choose <strong>Wallet</strong>.",
                            "Check the balance. Use the refresh control if the amount looks stale after a payment.",
                            "Tap <strong>Add Money</strong>, choose an amount, select a payment method, then confirm <strong>Add to balance</strong>.",
                            "At checkout, choose the wallet as the payment method when the balance is enough.",
                        ],
                        "shot": ("phone", f"{A}/features/wallet-topup.jpg", "Add money", "Amount chips, payment method, add to balance"),
                    },
                    {
                        "h3": "What you configure as operator",
                        "paras": [
                            'Payment gateways are managed in admin — see <a href="./admin-app/gateways.html">Payment gateways</a>. Enable only the gateways you actually use in each market before expecting top-ups to succeed in production.',
                        ],
                    },
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "subscriptions.html",
        "Membership plans — Customer app",
        "Membership plans",
        "How membership plans appear to customers, what benefits they unlock, and how those plans are created in admin.",
        ["Plans", "Benefits", "Subscribe"],
        [
            {
                "h2": "Membership in the customer app",
                "paras": [
                    "Customer subscriptions are recurring plans that unlock benefits such as free delivery, a food discount, member-only deals, or priority support. The customer app shows only plans whose target is <strong>customer</strong>.",
                    "Each plan card lists the name, price and billing cycle, the benefit bullets, and a Subscribe action.",
                ],
                "blocks": [
                    {
                        "h3": "How a customer subscribes",
                        "steps": [
                            "Sign in with a customer account.",
                            "Open the Subscriptions / membership screen from account or settings.",
                            "Compare the listed plans and tap <strong>Subscribe</strong> on the one you want.",
                            "Complete payment with an enabled gateway. Confirm the plan shows as active afterward.",
                        ],
                        "shot": ("phone", f"{A}/features/sub-customer.jpg", "Customer plans", "Plan cards with benefits and Subscribe"),
                    },
                    {
                        "h3": "Where plans are defined",
                        "paras": [
                            'Create and edit tiers in admin under Subscriptions (target = customer). Details: <a href="./admin-app/subscriptions.html">Admin subscriptions</a>.',
                        ],
                    },
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "order-tracking.html",
        "Live tracking — Customer app",
        "Live tracking",
        "How customers follow an order from acceptance to delivery, and how that ties to the map and the driver app.",
        ["Status steps", "ETA", "Map"],
        [
            {
                "h2": "Follow the order without calling support",
                "paras": [
                    "After checkout, customers should not need to call support to know where their food is. Track Order answers: was it accepted, is the kitchen cooking, is a courier on the way, and when will it arrive.",
                ],
                "blocks": [
                    {
                        "h3": "Status timeline",
                        "paras": [
                            "The screen shows the order id, timestamp, and a vertical status timeline: pending → preparing → out for delivery → delivered. Restaurant contact details sit on the same screen.",
                        ],
                        "steps": [
                            "Place an order and wait for the restaurant to accept it.",
                            "Open <strong>Order history</strong>, select the order, then <strong>Track order</strong>.",
                            "Watch the timeline advance as kitchen and driver statuses change.",
                            "When the driver is en route, ETA copy updates when your logistics / intelligence data provides it.",
                        ],
                        "shot": ("phone", f"{A}/features/tracking.jpg", "Track order", "Order id, status timeline, restaurant contact"),
                    },
                    {
                        "h3": "Delivery map while the courier is en route",
                        "paras": [
                            'When the order is out for delivery, Track Order can show a <strong>Delivery Map</strong>: destination pin, live courier position, route line, and an ETA badge. That is live tracking — not the nearby-restaurant discovery map. Driver-side job handling: <a href="./delivery-app/deliveries.html">Job board &amp; batching</a> and <a href="./delivery-app/proof-of-delivery.html">Photo &amp; signature POD</a>.',
                        ],
                        "shot": ("phone", f"{A}/features/tracking-map.jpg", "Delivery map", "Route, courier pin, destination, and ETA badge"),
                    },
                ],
            },
        ],
        C, CJ, CP,
    )

    r("ordering.html", "Ordering & discovery", "./discovery.html", "Browse & discover", C)
    r("intelligence.html", "AI intelligence", "./recommendations.html", "AI recommendations", C)

    # --- Driver ---
    w(
        "delivery-app/deliveries.html",
        "Job board & batching — Driver app",
        "Job board & batching",
        "The shift board: today’s jobs, batching nearby drops, and how assignment radius shapes which work appears.",
        ["List", "Online", "Radius"],
        [
            {
                "h2": "Job board, smart batching, and assignment radius",
                "paras": [
                    "The driver app centres on a clear list of jobs for the shift — pending, on the way, and completed. Batching nearby drops reduces empty miles at lunch peak.",
                ],
                "blocks": [
                    {
                        "h3": "Today’s delivery list",
                        "paras": [
                            "Deliveries is the shift board. Each row shows enough to decide the next move: restaurant / customer cues, status, and actions to accept or start.",
                        ],
                        "steps": [
                            "Go online / available so new assignments can reach you.",
                            "Open <strong>Deliveries</strong> (or Home’s active list) and scan statuses.",
                            "Accept or start the next job according to your marketplace rules.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-deliveries.jpg", "Deliveries", "Today’s jobs: pending, on the way, completed"),
                    },
                    {
                        "h3": "Assignment radius (restaurant side)",
                        "paras": [
                            "How far a restaurant (or the marketplace) is willing to send couriers is controlled with delivery settings such as radius and preparation time. Drivers experience the result as which jobs appear — not as a separate “driver radius” screen.",
                        ],
                        "shot": ("phone", f"{A}/features/delivery-settings.jpg", "Delivery settings", "Radius and prep time that shape which jobs appear"),
                    },
                ],
                "after": [
                    'On the road: <a href="./active-delivery.html">On the road</a>. At the door: <a href="./proof-of-delivery.html">Photo &amp; signature POD</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "delivery-app/active-delivery.html",
        "On the road — Driver app",
        "On the road",
        "The live job screen and customer details drivers use between restaurant and door.",
        ["Active job", "Details", "Navigate"],
        [
            {
                "h2": "On the road",
                "paras": [
                    'While a job is active, the courier needs the current order, status, and primary actions in one place — and customer details for the drop-off. Customers follow the same order on <a href="../order-tracking.html">order tracking</a>.',
                ],
                "blocks": [
                    {
                        "h3": "Active delivery",
                        "paras": [
                            "The active delivery screen keeps the live job front and centre: what to pick up or drop, current status, and the next action (navigate, mark arrived, complete).",
                        ],
                        "shot": ("phone", f"{A}/features/driver-active.jpg", "Active delivery", "Current job controls while on delivery"),
                    },
                    {
                        "h3": "Customer and order details",
                        "paras": [
                            "Details expose the customer information needed at the door (name, phone, address notes) plus order line context. From here the driver can open navigation toward the address.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-details.jpg", "Delivery details", "Customer, address, and order context"),
                    },
                ],
                "after": [
                    'Finish the job with <a href="./proof-of-delivery.html">Photo &amp; signature POD</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "delivery-app/proof-of-delivery.html",
        "Photo & signature POD — Driver app",
        "Photo & signature POD",
        "Photo and signature at the door so contactless and COD disputes have evidence.",
        ["Photo", "Signature", "Complete"],
        [
            {
                "h2": "Proof of delivery at the door",
                "paras": [
                    "When the driver marks the order delivered, a proof-of-delivery flow can require a photo and a signature — especially useful for contactless drop-off and cash-on-delivery disputes. The modal explains contactless rules and offers Clear on the signature pad before Complete delivery.",
                ],
                "blocks": [
                    {
                        "h3": "Complete with evidence",
                        "steps": [
                            "Arrive at the drop-off and open <strong>Mark as Delivered</strong> (or the equivalent action).",
                            "If contactless is on, capture the required photo.",
                            "Collect a signature on the pad (or clear and retry).",
                            "Confirm <strong>Complete delivery</strong>. The order status becomes delivered for customer, restaurant, and admin.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-pod.jpg", "Proof of delivery", "Photo + signature before complete"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "delivery-app/earnings.html",
        "Shift earnings — Driver app",
        "Shift earnings",
        "How drivers see what a shift paid before digging into transactions or payout methods.",
        ["Shift totals", "Periods"],
        [
            {
                "h2": "Know what a shift paid",
                "paras": [
                    "Couriers need a clear money picture: what they earned today and across periods. Job handling stays on the delivery screens; this page is the summary totals.",
                ],
                "blocks": [
                    {
                        "h3": "Earnings overview",
                        "paras": [
                            "Earnings summarizes the shift and periods your build shows — totals the driver can trust after completing deliveries.",
                        ],
                        "steps": [
                            'Complete deliveries for the shift (see <a href="./deliveries.html">Job board &amp; batching</a>).',
                            "Open <strong>Earnings</strong> to review today’s totals and available periods.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-earnings.jpg", "Earnings", "Driver earnings overview for the shift"),
                    },
                ],
                "after": [
                    'Line items and bank setup: <a href="./transactions-payouts.html">Payouts &amp; history</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "delivery-app/transactions-payouts.html",
        "Payouts & history — Driver app",
        "Payouts & history",
        "Line-by-line money history and where settlements are sent.",
        ["Transactions", "Payouts"],
        [
            {
                "h2": "History and settlement",
                "paras": [
                    "When a total looks wrong, or when cash needs to reach a bank account, drivers use transactions and payout methods.",
                ],
                "blocks": [
                    {
                        "h3": "Transaction history",
                        "paras": [
                            "Transactions are the line-by-line trail: delivery fees, adjustments, and related movements. Use this when support asks for proof of a specific job payout.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-transactions.jpg", "Transactions", "Line-by-line driver transaction history"),
                    },
                    {
                        "h3": "Payout methods",
                        "paras": [
                            "Payout methods tell the platform where to settle the driver (including Connect-style onboarding when you enable it). Incomplete payout setup is a common “where is my money?” ticket.",
                        ],
                        "steps": [
                            "Open <strong>Payout methods</strong> from the driver money area.",
                            "Add or update the settlement method your marketplace supports.",
                            "Confirm status shows ready before the next payout cycle.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-payouts.jpg", "Payouts", "Where the driver receives settlements"),
                    },
                ],
                "after": [
                    'Shift totals: <a href="./earnings.html">Shift earnings</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "delivery-app/subscriptions.html",
        "Priority plans — Driver app",
        "Priority plans",
        "How courier priority tiers appear in the driver app — and how you define those plans in admin.",
        ["Priority", "Benefits", "Subscribe"],
        [
            {
                "h2": "Priority plans for couriers",
                "paras": [
                    "Driver subscriptions are tiers targeted at <strong>driver</strong> accounts. Typical benefits include priority job access, support priority, or other marketplace rules you attach to the plan — a recurring revenue stream, not just a vanity badge.",
                ],
                "blocks": [
                    {
                        "h3": "Driver steps",
                        "steps": [
                            "Sign in with a driver account.",
                            "Open Subscriptions from the driver menu / settings.",
                            "Choose a plan and complete Subscribe through an enabled payment path.",
                            "Confirm the plan shows as active and that any access benefits apply on the next shift.",
                        ],
                    },
                    {
                        "h3": "Operator setup",
                        "paras": [
                            'Create and edit driver tiers in admin → Subscriptions (target = driver). See <a href="../admin-app/subscriptions.html">Admin subscriptions</a>.',
                        ],
                    },
                ],
                "shots": [
                    ("phone", f"{A}/features/sub-driver.jpg", "Driver plans", "Driver subscription plans"),
                ],
            },
        ],
        D, DJ, DP,
    )

    r("delivery-app/logistics.html", "Logistics & POD", "./deliveries.html", "Job board & batching", D)

    # --- Restaurant ---
    w(
        "restaurant-app/orders.html",
        "Incoming orders — Restaurant app",
        "Incoming orders",
        "Accept or reject incoming tickets and advance status through prep and ready.",
        ["Accept", "Reject", "Status"],
        [
            {
                "h2": "Live orders: accept and reject",
                "paras": [
                    "Incoming orders land in the restaurant orders list in real time. Operators accept or reject, then move the meal through prepare / ready so the driver (or pickup customer) can collect it.",
                    'For a paperless board on the pass, use the <a href="./kitchen-display.html">Kitchen Display (KDS)</a> — it shares the same order pipeline.',
                ],
                "blocks": [
                    {
                        "h3": "Service loop",
                        "steps": [
                            "Keep the restaurant <strong>open</strong> when you can fulfill orders.",
                            "Watch the orders list; accept what you can cook, reject with a clear reason when you cannot.",
                            "Advance status as food progresses; mark ready for courier or pickup.",
                            "Use order history when you need past tickets or disputes.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-ops-orders.jpg", "Orders", "Live restaurant orders"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/menu.html",
        "Menu management — Restaurant app",
        "Menu management",
        "Manage categories, dishes, prices, photos, variants, and availability from the restaurant app.",
        ["Catalog", "Items", "Availability"],
        [
            {
                "h2": "Menu management",
                "paras": [
                    "Partners manage categories, dishes, prices, photos, variants, and availability without waiting on admin for every price tweak.",
                ],
                "blocks": [
                    {
                        "h3": "Menu home",
                        "paras": [
                            "The menu screen is the catalog home: categories and items customers will browse.",
                        ],
                        "steps": [
                            "Open <strong>Menu</strong> from the restaurant drawer.",
                            "Add or edit categories and items; set prices and photos.",
                            "Toggle availability when an item is 86’d so customers cannot order it.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-ops-menu.jpg", "Menu", "Categories and dishes the restaurant sells"),
                    },
                    {
                        "h3": "Add or edit an item",
                        "paras": [
                            "Item forms cover name, price, photo, variants, and availability. Getting this right once prevents “price wrong on the app” tickets.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-ops-menu-edit.jpg", "Edit item", "Item form: price, photo, variants, availability"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/hours.html",
        "Hours & delivery zone — Restaurant app",
        "Hours & delivery zone",
        "Opening hours and delivery settings that drive open/closed and how far the restaurant sells.",
        ["Hours", "Radius", "Prep time"],
        [
            {
                "h2": "When and how far you sell",
                "paras": [
                    "Opening hours and delivery settings (radius, prep time) tell the customer app when the restaurant is open and how far it delivers. Out-of-date hours create orders you cannot fulfill.",
                ],
                "blocks": [
                    {
                        "h3": "Opening hours",
                        "paras": [
                            "Fix hours before service, not after the first rejection. Customers see the result as open/closed on the restaurant page.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-ops-hours.jpg", "Hours", "Opening hours that drive open/closed in the customer app"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/analytics.html",
        "Performance — Restaurant app",
        "Performance",
        "Dashboard KPIs after a few service days: periods, bestsellers, and peaks.",
        ["KPIs", "Bestsellers", "Peaks"],
        [
            {
                "h2": "See what is working",
                "paras": [
                    "Dashboard KPIs and analytics help owners see what sells and when. Empty charts on day one are normal; quiet slots and bestsellers appear once orders accumulate.",
                ],
                "blocks": [
                    {
                        "h3": "Analytics screen",
                        "paras": [
                            "Use periods, bestsellers, and service peaks after a few real service days — then coach menu and staffing from facts.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-ops-analytics.jpg", "Analytics", "Periods, bestsellers, and service peaks"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/kitchen-display.html",
        "Kitchen Display — Restaurant app",
        "Kitchen Display (KDS)",
        "How the paperless kitchen board works: tickets, columns, and running it on a tablet at the pass.",
        ["Tickets", "Columns", "Tablet"],
        [
            {
                "h2": "What the Kitchen Display does",
                "paras": [
                    "The Kitchen Display is a board inside the restaurant app for cooks and the pass. After an order is accepted, it appears as a ticket with items, timing cues, and actions to move it through prep.",
                    "Columns such as <strong>New</strong>, <strong>Preparing</strong>, and <strong>Ready</strong> group tickets. Age on the ticket helps the line see what is burning.",
                ],
                "blocks": [
                    {
                        "h3": "Happy path on a busy service",
                        "steps": [
                            "A customer places a delivery or pickup order.",
                            'Restaurant staff accept it on <a href="./orders.html">Live orders</a> (or via your auto-accept rules).',
                            "Open <strong>Kitchen Display</strong> from the drawer — preferably on a tablet in landscape.",
                            "Advance each ticket: accept → prepare → ready.",
                            "When food is ready, the driver (or pickup customer) completes the handoff.",
                        ],
                        "shot": ("phone", f"{A}/features/kds.jpg", "Kitchen Display", "Tickets across New / Preparing / Ready"),
                    },
                    {
                        "h3": "Tablet tips",
                        "paras": [
                            "Mount the device at eye level on the pass, keep brightness high, and disable auto-lock during service. Prefer a stable Wi‑Fi path to your API.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-drawer.jpg", "Drawer", "Navigation entry to Kitchen Display"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/subscriptions.html",
        "Partner plans — Restaurant app",
        "Partner plans",
        "How restaurant partners buy SaaS-style plans that change commission, visibility, or tool access.",
        ["SaaS plans", "Commission", "Subscribe"],
        [
            {
                "h2": "Partner plans restaurants buy in-app",
                "paras": [
                    "Restaurant subscriptions are tiers with target <strong>restaurant</strong>. Benefits often include a lower platform commission, eligibility for sponsored placement, better support, or tool access — monetization the partner feels every month.",
                ],
                "blocks": [
                    {
                        "h3": "Restaurant steps",
                        "steps": [
                            "Sign in as the restaurant user.",
                            "Open <strong>Subscriptions</strong> from the drawer or settings.",
                            "Review price, cycle, and benefits; tap Subscribe on the chosen plan.",
                            "After activation, confirm commission / feature changes on the next orders.",
                        ],
                    },
                    {
                        "h3": "Where you edit tiers",
                        "paras": [
                            'Admin → Subscriptions, target = restaurant. See <a href="../admin-app/subscriptions.html">Admin subscriptions</a>.',
                        ],
                    },
                ],
                "shots": [
                    ("phone", f"{A}/features/sub-restaurant.jpg", "Restaurant plans", "Restaurant subscription screen"),
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/sponsored.html",
        "Sponsored visibility — Restaurant app",
        "Sponsored visibility",
        "How a restaurant launches a paid placement campaign (search, home banner, or both) from its own app.",
        ["Campaign", "Bid", "Placement"],
        [
            {
                "h2": "Buy attention in the customer feed",
                "paras": [
                    "Sponsored listings let a restaurant pay for better visibility: top of search, a home banner slot, or both. The restaurant fills a short campaign form — headline, daily bid, placement — then launches.",
                ],
                "blocks": [
                    {
                        "h3": "Launch a campaign",
                        "steps": [
                            "Sign in to the restaurant app (live API mode recommended for real campaigns).",
                            "Open <strong>Sponsored listings</strong>.",
                            "Under New campaign, set a headline customers will recognize.",
                            "Enter a daily bid amount and choose placement (search top, home banner, or search + banner).",
                            "Tap <strong>Launch campaign</strong>, then confirm the campaign appears under My campaigns.",
                            'Optionally verify in <a href="../admin-app/sponsored.html">admin sponsored listings</a>.',
                        ],
                        "shot": ("phone", f"{A}/features/sponsored.jpg", "Sponsored form", "Headline, bid, and placement"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    r("restaurant-app/operations.html", "Orders & menu", "./orders.html", "Incoming orders", D)

    # --- Admin ---
    w(
        "admin-app/orders.html",
        "Orders & support — Admin app",
        "Orders & support",
        "Investigate live and past marketplace orders from one list — payment, partners, and fulfillment.",
        ["Orders", "Support", "Detail"],
        [
            {
                "h2": "Orders as the support spine",
                "paras": [
                    "Admin is the marketplace command center. Support should investigate from one place without asking three mobile apps for screenshots.",
                ],
                "blocks": [
                    {
                        "h3": "Orders list",
                        "paras": [
                            "The orders list shows payment state, customer, restaurant, driver, totals, and fulfillment status. View opens full detail for failed payments, stuck statuses, or missing drivers.",
                        ],
                        "steps": [
                            "Open <strong>Orders</strong> when a live incident starts.",
                            "Filter or find the order by customer / restaurant / id.",
                            "Use View for the full record before changing status or contacting partners.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-ops-orders.jpg", "Orders", "Admin orders list with payment and fulfillment state"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/partners.html",
        "Partners & users — Admin app",
        "Partners & users",
        "Onboard and control restaurants, drivers, and customer accounts.",
        ["Restaurants", "Drivers", "Users"],
        [
            {
                "h2": "People and places that run the marketplace",
                "paras": [
                    "Partner screens cover restaurants, couriers, and customers — activate, edit, or suspend without leaving admin.",
                ],
                "blocks": [
                    {
                        "h3": "Restaurants",
                        "paras": [
                            "Onboarding and ongoing control: activate or close partners, keep profiles consistent with what the customer app displays.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-ops-restaurants.jpg", "Restaurants", "Approve, edit, activate, or close restaurant partners"),
                    },
                    {
                        "h3": "Drivers",
                        "paras": [
                            "Approve drivers before they go online, keep identity and vehicle details coherent, and suspend when needed.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-ops-drivers.jpg", "Drivers", "Driver onboarding and ongoing control"),
                    },
                    {
                        "h3": "Users (customers)",
                        "paras": [
                            "Investigate accounts, edit profiles, or suspend abuse. Pair with the orders list when a dispute needs both the person and their tickets.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-ops-users.jpg", "Users", "Customer accounts for support and moderation"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/catalog.html",
        "Menus & catalog — Admin app",
        "Menus & catalog",
        "Central menus and catalog curation that power what customers browse.",
        ["Menus", "Categories", "Products"],
        [
            {
                "h2": "Menus and catalog",
                "paras": [
                    "Categories, menus, products, and variants can be curated centrally when partners need help — or when you seed a new city. What you publish here is what customers browse.",
                ],
                "shots": [
                    ("wide", f"{A}/features/admin-ops-menus.jpg", "Menus", "Admin menus / catalog"),
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/earnings.html",
        "Commissions & earnings — Admin app",
        "Commissions & earnings",
        "Platform vs restaurant splits and period totals before payouts or investigations.",
        ["Commission", "Periods", "Splits"],
        [
            {
                "h2": "Commissions and earnings",
                "paras": [
                    "Every completed order splits value between the marketplace and the restaurant. The baseline platform commission is configured in marketplace / app settings; restaurant subscription benefits can soften that cut.",
                    "The Earnings area is where you review periods and totals before payouts or investigations.",
                ],
                "blocks": [
                    {
                        "h3": "Operator checklist",
                        "steps": [
                            "Set or review the default commission rate in App Settings.",
                            "Place a test order end-to-end (customer → restaurant accept → complete).",
                            "Open <strong>Earnings</strong> and confirm the platform vs restaurant split.",
                            "Use View on a row when you need the detail behind a period.",
                        ],
                        "shot": ("wide", f"{A}/features/earnings.jpg", "Earnings", "Earnings list — periods and totals"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/subscriptions.html",
        "Subscription plans — Admin app",
        "Subscription plans",
        "Source of truth for plans sold in the customer, driver, and restaurant apps.",
        ["Tiers", "Targets", "Benefits"],
        [
            {
                "h2": "Subscription tiers for every role",
                "paras": [
                    "Each plan has a <strong>target</strong>: customer, driver, or restaurant — plus price, billing cycle, active flag, and benefit text / flags.",
                ],
                "blocks": [
                    {
                        "h3": "Create or edit a plan",
                        "steps": [
                            "Open <strong>Subscriptions</strong> in the admin sidebar.",
                            "Review existing rows (name, target, price, cycle, active).",
                            "Add New or View to edit: set target audience, price, billing cycle, and benefits.",
                            "Save, then open the matching mobile app and confirm the plan appears.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-subscriptions.jpg", "Subscriptions", "Admin subscription tiers"),
                    },
                ],
                "after": [
                    'Subscribe UIs: <a href="../subscriptions.html">customer</a>, <a href="../delivery-app/subscriptions.html">driver</a>, <a href="../restaurant-app/subscriptions.html">restaurant</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/gateways.html",
        "Payment gateways — Admin app",
        "Payment gateways",
        "Which PSPs and local methods power checkout, wallets, and COD.",
        ["Gateways", "Fees", "Active"],
        [
            {
                "h2": "Payment gateways",
                "paras": [
                    "Gateways tell the platform which PSPs and local methods are available. Turn on only what you have credentials and compliance for.",
                ],
                "blocks": [
                    {
                        "h3": "Configure for a market",
                        "steps": [
                            "Open <strong>Gateways</strong> in admin.",
                            "Enable the methods you support; disable the rest.",
                            "Enter provider credentials / fees as your form requires.",
                            'Verify a test checkout and a wallet top-up from the <a href="../wallet.html">customer wallet</a> path.',
                        ],
                        "shot": ("wide", f"{A}/features/gateways.jpg", "Gateways", "Active payment gateways and fees"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/promotions.html",
        "Promo campaigns — Admin app",
        "Promo campaigns",
        "Campaign objects: type, discount, schedule, and scope for marketplace growth.",
        ["Campaigns", "Scope", "Schedule"],
        [
            {
                "h2": "Grow volume with real campaigns",
                "paras": [
                    "The promotion engine supports percentage or fixed discounts, free delivery, Buy X Get Y / combos, flash sales, happy hours, and similar types. Scope a campaign to the platform or to a restaurant, category, or item.",
                ],
                "blocks": [
                    {
                        "h3": "Create a promotion",
                        "steps": [
                            "Open <strong>Promotions</strong> and create or edit a campaign.",
                            "Set type, discount, schedule, and scope.",
                            "Activate, then place a demo customer order to prove the discount applies.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-promotions.jpg", "Promotions", "Campaign list: type, schedule, scope, status"),
                    },
                ],
                "after": [
                    'Shareable codes: <a href="./coupons.html">Coupons</a>. Customer surface: <a href="../checkout.html">Checkout &amp; offers</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/coupons.html",
        "Coupon codes — Admin app",
        "Coupon codes",
        "Redeemable codes with usage limits, expiry, and first-order constraints.",
        ["Codes", "Limits", "Expiry"],
        [
            {
                "h2": "Constrained redemptions",
                "paras": [
                    "Coupon codes add minimum order, max uses, per-user limits, first-order-only, and expiry. Customers enter codes in cart / checkout.",
                ],
                "blocks": [
                    {
                        "h3": "Create a coupon",
                        "steps": [
                            "Open <strong>Coupons</strong> and create a code with usage limits.",
                            "Confirm checkout accepts the code on a test order.",
                            "Retire or expire codes that are no longer funded.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-coupons.jpg", "Coupons", "Redeemable codes with limits and expiry"),
                    },
                ],
                "after": [
                    'Automatic campaigns: <a href="./promotions.html">Promotions</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/languages.html",
        "Languages & RTL — Admin app",
        "Languages & RTL",
        "Language catalogue, default locale, and RTL behaviour — plus the customer language picker.",
        ["Catalogue", "Default", "RTL"],
        [
            {
                "h2": "Marketplace language catalogue",
                "paras": [
                    "Admin maintains the language catalogue (code, name, default flag). That is the operator side. Customers, drivers, and restaurants still change language inside their own apps — see the Languages &amp; RTL pages under each mobile app. Arabic and similar locales reverse layout (RTL) across admin and mobiles.",
                ],
                "blocks": [
                    {
                        "h3": "Admin language list",
                        "steps": [
                            "Open <strong>Settings → Languages</strong> (or Languages in the sidebar).",
                            "Add or enable the languages you sell in; mark one as default.",
                            "Save, then verify a mobile app picks up the default for a fresh session.",
                        ],
                        "shot": ("wide", f"{A}/features/languages.jpg", "Languages", "Admin language catalogue with default flag"),
                    },
                    {
                        "h3": "Customer language picker",
                        "paras": [
                            "Customers change language from their settings screen — including RTL when you enable Arabic or similar locales.",
                        ],
                        "shot": ("phone", f"{A}/features/lang-picker.jpg", "Customer settings", "Language selection in customer settings"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/currencies-taxes.html",
        "Currencies & taxes — Admin app",
        "Currencies & taxes",
        "Money language and tax catalogues so carts and reports match your jurisdiction.",
        ["Currencies", "Taxes"],
        [
            {
                "h2": "Currencies",
                "paras": [
                    "Menus, carts, wallets, subscriptions, and reports should speak one money language per market. Treat currency changes as a go-live decision.",
                ],
                "shots": [
                    ("wide", f"{A}/features/currencies.jpg", "Currencies", "Admin currencies"),
                ],
            },
            {
                "h2": "Taxes",
                "paras": [
                    "Local tax rules (VAT, GST, sales tax) belong in the Taxes catalogue so carts and reports collect the right amounts. Configure rates before go-live and verify on a test checkout.",
                ],
                "shots": [
                    ("wide", f"{A}/features/admin-taxes.jpg", "Taxes", "Admin tax settings"),
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/app-settings.html",
        "Marketplace settings — Admin app",
        "Marketplace settings",
        "Cross-cutting marketplace behaviour: timezone, COD, delivery defaults, channels, and commission baselines.",
        ["Timezone", "Delivery", "Channels"],
        [
            {
                "h2": "Marketplace app settings",
                "paras": [
                    "App Settings hold default language, timezone, cash-on-delivery, delivery fee defaults, maximum delivery distance, and related flags. Commission baselines and channel hooks often live here too.",
                ],
                "blocks": [
                    {
                        "h3": "Before launch in a city",
                        "steps": [
                            "Open <strong>Settings → App Settings</strong> and View the active app record.",
                            "Set timezone, default language, delivery fee / distance, and COD according to local rules.",
                            "Align currency, taxes, and gateways with that same market.",
                            "Enable only the order channels you will actually operate.",
                            "Run one full order in that configuration before inviting real restaurants.",
                        ],
                        "shot": ("wide", f"{A}/features/app-settings.jpg", "App settings", "Marketplace app settings"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/sales-reports.html",
        "Sales analytics — Admin app",
        "Sales analytics",
        "Period volume, AOV, fees, taxes, and category breakdowns for marketplace performance.",
        ["Sales", "AOV", "Fees"],
        [
            {
                "h2": "Prove what the marketplace earned",
                "paras": [
                    "Sales reports cover the period you care about: volume, AOV, delivery fees, taxes collected, and category breakdowns. Start the week here before partner conversations.",
                ],
                "blocks": [
                    {
                        "h3": "Sales reports",
                        "paras": [
                            "Use earnings for commission splits; use sales reports for period analytics across the marketplace.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-sales-reports.jpg", "Sales reports", "Period sales with fees, taxes, and breakdowns"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/partner-reports.html",
        "Partner scorecards — Admin app",
        "Partner scorecards",
        "Restaurant and driver scorecards for coaching, staffing, and commercial talks.",
        ["Restaurants", "Drivers"],
        [
            {
                "h2": "Partner performance",
                "paras": [
                    "Partner reports turn operational noise into coaching and staffing decisions.",
                ],
                "blocks": [
                    {
                        "h3": "Restaurant reports",
                        "paras": [
                            "Who is growing, who is rejecting too much, who needs help with menu or hours.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-resto-reports.jpg", "Restaurant reports", "Partner performance scorecards"),
                    },
                    {
                        "h3": "Driver reports",
                        "paras": [
                            "Late deliveries, coverage gaps, and top couriers — staff peaks with facts instead of anecdotes.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-driver-reports.jpg", "Driver reports", "Courier performance and reliability"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/transactions.html",
        "Money ledger — Admin app",
        "Money ledger",
        "The money ledger: payments, payouts, refunds, tips, and wallet movements.",
        ["Ledger", "Refunds", "Payouts"],
        [
            {
                "h2": "Transactions ledger",
                "paras": [
                    "Fee-level transparency for payments, payouts, refunds, tips, and wallet movements. Spot-check it when a payout or refund is disputed — before you invent a spreadsheet.",
                ],
                "blocks": [
                    {
                        "h3": "Ledger view",
                        "paras": [
                            "Open Transactions when finance or support needs proof of a money movement.",
                        ],
                        "shot": ("wide", f"{A}/features/admin-transactions.jpg", "Transactions", "Money ledger for payments, payouts, refunds"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    spon_img = "assets/images/features/admin-sponsored.jpg"
    if not (ROOT / spon_img).exists():
        spon_img = "assets/images/features/sponsored.jpg"

    w(
        "admin-app/sponsored.html",
        "Sponsored inventory — Admin app",
        "Sponsored inventory",
        "How operators oversee paid placement campaigns that restaurants create from their app.",
        ["Oversight", "Campaigns", "Marketplace"],
        [
            {
                "h2": "Keep paid placement under control",
                "paras": [
                    "Restaurants create and launch campaigns from the restaurant app. Admin Sponsored listings is the operator view: which campaigns exist, their state, and enough context to intervene.",
                ],
                "blocks": [
                    {
                        "h3": "Operator workflow",
                        "steps": [
                            "Open <strong>Sponsored listings</strong> in admin.",
                            "Review active and past campaigns (restaurant, placement, status).",
                            "Open View when you need campaign detail or to take an admin action.",
                            'Cross-check the <a href="../restaurant-app/sponsored.html">restaurant sponsored</a> form.',
                        ],
                        "shot": ("wide", spon_img, "Admin sponsored", "Sponsored listings in admin"),
                    },
                ],
            },
        ],
        D, DJ, DP,
    )

    r("admin-app/operations.html", "Operations", "./orders.html", "Orders & support", D)
    r("admin-app/monetization.html", "Monetization", "./earnings.html", "Commissions & earnings", D)
    r("admin-app/market.html", "Market & languages", "./languages.html", "Languages & RTL", D)
    r("admin-app/reports.html", "Reports & analytics", "./sales-reports.html", "Sales analytics", D)

    # --- Languages on mobile (not only admin) ---
    w(
        "languages-rtl.html",
        "Languages & RTL — Customer app",
        "Languages & RTL",
        "Customers switch English, French, Spanish, or Arabic — including a fully mirrored RTL layout — from Settings in the app.",
        ["EN / FR / ES / AR", "RTL", "Settings"],
        [
            {
                "h2": "Speak the customer’s language on their phone",
                "paras": [
                    "Languages are not an admin-only catalogue. In the customer app, shoppers open Settings and pick the language they want. Arabic flips the layout (RTL) so the marketplace feels local — the same capability buyers look for when launching outside one English-speaking city.",
                    "Admin still defines which languages exist and which is the marketplace default; the mobile picker is how each person overrides that for their own session.",
                ],
                "blocks": [
                    {
                        "h3": "Language picker in Settings",
                        "paras": [
                            "Open Settings / Account language, choose EN, FR, ES, or AR, and confirm strings update across home, menu, cart, and tracking.",
                        ],
                        "steps": [
                            "Sign in as a customer.",
                            "Open <strong>Settings</strong> (drawer or account).",
                            "Choose a language and return to Home — labels and layout should follow.",
                            "Try Arabic to verify RTL mirroring on key screens.",
                        ],
                        "shot": ("phone", f"{A}/features/lang-picker.jpg", "Language picker", "Customer settings language selection"),
                    },
                    {
                        "h3": "Arabic RTL in the customer app",
                        "paras": [
                            "With Arabic selected, the UI mirrors (I18nManager forceRTL): navigation, lists, and forms read right-to-left. That is a product feature for Gulf / MENA launches — not a hidden developer flag.",
                        ],
                        "shot": ("phone", f"{A}/features/customer-languages-rtl.jpg", "Arabic RTL", "Customer settings mirrored EN → AR"),
                    },
                ],
                "after": [
                    'Operator catalogue: <a href="./admin-app/languages.html">Admin — Languages &amp; RTL</a>. Same idea on <a href="./delivery-app/languages.html">driver</a> and <a href="./restaurant-app/languages.html">restaurant</a> apps.',
                ],
            },
        ],
        C, CJ, CP,
    )

    w(
        "delivery-app/languages.html",
        "Languages & RTL — Driver app",
        "Languages & RTL",
        "Couriers change app language from driver Settings — including Arabic RTL — so the shift board speaks their language.",
        ["Settings", "EN / FR / ES / AR", "RTL"],
        [
            {
                "h2": "Driver app in the courier’s language",
                "paras": [
                    "Drivers work long shifts; the app must speak their language. Settings exposes the same locale packs (English, French, Spanish, Arabic with RTL) that customers and restaurants use.",
                ],
                "blocks": [
                    {
                        "h3": "Change language in Settings",
                        "paras": [
                            "Open Settings from the drawer, pick a language, and confirm Deliveries / Active job strings update. Admin still controls which languages are enabled marketplace-wide.",
                        ],
                        "steps": [
                            "Sign in as a driver.",
                            "Open <strong>Settings</strong>.",
                            "Select a language and return to the job board.",
                        ],
                        "shot": ("phone", f"{A}/features/driver-settings.jpg", "Driver settings", "Driver settings where language is changed"),
                    },
                ],
                "after": [
                    'Customer picker: <a href="../languages-rtl.html">Languages &amp; RTL</a>. Admin catalogue: <a href="../admin-app/languages.html">Languages &amp; RTL</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "restaurant-app/languages.html",
        "Languages & RTL — Restaurant app",
        "Languages & RTL",
        "Restaurant staff switch language (and RTL when Arabic is on) from the partner Settings screen.",
        ["Settings", "EN / FR / ES / AR", "RTL"],
        [
            {
                "h2": "Partner app in the kitchen’s language",
                "paras": [
                    "Owners and line staff are not always fluent in the marketplace default language. The restaurant app Settings picker lets them run orders, menu, and KDS labels in EN / FR / ES / AR — with RTL when Arabic is selected.",
                ],
                "blocks": [
                    {
                        "h3": "Change language in Settings",
                        "paras": [
                            "Open Settings, choose a language, and verify Orders / Menu strings. Pair this with correct opening hours so open/closed copy matches the locale customers see.",
                        ],
                        "steps": [
                            "Sign in as the restaurant user.",
                            "Open <strong>Settings</strong>.",
                            "Select a language and confirm the drawer and orders list update.",
                        ],
                        "shot": ("phone", f"{A}/features/resto-settings.jpg", "Restaurant settings", "Restaurant settings where language is changed"),
                    },
                ],
                "after": [
                    'Customer: <a href="../languages-rtl.html">Languages &amp; RTL</a>. Admin defaults: <a href="../admin-app/languages.html">Languages &amp; RTL</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )

    w(
        "admin-app/order-channels.html",
        "Order channels — Admin app",
        "Order channels",
        "WhatsApp, USSD, and web intake so the marketplace takes orders beyond the mobile apps — with order source tracked for ops.",
        ["WhatsApp", "USSD", "Web"],
        [
            {
                "h2": "Reach customers where they already are",
                "paras": [
                    "Not every market starts with app installs. Hybrid channels let you notify and intake orders over WhatsApp Cloud API, USSD-style menus for feature phones, and web / API intake — each order tagged with its source (app / whatsapp / ussd / web / admin) so support knows how it arrived.",
                ],
                "blocks": [
                    {
                        "h3": "Configure channels with marketplace settings",
                        "paras": [
                            "Credentials and enablement live with marketplace / app settings (Meta phone number ID + token for WhatsApp, aggregator hooks for USSD, authenticated web intake). Turn on only the channels you will operate before go-live.",
                        ],
                        "steps": [
                            "Open <strong>Settings → App Settings</strong> (or your channels form).",
                            "Enable WhatsApp / USSD / web only when credentials and compliance are ready.",
                            "Place a test order per channel and confirm <code>orderSource</code> shows correctly on the order record.",
                            "Verify status notifications fan out on the channel you enabled.",
                        ],
                        "shot": ("wide", f"{A}/features/app-settings.jpg", "Marketplace settings", "Where channel and marketplace flags are configured"),
                    },
                ],
                "after": [
                    'Related: <a href="./app-settings.html">Marketplace settings</a>, <a href="./orders.html">Orders &amp; support</a>.',
                ],
            },
        ],
        D, DJ, DP,
    )


    # Update legacy feature redirects that pointed at fat pages
    for rel, dest in [
        ("features/intelligence.html", "../recommendations.html"),
        ("features/market-adaptability.html", "../admin-app/languages.html"),
    ]:
        p = ROOT / rel
        if p.exists():
            p.write_text(
                f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={dest}" />
    <link rel="canonical" href="{dest}" />
    <title>Moved</title>
  </head>
  <body>
    <p>This page moved. <a href="{dest}">Continue here</a>.</p>
  </body>
</html>
""",
                encoding="utf-8",
            )

    print("OK — feature pages written")


if __name__ == "__main__":
    main()
