/* Shared chrome for buyer docs — requires window.DOCS_NAV + window.DOCS_BASE */
(function () {
  const base = (window.DOCS_BASE || "./").replace(/\/?$/, "/");
  const path = (window.DOCS_PATH || "index.html").replace(/^\.\//, "");
  const nav = window.DOCS_NAV || [];

  function href(to) {
    return base + to.replace(/^\.\//, "");
  }

  function findTitle() {
    for (const section of nav) {
      for (const item of section.items || []) {
        if (item.href === path) return item.label;
      }
    }
    const h1 = document.querySelector(".doc h1");
    return h1 ? h1.textContent.trim() : "Documentation";
  }

  const aside = document.createElement("aside");
  aside.className = "sidebar";
  aside.innerHTML =
    '<a class="brand" href="' +
    href("index.html") +
    '">Good Food Pro<span>Buyer documentation</span></a>' +
    nav
      .map(function (section) {
        return (
          '<div class="nav-section"><h2>' +
          section.title +
          "</h2>" +
          (section.items || [])
            .map(function (item) {
              const active = item.href === path ? " is-active" : "";
              return (
                '<a class="' +
                active.trim() +
                '" href="' +
                href(item.href) +
                '">' +
                item.label +
                "</a>"
              );
            })
            .join("") +
          "</div>"
        );
      })
      .join("");

  const article = document.querySelector("article.doc");
  if (!article) return;

  const layout = document.createElement("div");
  layout.className = "layout";

  const main = document.createElement("div");
  main.className = "main";

  const topbar = document.createElement("div");
  topbar.className = "topbar";
  topbar.innerHTML =
    '<button type="button" class="menu-toggle" aria-label="Open menu">Menu</button>' +
    '<div class="crumb">Docs / <strong></strong></div>';
  topbar.querySelector("strong").textContent = findTitle();

  const content = document.createElement("div");
  content.className = "content";

  const footer = document.createElement("p");
  footer.className = "doc-footer";
  footer.innerHTML =
    '<a href="' + href("index.html") + '">← Documentation home</a>';

  const backdrop = document.createElement("div");
  backdrop.className = "sidebar-backdrop";

  const parent = article.parentNode;
  parent.insertBefore(layout, article);
  layout.appendChild(aside);
  layout.appendChild(main);
  main.appendChild(topbar);
  main.appendChild(content);
  content.appendChild(article);
  content.appendChild(footer);
  document.body.appendChild(backdrop);

  function closeNav() {
    document.body.classList.remove("nav-open");
  }
  function toggleNav() {
    document.body.classList.toggle("nav-open");
  }
  topbar.querySelector(".menu-toggle").addEventListener("click", toggleNav);
  backdrop.addEventListener("click", closeNav);
  aside.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", closeNav);
  });
})();
