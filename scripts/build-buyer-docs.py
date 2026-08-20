#!/usr/bin/env python3
"""Build good-food-docs/documentation from source-docs Markdown.

- Content is converted 1:1 (no wording changes)
- One shared CSS + JS chrome (sidebar injected at runtime)
- Pretty root names: README→index, 00-launch-suite→launch, environment-config→environment
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source-docs"
DEST = ROOT / "documentation"
ASSETS_SRC = Path(__file__).resolve().parent / "buyer-docs-assets"

# Prefer assets already under documentation/assets (edited in place)
ASSETS_DIR = DEST / "assets"

HTML_NAME = {
    "README.md": "index.html",
    "00-launch-suite.md": "launch.html",
    "environment-config.md": "environment.html",
}

# Sidebar order & labels (hrefs relative to documentation/)
NAV = [
    {
        "title": "Start here",
        "items": [
            {"label": "Home", "href": "index.html"},
            {"label": "Launch the suite", "href": "launch.html"},
            {"label": "Environment & branding", "href": "environment.html"},
        ],
    },
    {
        "title": "Backend",
        "items": [
            {"label": "Getting started", "href": "my-backend/getting-started.html"},
            {"label": "Order lifecycle", "href": "my-backend/order-lifecycle.html"},
            {"label": "Live updates", "href": "my-backend/live-updates.html"},
            {"label": "Payments & wallet", "href": "my-backend/payments-wallet.html"},
            {"label": "Commission engine", "href": "my-backend/commission-engine.html"},
            {"label": "Subscriptions engine", "href": "my-backend/subscriptions-engine.html"},
            {"label": "Intelligence engine", "href": "my-backend/intelligence-engine.html"},
            {"label": "Logistics engine", "href": "my-backend/logistics-engine.html"},
            {"label": "Channels API", "href": "my-backend/channels-api.html"},
            {"label": "Market data", "href": "my-backend/market-data.html"},
            {"label": "Catalog API", "href": "my-backend/catalog-api.html"},
        ],
    },
    {
        "title": "Customer app",
        "items": [
            {"label": "Getting started", "href": "customer-app/getting-started.html"},
            {"label": "Discovery", "href": "customer-app/discovery.html"},
            {"label": "Restaurant page", "href": "customer-app/restaurant-page.html"},
            {"label": "Menu & cart", "href": "customer-app/menu-cart.html"},
            {"label": "Checkout", "href": "customer-app/checkout.html"},
            {"label": "Order history", "href": "customer-app/order-history.html"},
            {"label": "Order tracking", "href": "customer-app/order-tracking.html"},
            {"label": "Wallet", "href": "customer-app/wallet.html"},
            {"label": "Subscriptions", "href": "customer-app/subscriptions.html"},
            {"label": "Recommendations", "href": "customer-app/recommendations.html"},
            {"label": "Smart ETA", "href": "customer-app/smart-eta.html"},
            {"label": "Delivery fee", "href": "customer-app/delivery-fee.html"},
            {"label": "Languages & RTL", "href": "customer-app/languages-rtl.html"},
            {"label": "Intelligence (index)", "href": "customer-app/intelligence.html"},
        ],
    },
    {
        "title": "Delivery app",
        "items": [
            {"label": "Getting started", "href": "delivery-app/getting-started.html"},
            {"label": "Deliveries", "href": "delivery-app/deliveries.html"},
            {"label": "Active delivery", "href": "delivery-app/active-delivery.html"},
            {"label": "Proof of delivery", "href": "delivery-app/proof-of-delivery.html"},
            {"label": "Earnings", "href": "delivery-app/earnings.html"},
            {"label": "Transactions & payouts", "href": "delivery-app/transactions-payouts.html"},
            {"label": "Subscriptions", "href": "delivery-app/subscriptions.html"},
            {"label": "Languages", "href": "delivery-app/languages.html"},
            {"label": "Logistics (index)", "href": "delivery-app/logistics.html"},
        ],
    },
    {
        "title": "Restaurant app",
        "items": [
            {"label": "Getting started", "href": "restaurant-app/getting-started.html"},
            {"label": "Orders", "href": "restaurant-app/orders.html"},
            {"label": "Menu", "href": "restaurant-app/menu.html"},
            {"label": "Hours", "href": "restaurant-app/hours.html"},
            {"label": "Analytics", "href": "restaurant-app/analytics.html"},
            {"label": "Kitchen display", "href": "restaurant-app/kitchen-display.html"},
            {"label": "Subscriptions", "href": "restaurant-app/subscriptions.html"},
            {"label": "Sponsored", "href": "restaurant-app/sponsored.html"},
            {"label": "Languages", "href": "restaurant-app/languages.html"},
        ],
    },
    {
        "title": "Admin app",
        "items": [
            {"label": "Getting started", "href": "admin-app/getting-started.html"},
            {"label": "Orders", "href": "admin-app/orders.html"},
            {"label": "Partners", "href": "admin-app/partners.html"},
            {"label": "Catalog", "href": "admin-app/catalog.html"},
            {"label": "Earnings", "href": "admin-app/earnings.html"},
            {"label": "Subscriptions", "href": "admin-app/subscriptions.html"},
            {"label": "Gateways", "href": "admin-app/gateways.html"},
            {"label": "Stripe", "href": "admin-app/gateway-stripe.html"},
            {"label": "PayPal", "href": "admin-app/gateway-paypal.html"},
            {"label": "Flutterwave", "href": "admin-app/gateway-flutterwave.html"},
            {"label": "Paystack", "href": "admin-app/gateway-paystack.html"},
            {"label": "OrangePay", "href": "admin-app/gateway-orangepay.html"},
            {"label": "Razorpay", "href": "admin-app/gateway-razorpay.html"},
            {"label": "Cash on delivery", "href": "admin-app/gateway-cod.html"},
            {"label": "Wallet", "href": "admin-app/gateway-wallet.html"},
            {"label": "Crypto", "href": "admin-app/gateway-crypto.html"},
            {"label": "Promotions", "href": "admin-app/promotions.html"},
            {"label": "Coupons", "href": "admin-app/coupons.html"},
            {"label": "Languages", "href": "admin-app/languages.html"},
            {"label": "Currencies & taxes", "href": "admin-app/currencies-taxes.html"},
            {"label": "App settings", "href": "admin-app/app-settings.html"},
            {"label": "Order channels", "href": "admin-app/order-channels.html"},
            {"label": "Sponsored", "href": "admin-app/sponsored.html"},
            {"label": "Sales reports", "href": "admin-app/sales-reports.html"},
            {"label": "Partner reports", "href": "admin-app/partner-reports.html"},
            {"label": "Transactions", "href": "admin-app/transactions.html"},
            {"label": "Monetization (index)", "href": "admin-app/monetization.html"},
            {"label": "Market (index)", "href": "admin-app/market.html"},
        ],
    },
]

SEP_RE = re.compile(r"^\|?[\s:\-|]+\|?$")


def norm(p: Path | str) -> str:
    return str(p).replace("\\", "/")


def html_out_for(rel: Path) -> str:
    key = norm(rel)
    if key in HTML_NAME:
        return HTML_NAME[key]
    return norm(rel.with_suffix(".html"))


def rel_href(from_html: str, to_html: str) -> str:
    from_dir = Path(from_html).parent
    target = Path(to_html)
    try:
        return norm(target.relative_to(from_dir if str(from_dir) != "." else Path(".")))
    except ValueError:
        start = Path(from_html).parent.resolve()
        # Use pure path math without resolve against missing files
        from_parts = Path(from_html).parent.parts
        to_parts = Path(to_html).parts
        # relative from from_dir to to
        ups = [".."] * len(from_parts)
        return "/".join(ups + list(to_parts)) if ups else "/".join(to_parts)


def path_rel(from_file: str, to_file: str) -> str:
    """Relative URL from from_file to to_file (both posix paths from dest root)."""
    a = Path(from_file).parent.parts
    b = Path(to_file).parts
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    ups = [".."] * (len(a) - i)
    downs = list(b[i:])
    return "/".join(ups + downs) if ups or downs else Path(to_file).name


def md_link(href: str, text_escaped: str, current_md: Path, current_html: str) -> str:
    if href.endswith(".md") and not href.startswith(("http://", "https://", "mailto:")):
        target = (current_md.parent / href).resolve()
        try:
            rel = target.relative_to(SRC.resolve())
            to_html = html_out_for(rel)
            href = path_rel(current_html, to_html)
        except ValueError:
            pass
    return f'<a href="{html.escape(str(href))}">{text_escaped}</a>'


def format_inline(text: str, current_md: Path, current_html: str) -> str:
    def link(m: re.Match[str]) -> str:
        return md_link(m.group(2), html.escape(m.group(1)), current_md, current_html)

    def bold_link(m: re.Match[str]) -> str:
        return "<strong>" + link(m) + "</strong>"

    # **[label](href)** must be handled before plain links / bold split
    text = re.sub(r"\*\*\[([^\]]+)\]\(([^)]+)\)\*\*", bold_link, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    parts = re.split(r"(<a\s[^>]*>.*?</a>|<strong>.*?</strong>)", text)
    out: list[str] = []
    for part in parts:
        if part.startswith(("<a ", "<strong>")):
            out.append(part)
            continue
        part = html.escape(part)
        part = re.sub(r"`([^`]+)`", r"<code>\1</code>", part)
        part = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", part)
        out.append(part)
    return "".join(out)


def convert_body(md_path: Path, current_html: str) -> tuple[str, str]:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    list_type: str | None = None
    title = md_path.stem.replace("-", " ").title()

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    while i < len(lines):
        line = lines[i]

        if in_code:
            if line.strip().startswith("```"):
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                in_code = False
                code_lines = []
            else:
                code_lines.append(line)
            i += 1
            continue

        if line.strip().startswith("```"):
            close_list()
            in_code = True
            i += 1
            continue

        if not line.strip():
            close_list()
            i += 1
            continue

        if line.startswith("#"):
            close_list()
            level = len(line) - len(line.lstrip("#"))
            heading = line[level:].strip()
            if level == 1 and title == md_path.stem.replace("-", " ").title():
                title = heading
            lvl = min(level, 3)
            out.append(f"<h{lvl}>{format_inline(heading, md_path, current_html)}</h{lvl}>")
            i += 1
            continue

        if re.match(r"^---+\s*$", line):
            close_list()
            out.append("<hr/>")
            i += 1
            continue

        if line.startswith(">"):
            close_list()
            out.append(
                f"<blockquote><p>{format_inline(line.lstrip('> ').strip(), md_path, current_html)}</p></blockquote>"
            )
            i += 1
            continue

        if "|" in line and i + 1 < len(lines) and SEP_RE.match(lines[i + 1].strip()):
            close_list()
            rows = [line]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(lines[i])
                i += 1
            out.append("<table>")
            for ri, row in enumerate(rows):
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                tag = "th" if ri == 0 else "td"
                out.append(
                    "<tr>"
                    + "".join(
                        f"<{tag}>{format_inline(c, md_path, current_html)}</{tag}>" for c in cells
                    )
                    + "</tr>"
                )
            out.append("</table>")
            continue

        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            _, bullet, content = m.groups()
            tag = "ol" if bullet[0].isdigit() else "ul"
            if list_type != tag:
                close_list()
                out.append(f"<{tag}>")
                list_type = tag
            out.append(f"<li>{format_inline(content, md_path, current_html)}</li>")
            i += 1
            continue

        close_list()
        out.append(f"<p>{format_inline(line, md_path, current_html)}</p>")
        i += 1

    close_list()
    if in_code and code_lines:
        out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
    return title, "".join(out)


def wrap_page(title: str, body: str, current_html: str) -> str:
    depth = len(Path(current_html).parts) - 1
    base = "../" * depth if depth else "./"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} — Good Food Pro</title>
  <link rel="stylesheet" href="{base}assets/docs.css" />
</head>
<body>
  <article class="doc">
{body}
  </article>
  <script>window.DOCS_BASE = "{base}"; window.DOCS_PATH = "{html.escape(current_html)}";</script>
  <script src="{base}assets/nav-data.js"></script>
  <script src="{base}assets/docs.js"></script>
</body>
</html>
"""


