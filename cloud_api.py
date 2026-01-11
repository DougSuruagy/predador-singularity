"""
PREDATOR v51.0 GOLDEN OMEGA - Cloud API (Render)
═══════════════════════════════════════════════════════════════
GOLDEN RATIO (Safety) + OMEGA BRAIN (HFT Intelligence)
FUSÃO SUPREMA: SL 1.8x | TP 6.0x | HFT ORDER FLOW
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
import httpx
from contextlib import asynccontextmanager

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
        raise HTTPException(status_code=401, detail="Unauthorized - Sovereign Security Block")

# ============================================================
# 🧠 BIO-NEURAL ENGINE STATE (LIVING ORGANISM v51)
# ============================================================
class EngineState:
    def __init__(self):
        self.uptime_start = time.time()
        self.is_healthy = True
        self.daily_max_drawdown = 5.0 
        self.is_shielded = False
        
        # 🩸 BIO-METRICS (Ajuste Fino v51)
        self.dopamine = 0.5 # Começa neutro
        self.adrenaline = 0.0 # Reativo ao mercado
        self.homeostasis = 100.0 
        self.cortisol = 0.0

    def get_stats(self):
        uptime = time.time() - self.uptime_start
        return {
            "uptime_sec": int(uptime),
            "bio": {
                "dopamine": round(self.dopamine, 2),
                "adrenaline": round(self.adrenaline, 2),
                "cortisol": round(self.cortisol, 2),
                "homeostasis": round(self.homeostasis, 1)
            }
        }

engine_state = EngineState()

# ============================================================
# 🚀 PREDATOR BRAIN v51.0 (GOLDEN OMEGA LOGIC)
# ============================================================
class NomadBrain:
    def __init__(self):
        self.price_memory = {} 
        self.genes = {"risk_appetite": 1.0}

    async def fetch_god_intelligence(self, symbol: str):
        """
        [v51.0] OMEGA EYE: Leitura HFT Real.
        """
        try:
            ticker_task = exchange.fetch_ticker(symbol)
            orderbook_task = exchange.fetch_order_book(symbol, limit=10)
            ticker, ob = await asyncio.gather(ticker_task, orderbook_task)
            
            price = float(ticker['last'])
            
            # 🌊 ORDER FLOW IMBALANCE (OFI)
            bids_vol = sum([b[1] for b in ob['bids']])
            asks_vol = sum([a[1] for a in ob['asks']])
            imbalance = (bids_vol - asks_vol) / (bids_vol + asks_vol + 0.0001)
            
            # ⚡ KINETIC ENERGY
            if symbol not in self.price_memory: self.price_memory[symbol] = []
            self.price_memory[symbol].append({"ts": time.time(), "p": price})
            if len(self.price_memory[symbol]) > 10: self.price_memory[symbol].pop(0)
            
            velocity = 0.0
            if len(self.price_memory[symbol]) >= 2:
                delta_p = price - self.price_memory[symbol][0]["p"]
                delta_t = time.time() - self.price_memory[symbol][0]["ts"]
                velocity = (delta_p / price) / max(delta_t, 0.1) * 10000 
                
            # ATR (Volatilidade)
            high = float(ticker.get('high', price * 1.01))
            low = float(ticker.get('low', price * 0.99))
            atr = (high - low) / price 
            
            return {
                "symbol": symbol,
                "price": price,
                "imbalance": imbalance,
                "velocity": velocity,
                "atr": atr
            }
        except Exception as e:
            print(f"⚠️ [INTEL-FAIL] {e}")
            return None

    def analyze_golden_omega(self, intel, state):
        """
        [v51.0] GOLDEN CORTEX: Segurança v44.2 + Precisão v50.0.
        """
        if not intel: return {"score": 0, "bias": "NEUTRAL"}
        
        imb = intel["imbalance"]
        vel = intel["velocity"]
        
        # 🧠 FUSÃO: Só ataca se Fluxo E Velocidade confirmarem (Golden Rule)
        raw_score = 0
        bias = "NEUTRAL"
        
        # Thresholds HFT Ajustados (Mais sensíveis que v50, mas filtrados pelo Score v44)
        if imb > 0.12 and vel > 0.3: 
            raw_score = (imb * 50) + (vel * 15) + (engine_state.dopamine * 10)
            bias = "GOD_LONG"
        elif imb < -0.12 and vel < -0.3: 
            raw_score = (abs(imb) * 50) + (abs(vel) * 15) + (engine_state.dopamine * 10)
            bias = "GOD_SHORT"
            
        return {"score": min(100, raw_score), "bias": bias}

brain = NomadBrain()

# ============================================================
# ⚡ FASTAPI APP
# ============================================================
class WebhookPayload(BaseModel):
    symbol: str = "BTCUSDT"
    action: str = "BUY"
    price: Optional[float] = None
    qty: Optional[float] = 0.01

app = FastAPI(title="PREDATOR v51.0 GOLDEN OMEGA", docs_url=None, redoc_url=None)

exchange = ccxt.bybit({
    'apiKey': os.environ.get('BYBIT_API_KEY'),
    'secret': os.environ.get('BYBIT_API_SECRET'),
    'options': {'defaultType': 'future'},
    'enableRateLimit': True
})

@app.on_event("startup")
async def startup_event():
    print("🔋 [GOLDEN OMEGA] SISTEMA INICIADO. FUSÃO ATIVA.")
    asyncio.create_task(exchange.load_markets())
    asyncio.create_task(autonomous_hunter_loop())

@app.on_event("shutdown")
async def shutdown_event():
    print("🔌 [GOLDEN OMEGA] DESLIGANDO...")
    await exchange.close()

@app.get("/health")
async def health():
    return {"status": "ALIVE", "version": "51.0.0", "stats": engine_state.get_stats()}

@app.get("/state")
async def get_state(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return {
        "pnl": state.daily_pnl,
        "mode": "HUNTING" if not state.is_shielded else "SHIELDED",
        "bio": engine_state.get_stats()["bio"],
        "last_order": state.last_order,
        "trades": state.trades
    }

# ============================================================
# 🦅 AUTONOMOUS HUNTER (GOLDEN OMEGA LOOP)
# ============================================================
class MarketState:
    def __init__(self):
        self.daily_pnl = 0.0
        self.trades = 0
        self.wins = 0
        self.last_order = {}
        self.balance = 0.0

state = MarketState()

def get_asset_config(symbol):
    """
    [v51.0] GOLDEN OMEGA CONFIG: A Fusão Real.
    Mantém a Segurança A-CLASS do v44.2 (SL 1.8 / TP 6.0).
    Usa Score 55 (Sniper) para validar o HFT da v50.
    """
    is_sol = "SOL" in symbol or "PEPE" in symbol
    is_major = "BTC" in symbol or "ETH" in symbol
    
    # RRR DOURADO (1.8x / 6.0x) - Estatisticamente Superior
    return {
        "threshold": 0.28 if is_sol else 0.22,
        "sl_mult": 1.8, # Segurança Valhalla
        "tp_mult": 6.0, # Lucro Otimizado
        "min_score": 55, # Gatilho Sniper (Exige confirmação HFT forte)
        "leverage": 10 if is_major else 7
    }

async def autonomous_hunter_loop():
    print("🦅 CAÇADOR GOLDEN OMEGA ATIVO. ESCANEANDO COM PRECISÃO...")
    while True:
        try:
            await asyncio.sleep(2)
            if engine_state.is_shielded:
                await asyncio.sleep(60)
                continue
                
            targets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
            
            for symbol in targets:
                intel = await brain.fetch_god_intelligence(symbol)
                if not intel: continue
                
                decision = brain.analyze_golden_omega(intel, state)
                config = get_asset_config(symbol)
                
                # FUSÃO: Decisão HFT (v50) deve superar Score Golden (v44)
                if decision["score"] > config["min_score"]:
                    print(f"⚡ [GOLDEN STRIKE] {symbol} | Score: {decision['score']:.1f} | Bias: {decision['bias']}")
                    
                    atr = intel["atr"] * intel["price"]
                    sl_dist = atr * config["sl_mult"]
                    tp_dist = atr * config["tp_mult"]
                    price = intel["price"]
                    
                    sl = price - sl_dist if decision["bias"] == "GOD_LONG" else price + sl_dist
                    tp = price + tp_dist if decision["bias"] == "GOD_LONG" else price - tp_dist
                    
                    if not exchange.apiKey:
                        print("🛑 [SIMULAÇÃO] Ordem Detectada (Sem Chave).")
                        continue
                        
                    # Execução Real
                    qty = 0.001 if "BTC" in symbol else 0.01
                    if "SOL" in symbol: qty = 0.1
                    
                    side = "buy" if decision["bias"] == "GOD_LONG" else "sell"
                    params = {'stopLoss': float(exchange.price_to_precision(symbol, sl)), 
                              'takeProfit': float(exchange.price_to_precision(symbol, tp))}
                    
                    try:
                        if symbol in exchange.markets:
                            order = await exchange.create_order(symbol, 'market', side, qty, params=params)
                            print(f"✅ [ORDEM EXECUTADA] {symbol} | ID: {order['id']}")
                            state.last_order = order
                            state.trades += 1
                            engine_state.dopamine += 0.05
                            engine_state.adrenaline += 0.1
                        else:
                            await exchange.load_markets()
                    except Exception as ex:
                        print(f"❌ [EXEC ERROR] {ex}")
                        engine_state.cortisol += 0.1
                    
                    await asyncio.sleep(5)
                    
        except Exception as e:
            print(f"⚠️ [Loop Error] {e}")
            await asyncio.sleep(5)

# ============================================================
# 💤 DREAM SIMULATOR (ADAPTED FOR v51)
# ============================================================
@app.post("/backtest")
async def run_backtest(payload: WebhookPayload):
    """
    [v51.0] HYBRID SIMULATOR: Tenta aproximar a lógica de fusão.
    """
    symbol = normalize_symbol(payload.symbol)
    limit = 1000
    ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=limit)
    
    sim_stats = {"pnl": 0.0, "trades": 0, "wins": 0}
    config = get_asset_config(symbol)
    
    for i in range(50, len(ohlcv)-1):
        c = ohlcv[i]
        vol_factor = c[5] / (sum([x[5] for x in ohlcv[i-10:i]]) / 10)
        
        # Simulação HFT baseada em Volume Spike + Tendência
        trend = (c[4] - ohlcv[i-1][4])
        score = 0
        bias = "NEUTRAL"
        
        if vol_factor > 1.5 and abs(trend) > 0:
            score = 60 # Assume score alto se houver volume forte
            bias = "GOD_LONG" if trend > 0 else "GOD_SHORT"
            
        if score > config["min_score"]:
            entry = c[4]
            atr = (c[2] - c[3]) / c[4]
            sl_dist = atr * config["sl_mult"]
            tp_dist = atr * config["tp_mult"]
            
            # Checa próximo candle
            next_c = ohlcv[i+1]
            pnl = 0
            if bias == "GOD_LONG":
                if next_c[2] >= entry + (tp_dist * entry): pnl = config["tp_mult"] * atr * 100
                elif next_c[3] <= entry - (sl_dist * entry): pnl = -config["sl_mult"] * atr * 100
            else:
                 if next_c[3] <= entry - (tp_dist * entry): pnl = config["tp_mult"] * atr * 100
                 elif next_c[2] >= entry + (sl_dist * entry): pnl = -config["sl_mult"] * atr * 100
            
            # Spread cost
            pnl -= 0.05
            
            if pnl != -0.05: # Teve ação real
                sim_stats["pnl"] += pnl
                sim_stats["trades"] += 1
                if pnl > 0: sim_stats["wins"] += 1

    return sim_stats
