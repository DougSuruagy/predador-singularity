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
    
    # 🧬 MASTER LOGIC v200.0 "QUANTUM SCALPER"
    # Objetivo: Lucro Líquido Real (Net Profit) em Bybit Fees (0.06% round trip)
    fee_round_trip = 0.08 # % total
    
    if intel["is_compressed"]:
        # Filtro de Rentabilidade Real: BB_Width deve ser > 3x as taxas para valer o risco
        # Movimento esperado é ~ bb_width / 2 (para a média)
        expected_move = intel["bb_width"] / 2
        if expected_move < (fee_round_trip * 2.5):
             return {"bias": "NEUTRAL", "score": 0, "intel": intel, "decision": "REJECT", "reason": "Fee Trap Zone"}

        # Wick Rejection (Pin-bar) - Mais estrito que v190
        candle_range = highs[-1] - lows[-1]
        body_size = abs(closes[-1] - payload.ohlcv[-1][1])
        body_ratio = (body_size / candle_range) if candle_range > 0 else 1.0
        
        # Filtro de Pin-bar Institucional
        wick_rejection = 0.45 if "SOL" not in payload.symbol.upper() else 0.55
        is_pin_bar = body_ratio < 0.40 # Corpo pequeno
        
        rejection_low = (closes[-1] > lows[-1] + (candle_range * wick_rejection)) and is_pin_bar
        rejection_high = (closes[-1] < highs[-1] - (candle_range * wick_rejection)) and is_pin_bar

        # Scalper Triggers
        if intel["touch_low"] and rejection_low and intel["rsi"] < 32: 
            bias = "GOD_LONG"; score = 98
        elif intel["touch_high"] and rejection_high and intel["rsi"] > 68: 
            bias = "GOD_SHORT"; score = 98
            
    else:
        # TREND SCALPING (PSI + Volume)
        if abs(intel["psi"]) > 0.28 and intel["vol_intensity"] > 2.2: 
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            score = 92
            
    # Filtro de Divergência
    if intel["divergence"]: score = 0 
            
    decision = "EXECUTE" if score >= 85 else "REJECT"

    return {
        "bias": bias, "score": score, "intel": intel, "decision": decision,
        "version": "200.0-QUANTUM"
    }
