"use strict";
(() => {
  const labels = {a: "Round blast", b: "Flared blast", c: "Layered blast", d: "Classic slim", e: "Fine needle", f: "Soft fade"};
  const modes = {
    following: "A set-length trail travels behind the moving head, even as it passes 12. On your watch, choose a short, medium or long following distance.",
    fixed: "The starting end stays at 12 while the trail grows clockwise. It clears when the head returns to 12, then starts again. Following distance does not affect this mode."
  };
  const display = document.getElementById("style-image");
  const caption = document.getElementById("style-caption");
  const controls = document.querySelector(".enhancement");
  const selection = {style: "d", mode: "following"};
  let latest = 0;

  function updatePreview() {
    const ticket = ++latest;
    const {style, mode} = selection;
    const next = new Image();
    display.setAttribute("aria-busy", "true");
    document.getElementById("mode-description").textContent = modes[mode];
    controls.querySelectorAll("[data-style]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.style === style));
    });
    next.onload = () => {
      if (ticket !== latest) return;
      display.src = next.src;
      display.alt = `${labels[style]} with ${mode === "fixed" ? "a trail starting at 12" : "a following trail"}, shown at 15 seconds into the minute`;
      display.setAttribute("aria-busy", "false");
      caption.textContent = `${labels[style]} · ${mode === "fixed" ? "Fixed at 12" : "Following"}`;
    };
    next.onerror = () => {
      if (ticket !== latest) return;
      display.setAttribute("aria-busy", "false");
      caption.textContent = "This preview could not load. The video and download are still available.";
    };
    next.src = `assets/${style}-${mode}.webp`;
  }

  controls.addEventListener("click", event => {
    const button = event.target.closest("button[data-style]");
    if (!button || !Object.hasOwn(labels, button.dataset.style)) return;
    selection.style = button.dataset.style;
    updatePreview();
  });
  controls.addEventListener("change", event => {
    const input = event.target;
    if (input.name !== "trail" || !Object.hasOwn(modes, input.value)) return;
    selection.mode = input.value;
    updatePreview();
  });
  controls.hidden = false;
})();
