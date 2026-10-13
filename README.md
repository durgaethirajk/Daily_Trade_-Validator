# Daily Trade Validator — automatic harmonic screenshot analysis

## What this package adds
- Harmonics tab upload UI for PNG/JPEG/WebP chart screenshots.
- A frontend request to a secure backend endpoint.
- Backend image analysis that returns candidate X-A-B-C-D swing points and labels, then draws the XABCD overlay on the uploaded screenshot in the app.
- Candidate pattern label, direction, confidence, PRZ description, invalidation guidance, and notes.
- API key is read only from the backend environment; never put it in GitHub Pages JavaScript.

## Important
The AI result is an estimate from a screenshot, not a verified pattern or trade signal. The model may misread swing points or price labels. Confirm points and levels against Kite before trading. This does not connect to live Kite market data or place orders.

## Deploy frontend to GitHub Pages
1. Replace your existing app's `index.html` with this package's `index.html`. If you want to preserve the existing app features, use the current project files and merge the `autoHarmonicCard` UI and the script block; this package's index is based on the latest available local app source.
2. Set `HARMONIC_API_ENDPOINT` near the end of `index.html` to your deployed backend URL plus `/analyze`, e.g. `https://your-api.example.com/analyze`.
3. Commit and wait for GitHub Pages to rebuild.

## Deploy backend
The backend folder contains a FastAPI service and Dockerfile, suitable for a Python/Docker hosting provider.
1. Deploy the `backend` folder as a web service.
2. Configure these server environment variables in the hosting provider:
   - `OPENAI_API_KEY`: your secret API key (server-side only)
   - `OPENAI_VISION_MODEL`: `gpt-4.1-mini` by default
   - `FRONTEND_ORIGIN`: exact origin of your GitHub Pages site, e.g. `https://username.github.io` (include repository path only if your host checks full origins; browsers normally send origin only)
3. Copy the service HTTPS URL and add `/analyze`.
4. Put that URL in `HARMONIC_API_ENDPOINT` in the frontend code and redeploy GitHub Pages.
5. Open `https://YOUR_BACKEND_URL/` to check the service health response.

## Cost/security
Vision API requests may incur API charges. Protect the endpoint with rate limits/authentication before public launch; a public endpoint without limits could be abused. Never commit `.env`, API keys, tokens, or account credentials. Consider adding a simple app access token and hosting-provider rate limits before making the site public.
