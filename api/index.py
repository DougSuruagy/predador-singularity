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
        
        # Stochastic RSI (Exhaustion Precision)
        rsi_min = min(past_rsi[-14:]) if len(past_rsi) >= 14 else 0
        rsi_max = max(past_rsi[-14:]) if len(past_rsi) >= 14 else 100
        stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min + 0.0001) * 100

        # EMA 200 (Trend Shield)
        ema200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else ma20
        trend_up = closes[-1] > ema200

        is_compressed = bb_width < 0.65 or entropy > 0.55
        ema9 = sum(closes[-9:]) / 9
        
        # 🔗 Elastic Divergence (Refined)
        divergence = False
        if closes[-1] > ma20 and rsi < 35: divergence = True
        elif closes[-1] < ma20 and rsi > 65: divergence = True

        return {
            "rsi": rsi, "stoch_rsi": stoch_rsi, "rsi_slope": rsi_slope, "psi": psi,
            "bb_width": bb_width, "z_vol": z_vol, "is_compressed": is_compressed,
            "touch_low": touch_low, "touch_high": touch_high,
            "divergence": divergence, "ema9": ema9, "ma20": ma20, "ema200": ema200,
            "trend_up": trend_up, "price": closes[-1]
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
    
    # 🧬 MASTER LOGIC v270.0 "ELASTIC-GOLD"
    # Objetivo: IGUALAR OU SUPERAR A v220 (+92.61% PnL)
    is_sol = "SOL" in payload.symbol.upper()
    is_eth = "ETH" in payload.symbol.upper()
    
    # 🕒 CRITICAL INACTIVITY PULSE: Evita que o robô fique parado
    idle_minutes = (time.time() - engine_state.last_trade_time) / 60
    inactivity_boost = 0
    if idle_minutes > 30: inactivity_boost = 5 # Facilita a entrada após 30min parado
    
    if intel["is_compressed"]:
        # Filtros ORIGINAIS v220 (Os Lucrativos)
        min_width = 0.80 if is_sol else 0.35
        if intel["bb_width"] < min_width:
             return {"bias": "NEUTRAL", "score": 0, "intel": intel, "decision": "REJECT", "reason": "Low Vol"}

        # Triggers de Estilingue de Alta Probabilidade
        oversold = (intel["rsi"] < 35 or (intel["rsi"] < 40 and intel["rsi_slope"] < -5))
        overbought = (intel["rsi"] > 65 or (intel["rsi"] > 60 and intel["rsi_slope"] > 5))
        
        # Z-Volume (Confirmador de Fluxo Institucional)
        min_z = 3.2 if is_sol else 2.2 # v220 Pure Levels
        strong_push = intel["z_vol"] > min_z

        if strong_push and oversold:
            bias = "GOD_LONG"; score = 95 + inactivity_boost
        elif strong_push and overbought:
            bias = "GOD_SHORT"; score = 95 + inactivity_boost
            
    else:
        # TREND LOGIC (v220 levels)
        if abs(intel["psi"]) > 0.35 and intel["z_vol"] > 2.8: 
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            score = 90 + (inactivity_boost / 2)
            
    # Hard Divergence Reject
    if intel["divergence"]: score = 0 
            
    decision = "EXECUTE" if score >= (92 - (inactivity_boost)) else "REJECT"

    return {
        "bias": bias, "score": score, "intel": intel, "decision": decision,
        "targets": {"tp": intel["ema9"], "sl_factor": 2.5 if is_sol else 1.8},
        "version": "270.0-GOLD"
    }
