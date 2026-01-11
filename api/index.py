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
    def calculate_indicators(self, closes, highs, lows, volumes=None):
        if len(closes) < 30: return None
        
        # Momentum & Flow
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        rsi = self._calc_rsi(deltas)
        
        # PSI Intensity (5-min window velocity)
        psi = (closes[-1] - closes[-5]) / closes[-5] * 100
        velocity = abs(psi) / 5 # Variação por minuto
        
        # Volatility & Compression
        ma20 = sum(closes[-20:]) / 20
        std_dev = (sum((x - ma20)**2 for x in closes[-20:]) / 20)**0.5
        bb_upper = ma20 + (std_dev * 2)
        bb_lower = ma20 - (std_dev * 2)
        bb_width = (std_dev * 4) / ma20 * 100 
        
        # Band Touch Logic
        touch_low = closes[-1] <= bb_lower or lows[-1] <= bb_lower
        touch_high = closes[-1] >= bb_upper or highs[-1] >= bb_upper
        
        # Entropy & Directional Chaos
        direction_changes = sum(1 for i in range(len(deltas)-10, len(deltas)) if (deltas[i] > 0) != (deltas[i-1] > 0))
        entropy = direction_changes / 10.0
        
        # Volume Intensity (2-Sigma)
        vol_intensity = 1.0
        if volumes and len(volumes) > 20:
            avg_vol = sum(volumes[-20:-1]) / 19
            std_vol = (sum((v - avg_vol)**2 for v in volumes[-20:-1]) / 20)**0.5
            vol_intensity = (volumes[-1] - avg_vol) / (std_vol + 0.0001)

        is_compressed = bb_width < 0.60 or entropy > 0.50
        
        # 🔗 Divergence Check
        divergence = False
        if closes[-1] > ma20 and rsi < 40: divergence = True
        elif closes[-1] < ma20 and rsi > 60: divergence = True

        return {
            "rsi": rsi, "psi": psi, "velocity": velocity, 
            "bb_width": bb_width, "entropy": entropy, 
            "vol_intensity": vol_intensity, "is_compressed": is_compressed,
            "touch_low": touch_low, "touch_high": touch_high,
            "trend_strong": bb_width > 0.8 and entropy < 0.4,
            "divergence": divergence,
            "price": closes[-1],
            "ma20": ma20
        }

    def _calc_rsi(self, deltas):
        gains = [d for d in deltas if d > 0]
        losses = [abs(d) for d in deltas if d < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

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
    volumes = [x[5] for x in payload.ohlcv]
    
    intel = brain.calculate_indicators(closes, highs, lows, volumes)
    if not intel:
        return {"action": "WAIT", "reason": "Insufficient Data"}
    
    bias = "NEUTRAL"
    score = 0
    decision = "REJECT"
    
    # 🧬 MASTER LOGIC v190.0 "SCALPER-SOUL"
    # Foco: Alta frequência, lucros rápidos na exaustão.
    if intel["is_compressed"]:
        # Floor de Volatilidade reduzido para Scalping (0.25%)
        # Mas exige Volume Intensity alto (> 1.5)
        if intel["bb_width"] < 0.25:
             return {"bias": "NEUTRAL", "score": 0, "intel": intel, "decision": "REJECT", "reason": "Dead Zone"}

        # Exaustão RSI (Nível primário de scalper)
        rsi_oversold = intel["rsi"] < 28
        rsi_overbought = intel["rsi"] > 72
        
        # Volume Shock (Nível secundário)
        strong_flow = intel["vol_intensity"] > 1.8
        
        if (intel["touch_low"] and rsi_oversold) or (rsi_oversold and strong_flow):
            bias = "GOD_LONG"; score = 95
        elif (intel["touch_high"] and rsi_overbought) or (rsi_overbought and strong_flow):
            bias = "GOD_SHORT"; score = 95
            
    else:
        # TREND SCALPING: Segue o fluxo se a PSI for explosiva
        if abs(intel["psi"]) > 0.25 and intel["vol_intensity"] > 2.0: 
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            score = 90
            
    # Filtro de Divergência (Hard Reject para Scalper)
    if intel["divergence"]: score = 0 
            
    decision = "EXECUTE" if score >= 85 else "REJECT"

    return {
        "bias": bias, "score": score, "intel": intel, "decision": decision,
        "version": "190.0-SCALPER"
    }
