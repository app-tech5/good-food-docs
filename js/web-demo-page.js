window.addEventListener("DOMContentLoaded", () => {
  const config = window.GOOD_FOOD_WEB_DEMO_CONFIG;
  if (!config) return;

  const demoUrl = String(config.demoUrl || "").trim();
  if (!demoUrl) return;

  const isMobile = /Android|iPhone|iPad|iPod|Mobile|webOS|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent || ""
  );

  // Phones/tablets open the web demo directly. Desktops stay on the QR page.
  if (isMobile) {
    window.location.replace(demoUrl);
    return;
  }

  const qrBase = "https://api.qrserver.com/v1/create-qr-code/";
  const qrUrl = `${qrBase}?size=360x360&data=${encodeURIComponent(demoUrl)}`;

  const setText = (selector, value) => {
    const element = document.querySelector(selector);
    if (element) element.textContent = value;
  };

  setText("[data-app-name]", config.appName);
  setText("[data-page-title]", config.pageTitle);
  setText("[data-page-subtitle]", config.pageSubtitle);
  setText("[data-qr-label]", config.qrLabel);
  setText("[data-demo-path]", config.demoPath || demoUrl);

  const qrImage = document.querySelector("[data-qr-image]");
  if (qrImage) qrImage.setAttribute("src", qrUrl);

  const tipsList = document.querySelector("[data-tips-list]");
  if (tipsList && Array.isArray(config.tips)) {
    tipsList.innerHTML = "";
    config.tips.forEach((tip) => {
      const li = document.createElement("li");
      li.textContent = tip;
      tipsList.appendChild(li);
    });
  }

  // Never offer a desktop "Open demo" CTA — mobile-only via QR scan.
  document.querySelectorAll("[data-desktop-hide]").forEach((el) => {
    el.setAttribute("hidden", "");
  });
});
