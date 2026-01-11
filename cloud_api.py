"""
PREDATOR v53.0 ADAPTIVE RESILIENCE - Cloud API (Render)
═══════════════════════════════════════════════════════════════
ADAPTIVE REGIME: TREND FOLLOWING vs MEAN REVERSION
A Justo para Mercados Laterais (Choppy Market)
═══════════════════════════════════════════════════════════════
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import os
import random  
import ccxt.async_support as ccxt
from dotenv import load_dotenv
import asyncio
import time
import math
import statistics

# ============================================================
# ⚙️ GLOBAL CONFIG
# ============================================================
load_dotenv()
INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")
def normalize_symbol(symbol: str) -> str:
    return symbol.replace("/", "").replace("-", "").upper()

async def sovereign_auth(x_token: Optional[str] = Header(None)):
    if not INTERNAL_SECRET_TOKEN: return 
    if x_token != INTERNAL_SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ============================================================
# 🧠 ENGINE STATE
# ============================================================
class EngineState:
    def __init__(self):
        self.uptime_start = time.time()
        self.daily_pnl = 0.0
        self.trades = 0
        self.regime = "ANALYZING" # TRENDING or RANGING

    def get_stats(self):
        return {
            "uptime": int(time.time() - self.uptime_start),
            "pnl": round(self.daily_pnl, 2),
            "regime": self.regime,
            "trades": self.trades
        }

engine_state = EngineState()

# ============================================================
# 🚀 PREDATOR BRAIN v53.0 (ADAPTIVE LOGIC)
# ============================================================
class NomadBrain:
    def calculate_indicators(self, closes, highs, lows):
        if len(closes) < 30: return None
        
        # 1. RSI (Momentum)
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d for d in deltas if d > 0]
        losses = [abs(d) for d in deltas if d < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # 2. ADX Simplificado (Força da Tendência)
        # Se range (High-Low) está expandindo, ADX sobe.
        tr_sum = sum([highs[i]-lows[i] for i in range(-14, 0)])
        adx_proxy = (tr_sum / closes[-1]) * 1000 # Normalized Volatility
        
        # 3. Regime Detection
        regime = "TRENDING" if adx_proxy > 2.5 else "RANGING"
        
        # 4. Bollinger Bands (para Reversão)
        ma20 = sum(closes[-20:]) / 20
        std20 = statistics.stdev(closes[-20:])
        upper = ma20 + (2 * std20)
        lower = ma20 - (2 * std20)
        
        return {
            "rsi": rsi,
            "adx": adx_proxy,
            "regime": regime,
            "bb_upper": upper,
            "bb_lower": lower,
            "price": closes[-1],
            "atr": (tr_sum / 14)
        }

brain = NomadBrain()

# ============================================================
# ⚡ FASTAPI APP
# ============================================================
class WebhookPayload(BaseModel):
    symbol: str = "BTCUSDT"
    action: str = "BUY"
    price: Optional[float] = None
    qty: Optional[float] = 0.01

app = FastAPI(title="PREDATOR v53.0 ADAPTIVE")
exchange = ccxt.bybit({'apiKey': os.environ.get('BYBIT_API_KEY'), 'secret': os.environ.get('BYBIT_API_SECRET'), 'options': {'defaultType': 'future'}})

@app.on_event("startup")
async def startup_event():
    print("🔋 [V53 ADAPTIVE] SISTEMA INICIADO.")
    asyncio.create_task(exchange.load_markets())
    asyncio.create_task(autonomous_hunter_loop())

@app.get("/state")
async def get_state(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return engine_state.get_stats()

# ============================================================
# 🦅 AUTONOMOUS HUNTER (ADAPTIVE LOOP)
# ============================================================
async def autonomous_hunter_loop():
    print("🦅 CAÇADOR V53 ATIVO.")
    while True:
        try:
            await asyncio.sleep(5)
            for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
                ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=50)
                if not ohlcv: continue
                
                closes = [x[4] for x in ohlcv]
                highs = [x[2] for x in ohlcv]
                lows = [x[3] for x in ohlcv]
                
                intel = brain.calculate_indicators(closes, highs, lows)
                if not intel: continue
                
                engine_state.regime = intel["regime"]
                
                bias = "NEUTRAL"
                score = 0
                
                # 🧠 LÓGICA HÍBRIDA
                if intel["regime"] == "TRENDING":
                    # Trend Following (RSI Breakout)
                    if intel["rsi"] > 60: bias = "GOD_LONG"
                    if intel["rsi"] < 40: bias = "GOD_SHORT"
                else:
                    # Mean Reversion (Bollinger Bounce)
                    if intel["price"] < intel["bb_lower"] and intel["rsi"] < 30: bias = "GOD_LONG"
                    if intel["price"] > intel["bb_upper"] and intel["rsi"] > 70: bias = "GOD_SHORT"

                if bias != "NEUTRAL":
                    print(f"⚡ [V53 STRIKE] {symbol} | Regime: {intel['regime']} | Bias: {bias}")
                    
                    sl_mult = 1.5 if intel["regime"] == "RANGING" else 1.8
                    tp_mult = 2.0 if intel["regime"] == "RANGING" else 5.5
                    
                    atr = intel["atr"]
                    sl = intel["price"] - (atr*sl_mult) if bias=="GOD_LONG" else intel["price"] + (atr*sl_mult)
                    tp = intel["price"] + (atr*tp_mult) if bias=="GOD_LONG" else intel["price"] - (atr*tp_mult)
                    
                    if exchange.apiKey:
                        qty = 0.001 if "BTC" in symbol else 0.01
                        # Execução Real...
                        pass 

        except Exception as e:
            print(f"Warning: {e}")
            await asyncio.sleep(5)

# ============================================================
# 🔙 BACKTEST ENGINE (ADAPTIVE)
# ============================================================
@app.post("/backtest")
async def run_backtest(payload: WebhookPayload):
    symbol = normalize_symbol(payload.symbol)
    ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=2000)
    
    sim = {"pnl": 0.0, "trades": 0, "wins": 0, "history": []}
    
    for i in range(50, len(ohlcv)-1):
        # Recria passado
        past_closes = [x[4] for x in ohlcv[i-50:i+1]]
        past_highs = [x[2] for x in ohlcv[i-50:i+1]]
        past_lows = [x[3] for x in ohlcv[i-50:i+1]]
        
        intel = brain.calculate_indicators(past_closes, past_highs, past_lows)
        bias = "NEUTRAL"
        
        # LÓGICA HÍBRIDA
        if intel["regime"] == "TRENDING":
             if intel["rsi"] > 60: bias = "GOD_LONG"
             if intel["rsi"] < 40: bias = "GOD_SHORT"
        else:
             if past_closes[-1] < intel["bb_lower"] and intel["rsi"] < 30: bias = "GOD_LONG"
             if past_closes[-1] > intel["bb_upper"] and intel["rsi"] > 70: bias = "GOD_SHORT"
             
        if bias != "NEUTRAL":
            sl_mult = 1.5 if intel["regime"] == "RANGING" else 1.8
            tp_mult = 2.0 if intel["regime"] == "RANGING" else 5.5
            atr = intel["atr"]
            entry = ohlcv[i][4]
            sl_dist = atr * sl_mult
            tp_dist = atr * tp_mult

            # Trade Outcome
            pnl = 0
            for j in range(i+1, min(i+60, len(ohlcv))):
                f = ohlcv[j]
                if bias == "GOD_LONG":
                    if f[2] >= entry + tp_dist:
                         pnl = tp_mult * (atr/entry) * 100
                         break
                    if f[3] <= entry - sl_dist:
                         pnl = -sl_mult * (atr/entry) * 100
                         break
                else:
                    if f[3] <= entry - tp_dist:
                         pnl = tp_mult * (atr/entry) * 100
                         break
                    if f[2] >= entry + sl_dist:
                         pnl = -sl_mult * (atr/entry) * 100
                         break
            
            pnl -= 0.06
            if pnl != -0.06:
                sim["pnl"] += pnl
                sim["trades"] += 1
                if pnl > 0: sim["wins"] += 1
                i += 10 # Pula candles para não scalpar demais

    return {
        "symbol": symbol,
        "total_pnl_percent": round(sim["pnl"], 2),
        "total_trades": sim["trades"],
        "win_rate": round(sim["wins"]/sim["trades"]*100, 1) if sim["trades"] > 0 else 0
    }
