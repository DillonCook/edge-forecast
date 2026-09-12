/* Shared counts come only from GitHub Release assets, never local clicks/storage. */
(function () {
  "use strict";
  const endpoint = "https://api.github.com/repos/DillonCook/edge-forecast/releases";
  const apkName = /^edge-forecast-\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?\.apk$/;

  async function getTotal(fetcher = fetch) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    const assets = new Map();
    let page = 1;
    try {
      while (page <= 10) {
        const url = endpoint + "?per_page=100" + (page === 1 ? "" : "&page=" + page);
        const response = await fetcher(url, {
          headers: {Accept: "application/vnd.github+json"},
          credentials: "omit", referrerPolicy: "no-referrer", signal: controller.signal
        });
        if (!response.ok) throw new Error("GitHub count unavailable");
        const releases = await response.json();
        if (!Array.isArray(releases)) throw new Error("Invalid release list");
        for (const release of releases) {
          if (release.draft === true) continue;
          if (release.draft !== false || !Array.isArray(release.assets)) throw new Error("Invalid release");
          for (const asset of release.assets) {
            if (!apkName.test(asset.name) || asset.state !== "uploaded") continue;
            if (!Number.isSafeInteger(asset.id) || asset.id < 1 || !Number.isSafeInteger(asset.download_count) || asset.download_count < 0) throw new Error("Invalid asset count");
            assets.set(asset.id, Math.max(assets.get(asset.id) || 0, asset.download_count));
          }
        }
        const link = response.headers.get("Link") || "";
        const next = link.match(/<([^>]+)>;\s*rel="next"/);
        if (!next) {
          if (/rel="next"/.test(link)) throw new Error("Invalid pagination");
          if (!assets.size) throw new Error("No published APK found");
          const total = [...assets.values()].reduce((sum, count) => sum + count, 0);
          if (!Number.isSafeInteger(total)) throw new Error("Invalid total");
          return total;
        }
        const parsed = new URL(next[1]);
        const canonical = new URL(endpoint);
        // GitHub may emit a numeric repository path. Only its page number is used;
        // subsequent requests always stay pinned to this project's endpoint.
        if (parsed.origin !== canonical.origin || !(parsed.pathname === canonical.pathname || /^\/repositories\/\d+\/releases$/.test(parsed.pathname)) || parsed.username || parsed.password || Number(parsed.searchParams.get("page")) !== page + 1) throw new Error("Unsafe pagination");
        page += 1;
      }
      throw new Error("Incomplete release list");
    } finally { clearTimeout(timeout); }
  }

  async function renderCounter(container, number, status, fetcher = fetch) {
    container.setAttribute("aria-busy", "true");
    try {
      const total = await getTotal(fetcher);
      number.textContent = new Intl.NumberFormat().format(total);
      container.dataset.total = String(total);
      container.dataset.state = "ready";
      status.textContent = "Since September 12, 2026 · GitHub Release downloads";
    } catch (_) {
      number.textContent = "—";
      delete container.dataset.total;
      container.dataset.state = "unavailable";
      status.textContent = "Count temporarily unavailable. Download still works.";
    } finally { container.setAttribute("aria-busy", "false"); }
  }

  if (typeof module !== "undefined" && module.exports) module.exports = {getTotal, renderCounter};
  if (typeof document !== "undefined") {
    const container = document.getElementById("download-stats");
    if (container) renderCounter(container, document.getElementById("download-count"), document.getElementById("download-count-status"));
  }
})();
