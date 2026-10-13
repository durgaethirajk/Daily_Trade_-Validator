# Daily Trade Validator — iPhone PWA MVP

## What's included
- Manual checklist for Nifty 50 and Sensex options
- 5-minute opening-range breakout, BOS, FVG retracement, rejection candle and VWAP checks
- Entry/stop-loss risk and 1R target calculation
- Manual open-trade review using option premium and invalidation flags
- Local-only journal and CSV export
- PWA manifest and service worker for Home Screen installation/offline shell

## Important rule notes
The first version is deliberately conservative and manual. The user must confirm BOS/FVG/retracement from their chart; it does not calculate these automatically. It uses the entered 9:15–10:15 opening-range high/low as a directional filter. A completed close above the range is required for CE; below is required for PE. VWAP must align. FVG zone overlap is a consistency check, not a proof of a valid FVG. The 1R target shown is entry premium + absolute entry-to-stop distance for a long option. Validate sizing/lot quantity and all exchange rules yourself.

## Run locally for testing
Open `index.html` in a browser. Some PWA features only work when hosted on HTTPS or localhost.

## Install on iPhone
1. Host the contents of this folder on an HTTPS static host (for example, a private GitHub Pages site or another static web host).
2. Open the HTTPS URL in Safari on your iPhone.
3. Tap Share → Add to Home Screen → Add.
4. Launch from the Home Screen. Data is stored in Safari's local storage on that device; export CSV backups regularly.

## Before real-money use
Test with paper trades and historical examples. This is not a live feed, financial advice, a validated profitable strategy, or an order execution tool. The app cannot see your chart, verify screenshots, or guarantee stop execution. For live data, add a licensed market-data API through a secure backend; do not put broker/API secrets in client-side JavaScript.
