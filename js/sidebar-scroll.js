window.addEventListener("load", () => {
  const sidebar = document.querySelector(".sidebar");
  if (!sidebar) return;

  const activeLink = sidebar.querySelector(".nav a.active");
  if (!activeLink) return;

  const linkTop = activeLink.offsetTop;
  const linkHeight = activeLink.offsetHeight;
  const sidebarHeight = sidebar.clientHeight;

  sidebar.scrollTo({
    top: linkTop - sidebarHeight / 2 + linkHeight / 2,
    behavior: "smooth",
  });
});
