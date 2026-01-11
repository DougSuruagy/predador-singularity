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
        
        # Z-Score Volume (Outlier Detection)
        z_vol = 0.0
        if volumes and len(volumes) > 30:
            avg_v = sum(volumes[-30:-1]) / 29
            std_v = (sum((v - avg_v)**2 for v in volumes[-30:-1]) / 29)**0.5
            z_vol = (volumes[-1] - avg_v) / (std_v + 0.0001)

        # RSI Slope (Momentum Exhaustion)
        past_rsi = [self._calc_rsi([closes[j] - closes[j-1] for j in range(max(1, i-14), i+1)]) for i in range(len(closes)-5, len(closes))]
        rsi_slope = past_rsi[-1] - past_rsi[-3] if len(past_rsi) > 3 else 0

        is_compressed = bb_width < 0.65 or entropy > 0.55
        ema9 = sum(closes[-9:]) / 9
        
        # 🔗 Elastic Divergence
        divergence = False
        if closes[-1] > ma20 and rsi < 38: divergence = True
        elif closes[-1] < ma20 and rsi > 62: divergence = True

        return {
            "rsi": rsi, "rsi_slope": rsi_slope, "psi": psi,
            "bb_width": bb_width, "z_vol": z_vol, "is_compressed": is_compressed,
            "touch_low": touch_low, "touch_high": touch_high,
            "divergence": divergence, "ema9": ema9, "ma20": ma20,
            "price": closes[-1]
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
    
    # 🧬 MASTER LOGIC v220.0 "ELASTIC-SOL-ARMOR"
    is_sol = "SOL" in payload.symbol.upper()
    
    if intel["is_compressed"]:
        # Filtro de Rentabilidade (SOL exige mais espaço por causa dos spreads e volatilidade)
        min_width = 0.80 if is_sol else 0.35
        if intel["bb_width"] < min_width:
             return {"bias": "NEUTRAL", "score": 0, "intel": intel, "decision": "REJECT", "reason": "Low Vol Zone"}

        # Triggers de Estilingue
        oversold = (intel["rsi"] < 30 or (intel["rsi"] < 35 and intel["rsi_slope"] < -6))
        overbought = (intel["rsi"] > 70 or (intel["rsi"] > 65 and intel["rsi_slope"] > 6))
        
        # Z-Volume Crítico (SOL precisa de volume gigante para não ser "fakeout")
        min_z = 3.2 if is_sol else 2.2
        strong_push = intel["z_vol"] > min_z

        if strong_push and oversold:
            bias = "GOD_LONG"; score = 98 if is_sol else 96
        elif strong_push and overbought:
            bias = "GOD_SHORT"; score = 98 if is_sol else 96
            
    else:
        # TREND LOGIC: Apenas com Z-Vol explosivo
        min_trend_z = 4.0 if is_sol else 2.8
        if abs(intel["psi"]) > 0.35 and intel["z_vol"] > min_trend_z: 
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            score = 92
            
    # Divergence Hard-Reject
    if intel["divergence"]: score = 0 
            
    decision = "EXECUTE" if score >= 90 else "REJECT"

    return {
        "bias": bias, "score": score, "intel": intel, "decision": decision,
        "targets": {"tp": intel["ema9"], "sl_factor": 2.2 if is_sol else 1.8},
        "version": "220.0-ARMOR"
    }
