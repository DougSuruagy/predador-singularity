"""
PREDATOR v56.0 VALHALLA SUPREME - Cloud API (Render)
═══════════════════════════════════════════════════════════════
THE ULTIMATE FUSION:
1. DYNAMIC THRESHOLD: Adapts Aggression based on Market Trend.
   - Trending? Be Valhalla (0.22) -> Catch Big Moves.
   - Ranging? Be Iron (0.35) -> Avoid Chop.
2. JUNIOR SNIPER: Surgical Scalping on SOL.
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
from supabase import create_client, Client
from dotenv import load_dotenv
import asyncio
import time
import math
import psutil
import statistics

# ============================================================
# ⚙️ GLOBAL CONFIG
# ============================================================
load_dotenv()
INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")
def normalize_symbol(symbol: str) -> str:
    return symbol.replace("/", "").replace("-", "").upper()

# ============================================================
# 🛡️ SOVEREIGN SECURITY LAYER
# ============================================================
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
        self.is_healthy = True
        self.daily_pnl = 0.0
        self.trades = 0
        self.last_order = {}

    def get_stats(self):
        return {
            "uptime": int(time.time() - self.uptime_start),
            "pnl": round(self.daily_pnl, 2),
            "trades": self.trades
        }

engine_state = EngineState()

# ============================================================
# 🚀 PREDATOR BRAIN v56.0 (SUPREME LOGIC)
# ============================================================
class NomadBrain:
    def calculate_indicators(self, closes, highs, lows):
        if len(closes) < 30: return None
        
        # Momentum
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d for d in deltas if d > 0]
        losses = [abs(d) for d in deltas if d < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        psi = (closes[-1] - closes[-5]) / closes[-5] * 100
        
        tr = max(highs[-1] - lows[-1], abs(highs[-1] - closes[-2]), abs(lows[-1] - closes[-2]))
        atr = tr 
        
        # Trend Strength (The Fusion Key)
        ma20 = sum(closes[-20:]) / 20
        ma50 = sum(closes[-30:]) / 30 
        # Se as médias estão afastadas > 0.1%, temos tendência clara -> Modo Valhalla
        trend_strong = abs(ma20 - ma50) > (closes[-1] * 0.001)
        
        return {
            "rsi": rsi,
            "psi": psi,
            "atr": atr,
            "trend_strong": trend_strong,
            "price": closes[-1]
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

app = FastAPI(title="PREDATOR v56.0 VALHALLA SUPREME")
exchange = ccxt.bybit({'apiKey': os.environ.get('BYBIT_API_KEY'), 'secret': os.environ.get('BYBIT_API_SECRET'), 'options': {'defaultType': 'future'}})

@app.on_event("startup")
async def startup_event():
    print("🔋 [VALHALLA SUPREME] FUSÃO DINÂMICA INICIADA.")
    asyncio.create_task(exchange.load_markets())
    asyncio.create_task(autonomous_hunter_loop())

@app.get("/state")
async def get_state(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return engine_state.get_stats()

# ============================================================
# 🦅 AUTONOMOUS HUNTER (SUPREME LOOP)
# ============================================================
def get_supreme_config(symbol, is_trending):
    """ 
    [BTC/ETH] Configuração Dinâmica 
    Trending (True) -> Valhalla (0.22) -> Agressivo
    Chop (False) -> Iron (0.35) -> Defensivo
    """
    threshold = 0.22 if is_trending else 0.35 # O Pulso do Gato
    
    return {
        "threshold": threshold,
        "min_score": 55 if is_trending else 65, # Mais exigente se lateral
        "sl_mult": 1.8, # Padrão Valhalla
        "tp_mult": 5.5, # Padrão Valhalla
        "leverage": 10
    }

def get_sniper_config(symbol):
    """ [SOL] Junior Sniper v1.1 """
    return {
        "min_score": 75,
        "sl_mult": 1.0,
        "tp_mult": 1.5,
        "leverage": 5
    }

async def autonomous_hunter_loop():
    print("🦅 PREDADOR SUPREMO & 🦖 SNIPER JUNIOR ATIVOS.")
    while True:
        try:
            await asyncio.sleep(4)
            # PREDADOR (BTC/ETH)
            for symbol in ["BTCUSDT", "ETHUSDT"]: await run_strategy(symbol, "SUPREME")
            # SNIPER (SOL)
            await run_strategy("SOLUSDT", "SNIPER")
        except Exception as e:
            print(f"⚠️ Loop: {e}")
            await asyncio.sleep(5)

async def run_strategy(symbol, mode):
    ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=35)
    if not ohlcv: return
    
    closes = [x[4] for x in ohlcv]
    intel = brain.calculate_indicators(closes, [x[2] for x in ohlcv], [x[3] for x in ohlcv])
    if not intel: return
    
    bias = "NEUTRAL"
    score = 0
    config = {}
    
    if mode == "SUPREME":
        # AQUI ESTÁ A MÁGICA DINÂMICA
        config = get_supreme_config(symbol, intel["trend_strong"])
        
        threshold = config["threshold"]
        if abs(intel["psi"]) > threshold:
            score = 60 + (abs(intel["psi"]) * 10)
            bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
        
        # Filtro RSI Blindado
        if (bias == "GOD_LONG" and intel["rsi"] > 70) or (bias == "GOD_SHORT" and intel["rsi"] < 30): score = 0
        
    elif mode == "SNIPER":
        config = get_sniper_config(symbol)
        if intel["rsi"] < 20: 
            bias = "GOD_LONG"; score = 80
        elif intel["rsi"] > 80: 
            bias = "GOD_SHORT"; score = 80
            
    if score >= config["min_score"]:
        current_threshold_name = "VALHALLA (Agro)" if (mode == "SUPREME" and intel["trend_strong"]) else "IRON (Safe)"
        print(f"⚡ [{mode}-{current_threshold_name}] {symbol} | Score: {score:.1f} | Bias: {bias}")
        
        price = intel["price"]
        atr = intel["atr"]
        sl = price - (atr*config["sl_mult"]) if bias == "GOD_LONG" else price + (atr*config["sl_mult"])
        tp = price + (atr*config["tp_mult"]) if bias == "GOD_LONG" else price - (atr*config["tp_mult"])
        
        if exchange.apiKey:
            try:
                qty = 0.001 if "BTC" in symbol else 0.01
                if "SOL" in symbol: qty = 0.1
                
                side = "buy" if bias == "GOD_LONG" else "sell"
                params = {'stopLoss': float(exchange.price_to_precision(symbol, sl)), 
                          'takeProfit': float(exchange.price_to_precision(symbol, tp))}
                
                order = await exchange.create_order(symbol, 'market', side, qty, params=params)
                print(f"✅ ORDEM ENVIADA! ID: {order['id']}")
                engine_state.trades += 1
            except Exception as ex:
                print(f"❌ Erro Exec: {ex}")
        
        await asyncio.sleep(10)

# ============================================================
# 🔙 BACKTEST (DUAL DYNAMIC)
# ============================================================
@app.post("/backtest")
async def run_backtest(payload: WebhookPayload):
    symbol = normalize_symbol(payload.symbol)
    ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=2000)
    
    sim = {"pnl": 0.0, "trades": 0, "wins": 0}
    mode = "SNIPER" if "SOL" in symbol else "SUPREME"
    
    for i in range(35, len(ohlcv)-1):
        past_closes = [x[4] for x in ohlcv[i-35:i+1]]
        intel = brain.calculate_indicators(past_closes, [x[2] for x in ohlcv[i-35:i+1]], [x[3] for x in ohlcv[i-35:i+1]])
        
        bias = "NEUTRAL"
        score = 0
        config = {}
        
        if mode == "SUPREME":
            config = get_supreme_config(symbol, intel["trend_strong"])
            if abs(intel["psi"]) > config["threshold"]: 
                score = 60 + (abs(intel["psi"])*10)
                bias = "GOD_LONG" if intel["psi"] > 0 else "GOD_SHORT"
            if (bias == "GOD_LONG" and intel["rsi"] > 70) or (bias == "GOD_SHORT" and intel["rsi"] < 30): score = 0
            
        elif mode == "SNIPER":
            config = get_sniper_config(symbol)
            if intel["rsi"] < 20: bias = "GOD_LONG"; score = 80
            elif intel["rsi"] > 80: bias = "GOD_SHORT"; score = 80
            
        if score >= config["min_score"]:
            entry = ohlcv[i][4]
            atr = intel["atr"]
            sl_dist = atr * config["sl_mult"]
            tp_dist = atr * config["tp_mult"]
            
            pnl = 0
            # Simula futuro (120 min)
            for j in range(i+1, min(i+120, len(ohlcv))):
                f = ohlcv[j]
                if bias == "GOD_LONG":
                    if f[2] >= entry + tp_dist: pnl = config["tp_mult"] * (atr/entry) * 100; break
                    if f[3] <= entry - sl_dist: pnl = -config["sl_mult"] * (atr/entry) * 100; break
                else:
                    if f[3] <= entry - tp_dist: pnl = config["tp_mult"] * (atr/entry) * 100; break
                    if f[2] >= entry + sl_dist: pnl = -config["sl_mult"] * (atr/entry) * 100; break
            
            pnl -= 0.06
            if pnl != -0.06:
                sim["pnl"] += pnl
                sim["trades"] += 1
                if pnl > 0: sim["wins"] += 1
                i += 10 # Pula candles

    return {"symbol": symbol, "total_pnl_percent": round(sim["pnl"], 2), "total_trades": sim["trades"]}
