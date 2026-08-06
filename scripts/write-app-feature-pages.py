#!/usr/bin/env python3
"""Write feature pages under each app (customer / driver / restaurant / admin)."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path("/Users/nass/Documents/good-food-docs")
A = "assets/images"
SS = Path("/Users/nass/Documents/good-foods-description/img/pro/screenshots")


def page(title, h1, subtitle, pills, sections, css_href, js_href, img_prefix):
    pills_html = "\n".join(f'            <span class="meta-pill">{p}</span>' for p in pills)
    section_html = []
    for h2, paras, shots in sections:
        parts = [f'          <section class="section-block">\n            <h2>{h2}</h2>']
        for i, p in enumerate(paras):
            cls = "" if i == 0 else ' class="section-subtext"'
            parts.append(f"            <p{cls}>\n              {p}\n            </p>")
        if shots:
            phones = [s for s in shots if s[0] == "phone"]
            wides = [s for s in shots if s[0] == "wide"]
            if phones:
                parts.append('            <div class="shot-grid phones">')
                for _, src, alt, cap in phones:
                    parts.append(
                        f"""              <div class="shot phone">
                <img src="{img_prefix}{src}" alt="{alt}" />
                <p>{cap}</p>
              </div>"""
                    )
                parts.append("            </div>")
            if wides:
                style = ' style="margin-top: 12px;"' if phones else ""
                parts.append(f'            <div class="shot-grid"{style}>')
                for _, src, alt, cap in wides:
                    parts.append(
                        f"""              <div class="shot wide">
                <img src="{img_prefix}{src}" alt="{alt}" />
                <p>{cap}</p>
              </div>"""
                    )
                parts.append("            </div>")
        parts.append("          </section>")
        section_html.append("\n".join(parts))

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="{css_href}" />
  </head>
  <body>
    <script src="{js_href}"></script>
    <main class="layout">
      <aside class="sidebar" data-docs-sidebar></aside>
      <section class="content">
        <header id="top" class="hero">
          <h1>{h1}</h1>
          <p class="subtitle">
            {subtitle}
          </p>
          <div class="meta-strip">
{pills_html}
          </div>
        </header>

        <section class="overview">
{chr(10).join(section_html)}
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
            "A balance customers like to keep topped up — plus cards on file and smoother refunds when you enable them.",
            ["Wallet", "Top up", "Payment methods"],
            [
                (
                    "A wallet that brings people back",
                    [
                        "A wallet turns one-off checkout into a relationship. Customers see their balance, add money when they need to, and keep a card under payment methods. Cashback-style rewards and smoother refunds (when you enable them) make the balance feel useful — not like a dead prepaid card.",
                        'From the customer app, the flow is simple: open Wallet, check the balance, tap Add Money, pay. Operators configure related flags and gateways from the <a href="./admin-app/monetization.html">admin monetization</a> screens.',
                    ],
                    [
                        ("phone", f"{A}/features/wallet.jpg", "Customer wallet", "Wallet — balance and payment methods"),
                        ("phone", f"{A}/features/wallet-topup.jpg", "Add money", "Top up the balance"),
                    ],
                ),
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
            "Member plans for free delivery and offers — recurring value that keeps customers opening the app.",
            ["Member plans", "Free delivery", "Renewals"],
            [
                (
                    "Plans customers can subscribe to",
                    [
                        'Offer monthly (or other) plans with benefits such as free delivery or member-only offers. Customers pick a plan in the app; you create and edit tiers in <a href="./admin-app/monetization.html">admin monetization</a> (target: customer, price, billing cycle, benefits).',
                        "Recurring membership sits next to order revenue — still useful when weekday volume dips.",
                    ],
                    [
                        ("phone", f"{A}/features/sub-customer.jpg", "Customer subscription plans", "Customer — choose a membership plan"),
                    ],
                ),
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
            "Smarter carts, clearer arrival times, and fees that flex when the city gets hungry — right in the customer experience.",
            ["Recommendations", "Smart ETA", "Surge"],
            [
                (
                    "Recommendations that grow the order",
                    [
                        "Suggestions surface sides, drinks, and extras that fit past orders, time of day, and even the weather. The “Recommended for you” block explains why — natural add-to-cart, higher average order value.",
                    ],
                    [("phone", f"{A}/features/ai-reco.jpg", "Recommendations", "Recommended for you")],
                ),
                (
                    "Arrival times customers trust",
                    [
                        "Smart ETA looks at kitchen load and travel time. Clearer arrivals mean fewer “where is my food?” messages.",
                    ],
                    [("phone", f"{A}/features/ai-eta.jpg", "ETA badges", "ETA on discovery")],
                ),
                (
                    "Surge when demand spikes",
                    [
                        "When everyone orders at once and drivers are scarce, delivery fees can flex automatically. Quiet hours stay friendly; peaks stay fair.",
                    ],
                    [("phone", f"{A}/features/ai-surge.jpg", "Surge", "Surge at checkout")],
                ),
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
            "From pending to delivered — customers follow the order without calling support.",
            ["Live status", "ETA", "Map context"],
            [
                (
                    "Follow the order to the door",
                    [
                        "After checkout, customers watch status move from pending to preparing, out for delivery, and delivered — with ETA when available. That transparency cuts support tickets and creates the wow moment that makes someone order again.",
                        'Nearby map views help before and during the order. Driver-side logistics and proof of delivery live in the <a href="./delivery-app/logistics.html">delivery app docs</a>.',
                    ],
                    [
                        ("phone", f"{A}/features/tracking.jpg", "Track order", "Track order — status steps"),
                        ("phone", f"{A}/features/map-nearby.jpg", "Map nearby", "Map — nearby places"),
                    ],
                ),
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
            "Batching, live jobs, and proof at the door — the last mile in the driver app.",
            ["Batching", "Active delivery", "Photo + signature"],
            [
                (
                    "Fewer empty miles",
                    [
                        "At lunch peak, one bag across town burns time. Batching and a clear deliveries list help couriers stack nearby drops. Assignment radius is configured with delivery settings on the restaurant / admin side.",
                    ],
                    [
                        ("phone", f"{A}/features/driver-deliveries.jpg", "Deliveries", "Today’s deliveries"),
                        ("phone", f"{A}/features/delivery-settings.jpg", "Settings", "Delivery settings / radius"),
                    ],
                ),
                (
                    "On the road",
                    [
                        'Drivers open an active job, see customer details, and navigate. Customers follow progress in the <a href="../order-tracking.html">customer order tracking</a> screens.',
                    ],
                    [
                        ("phone", f"{A}/features/driver-active.jpg", "Active", "Active delivery"),
                        ("phone", f"{A}/features/driver-details.jpg", "Details", "Delivery details"),
                    ],
                ),
                (
                    "Proof of delivery",
                    [
                        "At the door, capture a photo and customer signature. Cash-on-delivery and high-value meals suddenly have evidence when “I never got it” used to win.",
                    ],
                    [("phone", f"{A}/features/driver-pod.jpg", "POD", "Photo + signature")],
                ),
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
            "Driver plans for access and priority — membership that rewards the couriers who keep your SLA honest.",
            ["Driver plans", "Priority", "Renewals"],
            [
                (
                    "Plans for couriers",
                    [
                        'Drivers subscribe to tiers from the driver app. You define those tiers in <a href="../admin-app/monetization.html">admin monetization</a> with target “driver”, price, and benefits.',
                    ],
                    [("phone", f"{A}/features/sub-driver.jpg", "Driver plans", "Driver — choose a plan")],
                ),
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
            "Paperless tickets for the line — accept in orders, cook on the board, hand off to the driver.",
            ["Tickets", "Status flow", "Tablet ready"],
            [
                (
                    "From accept to ready for pickup",
                    [
                        "Once staff accept an order, the Kitchen Display focuses on tickets: what to cook, what is in progress, what is ready. Large controls suit a tablet on the pass. The same order still feeds admin and the driver app.",
                    ],
                    [("phone", f"{A}/features/kds.jpg", "KDS", "Kitchen Display tickets")],
                ),
                (
                    "Tied to live orders",
                    [
                        "Orders land in the restaurant list first; then the kitchen board keeps the line moving without hunting paper slips.",
                    ],
                    [
                        ("phone", f"{A}/features/resto-orders.jpg", "Orders", "Live orders"),
                        ("phone", f"{A}/features/resto-drawer.jpg", "Drawer", "Open KDS from the menu"),
                    ],
                ),
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
            "Restaurant plans for better rates, visibility, and SaaS-style access — sold from the partner app.",
            ["Restaurant plans", "Commission relief", "Renewals"],
            [
                (
                    "Plans partners will pay for",
                    [
                        'Restaurants subscribe to Pro or SaaS-style access from their app. Lower commission, sponsored eligibility, priority support — configured as tiers in <a href="../admin-app/monetization.html">admin monetization</a>.',
                    ],
                    [("phone", f"{A}/features/sub-restaurant.jpg", "Restaurant plans", "Restaurant — subscribe")],
                ),
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
            "Restaurants bid for search or home placement — campaigns they launch themselves.",
            ["Campaigns", "Bid", "Placement"],
            [
                (
                    "Buy the spotlight",
                    [
                        "Partners create a campaign: headline, daily bid, placement (search top, home banner, or both), then launch. The customer feed stays polished; restaurants pay for attention.",
                        'Operators monitor campaigns from <a href="../admin-app/sponsored.html">admin sponsored listings</a>.',
                    ],
                    [("phone", f"{A}/features/sponsored.jpg", "Sponsored form", "Launch a campaign")],
                ),
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
            "Commissions, subscription tiers, earnings splits, and payment gateways — the money control room.",
            ["Commissions", "Subscriptions", "Earnings", "Gateways"],
            [
                (
                    "Commissions and earnings",
                    [
                        "Set the platform cut, tune per restaurant when needed, and reward stronger subscription plans with a lower rate. Earnings views show platform vs restaurant splits ready for payouts.",
                    ],
                    [("wide", f"{A}/features/earnings.jpg", "Earnings", "Earnings — platform vs restaurant")],
                ),
                (
                    "Subscription tiers for every role",
                    [
                        "Create plans for customers, drivers, and restaurants: price, billing cycle, benefits. Each mobile app shows the matching subscribe screen.",
                    ],
                    [("wide", f"{A}/features/admin-subscriptions.jpg", "Admin subscriptions", "Admin — manage subscription tiers")],
                ),
                (
                    "Payment gateways",
                    [
                        'Configure cards and regional PSPs so checkout and wallet top-ups match each market. Customer-facing wallet screens are documented under the <a href="../wallet.html">customer app</a>.',
                    ],
                    [("wide", f"{A}/features/gateways.jpg", "Gateways", "Payment gateways")],
                ),
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
            "Languages, currencies, and marketplace settings so each city feels local.",
            ["Languages", "Currencies", "Settings"],
            [
                (
                    "Languages",
                    [
                        "Enable English, French, Spanish, and Arabic (with RTL where needed). Set the default; mobile apps follow the user’s choice in settings.",
                    ],
                    [
                        ("wide", f"{A}/features/languages.jpg", "Languages", "Admin languages"),
                        ("phone", f"{A}/features/lang-picker.jpg", "Picker", "Customer language picker"),
                    ],
                ),
                (
                    "Currencies",
                    [
                        "Menus, carts, wallets, and reports follow the currency you configure. Change the default when you expand.",
                    ],
                    [("wide", f"{A}/features/currencies.jpg", "Currencies", "Admin currencies")],
                ),
                (
                    "Marketplace settings",
                    [
                        "App settings hold marketplace behaviour in one place — including hooks that support hybrid channels and regional defaults.",
                    ],
                    [("wide", f"{A}/features/app-settings.jpg", "Settings", "App settings")],
                ),
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
            "Oversee paid placement campaigns restaurants launch from their app.",
            ["Campaigns", "Visibility", "Oversight"],
            [
                (
                    "Monitor sponsored campaigns",
                    [
                        'Restaurants create campaigns in the <a href="../restaurant-app/sponsored.html">restaurant app</a>. From admin you keep oversight of what is live on the marketplace — so paid placement stays controlled.',
                    ],
                    [("wide", spon_img, "Admin sponsored", "Admin — sponsored listings")],
                ),
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
