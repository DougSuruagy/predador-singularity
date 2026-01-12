from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import ccxt.async_support as ccxt
from dotenv import load_dotenv
import asyncio
import time

# ============================================================
# ⚙️ VERCEL MASTER BRAIN - v271.0 "Quantum Sovereign Gold"
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
        past_rsi = []
        for i in range(len(closes)-5, len(closes)):
             window_deltas = [closes[j] - closes[j-1] for j in range(max(1, i-14), i+1)]
             past_rsi.append(self._calc_rsi(window_deltas))
        rsi_slope = past_rsi[-1] - past_rsi[-3] if len(past_rsi) > 3 else 0

        # Stochastic RSI (Exhaustion Precision)
        rsi_min = min(past_rsi) if past_rsi else 0
        rsi_max = max(past_rsi) if past_rsi else 100
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
    return {"status": "BRAIN_ACTIVE", "location": "VERCEL", "version": "271.0"}

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
    
    # 🧬 MASTER LOGIC v310.0 "LEGEND-ADAPTIVE"
    # Objetivo: Equilibrar Precisão e Atividade (v220 Hybrid)
    is_sol = "SOL" in payload.symbol.upper()
    is_eth = "ETH" in payload.symbol.upper()
    
    # Body Ratio Relaxado para mais entradas 
    if len(payload.ohlcv) > 0:
        o, h, l, c = payload.ohlcv[-1][1], payload.ohlcv[-1][2], payload.ohlcv[-1][3], payload.ohlcv[-1][4]
        body_ratio = abs(o - c) / max(0.0001, h - l)
    else: body_ratio = 1.0

    if intel["is_compressed"]:
        # Filtros de Atividade v220
        min_width = 0.85 if is_sol else (0.40 if is_eth else 0.30)
        if intel["bb_width"] < min_width:
             return {"bias": "NEUTRAL", "score": 0, "intel": intel, "decision": "REJECT", "reason": "Low Activity"}

        # RSI Precision (v220 Levels)
        lo_rsi = 25 if is_sol else 30
        hi_rsi = 75 if is_sol else 70
        
        oversold = (intel["rsi"] < lo_rsi) and (body_ratio < 0.70)
        overbought = (intel["rsi"] > hi_rsi) and (body_ratio < 0.70)
        
        # Z-Volume 
        min_z = 2.5 if is_sol else 2.2
        strong_push = intel["z_vol"] > min_z

        if strong_push:
            if oversold: bias = "GOD_LONG"; score = 96
            elif overbought: bias = "GOD_SHORT"; score = 96
            
    else:
        # TREND LOGIC
        if abs(intel["psi"]) > 0.40 and intel["z_vol"] > 3.0: 
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            score = 92
            
    # Hard Divergence Reject
    if intel["divergence"]: score = 0 
            
    decision = "EXECUTE" if score >= 92 else "REJECT"

    return {
        "bias": bias, "score": score, "intel": intel, "decision": decision,
        "targets": {"tp": intel["ema9"], "sl_factor": 2.0},
        "version": "310.0-ADAPTIVE"
    }
