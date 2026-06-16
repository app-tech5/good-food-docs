window.addEventListener("DOMContentLoaded", () => {
  const config = window.GOOD_FOOD_DOWNLOAD_CONFIG;
  if (!config) return;

  const appUrl = new URL(config.baseUrl);
  const appPath = `${config.downloadsPath.replace(/\/$/, "")}/${config.apkFileName}`;
  appUrl.pathname = appPath;
  const apkUrl = appUrl.toString();

  const qrBase = "https://api.qrserver.com/v1/create-qr-code/";
  const qrUrl = `${qrBase}?size=360x360&data=${encodeURIComponent(apkUrl)}`;

  const setText = (selector, value) => {
    const element = document.querySelector(selector);
    if (element) element.textContent = value;
  };

  const setHref = (selector, value) => {
    const element = document.querySelector(selector);
    if (element) element.setAttribute("href", value);
  };

  setText("[data-app-name]", config.appName);
  setText("[data-page-title]", config.pageTitle);
  setText("[data-page-subtitle]", config.pageSubtitle);
  setText("[data-apk-file-name]", config.apkFileName);
  setText("[data-apk-path]", appPath);
  setText("[data-cta-primary]", config.ctaPrimaryLabel);
  setText("[data-cta-secondary]", config.ctaSecondaryLabel);
  setText("[data-qr-label]", config.qrLabel);

  setHref("[data-apk-link-primary]", apkUrl);
  setHref("[data-apk-link-secondary]", apkUrl);

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
});