def clean_source_docs_html() -> None:
    """Remove previous inline HTML experiments from source-docs (Markdown stays)."""
    for p in SRC.rglob("*"):
        if p.suffix.lower() in {".html", ".txt"} and p.name in {
            "index.html",
            "launch.html",
            "environment.html",
            "environment-config.html",
            "00-launch-suite.html",
            "getting-started.html",
            "OPEN-ME.txt",
        }:
            p.unlink(missing_ok=True)


def build() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"Missing source-docs: {SRC}")

    # Keep CSS/JS; wipe generated HTML pages only
    if DEST.exists():
        for p in DEST.rglob("*.html"):
            p.unlink()
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure CSS/JS exist (already written next to this build)
    if not (ASSETS_DIR / "docs.css").exists():
        raise SystemExit(f"Missing {ASSETS_DIR / 'docs.css'}")
    if not (ASSETS_DIR / "docs.js").exists():
        raise SystemExit(f"Missing {ASSETS_DIR / 'docs.js'}")

    (ASSETS_DIR / "nav-data.js").write_text(
        "window.DOCS_NAV = " + json.dumps(NAV, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    md_files = sorted(SRC.rglob("*.md"))
    count = 0
    for md in md_files:
        rel = md.relative_to(SRC)
        current_html = html_out_for(rel)
        title, body = convert_body(md, current_html)
        page = wrap_page(title, body, current_html)
        out = DEST / current_html
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        count += 1

    (DEST / "OPEN-ME.txt").write_text(
        """Good Food Pro — Documentation
================================

Open index.html in your browser.
Markdown sources live in ../source-docs/ (same content).
""",
        encoding="utf-8",
    )

    clean_source_docs_html()
    print(f"Built {count} HTML pages → {DEST}")


if __name__ == "__main__":
    build()
