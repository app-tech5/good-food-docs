window.addEventListener("load", () => {
    const sidebar = document.querySelector(".sidebar");
    const activeLink = sidebar.querySelector(".nav a.active");

    if (sidebar && activeLink) {
      const linkTop = activeLink.offsetTop;
      const linkHeight = activeLink.offsetHeight;
      const sidebarHeight = sidebar.clientHeight;

      sidebar.scrollTo({
        top: linkTop - sidebarHeight / 2 + linkHeight / 2,
        behavior: "smooth"
      });
    }
  });