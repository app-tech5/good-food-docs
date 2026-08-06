#!/usr/bin/env python3
"""Inject shared sidebar into all Good Food Pro docs HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/nass/Documents/good-food-docs")

FEATURES = [
    ("monetization.html", "Monetization"),
    ("market-adaptability.html", "Market adaptability"),
    ("kitchen-display.html", "Kitchen Display (KDS)"),
    ("logistics.html", "Logistics & POD"),
    ("intelligence.html", "AI intelligence"),
]


def rel_prefix(html_path: Path) -> str:
    depth = len(html_path.relative_to(ROOT).parts) - 1
    if depth <= 0:
        return "./"
    return "../" * depth


def features_block(prefix: str, active_file: str | None) -> str:
    links = []
    for fname, label in FEATURES:
        href = f"{prefix}features/{fname}"
        cls = ' class="active"' if active_file == fname else ""
        links.append(f'          <a{cls} href="{href}">{label}</a>')
    return (
        '        <p class="sidebar-label">Platform features</p>\n'
        '        <nav class="nav">\n'
        + "\n".join(links)
        + "\n        </nav>\n"
    )


def build_sidebar(html_path: Path) -> str:
    prefix = rel_prefix(html_path)
    rel = html_path.relative_to(ROOT).as_posix()
    active_feature = html_path.name if html_path.parent.name == "features" else None

    def link(href: str, label: str, active: bool = False) -> str:
        cls = ' class="active"' if active else ""
        return f'          <a{cls} href="{href}">{label}</a>'

    # Resolve active flags
    is_env = rel == "environment-setup.html"
    is_dl = rel.startswith("downloads/")
    is_cust_ov = rel == "index.html"
    is_cust_gs = rel == "getting-started.html"
    is_drv_ov = rel == "delivery-app/index.html"
    is_drv_gs = rel == "delivery-app/getting-started.html"
    is_res_ov = rel == "restaurant-app/index.html"
    is_res_gs = rel == "restaurant-app/getting-started.html"
    is_adm_ov = rel == "admin-app/index.html"
    is_adm_gs = rel == "admin-app/getting-started.html"
    is_be_ov = rel == "my-backend/index.html"
    is_be_gs = rel == "my-backend/getting-started.html"

    # Customer overview/getting-started use #overview or relative links when on those pages
    cust_ov_href = f"{prefix}index.html" if not is_cust_ov else "#overview"
    cust_gs_href = f"{prefix}getting-started.html"
    drv_ov = f"{prefix}delivery-app/index.html" if not is_drv_ov else "#overview"
    drv_gs = f"{prefix}delivery-app/getting-started.html"
    res_ov = f"{prefix}restaurant-app/index.html" if not is_res_ov else "#overview"
    res_gs = f"{prefix}restaurant-app/getting-started.html"
    adm_ov = f"{prefix}admin-app/index.html" if not is_adm_ov else "#overview"
    adm_gs = f"{prefix}admin-app/getting-started.html"
    be_ov = f"{prefix}my-backend/index.html" if not is_be_ov else "#overview"
    be_gs = f"{prefix}my-backend/getting-started.html"

    lines = [
        f'        <a class="brand-link" href="{prefix}index.html" aria-label="Good Food Pro Docs home">',
        '          <span class="brand-dot" aria-hidden="true"></span>',
        '          <span class="brand-title">Good Food Pro Docs</span>',
        "        </a>",
        '        <p class="sidebar-label">All apps</p>',
        '        <nav class="nav">',
        link(f"{prefix}environment-setup.html", "Environment setup", is_env),
        link(f"{prefix}downloads/index.html", "Android downloads", is_dl and rel == "downloads/index.html"),
        "        </nav>",
        features_block(prefix, active_feature).rstrip("\n"),
        '        <p class="sidebar-label">Customer app</p>',
        '        <nav class="nav">',
        link(cust_ov_href, "Overview", is_cust_ov),
        link(cust_gs_href, "Getting Started", is_cust_gs),
        "        </nav>",
        '        <p class="sidebar-label">Delivery app (driver)</p>',
        '        <nav class="nav">',
        link(drv_ov, "Overview", is_drv_ov),
        link(drv_gs, "Getting Started", is_drv_gs),
        "        </nav>",
        '        <p class="sidebar-label">Restaurant app</p>',
        '        <nav class="nav">',
        link(res_ov, "Overview", is_res_ov),
        link(res_gs, "Getting Started", is_res_gs),
        "        </nav>",
        '        <p class="sidebar-label">Admin app (web)</p>',
        '        <nav class="nav">',
        link(adm_ov, "Overview", is_adm_ov),
        link(adm_gs, "Getting Started", is_adm_gs),
        "        </nav>",
        '        <p class="sidebar-label">Backend (API)</p>',
        '        <nav class="nav">',
        link(be_ov, "Overview", is_be_ov),
        link(be_gs, "Getting Started", is_be_gs),
        "        </nav>",
    ]
    return "\n".join(lines) + "\n"


SIDEBAR_RE = re.compile(
    r"(<aside class=\"sidebar\"[^>]*>)(.*?)(</aside>)",
    re.DOTALL,
)


def patch_file(html_path: Path) -> bool:
    text = html_path.read_text(encoding="utf-8")
    sidebar = build_sidebar(html_path)
    m = SIDEBAR_RE.search(text)
    if not m:
        print("NO SIDEBAR", html_path)
        return False
    # Preserve opening tag; replace inner content
    new = text[: m.start(2)] + "\n" + sidebar + "      " + text[m.end(2) :]
    # Ensure data attribute for future scripts
    new = new.replace('<aside class="sidebar">', '<aside class="sidebar" data-docs-sidebar>', 1)
    if new != text:
        html_path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if patch_file(path):
            changed += 1
            print("updated", path.relative_to(ROOT))
    print(f"done, changed={changed}")


if __name__ == "__main__":
    main()
