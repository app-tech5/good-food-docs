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


def main():
    ensure_admin_sponsored()

    ROOT.joinpath("wallet.html").write_text(
        page(
            "Wallet & payments — Customer app",
            "Wallet & payments",
            "How the in-app balance works for customers, how they top up, and what you configure so checkout and refunds stay coherent.",
            ["Balance", "Top up", "Payment methods"],
            [
                {
                    "h2": "What the wallet is for",
                    "paras": [
                        "The wallet is a prepaid balance inside the customer app. Instead of entering a card on every order, the customer can pay from money already on the account. That shortens checkout, reduces failed payments at the door of the kitchen, and gives you a place to land refunds or promotions as credit.",
                    ],
                    "blocks": [
                        {
                            "h3": "What the customer sees on Wallet",
                            "paras": [
                                "The Wallet screen shows the current balance at the top, then actions to add (and optionally send) money, then the list of saved payment methods — card brands, Google Pay, PayPal, cash, and similar options you enable. This is the home base before any top-up or checkout choice.",
                            ],
                            "shot": ("phone", f"{A}/features/wallet.jpg", "Customer wallet", "Balance, actions, and saved payment methods"),
                        },
                        {
                            "h3": "How a customer tops up",
                            "paras": [
                                "Add Money opens a focused top-up flow: pick an amount (or a quick chip such as $10 / $20 / $50), choose how to pay, then confirm. Once the balance updates, checkout can use the wallet when the amount covers the order (or the share your rules allow).",
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
                                'Payment gateways and marketplace payment behaviour are managed in the admin app — see <a href="./admin-app/monetization.html">Monetization</a>. Enable only the gateways you actually use in each market before expecting top-ups to succeed in production.',
                            ],
                        },
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("subscriptions.html").write_text(
        page(
            "Subscriptions — Customer app",
            "Subscriptions",
            "How membership plans appear to customers, what benefits they unlock, and how those plans are created in admin.",
            ["Plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Membership in the customer app",
                    "paras": [
                        "Customer subscriptions are recurring plans (for example monthly) that unlock benefits such as free delivery, a food discount, member-only deals, or priority support. The customer app shows only plans whose target is <strong>customer</strong>.",
                        "Each plan card lists the name, price and billing cycle, the benefit bullets, and a Subscribe action. After a successful purchase path (via your configured gateways), the membership stays attached to that account until it expires or is cancelled under your rules.",
                    ],
                    "blocks": [
                        {
                            "h3": "How a customer subscribes",
                            "steps": [
                                "Sign in with a customer account.",
                                "Open the Subscriptions / membership screen from account or settings (label depends on your translations).",
                                "Compare the listed plans and tap <strong>Subscribe</strong> on the one you want.",
                                "Complete payment with an enabled gateway. Confirm the plan shows as active afterward.",
                            ],
                            "shot": ("phone", f"{A}/features/sub-customer.jpg", "Customer plans", "Plan cards with benefits and Subscribe"),
                        },
                        {
                            "h3": "Where plans are defined",
                            "paras": [
                                'You create and edit tiers in the admin app under Subscriptions (name, price, billing cycle, benefits, active flag, target = customer). Details and earnings impact are covered in <a href="./admin-app/monetization.html">admin monetization</a>.',
                            ],
                        },
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("intelligence.html").write_text(
        page(
            "AI intelligence — Customer app",
            "AI intelligence",
            "Three customer-facing helpers: personalized recommendations, smarter arrival times, and delivery fees that can rise when demand spikes.",
            ["Recommendations", "Smart ETA", "Surge"],
            [
                {
                    "h2": "Recommendations that grow the basket",
                    "paras": [
                        "On restaurant and discovery surfaces, a <strong>Recommended for you</strong> block can suggest dishes that fit the customer’s history, time of day, and context such as weather. Each card shows a short reason line so the suggestion feels explained rather than random.",
                        "The goal is a natural add-to-cart moment (sides, drinks, extras) that raises average order value without forcing a separate upsell screen.",
                    ],
                    "blocks": [
                        {
                            "h3": "What the customer sees",
                            "paras": [
                                "A horizontal row of recommended items with title, price, and a short match reason. Tapping a card follows your normal product / add-to-cart path — same as browsing the menu, just smarter placement.",
                            ],
                            "shot": ("phone", f"{A}/features/ai-reco.jpg", "Recommendations", "Recommended for you with reason lines on the restaurant screen"),
                        },
                    ],
                },
                {
                    "h2": "Arrival times customers can trust",
                    "paras": [
                        "Smart ETA estimates how long food will take, using kitchen load and travel time where your backend intelligence stack is enabled. On the restaurant page the estimate appears as its own chip (for example “ETA 26–36 min”).",
                        "Clearer arrivals reduce “where is my food?” support load and set expectations before the customer commits to checkout.",
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
                },
                {
                    "h2": "Delivery fee when the city is busy",
                    "paras": [
                        "When demand is high and courier capacity is tight, the delivery-fee chip can show a surge multiplier (for example “Surge 1.45x”). Quiet periods keep a standard fee; peaks stay explicit so the customer understands the cost before paying.",
                        "Fee / surge is a marketplace lever for reliability — separate from the ETA chip, which only answers “how long?”.",
                    ],
                    "blocks": [
                        {
                            "h3": "The fee / surge chip",
                            "paras": [
                                "On restaurant detail, read the fee chip for what delivery costs now. Surge replaces the standard fee when your rules say demand is elevated; if you only see “Standard fee”, that hour is quiet.",
                            ],
                            "shot": ("phone", f"{A}/features/ai-surge.jpg", "Fee / surge", "Surge (or standard) fee chip on restaurant detail"),
                        },
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    ROOT.joinpath("order-tracking.html").write_text(
        page(
            "Order tracking — Customer app",
            "Order tracking",
            "How customers follow an order from acceptance to delivery, and how that ties to the map and the driver app.",
            ["Status steps", "ETA", "Map"],
            [
                {
                    "h2": "Follow the order without calling support",
                    "paras": [
                        "After checkout, customers should not need to call support to know where their food is. Track Order is the single place that answers: was it accepted, is the kitchen cooking, is a courier on the way, and when will it arrive.",
                    ],
                    "blocks": [
                        {
                            "h3": "Status timeline",
                            "paras": [
                                "The screen shows the order id, timestamp, and a vertical status timeline: pending → preparing → out for delivery → delivered. Active steps are highlighted; later steps stay muted until they happen. Restaurant contact details sit on the same screen so the customer can call about the meal itself while delivery progress stays visible — without opening a separate chat.",
                            ],
                            "steps": [
                                "Place an order and wait for the restaurant to accept it.",
                                "Open <strong>Order history</strong>, select the order, then <strong>Track order</strong> (or the deep link after payment).",
                                "Watch the timeline advance as kitchen and driver statuses change on the shared order record.",
                                "When the driver is en route, ETA copy updates when your logistics / intelligence data provides it.",
                            ],
                            "shot": ("phone", f"{A}/features/tracking.jpg", "Track order", "Order id, status timeline, restaurant contact"),
                        },
                        {
                            "h3": "Delivery map while the courier is en route",
                            "paras": [
                                'When the order is out for delivery, Track Order can show a <strong>Delivery Map</strong>: destination pin, live courier position, route line, and an ETA badge (for example “ETA ~3 min”). That is the live tracking view — not the nearby-restaurant discovery map. Driver-side job handling and proof of delivery are documented under <a href="./delivery-app/logistics.html">Logistics &amp; POD</a>.',
                            ],
                            "shot": ("phone", f"{A}/features/tracking-map.jpg", "Delivery map", "Route, courier pin, destination, and ETA badge"),
                        },
                    ],
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/logistics.html").write_text(
        page(
            "Logistics & POD — Driver app",
            "Logistics & proof of delivery",
            "How drivers work a shift: today’s jobs, an active delivery, customer details, and proof at the door.",
            ["Deliveries", "Active job", "Proof of delivery"],
            [
                {
                    "h2": "Today’s deliveries and assignment radius",
                    "paras": [
                        "The driver app centres on a clear list of jobs for the shift — pending, on the way, and completed. Batching nearby drops reduces empty miles at lunch peak: one courier can stack orders in the same neighbourhood instead of zigzagging across the city.",
                    ],
                    "blocks": [
                        {
                            "h3": "Today’s delivery list",
                            "paras": [
                                "Deliveries is the shift board. Each row shows enough to decide the next move: restaurant / customer cues, status, and actions to accept or start. Drivers go online first so new assignments can reach them, then work the list in order.",
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
                                "How far a restaurant (or the marketplace) is willing to send couriers is controlled with delivery settings such as radius and preparation time. Those settings live with the restaurant / marketplace configuration; drivers experience the result as which jobs appear and how far they run — not as a separate “driver radius” screen.",
                            ],
                            "shot": ("phone", f"{A}/features/delivery-settings.jpg", "Delivery settings", "Radius and prep time that shape which jobs appear"),
                        },
                    ],
                },
                {
                    "h2": "On the road",
                    "paras": [
                        'While a job is active, the courier needs the current order, status, and primary actions in one place — and customer details for the drop-off. Customers follow the same order on <a href="../order-tracking.html">order tracking</a>: there is one order record, not a separate “driver copy”.',
                    ],
                    "blocks": [
                        {
                            "h3": "Active delivery",
                            "paras": [
                                "The active delivery screen keeps the live job front and centre: what to pick up or drop, current status, and the next action (navigate, mark arrived, complete). This is the screen drivers live on between restaurant and door.",
                            ],
                            "shot": ("phone", f"{A}/features/driver-active.jpg", "Active delivery", "Current job controls while on delivery"),
                        },
                        {
                            "h3": "Customer and order details",
                            "paras": [
                                "Details expose the customer information needed at the door (name, phone, address notes) plus order line context. From here the driver can open navigation toward the address without leaving the job context.",
                            ],
                            "shot": ("phone", f"{A}/features/driver-details.jpg", "Delivery details", "Customer, address, and order context"),
                        },
                    ],
                },
                {
                    "h2": "Proof of delivery at the door",
                    "paras": [
                        "When the driver marks the order delivered, a proof-of-delivery flow can require a photo and a signature — especially useful for contactless drop-off and cash-on-delivery disputes. The modal explains contactless rules (for example staying within a short distance of the address) and offers Clear on the signature pad before Complete delivery.",
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
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/driver-pod.jpg", "Proof of delivery", "Photo + signature before complete"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/subscriptions.html").write_text(
        page(
            "Subscriptions — Driver app",
            "Subscriptions",
            "How courier membership plans appear in the driver app and how you define those tiers in admin.",
            ["Driver plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Plans for couriers",
                    "paras": [
                        "Driver subscriptions are tiers targeted at <strong>driver</strong> accounts. Typical benefits include access perks, support priority, or other marketplace rules you attach to the plan. The driver app lists those plans with price, cycle, and a Subscribe action — the same pattern customers and restaurants see for their own targets.",
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
                                'Create and edit driver tiers in admin → Subscriptions (target = driver). See <a href="../admin-app/monetization.html">Monetization</a> for the full money picture.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sub-driver.jpg", "Driver plans", "Driver subscription plans"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/kitchen-display.html").write_text(
        page(
            "Kitchen Display — Restaurant app",
            "Kitchen Display (KDS)",
            "How the paperless kitchen board works: where tickets come from, how staff advance them, and how to run it on a tablet at the pass.",
            ["Tickets", "Columns", "Orders"],
            [
                {
                    "h2": "What the Kitchen Display does",
                    "paras": [
                        "The Kitchen Display is a board inside the restaurant app for cooks and the pass. After an order is accepted, it appears as a ticket with items, timing cues, and actions to move it through prep. The idea is simple: stop hunting paper slips; keep one shared order story with the customer, the driver, and admin.",
                        "Columns such as <strong>New</strong>, <strong>Preparing</strong>, and <strong>Ready</strong> group tickets. Staff accept new work, start preparation, then mark food ready for pickup or courier handoff. Age on the ticket helps the line see what is burning.",
                    ],
                    "blocks": [
                        {
                            "h3": "Happy path on a busy service",
                            "steps": [
                                "A customer places a delivery or pickup order.",
                                "Restaurant staff accept it on the normal <strong>Orders</strong> list (or via your auto-accept rules).",
                                "Open <strong>Kitchen Display</strong> from the drawer / navigation — preferably on a tablet in landscape.",
                                "Advance each ticket: accept → prepare → ready.",
                                "When food is ready, the driver (or the customer for pickup) completes the handoff; admin still sees the same order for support and earnings.",
                            ],
                        },
                        {
                            "h3": "Tablet tips",
                            "paras": [
                                "Mount the device at eye level on the pass, keep brightness high, and disable auto-lock during service. Prefer a stable Wi‑Fi path to your API — a flaky network looks like “KDS is broken”.",
                                "Demo databases can include kitchen-oriented sample tickets so you can train staff or screenshot the board before the first real rush.",
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/kds.jpg", "Kitchen Display", "Tickets across New / Preparing / Ready"),
                    ],
                },
                {
                    "h2": "Tied to the live orders list",
                    "paras": [
                        "Orders still land in the restaurant orders UI first. The Kitchen Display is the kitchen-oriented view of that same pipeline — not a second database. If a ticket is missing on the board, refresh and confirm the order exists and was accepted for this restaurant account.",
                    ],
                    "blocks": [
                        {
                            "h3": "Live restaurant orders",
                            "paras": [
                                "Accept and reject happen here. New-order alerts can deep-link back to the order so nobody misses a ticket during rush. Advance status as food progresses; the KDS board mirrors that same pipeline for the pass.",
                            ],
                            "shot": ("phone", f"{A}/features/resto-orders.jpg", "Orders", "Accept / reject and advance live restaurant orders"),
                        },
                        {
                            "h3": "Open Kitchen Display from the menu",
                            "paras": [
                                "Staff open <strong>Kitchen Display</strong> from the drawer / navigation — preferably on a tablet in landscape at the pass. Keep brightness high and disable auto-lock during service; a flaky network looks like “KDS is broken”.",
                            ],
                            "shot": ("phone", f"{A}/features/resto-drawer.jpg", "Drawer", "Navigation entry to Kitchen Display"),
                        },
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/subscriptions.html").write_text(
        page(
            "Subscriptions — Restaurant app",
            "Subscriptions",
            "How restaurant partners subscribe to plans that change commission, visibility, or SaaS-style access.",
            ["Restaurant plans", "Benefits", "Subscribe"],
            [
                {
                    "h2": "Plans partners buy from their app",
                    "paras": [
                        "Restaurant subscriptions are tiers with target <strong>restaurant</strong>. Benefits often include a lower platform commission, eligibility for sponsored placement, better support, or tool access you attach to the plan. Partners see those plans inside the restaurant app and subscribe without leaving their day-to-day workspace.",
                    ],
                    "blocks": [
                        {
                            "h3": "Restaurant steps",
                            "steps": [
                                "Sign in as the restaurant user.",
                                "Open <strong>Subscriptions</strong> from the drawer or settings.",
                                "Review price, cycle, and benefits; tap Subscribe on the chosen plan.",
                                "After activation, confirm commission / feature changes on the next orders (and in admin earnings if you are verifying).",
                            ],
                        },
                        {
                            "h3": "Where you edit tiers",
                            "paras": [
                                'Admin → Subscriptions, target = restaurant. Full monetization context: <a href="../admin-app/monetization.html">Monetization</a>.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sub-restaurant.jpg", "Restaurant plans", "Restaurant subscription screen"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/sponsored.html").write_text(
        page(
            "Sponsored listings — Restaurant app",
            "Sponsored listings",
            "How a restaurant launches a paid placement campaign (search, home banner, or both) from its own app.",
            ["Campaign", "Bid", "Placement"],
            [
                {
                    "h2": "Buy attention in the customer feed",
                    "paras": [
                        "Sponsored listings let a restaurant pay for better visibility: top of search, a home banner slot, or both. The restaurant fills a short campaign form — headline, daily bid, placement — then launches. Active campaigns can appear in the customer experience without looking like a bolted-on ad unit.",
                        "Admin keeps oversight of what is live so paid placement stays controlled marketplace-wide.",
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
                                'Optionally verify in the customer app that the placement shows, and in <a href="../admin-app/sponsored.html">admin sponsored listings</a> that the campaign is visible to operators.',
                            ],
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/sponsored.jpg", "Sponsored form", "Headline, bid, and placement"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/monetization.html").write_text(
        page(
            "Monetization — Admin app",
            "Monetization",
            "How operators set the platform cut, subscription tiers, earnings views, and payment gateways that power wallets and checkout.",
            ["Earnings", "Subscriptions", "Gateways"],
            [
                {
                    "h2": "Commissions and earnings",
                    "paras": [
                        "Every completed order splits value between the marketplace and the restaurant (and related parties under your rules). The baseline platform commission is configured in marketplace / app settings; restaurant subscription benefits can soften that cut when an active plan says so.",
                        "The Earnings area in admin is where you review periods and totals — what the platform kept versus what restaurants earned — before you run payouts or investigations.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator checklist",
                            "steps": [
                                "Set or review the default commission rate in App Settings.",
                                "Place a test order end-to-end (customer → restaurant accept → complete).",
                                "Open <strong>Earnings</strong> and confirm the platform vs restaurant split matches your rate and any active restaurant plan benefits.",
                                "Use View on a row when you need the detail behind a period.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/earnings.jpg", "Earnings", "Earnings list — periods and totals"),
                    ],
                },
                {
                    "h2": "Subscription tiers for every role",
                    "paras": [
                        "Subscriptions in admin are the source of truth for plans sold in the three mobile apps. Each plan has a <strong>target</strong>: customer, driver, or restaurant — plus price, billing cycle, active flag, and benefit text / flags.",
                        "Seeded demos usually include sample tiers so lists are not empty after migrations. Edit those to match your pricing story before go-live.",
                    ],
                    "blocks": [
                        {
                            "h3": "Create or edit a plan",
                            "steps": [
                                "Open <strong>Subscriptions</strong> in the admin sidebar.",
                                "Review existing rows (name, target, price, cycle, active).",
                                "Add New or View to edit: set target audience, price, billing cycle, and benefits.",
                                "Save, then open the matching mobile app and confirm the plan appears on that role’s subscription screen.",
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-subscriptions.jpg", "Subscriptions", "Admin subscription tiers"),
                    ],
                    "after": [
                        'Customer, driver, and restaurant subscribe UIs: <a href="../subscriptions.html">customer</a>, <a href="../delivery-app/subscriptions.html">driver</a>, <a href="../restaurant-app/subscriptions.html">restaurant</a>.',
                    ],
                },
                {
                    "h2": "Payment gateways",
                    "paras": [
                        "Gateways tell the platform which PSPs and local methods are available (cards, wallets, cash on delivery, regional providers, and the internal wallet). Each row typically shows fees, name, and whether it is active.",
                        "Turn on only what you have credentials and compliance for. Checkout and wallet top-ups will fail in production if the customer’s method points at a disabled or misconfigured gateway.",
                    ],
                    "blocks": [
                        {
                            "h3": "Configure for a market",
                            "steps": [
                                "Open <strong>Gateways</strong> in admin.",
                                "Enable the methods you support; disable the rest.",
                                "Enter provider credentials / fees as your form requires (View on a row).",
                                'Verify a test checkout and a wallet top-up from the <a href="../wallet.html">customer wallet</a> docs path.',
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/gateways.jpg", "Gateways", "Active payment gateways and fees"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/market.html").write_text(
        page(
            "Market & languages — Admin app",
            "Market & languages",
            "How to make the marketplace feel local: languages (including RTL), currencies, and app-level marketplace settings.",
            ["Languages", "Currencies", "App settings"],
            [
                {
                    "h2": "Languages",
                    "paras": [
                        "Admin maintains the language catalogue (code, name, default flag). Mobile apps and the admin UI follow the active / default language. Arabic and similar locales can reverse layout (RTL) when the selected language requires it — so the marketplace feels local, not translated as an afterthought.",
                    ],
                    "blocks": [
                        {
                            "h3": "Admin language list",
                            "paras": [
                                "This is where you decide which languages exist and which one is the marketplace default for new users. Open Settings → Languages (or Languages in the sidebar), ensure every market you sell in is present, and mark one default.",
                            ],
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
                                "Customers change language from their settings screen. Switch language in a customer (or driver / restaurant) app to verify strings and layout — including RTL when you enable Arabic or similar locales.",
                            ],
                            "shot": ("phone", f"{A}/features/lang-picker.jpg", "Customer settings", "Language selection in customer settings"),
                        },
                    ],
                },
                {
                    "h2": "Currencies",
                    "paras": [
                        "Menus, carts, wallets, subscriptions, and reports should speak one money language per market. The Currencies list is where you define codes and defaults; changing the active currency without a plan will confuse prices already shown to users, so treat it as a go-live decision.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/currencies.jpg", "Currencies", "Admin currencies"),
                    ],
                },
                {
                    "h2": "Taxes",
                    "paras": [
                        "Local tax rules (VAT, GST, sales tax, and similar) belong in the Taxes catalogue so carts and reports collect the right amounts for your jurisdiction. Configure rates before go-live and verify on a test checkout that tax lines match finance expectations.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-taxes.jpg", "Taxes", "Admin tax settings"),
                    ],
                },
                {
                    "h2": "Marketplace app settings",
                    "paras": [
                        "App Settings hold cross-cutting marketplace behaviour: default language, timezone, cash-on-delivery, delivery fee defaults, maximum delivery distance, and related flags. Commission baselines and channel hooks (WhatsApp / USSD / web ordering when enabled) often live here too — review this screen when you enter a new city.",
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
                        },
                    ],
                    "shots": [
                        ("wide", f"{A}/features/app-settings.jpg", "App settings", "Marketplace app settings"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    # --- Pages covering CodeCanyon / Pro feature gaps ---

    ROOT.joinpath("ordering.html").write_text(
        page(
            "Ordering & discovery — Customer app",
            "Ordering & discovery",
            "How customers find restaurants, open a place, browse the menu, add items, apply offers, and check out — one screen, one idea.",
            ["Home", "Map", "Restaurant", "Menu", "Cart", "Checkout"],
            [
                {
                    "h2": "Find food in a multi-restaurant marketplace",
                    "paras": [
                        "The customer app is a multi-store marketplace: one install, many restaurants. Each screen below is a distinct step — the capture next to it shows only that step, not the whole journey at once.",
                    ],
                    "blocks": [
                        {
                            "h3": "Homepage — delivery / pickup, categories, banners",
                            "paras": [
                                "Home starts with the Delivery / Pickup toggle, a search field, a horizontal category row, and a promo carousel (for example “15% off” with Browse Offers). Below that, Special Offers lists restaurant cards with rating, distance / prep cues, and offer badges. This screen is discovery — not the restaurant header, not the menu.",
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
                                "The nearby map is the geographic discovery view: restaurant pins on the city map and a swipeable restaurant card at the bottom. Use it when the customer wants “what’s close”, not when they already opened a restaurant menu.",
                            ],
                            "shot": ("phone", f"{A}/features/map-nearby.jpg", "Nearby map", "Map pins with swipeable restaurant card"),
                        },
                        {
                            "h3": "Open / closed status",
                            "paras": [
                                "On the restaurant page, the status line tells customers whether they can order now — for example a green “Open until 11:00 PM” or a closed state with the next opening time. This is only the open/closed cue (plus the usual name / rating / address header), not the ETA or fee chips.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-restaurant-open.jpg", "Open / closed", "Open until … (or closed) on the restaurant page"),
                        },
                        {
                            "h3": "Smart ETA",
                            "paras": [
                                "The ETA chip (for example “ETA 26–36 min”) estimates how long food will take before the customer commits. It is its own cue on the restaurant header — separate from open/closed and from the fee chip. More on how ETA is computed: <a href=\"./intelligence.html\">AI intelligence</a>.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-restaurant-eta.jpg", "ETA", "ETA chip on the restaurant page"),
                        },
                        {
                            "h3": "Delivery fee (standard or surge)",
                            "paras": [
                                "The fee chip sits beside the ETA and shows what delivery costs right now — “Standard fee” in quiet periods, or a surge multiplier when demand is high. Fee / surge is a separate marketplace lever from ETA timing. Details: <a href=\"./intelligence.html\">AI intelligence</a>.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-restaurant-fee.jpg", "Delivery fee", "Fee / surge chip on the restaurant page"),
                        },
                        {
                            "h3": "Offers and reviews on the restaurant",
                            "paras": [
                                "Scrolling the restaurant page reaches Available Offers (discount / free-delivery cards with validity) and Recent Reviews. This is not the global Offers tab — it is the offers block attached to that restaurant.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-restaurant-offers.jpg", "Restaurant offers", "Available Offers cards and Recent Reviews"),
                        },
                        {
                            "h3": "Menu — categories and items",
                            "paras": [
                                "The menu lists categories (Italian, Mediterranean, …) with dish name, short description, price, and a + control. This capture is the catalog itself — not status chips, not offers, not the cart banner.",
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
                                "After an item is added, the menu shows quantity steppers (− / +) on that line and a floating <strong>View Cart</strong> bar (item count + total). The tab-bar cart badge increments too. That is the add-to-cart moment — separate from reviewing the full cart screen.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-add-to-cart.jpg", "Add to cart", "Quantity steppers and View Cart bar on the menu"),
                        },
                    ],
                },
                {
                    "h2": "Cart, offers tab, and checkout",
                    "paras": [
                        "Once items are in the cart, conversion is three distinct screens: the cart list, the dedicated Offers surface, and checkout.",
                    ],
                    "blocks": [
                        {
                            "h3": "Cart — line items and totals",
                            "paras": [
                                "The cart screen lists what the customer will pay for: quantities, extras, and a running total. Change amounts or remove lines here before opening checkout.",
                            ],
                            "steps": [
                                "Open the cart from the tab bar or the View Cart bar.",
                                "Review quantities, extras, and totals.",
                                "Continue to checkout when the basket looks right.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-cart.jpg", "Cart", "Line items, quantities, and totals"),
                        },
                        {
                            "h3": "Offers tab — vouchers to claim",
                            "paras": [
                                "The Offers surface is where customers browse claimable vouchers / campaigns (separate from the small offers block on a restaurant page). Coupon codes and campaign rules are configured in admin — see <a href=\"./admin-app/promotions.html\">Promotions &amp; coupons</a>.",
                            ],
                            "shot": ("phone", f"{A}/features/ordering-offers.jpg", "Offers", "Offers / vouchers list to claim"),
                        },
                        {
                            "h3": "Checkout — address, payment, place order",
                            "paras": [
                                "Checkout confirms fulfillment (delivery vs pickup), the address, and the payment method (card, cash on delivery, wallet, or other gateways you activate). After place order, follow progress in order history / <a href=\"./order-tracking.html\">tracking</a>.",
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
                {
                    "h2": "Order history",
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
                },
            ],
            "./site.css",
            "./js/sidebar-scroll.js",
            "./",
        ),
        encoding="utf-8",
    )

    (ROOT / "delivery-app/earnings.html").write_text(
        page(
            "Earnings & payouts — Driver app",
            "Earnings & payouts",
            "How drivers see today’s money, delivery history, transactions, and where payouts are sent.",
            ["Earnings", "Transactions", "Payouts"],
            [
                {
                    "h2": "Know what a shift paid",
                    "paras": [
                        "Couriers need a clear money picture: what they earned today, what sits in history, and how cash reaches their bank. Job handling, batching, and proof of delivery stay on the logistics screens; this page is the money side of the same role.",
                    ],
                    "blocks": [
                        {
                            "h3": "Earnings overview",
                            "paras": [
                                "Earnings summarizes the shift and periods your build shows — totals the driver can trust after completing deliveries. Open it at the end of a block of jobs to confirm the marketplace recorded the work.",
                            ],
                            "steps": [
                                'Complete deliveries for the shift (see <a href="./logistics.html">Logistics &amp; POD</a>).',
                                "Open <strong>Earnings</strong> to review today’s totals and available periods.",
                            ],
                            "shot": ("phone", f"{A}/features/driver-earnings.jpg", "Earnings", "Driver earnings overview for the shift"),
                        },
                        {
                            "h3": "Transaction history",
                            "paras": [
                                "Transactions are the line-by-line trail: delivery fees, adjustments, and related movements. Use this when a total looks wrong or when support asks for proof of a specific job payout.",
                            ],
                            "shot": ("phone", f"{A}/features/driver-transactions.jpg", "Transactions", "Line-by-line driver transaction history"),
                        },
                        {
                            "h3": "Payout methods",
                            "paras": [
                                "Payout methods tell the platform where to settle the driver (including Connect-style onboarding when you enable it). Drivers should add or update methods before expecting bank transfers — incomplete payout setup is a common “where is my money?” ticket.",
                            ],
                            "steps": [
                                "Open <strong>Payout methods</strong> from the driver money area.",
                                "Add or update the settlement method your marketplace supports.",
                                "Confirm status shows ready before the next payout cycle.",
                            ],
                            "shot": ("phone", f"{A}/features/driver-payouts.jpg", "Payouts", "Where the driver receives settlements"),
                        },
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "restaurant-app/operations.html").write_text(
        page(
            "Orders & menu — Restaurant app",
            "Orders & menu",
            "Day-to-day partner ops: accept or reject orders, manage the menu, set hours, and read analytics — before or beside the Kitchen Display.",
            ["Orders", "Menu", "Hours", "Analytics"],
            [
                {
                    "h2": "Live orders: accept and reject",
                    "paras": [
                        "Incoming orders land in the restaurant orders list in real time. Operators accept or reject, then move the meal through prepare / ready so the driver (or pickup customer) can collect it. New-order alerts can deep-link back to the order so nobody misses a ticket during rush.",
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
                        },
                    ],
                    "shots": [
                        ("phone", f"{A}/features/resto-ops-orders.jpg", "Orders", "Live restaurant orders"),
                    ],
                },
                {
                    "h2": "Menu, hours, and analytics",
                    "paras": [
                        "Partners manage categories, dishes, prices, photos, variants, and availability from the restaurant app — without waiting on admin for every price tweak. Opening hours and delivery / pickup controls define when and how far you sell. Analytics help owners see what is working after a few service days.",
                    ],
                    "blocks": [
                        {
                            "h3": "Menu management",
                            "paras": [
                                "The menu screen is the catalog home: categories and items customers will browse. From here partners add dishes, reorder sections, and keep the sellable list honest for the next rush.",
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
                                "Item forms cover name, price, photo, variants, and availability. Getting this right once prevents “price wrong on the app” tickets and keeps kitchen tickets aligned with what the customer paid for.",
                            ],
                            "shot": ("phone", f"{A}/features/resto-ops-menu-edit.jpg", "Edit item", "Item form: price, photo, variants, availability"),
                        },
                        {
                            "h3": "Opening hours",
                            "paras": [
                                "Opening hours and delivery settings (radius, prep time) tell the customer app when the restaurant is open and how far it delivers. Out-of-date hours create orders you cannot fulfill — fix them before service, not after the first rejection.",
                            ],
                            "shot": ("phone", f"{A}/features/resto-ops-hours.jpg", "Hours", "Opening hours that drive open/closed in the customer app"),
                        },
                        {
                            "h3": "Analytics",
                            "paras": [
                                "Dashboard KPIs and analytics (periods, bestsellers, peaks) help owners see what sells and when. Use them after a few real service days — empty charts on day one are normal; quiet slots and bestsellers appear once orders accumulate.",
                            ],
                            "shot": ("phone", f"{A}/features/resto-ops-analytics.jpg", "Analytics", "Periods, bestsellers, and service peaks"),
                        },
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/operations.html").write_text(
        page(
            "Operations — Admin app",
            "Operations",
            "The day-to-day control room: orders, restaurants, customers, drivers, and the food catalog that powers every mobile app.",
            ["Orders", "Partners", "Catalog", "Users"],
            [
                {
                    "h2": "Orders and partners",
                    "paras": [
                        "Admin is the marketplace command center. Support should investigate from one place without asking three mobile apps for screenshots. Start from dashboard KPIs, then drill into orders and partner accounts.",
                    ],
                    "blocks": [
                        {
                            "h3": "Orders",
                            "paras": [
                                "The orders list shows payment state, customer, restaurant, driver, totals, and fulfillment status. View opens full detail (line items, delivery, timeline) for failed payments, stuck statuses, or missing drivers.",
                            ],
                            "steps": [
                                "Open <strong>Orders</strong> when a live incident starts.",
                                "Filter or find the order by customer / restaurant / id.",
                                "Use View for the full record before changing status or contacting partners.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-ops-orders.jpg", "Orders", "Admin orders list with payment and fulfillment state"),
                        },
                        {
                            "h3": "Restaurants",
                            "paras": [
                                "Restaurant management covers onboarding and ongoing control: activate or close partners, keep profiles consistent with what the customer app displays, and intervene when a location should not stay live.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-ops-restaurants.jpg", "Restaurants", "Approve, edit, activate, or close restaurant partners"),
                        },
                        {
                            "h3": "Drivers",
                            "paras": [
                                "Approve drivers before they go online, keep identity and vehicle details coherent, and suspend when needed. Couriers that skip approval create support noise and marketplace risk.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-ops-drivers.jpg", "Drivers", "Driver onboarding and ongoing control"),
                        },
                        {
                            "h3": "Users (customers)",
                            "paras": [
                                "Customer users are where you investigate accounts, edit profiles, or suspend abuse. Pair this with the orders list when a dispute needs both the person and their tickets.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-ops-users.jpg", "Users", "Customer accounts for support and moderation"),
                        },
                    ],
                },
                {
                    "h2": "Menus and catalog",
                    "paras": [
                        "Categories, menus, products, and variants can be curated centrally when partners need help — or when you seed a new city. What you publish here is what customers browse and what restaurants edit on mobile when you allow dual management.",
                    ],
                    "shots": [
                        ("wide", f"{A}/features/admin-ops-menus.jpg", "Menus", "Admin menus / catalog"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/promotions.html").write_text(
        page(
            "Promotions & coupons — Admin app",
            "Promotions & coupons",
            "How operators run growth campaigns: promotion types, scoping, and coupon codes customers redeem at checkout.",
            ["Promotions", "Coupons", "Campaigns"],
            [
                {
                    "h2": "Grow volume with real campaigns",
                    "paras": [
                        "The promotion engine supports the campaign styles buyers expect: percentage or fixed discounts, free delivery, Buy X Get Y / combos, flash sales, happy hours, and similar types your build exposes. Scope a campaign to the whole platform or to a restaurant, category, or item — and target audiences such as all, new, existing, or VIP when those flags exist.",
                    ],
                    "blocks": [
                        {
                            "h3": "Promotions",
                            "paras": [
                                "Promotions are the campaign objects: type, discount, schedule, and scope. Create or edit here, activate only what you can afford on margin, then verify the offer appears on customer home / restaurant surfaces before you announce it.",
                            ],
                            "steps": [
                                "Open <strong>Promotions</strong> and create or edit a campaign.",
                                "Set type, discount, schedule, and scope (platform / restaurant / category / item).",
                                "Activate, then place a demo customer order to prove the discount applies.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-promotions.jpg", "Promotions", "Campaign list: type, schedule, scope, status"),
                        },
                        {
                            "h3": "Coupons",
                            "paras": [
                                "Coupon codes add constrained redemptions: minimum order, max uses, per-user limits, first-order-only, and expiry. Customers enter codes in cart / checkout — documented under Ordering &amp; discovery. Use coupons when you want a shareable code instead of (or on top of) an automatic promotion.",
                            ],
                            "steps": [
                                "Open <strong>Coupons</strong> and create a code with usage limits.",
                                "Confirm checkout accepts the code on a test order.",
                                "Retire or expire codes that are no longer funded.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-coupons.jpg", "Coupons", "Redeemable codes with limits and expiry"),
                        },
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    (ROOT / "admin-app/reports.html").write_text(
        page(
            "Reports & analytics — Admin app",
            "Reports & analytics",
            "Sales, restaurant, and driver reports so you can prove performance — not guess from a single dashboard card.",
            ["Sales", "Restaurants", "Drivers", "Ledger"],
            [
                {
                    "h2": "Prove what the marketplace earned",
                    "paras": [
                        "Reports turn operational noise into decisions. Use earnings under Monetization for commission splits; use reports when you need period analytics and partner scorecards — sales, restaurant performance, driver performance, and the money ledger.",
                    ],
                    "blocks": [
                        {
                            "h3": "Sales reports",
                            "paras": [
                                "Sales reports cover the period you care about: volume, AOV, delivery fees, taxes collected, and category breakdowns. Start the week here before partner conversations.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-sales-reports.jpg", "Sales reports", "Period sales with fees, taxes, and breakdowns"),
                        },
                        {
                            "h3": "Restaurant reports",
                            "paras": [
                                "Restaurant reports surface partner performance for coaching and commercial talks — who is growing, who is rejecting too much, who needs help with menu or hours.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-resto-reports.jpg", "Restaurant reports", "Partner performance scorecards"),
                        },
                        {
                            "h3": "Driver reports",
                            "paras": [
                                "Driver reports highlight late deliveries, coverage gaps, and top couriers. Use them to staff peaks and to investigate complaints with facts instead of anecdotes.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-driver-reports.jpg", "Driver reports", "Courier performance and reliability"),
                        },
                        {
                            "h3": "Transactions ledger",
                            "paras": [
                                "The transactions ledger is fee-level transparency: payments, payouts, refunds, tips, and wallet movements. Spot-check it when a payout or refund is disputed — before you invent a spreadsheet.",
                            ],
                            "shot": ("wide", f"{A}/features/admin-transactions.jpg", "Transactions", "Money ledger for payments, payouts, refunds"),
                        },
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    spon_img = "assets/images/features/admin-sponsored.jpg"
    if not (ROOT / spon_img).exists():
        spon_img = "assets/images/features/sponsored.jpg"

    (ROOT / "admin-app/sponsored.html").write_text(
        page(
            "Sponsored listings — Admin app",
            "Sponsored listings",
            "How operators oversee paid placement campaigns that restaurants create from their app.",
            ["Oversight", "Campaigns", "Marketplace"],
            [
                {
                    "h2": "Keep paid placement under control",
                    "paras": [
                        "Restaurants create and launch campaigns from the restaurant app. Admin Sponsored listings is the operator view: which campaigns exist, their state, and enough context to intervene if something should not stay live on the customer feed.",
                        "Use this screen together with the restaurant flow — partners self-serve the creative and bid; you keep marketplace hygiene.",
                    ],
                    "blocks": [
                        {
                            "h3": "Operator workflow",
                            "steps": [
                                "Open <strong>Sponsored listings</strong> in admin.",
                                "Review active and past campaigns (restaurant, placement, status).",
                                "Open View when you need campaign detail or to take an admin action your build exposes.",
                                'Cross-check the customer home / search experience and the <a href="../restaurant-app/sponsored.html">restaurant sponsored</a> form so creative and bid match what you expect.',
                            ],
                        },
                    ],
                    "shots": [
                        ("wide", spon_img, "Admin sponsored", "Sponsored listings in admin"),
                    ],
                },
            ],
            "../site.css",
            "../js/sidebar-scroll.js",
            "../",
        ),
        encoding="utf-8",
    )

    print("OK")


if __name__ == "__main__":
    main()
