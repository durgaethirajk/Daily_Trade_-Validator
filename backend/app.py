import base64
import json
import os
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI(title="Daily Trade Validator Harmonic Screenshot API")

# Set FRONTEND_ORIGIN to the exact GitHub Pages origin, e.g. https://username.github.io
allowed_origin = os.getenv("FRONTEND_ORIGIN", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin] if allowed_origin != "*" else ["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
MAX_BYTES = 8 * 1024 * 1024
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp"}

@app.get("/")
def health():
    return {"ok": True, "service": "daily-trade-validator-harmonic-api"}

@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    instrument: str = Form("NIFTY"),
    timeframe: str = Form("5-minute"),
    note: str = Form(""),
):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=503, detail="Server API key is not configured.")
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Upload PNG, JPEG or WebP.")
    raw = await image.read()
    if not raw or len(raw) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image is empty or exceeds 8 MB.")
    b64 = base64.b64encode(raw).decode("ascii")
    data_url = f"data:{image.content_type};base64,{b64}"

    prompt = f"""
You are assisting with visual chart review for an educational trading checklist.
Instrument: {instrument}. Timeframe: {timeframe}. User note: {note[:500]}.
Inspect this screenshot only. Do not invent hidden prices or candles. Identify whether a plausible
X-A-B-C-D harmonic pattern is visually present. Common candidates: Gartley, Bat, Butterfly, Crab.
If the screenshot does not clearly support one, return "Unconfirmed pattern" and low confidence.
Return ONLY valid JSON with this schema:
{{
 "pattern": "Gartley | Bat | Butterfly | Crab | Unconfirmed pattern",
 "direction": "bullish reversal candidate | bearish reversal candidate | unclear",
 "confidence": "low | medium | high",
 "points": [
  {{"label":"X","x":0,"y":0,"price":null}},
  {{"label":"A","x":0,"y":0,"price":null}},
  {{"label":"B","x":0,"y":0,"price":null}},
  {{"label":"C","x":0,"y":0,"price":null}},
  {{"label":"D","x":0,"y":0,"price":null}}
 ],
 "prz": "short description; say unclear if price scale cannot support a level",
 "setup": "confirmation needed before entry; no guaranteed CE/PE",
 "invalidation": "describe what would invalidate the pattern; no fabricated price",
 "notes": ["brief observation", "ratio or image uncertainty", "confirmation checklist"]
}}
Coordinates x and y must be normalized integers from 0 to 1000 relative to the image (top-left is 0,0).
Use price only if the value is legible on the screenshot; otherwise null. The points must be in
chronological X-A-B-C-D order and refer to visible candle swing points. Do not claim live market access.
Do not provide a guaranteed prediction or a personalized financial recommendation.
"""
    try:
        response = client.responses.create(
            model=MODEL,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url, "detail": "high"},
                ],
            }],
            max_output_tokens=1200,
        )
        text_out = response.output_text.strip()
        if text_out.startswith("```"):
            text_out = text_out.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        result = json.loads(text_out)
        points = result.get("points", [])
        if not isinstance(points, list) or len(points) < 5:
            raise ValueError("Missing points")
        for p in points[:5]:
            p["x"] = max(0, min(1000, int(p["x"])))
            p["y"] = max(0, min(1000, int(p["y"])))
        result["points"] = points[:5]
        result["pattern"] = str(result.get("pattern", "Unconfirmed pattern"))[:100]
        result["direction"] = str(result.get("direction", "unclear"))[:100]
        result["confidence"] = str(result.get("confidence", "low"))[:20]
        result["notes"] = [str(x)[:300] for x in result.get("notes", [])[:8]]
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Vision analysis failed: {type(exc).__name__}") from exc
