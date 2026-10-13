# Daily Trade Validator v2 — Harmonics + screenshot reference

## Features
- Validate CE candidate / PE candidate / NO TRADE from manually selected market context.
- Harmonic ratio checker for Gartley, Bat, Butterfly and Crab using X-A-B-C-D swing prices.
- Screenshot upload preview (reference only; no automatic OCR or chart recognition).
- Long-option premium risk/target calculator, open-trade P&L check, local journal and CSV export.
- Updated service-worker cache name (`dtv-v2-harmonics`) to help avoid old tab versions.

## Deploy to GitHub Pages
1. Unzip this package on a computer or phone file manager.
2. In your GitHub repository, replace `index.html`, `manifest.webmanifest`, `sw.js`, `icon-192.png`, and `icon-512.png` with these files. Upload the extracted files, not the ZIP.
3. Commit the changes.
4. On iPhone Safari, open the Pages website, refresh it, then if the old version persists remove the Home Screen icon and add it again after confirming Safari shows the new Harmonics tab.

## Important limitations
This version does not connect to Zerodha Kite, read live candles, interpret screenshots automatically, or place orders. GitHub Pages is static hosting; do not place API keys or secrets in its files. A later live-data version would need an authorised backend and a review of Kite Connect's current terms.
The CE/PE result is a rules checklist, not a prediction or financial advice. A harmonic ratio match alone is not a buy signal.
