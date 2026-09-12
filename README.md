# Edge Forecast

A standalone showcase and free APK download page for Edge Forecast, an independent Wear OS watch face.

**Website:** https://dilloncook.github.io/edge-forecast/

## Hosting

GitHub Pages serves `docs/` from the `main` branch. No custom domain, build service, analytics, signup form or paid dependency. `.nojekyll` keeps the site static. All imagery and video are first-party local assets. The repository contains the website and public download, not the private watch-face development workspace or signing materials.

## Download

`docs/downloads/edge-forecast-1.5.17.apk` is the exact signed 1.5.17 APK, not a rebuild. Its fingerprint is in `docs/downloads/SHA256SUMS.txt` and metadata in `docs/release.json`. Free download/use does not imply that the APK or bundled third-party materials have been relicensed as open source.

This is a **preview release requiring WFF 5 support**, introduced with Wear OS 7. The APK's lower Android install floor is not a claim of renderer compatibility with older Wear OS versions. Automated build validation does not certify individual devices, battery life or AOD transitions.

## Media and claims

The six stills in each trail mode and the video derive from the packaged WFF effect geometry and image assets. The face data is illustrative. They are not physical-watch screenshots; the video is silent and runs at 10x speed. The original clean ring, time, weather, battery and AOD code is preserved in 1.5.17.

Compatibility reference: https://android-developers.googleblog.com/2026/05/whats-new-wear-os-7.html

Phone-side installation reference: https://freepoc.org/wear-installer-2-help-page/

Hosting/privacy reference: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages

## Development

No package installation or bundler is required. Serve the repository with `python -m http.server 8874 --bind 127.0.0.1`, then open `http://127.0.0.1:8874/docs/`.

`python scripts/check_site.py` checks links, required disclosures, APK integrity, public-file scope and release consistency. Browser verification is performed on desktop/mobile, both trail choices, all six styles, video playback, keyboard use, reduced motion and actual download bytes before publishing. QA outputs are ignored, not published.
