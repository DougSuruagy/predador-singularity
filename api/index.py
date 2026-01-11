from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import ccxt.async_support as ccxt
from dotenv import load_dotenv
import asyncio
import time

# ============================================================
# ⚙️ VERCEL MASTER BRAIN - v75.0 "Sovereign Apex"
# ============================================================
load_dotenv()
app = FastAPI(title="PREDATOR Master Brain (Vercel)")

INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

class NomadBrain:
    def calculate_indicators(self, closes, highs, lows):
        if len(closes) < 30: return None
        
        # Momentum (RSI)
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d for d in deltas if d > 0]
        losses = [abs(d) for d in deltas if d < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Intensity (PSI)
        psi = (closes[-1] - closes[-5]) / closes[-5] * 100
        
        # Volatility (ATR & BB Width)
        tr = max(highs[-1] - lows[-1], abs(highs[-1] - closes[-2]), abs(lows[-1] - closes[-2]))
        atr = tr 
        
        ma20 = sum(closes[-20:]) / 20
        variance = sum((x - ma20)**2 for x in closes[-20:]) / 20
        std_dev = variance**0.5
        bb_width = (std_dev * 4) / ma20 * 100 
        
        # Trend
        ma50 = sum(closes[-30:]) / 30 
        trend_strong = abs(ma20 - ma50) > (closes[-1] * 0.001)
        
        # Entropy
        direction_changes = sum(1 for i in range(len(deltas)-10, len(deltas)) if (deltas[i] > 0) != (deltas[i-1] > 0))
        entropy = direction_changes / 10.0
        
        is_compressed = bb_width < 0.60 or entropy > 0.7
        
        return {
            "rsi": rsi, "psi": psi, "atr": atr, "trend_strong": trend_strong,
            "is_compressed": is_compressed, "entropy": entropy, "price": closes[-1]
        }

brain = NomadBrain()

class HuntRequest(BaseModel):
    symbol: str
    mode: str
    ohlcv: List[List[float]] # [[t, o, h, l, c, v], ...]

@app.get("/")
async def health():
    return {"status": "BRAIN_ACTIVE", "location": "VERCEL", "version": "75.0"}

@app.post("/api/hunt")
async def analyze_hunt(payload: HuntRequest, x_token: str = Header(None)):
    if x_token != INTERNAL_SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    closes = [x[4] for x in payload.ohlcv]
    highs = [x[2] for x in payload.ohlcv]
    lows = [x[3] for x in payload.ohlcv]
    
    intel = brain.calculate_indicators(closes, highs, lows)
    if not intel:
        return {"action": "WAIT", "reason": "Insufficient Data"}
    
    bias = "NEUTRAL"
    score = 0
    
    # 🧬 SOVEREIGN LOGIC (v71.0 DNA)
    if payload.mode == "SUPREME":
        if intel["is_compressed"]:
            if intel["rsi"] < 18: bias = "GOD_LONG"; score = 95
            elif intel["rsi"] > 82: bias = "GOD_SHORT"; score = 95
        else:
            if abs(intel["psi"]) > 0.25: # Dynamic Threshold
                score = 75 + (abs(intel["psi"]) * 10)
                bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
                
    elif payload.mode == "SNIPER":
        if intel["is_compressed"]:
            if intel["rsi"] < 15: bias = "GOD_LONG"; score = 95
            elif intel["rsi"] > 85: bias = "GOD_SHORT"; score = 95
        else:
            if abs(intel["psi"]) > 0.35:
                score = 75 + (abs(intel["psi"]) * 10)
                bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"

    return {
        "bias": bias,
        "score": score,
        "intel": intel,
        "decision": "EXECUTE" if score >= 75 else "REJECT"
    }
