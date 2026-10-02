# Edge Forecast

A standalone showcase and free APK download page for Edge Forecast, an independent Wear OS watch face.

**Website:** https://dilloncook.github.io/edge-forecast/

## Hosting

GitHub Pages serves `docs/` from the `main` branch. No custom domain, build service, signup form or paid dependency. A local script reads public GitHub Release download counts without credentials or click tracking. `.nojekyll` keeps the site static. All imagery and video are first-party local assets. The repository contains the website and public download, not the private watch-face development workspace or signing materials.

## Download

The download button now points to the GitHub Release asset. `artifacts/edge-forecast-1.5.25.apk` retains the current exact signed APK for reproducible integrity checks, outside the Pages publication tree. The previous static Pages APK endpoint is retired. Its fingerprint is in `docs/downloads/SHA256SUMS.txt` and metadata in `docs/release.json`. Free download/use does not imply that the APK or bundled third-party materials have been relicensed as open source.

This is a **preview release requiring WFF 5 support**, introduced with Wear OS 7. The APK's lower Android install floor is not a claim of renderer compatibility with older Wear OS versions. Automated build validation does not certify individual devices, battery life or AOD transitions.

## Installation requirements

The public page gives the complete phone-only method using **Wear Installer 2 by Malcolm Bryant**, installed on the **Android phone only**. No Wear Installer companion is required on the watch. The steps explicitly cover Samsung Developer options, ADB debugging, Wireless debugging, the IP address, the pairing code/port, the different connection port, Custom APK â†’ Install, selection in the watch-face picker, and disabling debugging afterward.

**Phone Battery Complication by amoledwatchfaces** is optional; install and open it on both phone and watch only to populate the phone-battery slot. Weather depends on the watch weather service; tapping weather targets Samsung Weather on the watch. Installer/app instructions were checked against the developer help page and current Play listings, not physically rehearsed on an attached device.

## Media and claims

The selector offers eight effects in both trail modes. Ribbon trail maps to Energy Filaments in the watch editor; Sparkling dust maps to Comet Dust. The four new stills and the new four-panel motion demo retain the earlier scene and decoded mask pixels; the artwork is unchanged in the published 1.5.25 APK. The unchanged face data is illustrative. These are offline renders, not physical-watch screenshots or performance proof; the silent demo runs at 10x speed. The six original styles retain their earlier source-derived previews. Version 1.5.25 includes smoother filament joins and the modest dust brightness lift. Phone text colors/formatting, on-watch editor stability, and empty-slot/AOD transitions retain the limitations stated beside the download.

Compatibility reference: https://android-developers.googleblog.com/2026/05/whats-new-wear-os-7.html

Phone-side installation reference: https://freepoc.org/wear-installer-2-help-page/

Hosting/privacy reference: https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages

## Download counter

The counter sums `download_count` for published `edge-forecast-<version>.apk` Release assets, including prereleases, across paginated API responses. Counts are shared and server-sourced; the page never increments them locally. API errors or rate limits show an unavailable state, not a fabricated zero. Counting began with Release hosting on September 12, 2026; earlier static downloads cannot be recovered. Counts include repeats and verification downloads and do not measure unique people, completed installations, or all repository clones. Deleting Release assets would lose their counters; retain them across updates.

Run `node --test scripts/test_download_counter.cjs` for fixture-based pagination/filtering/failure tests. Actual published counts must be verified separately through GitHub and the live browser.

## Development

No package installation or bundler is required. Serve the repository with `python -m http.server 8874 --bind 127.0.0.1`, then open `http://127.0.0.1:8874/docs/`.

`python scripts/check_site.py` checks links, required disclosures, APK integrity, public-file scope and release consistency. Routine browser verification covers desktop/mobile, both trail choices, all eight styles, video playback, keyboard use, reduced motion and the live download link. It verifies the published asset ID, name, size and GitHub SHA-256 digest against the local release artifact without requesting APK bytes. Public release-download URLs are blocked during routine QA. An actual download requires explicit `--verify-apk-download` approval and can increment GitHubâ€™s count; do not use it for website-only changes. Earlier verification downloads remain in the historical total, which cannot be reliably converted into unique-user or install counts. QA outputs are ignored, not published.

## 1.5.25 forecast spacing
Forecast data, day/night icons, availability and time labels now use +3/+6/+9 hours. Existing effect imagery is retained as illustrative style artwork, with older weather labels disclosed beside the download. Source tests cover all 24 local hours, 12/24-hour formats and midnight wrap; physical watch validation remains incomplete.
