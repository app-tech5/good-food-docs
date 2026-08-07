/* Docs nav — mobile toggle, collapsible groups, active scroll */
(function () {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    var sidebar = document.querySelector(".sidebar[data-docs-sidebar]");
    if (!sidebar) return;

    // Mobile chrome: toggle + backdrop
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "docs-nav-toggle";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "docs-sidebar");
    toggle.innerHTML =
      '<span class="docs-nav-toggle-bars" aria-hidden="true"></span><span class="docs-nav-toggle-label">Menu</span>';

    var backdrop = document.createElement("div");
    backdrop.className = "sidebar-backdrop";
    backdrop.hidden = true;

    sidebar.id = "docs-sidebar";
    document.body.appendChild(toggle);
    document.body.appendChild(backdrop);

    var closeBtn = sidebar.querySelector(".sidebar-close");

    function setOpen(open) {
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      backdrop.hidden = !open;
    }

    toggle.addEventListener("click", function () {
      setOpen(!document.body.classList.contains("nav-open"));
    });
    backdrop.addEventListener("click", function () {
      setOpen(false);
    });
    if (closeBtn) {
      closeBtn.removeAttribute("hidden");
      closeBtn.addEventListener("click", function () {
        setOpen(false);
      });
    }
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });

    // Accordion: keep one product group open at a time (Suite can stay open)
    var groups = Array.prototype.slice.call(sidebar.querySelectorAll("details.nav-group"));
    groups.forEach(function (group) {
      group.addEventListener("toggle", function () {
        if (!group.open) return;
        var title = group.querySelector(".nav-group-title");
        var isSuite = title && title.textContent.trim() === "Suite";
        if (isSuite) return;
        groups.forEach(function (other) {
          if (other === group) return;
          var ot = other.querySelector(".nav-group-title");
          if (ot && ot.textContent.trim() === "Suite") return;
          other.open = false;
        });
      });
    });

    // Scroll active link into view inside sidebar
    var activeLink = sidebar.querySelector(".nav a.active");
    if (activeLink) {
      var group = activeLink.closest("details.nav-group");
      if (group) group.open = true;
      requestAnimationFrame(function () {
        var body = sidebar.querySelector(".sidebar-body") || sidebar;
        var linkTop = activeLink.offsetTop;
        var linkHeight = activeLink.offsetHeight;
        var view = body.clientHeight;
        body.scrollTo({
          top: Math.max(0, linkTop - view / 2 + linkHeight / 2),
          behavior: "smooth",
        });
      });
    }
  });
})();
