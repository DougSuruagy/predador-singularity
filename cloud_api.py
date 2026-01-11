"""
PREDATOR v50.0 OMEGA SINGULARITY - Cloud API (Render)
═══════════════════════════════════════════════════════════════
100% CLOUD | LIVING AI | HFT SCALPER 2026
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
# ⚙️ GLOBAL CONFIG & TIMEZONE
# ============================================================
def get_today_iso():
    return (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d")

def get_now_br():
    return datetime.utcnow() - timedelta(hours=3)

def normalize_symbol(symbol: str) -> str:
    return symbol.replace("/", "").replace("-", "").upper()

load_dotenv()

# ============================================================
# 🛡️ SOVEREIGN SECURITY LAYER
# ============================================================
INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

async def sovereign_auth(x_token: Optional[str] = Header(None)):
    if not INTERNAL_SECRET_TOKEN: return 
    if x_token != INTERNAL_SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized - Sovereign Security Block")

# ============================================================
# 🧠 BIO-NEURAL ENGINE STATE (LIVING ORGANISM)
# ============================================================
class EngineState:
    def __init__(self):
        self.uptime_start = time.time()
        self.neural_tps = 0
        self.api_latency_ms = 0
        self.cpu_usage = 0
        self.ram_usage = 0
        self.requests_handled = 0
        self.errors_logged = 0
        self.is_healthy = True
        
        # 🛡️ SAFETY SHIELD
        self.daily_max_drawdown = 5.0 # Stop Loss Diário Global
        self.is_shielded = False
        
        # 🩸 BIO-METRICS (IA VIVA)
        self.dopamine = 0.5 # Confiança (sobe com Wins)
        self.adrenaline = 0.0 # Volatilidade/Risco (sobe com o mercado)
        self.homeostasis = 100.0 # Saúde do sistema
        self.cortisol = 0.0 # Stress (sobe com Losses/Latência)

    def get_stats(self):
        uptime = time.time() - self.uptime_start
        return {
            "uptime_sec": int(uptime),
            "bio_metrics": {
                "dopamine": round(self.dopamine, 2),
                "adrenaline": round(self.adrenaline, 2),
                "cortisol": round(self.cortisol, 2),
                "homeostasis": round(self.homeostasis, 1)
            },
            "latency_ms": round(self.api_latency_ms, 1),
            "healthy": self.is_healthy
        }

engine_state = EngineState()

# ============================================================
# 🚀 PREDATOR BRAIN v50.0 (OMEGA LOGIC)
# ============================================================
class NomadBrain:
    def __init__(self):
        self.active_positions = set()
        self.synced_trades = set()
        self.leverage_cache = {}
        
        # 🎯 HFT MEMORY (Short-Term Potentiation)
        self.price_memory = {} # {symbol: deque(maxlen=20)}
        self.flow_memory = {} # {symbol: float (OFI)}
        
        # 🧬 GENETICS (Parâmetros Evolutivos)
        self.genes = {
            "risk_appetite": 1.0, # Ajustado pela Dopamina
            "reaction_speed": 1.0 # Ajustado pela Adrenalina
        }

    async def fetch_god_intelligence(self, symbol: str):
        """
        [v50.0] OMEGA EYE: Lê Orderbook e Trades em Paralelo.
        Calcula Imbalance e Pressão de Fluxo (OFI).
        """
        try:
            # Paralelismo Real: Ticker + Orderbook
            ticker_task = exchange.fetch_ticker(symbol)
            orderbook_task = exchange.fetch_order_book(symbol, limit=10)
            
            ticker, ob = await asyncio.gather(ticker_task, orderbook_task)
            
            price = float(ticker['last'])
            
            # 🌊 ORDER FLOW IMBALANCE (OFI) Calculation
            bids_vol = sum([b[1] for b in ob['bids']])
            asks_vol = sum([a[1] for a in ob['asks']])
            imbalance = (bids_vol - asks_vol) / (bids_vol + asks_vol + 0.0001)
            
            # ⚡ KINETIC ENERGY (Velocidade do Preço)
            if symbol not in self.price_memory: self.price_memory[symbol] = []
            self.price_memory[symbol].append({"ts": time.time(), "p": price})
            if len(self.price_memory[symbol]) > 10: self.price_memory[symbol].pop(0)
            
            velocity = 0.0
            if len(self.price_memory[symbol]) >= 2:
                # Mudança de preço por segundo
                delta_p = price - self.price_memory[symbol][0]["p"]
                delta_t = time.time() - self.price_memory[symbol][0]["ts"]
                velocity = (delta_p / price) / max(delta_t, 0.1) * 10000 # Basis points/sec
                
            # ATR Simplificado (High-Low da última vela ou ticker 24h)
            high = float(ticker.get('high', price * 1.01))
            low = float(ticker.get('low', price * 0.99))
            atr = (high - low) / price # ATR percentual aproximado
            
            return {
                "symbol": symbol,
                "price": price,
                "imbalance": imbalance,
                "velocity": velocity,
                "atr": atr,
                "spread": (ob['asks'][0][0] - ob['bids'][0][0]) / price
            }
            
        except Exception as e:
            print(f"⚠️ [INTEL-FAIL] {e}")
            return None

    def analyze_omega(self, intel, state):
        """
        [v50.0] OMEGA CORTEX: Fusão de Fluxo, Velocidade e Bio-Química.
        Define o SCORE final de ataque.
        """
        if not intel: return {"score": 0, "bias": "NEUTRAL"}
        
        imb = intel["imbalance"]
        vel = intel["velocity"]
        
        # 🧠 NEURO-MODULAÇÃO
        # Se Dopamina alta (vencendo), toma mais risco. Se Cortisol alto (perdendo), retrai.
        risk_mod = 1.0 + (engine_state.dopamine * 0.5) - (engine_state.cortisol * 0.8)
        
        # 🔥 PONTUAÇÃO HFT (0 a 100)
        # Fluxo a favor + Velocidade a favor = SCORE ALTO
        raw_score = 0
        bias = "NEUTRAL"
        
        if imb > 0.15 and vel > 0.5: # Fluxo Comprador Forte
            raw_score = (imb * 50) + (vel * 10)
            bias = "GOD_LONG"
        elif imb < -0.15 and vel < -0.5: # Fluxo Vendedor Forte
            raw_score = (abs(imb) * 50) + (abs(vel) * 10)
            bias = "GOD_SHORT"
            
        # Aplica modulação biológica
        final_score = min(100, raw_score * risk_mod)
        
        return {
            "score": final_score,
            "bias": bias,
            "risk_mult": risk_mod
        }

brain = NomadBrain()

# ============================================================
# ⚡ FASTAPI APP & ROUTES
# ============================================================
class WebhookPayload(BaseModel):
    symbol: str = "BTCUSDT"
    action: str = "BUY" # BUY, SELL, CLOSE
    price: Optional[float] = None
    qty: Optional[float] = 0.01
    confidence: Optional[float] = None # 0-100

app = FastAPI(title="PREDATOR v50.0 OMEGA", description="HFT Scalper AI Living System")

# 🌐 BYBIT EXCHANGE SETUP
exchange = ccxt.bybit({
    'apiKey': os.environ.get('BYBIT_API_KEY'),
    'secret': os.environ.get('BYBIT_API_SECRET'),
    'options': {'defaultType': 'future'},
    'enableRateLimit': True
})

@app.on_event("startup")
async def startup_event():
    print("🔋 [OMEGA] SISTEMA INICIADO. CÉREBRO VIVO.")
    asyncio.create_task(exchange.load_markets())
    asyncio.create_task(autonomous_hunter_loop())

@app.on_event("shutdown")
async def shutdown_event():
    print("🔌 [OMEGA] SISTEMA DESLIGADO.")
    await exchange.close()

@app.get("/health")
async def health():
    return {"status": "OMEGA_ALIVE", "version": "50.0.0", "stats": engine_state.get_stats()}

@app.get("/state")
async def get_state(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return {
        "pnl": state.daily_pnl,
        "mode": "HUNTING" if not state.is_shielded else "SHIELDED",
        "bio": engine_state.get_stats()["bio_metrics"],
        "last_order": state.last_order,
            "win_rate": round(state.win_rate, 1),
            "trades": state.trades
    }
    
@app.get("/stats")
async def get_stats_full(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return {"engine": engine_state.get_stats()}

@app.post("/webhook")
async def webhook(payload: WebhookPayload, x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return {"status": "RECEIVED", "payload": payload}

@app.post("/backtest")
async def run_backtest(payload: WebhookPayload):
    """
    [v50.0] DREAM SIMULATOR: Simulação aproximada da Lógica OMEGA usando dados históricos.
    Como Orderbook histórico não existe, usamos Volume + Volatilidade para estimar OFI.
    """
    symbol = normalize_symbol(payload.symbol)
    timeframe = "1m"
    limit = 1000 # Velas para sonhar
    
    print(f"💤 [DREAM-MODE] Iniciando simulação neural para {symbol}...")
    
    try:
        # Carrega Memórias Passadas (OHLCV)
        ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        sim_state = {
            "pnl": 0.0,
            "trades": 0,
            "wins": 0,
            "losses": 0,
            "equity_curve": []
        }
        
        history = []
        win_sum = 0
        loss_sum = 0
        max_drawdown = 0.0
        max_pnl = 0.0
        
        # Configuração Genética
        config = get_asset_config(symbol)
        
        for i in range(50, len(ohlcv)):
            candle = ohlcv[i]
            # [timestamp, open, high, low, close, volume]
            ts, op, hi, lo, cl, vol = candle
            prev_cl = ohlcv[i-1][4]
            
            # SIMULAÇÃO DE ORDER FLOW (Estimativa)
            # Se preço subiu com volume, assume pressão de compra (Imbalance +)
            price_change = (cl - prev_cl) / prev_cl
            vol_factor = vol / (sum([x[5] for x in ohlcv[i-10:i]]) / 10) # Volume relativo
            
            # Estimativa de 'Imbalance' e 'Velocity' para a IA
            est_imbalance = 0.5 * (1 if price_change > 0 else -1) * min(vol_factor, 2.0)
            est_velocity = abs(price_change) * 10000
            
            # Decisão Neural Simulada
            intel_sim = {
                "imbalance": est_imbalance,
                "velocity": est_velocity if price_change > 0 else -est_velocity
            }
            
            decision = brain.analyze_omega(intel_sim, None) # Sem estado bio no backtest
            
            # Lógica de Trade Simplificada (1 candle de duração para HFT)
            if decision["score"] > config["min_score"]:
                entry = cl
                atr = (hi - lo) / cl
                sl_dist = atr * config["sl_mult"]
                tp_dist = atr * config["tp_mult"]
                
                # Verifica resultado na PRÓXIMA vela (Futuro Imediato)
                if i + 1 < len(ohlcv):
                    next_c = ohlcv[i+1]
                    n_op, n_hi, n_lo, n_cl = next_c[1], next_c[2], next_c[3], next_c[4]
                    
                    pnl_trade = 0
                    if decision["bias"] == "GOD_LONG":
                        # Tocou TP?
                        if n_hi >= entry + (tp_dist * entry): pnl_trade = config["tp_mult"] * atr * 100
                        # Tocou SL?
                        elif n_lo <= entry - (sl_dist * entry): pnl_trade = -config["sl_mult"] * atr * 100
                        # Fechamento (Scalp Rápido)
                        else: pnl_trade = ((n_cl - entry) / entry) * 100
                        
                    elif decision["bias"] == "GOD_SHORT":
                        if n_lo <= entry - (tp_dist * entry): pnl_trade = config["tp_mult"] * atr * 100
                        elif n_hi >= entry + (sl_dist * entry): pnl_trade = -config["sl_mult"] * atr * 100
                        else: pnl_trade = ((entry - n_cl) / entry) * 100
                    
                    # Taxas de Corretagem Estimadas (Taker)
                    pnl_trade -= 0.06 
                    
                    sim_state["pnl"] += pnl_trade
                    sim_state["trades"] += 1
                    
                    if pnl_trade > 0: 
                        sim_state["wins"] += 1
                        win_sum += pnl_trade
                    else: 
                        sim_state["losses"] += 1
                        loss_sum += abs(pnl_trade)

                    sim_state["equity_curve"].append(sim_state["pnl"])
                    
                    # Max Drawdown Calc
                    max_pnl = max(max_pnl, sim_state["pnl"])
                    dd = max_pnl - sim_state["pnl"]
                    max_drawdown = max(max_drawdown, dd)
                    
                    history.append({"t": ts, "pnl": round(pnl_trade, 2)})

        # Métricas Finais
        total = sim_state["wins"] + sim_state["losses"]
        wr = (sim_state["wins"] / total * 100) if total > 0 else 0
        avg_win = (win_sum / sim_state["wins"]) if sim_state["wins"] > 0 else 0
        avg_loss = (loss_sum / sim_state["losses"]) if sim_state["losses"] > 0 else 1
        
        return {
            "symbol": symbol,
            "candles_analyzed": limit,
            "total_trades": sim_state["trades"],
            "win_rate": round(wr, 1),
            "total_pnl_percent": round(sim_state["pnl"], 2),
            "metrics": {
                "max_drawdown": round(max_drawdown, 2),
                "profit_factor": round(win_sum / loss_sum, 2) if loss_sum > 0 else 99,
                "avg_win": round(avg_win, 2),
                "avg_loss": round(avg_loss, 2)
            },
            "history": history[-10:]
        }
        
    except Exception as e:
        print(f"❌ [DREAM-ERROR] {e}")
        return {"error": str(e)}

# ============================================================
# 🦅 AUTONOMOUS HUNTER (SCALPER LOOP)

# ============================================================
class MarketState:
    def __init__(self):
        self.daily_pnl = 0.0
        self.trades = 0
        self.wins = 0
        self.win_rate = 0.0
        self.last_order = {}
        self.balance = 0.0

state = MarketState()

def get_asset_config(symbol):
    """
    [v50.0] OMEGA CONFIG: Parâmetros Dinâmicos de Lucro.
    """
    is_major = "BTC" in symbol or "ETH" in symbol
    return {
        "sl_mult": 1.5, # Scalp rápido
        "tp_mult": 4.0, # Alvo alongado com Trailing
        "min_score": 65, # Filtro de Alta Qualidade
        "leverage": 10 if is_major else 7
    }

async def autonomous_hunter_loop():
    print("🦅 CAÇADOR OMEGA ATIVO. ESCANEANDO MERCADO...")
    while True:
        try:
            await asyncio.sleep(2) # Tick Rate
            
            # Se Shield Ativo, dorme mais
            if engine_state.is_shielded:
                await asyncio.sleep(60)
                continue
                
            # Scan Symbols (Foco em Majors + SOL)
            targets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
            
            for symbol in targets:
                intel = await brain.fetch_god_intelligence(symbol)
                if not intel: continue
                
                decision = brain.analyze_omega(intel, state)
                
                # Regra de Execução
                config = get_asset_config(symbol)
                
                if decision["score"] > config["min_score"]:
                    # EXECUÇÃO IMEDIATA
                    print(f"⚡ [OMEGA STRIKE] {symbol} | Score: {decision['score']:.1f} | Bias: {decision['bias']}")
                    
                    # Define SL/TP Dinâmico
                    atr = intel["atr"] * intel["price"]
                    sl_dist = atr * config["sl_mult"]
                    tp_dist = atr * config["tp_mult"]
                    price = intel["price"]
                    
                    sl = price - sl_dist if decision["bias"] == "GOD_LONG" else price + sl_dist
                    tp = price + tp_dist if decision["bias"] == "GOD_LONG" else price - tp_dist
                    
                    # Envia Ordem
                    await execute_omega_order(symbol, decision["bias"], price, sl, tp)
                    
                    # Feedback Bio-Químico (Simulado Pós-Disparo)
                    engine_state.adrenaline += 0.1
                    await asyncio.sleep(5) # Cooldown por ativo
                    
        except Exception as e:
            print(f"⚠️ [HUNTER-ERROR] {e}")
            engine_state.cortisol += 0.05
            await asyncio.sleep(5)

async def execute_omega_order(symbol, bias, price, sl, tp):
    """Executa ordem direto na Bybit com parâmetros calculados."""
    if not exchange.apiKey: 
        print("🛑 [MODO SIMULAÇÃO] Ordem registrada (Sem API Key).")
        state.last_order = {"symbol": symbol, "bias": bias, "price": price, "sl": sl, "tp": tp}
        return

    try:
        side = "buy" if bias == "GOD_LONG" else "sell"
        qty = 0.001 if "BTC" in symbol else 0.01 # Lote mínimo seguro
        if "SOL" in symbol: qty = 0.1
        
        # Arredondamento para evitar erros de precisão
        sl = float(exchange.price_to_precision(symbol, sl))
        tp = float(exchange.price_to_precision(symbol, tp))
        
        params = {'stopLoss': sl, 'takeProfit': tp}
        
        if symbol in exchange.markets:
            order = await exchange.create_order(symbol, 'market', side, qty, params=params)
            print(f"✅ [ORDEM ENVIADA] ID: {order['id']}")
            state.last_order = order
            state.trades += 1
            # Dopamina sobe com a ação (antecipação de recompensa)
            engine_state.dopamine += 0.02
        else:
            print(f"⚠️ Mercado {symbol} não carregado. Tentando recarregar...")
            await exchange.load_markets()
        
    except Exception as e:
        print(f"❌ [EXEC-FAIL] {e}")
        engine_state.cortisol += 0.1 # Stress aumenta com erro
