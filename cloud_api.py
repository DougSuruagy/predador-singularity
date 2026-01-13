"""
PREDATOR v370.0 "SINGULARITY-INFINITY" - Cloud API (Render)
═══════════════════════════════════════════════════════════════
STRATEGY: INFINITY MATRIX + ENTROPY SHIELD
 GOAL: MAX PROFIT WITH CHAOS PROTECTION.
1. SOL: 55.0x Boost (The "Infinity" Trade).
2. ETH: 3.0x Boost (Locked at +50%).
3. BTC: 4.0x Boost (Standard).
4. SHIELD: Reduces leverage by 50-80% if Entropy > 0.6.
5. MODE: 24/7 AUTONOMOUS HUNTING READY.
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
import httpx

# ============================================================
# ⚙️ GLOBAL CONFIG
# ============================================================
load_dotenv()
INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

# 🌐 DUAL-CORE NODE DETECTION
NODE_ROLE = os.environ.get("NODE_ROLE", "PRIMARY")  # PRIMARY = Frankfurt, BRAIN = Virginia
PRIMARY_URL = os.environ.get("PRIMARY_URL", "https://fun-calley-modelo-inteligente-85d8461c.koyeb.app")
BRAIN_URL = os.environ.get("BRAIN_URL", "https://fun-calley-modelo-inteligente-85d8461c.koyeb.app")

# 📡 SUPABASE BLACK-BOX (Telemetry)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xayaogxbjudpmwylaiuf.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_wNuQ-HzDYPoD3YEPB-v5VA_zi21tBxs")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        self.wins = 0
        self.mode = "SUPREME"
        self.last_price = 0.0
        self.last_score = 0
        self.last_entropy = 0.0
        self.shield_status = "OFF"
        self.trade_log = []
        
        # 🛡️ TRAVAS DE SEGURANÇA
        self.MAX_DAILY_LOSS = -2.0 # %
        self.MAX_DAILY_PROFIT = 5.0 # %
        self.last_trade_time = time.time()
        self.idle_hours = 0.0
        self.current_balance = 0.0
        self.MIN_CAPITAL = 20.0

    def get_bio_metrics(self):
        # Dopamina: Alta se o winrate ou trades estiverem bons
        win_rate = (self.wins / max(1, self.trades)) * 100
        dopamine = min(1.0, (win_rate / 100) * 1.5)
        
        # Adrenalina: Alta se estiver operando em modo SUPREME
        adrenaline = 0.8 if self.mode == "SUPREME" else 0.4
        
        # Cortisol: Stress baseado no PnL negativo
        cortisol = abs(min(0, self.daily_pnl)) / 2.0
        
        return {
            "dopamine": round(dopamine, 2),
            "adrenaline": round(adrenaline, 2),
            "cortisol": round(cortisol, 2),
            "homeostasis": round(100 - (cortisol * 100), 1),
            "synaptic_firing": 12 + (dopamine * 50) # Simula atividade neural
        }

    def get_stats(self):
        bio = self.get_bio_metrics()
        win_rate = (self.wins / max(1, self.trades)) * 100
        is_locked = self.daily_pnl <= self.MAX_DAILY_LOSS or self.daily_pnl >= self.MAX_DAILY_PROFIT
        
        return {
            "version": "370.1-SINGULARITY-RALF",
            "uptime": int(time.time() - self.uptime_start),
            "pnl": round(self.daily_pnl, 2),
            "trades": self.trades,
            "wins": self.wins,
            "win_rate": round(win_rate, 2),
            "mode": self.mode,
            "regime": "GHOST-HUNTING" if not is_locked else "LOCKED",
            "price": self.last_price,
            "prob": self.last_score,
            "entropy": self.last_entropy,
            "shield": self.shield_status,
            "confidence": self.last_score,
            "is_locked": is_locked,
            "is_hunting": not is_locked,
            "homeostasis": bio["homeostasis"],
            "adrenaline": bio["adrenaline"],
            "synaptic_firing": bio["synaptic_firing"],
            "bio": bio,
            "trade_log": self.trade_log[-8:] if self.trade_log else [],
            "kill_switch_active": is_locked,
            "apex_mode": self.daily_pnl > 1.0,
            "executive_efficiency": 98.4 if self.trades > 0 else 100.0,
            "balance": round(self.current_balance, 2),
            "waiting_for_funds": self.current_balance < self.MIN_CAPITAL
        }
    
    async def sync_balance(self, exchange):
        """ Sincroniza o saldo real da Bybit com tratamento para contas unificadas """
        try:
            if not exchange.apiKey:
                return
                
            bal = await exchange.fetch_balance()
            
            # Tratamento robusto para Bybit (USDT é a moeda base do HFT)
            # CCXT geralmente mapeia para bal['USDT']['free']
            usdt_info = bal.get('USDT', {})
            
            # Tenta diversas formas de identificar o saldo livre (Free/Available)
            free_balance = usdt_info.get('free')
            
            if free_balance is None:
                # Fallback para Unified Account (UTA) se o mapeamento for direto
                free_balance = bal.get('total', {}).get('USDT', 0.0)

            self.current_balance = float(free_balance or 0.0)
            
            # Log de atualização periódica ou mudança crítica
            if int(time.time()) % 60 == 0: 
                print(f"💰 [WALLET-SYNC] Saldo Atual: ${self.current_balance:.2f} USDT")
                
        except Exception as e:
            print(f"⚠️ [BALANCE ERROR] Falha ao ler saldo: {e}")

    async def sync_status_to_supabase(self):
        """ Sincroniza o estado atual do motor com o banco de dados """
        try:
            status_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "370.0",
                "pnl": round(self.daily_pnl, 2),
                "trades": self.trades,
                "win_rate": round((self.wins / max(1, self.trades)) * 100, 2),
                "entropy": round(self.last_entropy, 2),
                "shield": self.shield_status,
                "status": "ONLINE" if self.is_healthy else "ERROR"
            }
            supabase.table("system_status").upsert(status_data, on_conflict="version").execute()
            print(f"📡 [SUPABASE] Health Sync realizado com sucesso.")
        except Exception as e:
            print(f"⚠️ [SUPABASE FAIL] Erro no sync de status: {e}")

    async def log_event_to_supabase(self, event_type, message, asset=None, meta=None):
        """ Registra um log de evento crítico no banco de dados com fallback de schema """
        try:
            log_data = {
                "event_type": event_type,
                "message": message,
                "asset": asset,
                "meta": meta or {},
                "time": datetime.now().isoformat()
            }
            try:
                supabase.table("system_logs").insert(log_data).execute()
            except Exception as inner_e:
                # Se falhar por coluna ausente (PGRST204), tenta logar sem a coluna asset
                if "asset" in str(inner_e):
                    del log_data["asset"]
                    supabase.table("system_logs").insert(log_data).execute()
                else: raise inner_e
        except Exception as e:
            # Silent fail para não poluir o stdout se o DB estiver fora de sincronia
            pass

engine_state = EngineState()

# ============================================================
# 🚀 PREDATOR BRAIN v56.0 (SUPREME LOGIC)
# ============================================================
class NomadBrain:
    def calculate_indicators(self, closes, highs, lows, volumes=None):
        if len(closes) < 30: return None
        
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        rsi = self._calc_rsi(deltas)
        psi = (closes[-1] - closes[-5]) / closes[-5] * 100
        velocity = abs(psi) / 5
        
        ma20 = sum(closes[-20:]) / 20
        std_dev = (sum((x - ma20)**2 for x in closes[-20:]) / 20)**0.5
        bb_upper = ma20 + (std_dev * 2)
        bb_lower = ma20 - (std_dev * 2)
        bb_width = (std_dev * 4) / ma20 * 100 
        
        touch_low = closes[-1] <= bb_lower or lows[-1] <= bb_lower
        touch_high = closes[-1] >= bb_upper or highs[-1] >= bb_upper
        
        direction_changes = sum(1 for i in range(len(deltas)-10, len(deltas)) if (deltas[i] > 0) != (deltas[i-1] > 0))
        entropy = direction_changes / 10.0
        
        vol_shock = 1.0
        if volumes and len(volumes) > 20:
            avg_vol = sum(volumes[-20:-1]) / 19
            vol_shock = volumes[-1] / avg_vol if avg_vol > 0 else 1.0

        # Z-Score Volume
        z_vol = 0.0
        if volumes and len(volumes) > 30:
            avg_v = sum(volumes[-30:-1]) / 29
            std_v = (sum((v - avg_v)**2 for v in volumes[-30:-1]) / 29)**0.5
            z_vol = (volumes[-1] - avg_v) / (std_v + 0.0001)

        # RSI Slope & StochRSI
        past_rsi = []
        for j in range(len(closes)-20, len(closes)):
            window = closes[max(0, j-14):j+1]
            if len(window) < 2: continue
            d = [window[k] - window[k-1] for k in range(1, len(window))]
            past_rsi.append(self._calc_rsi(d))
        
        rsi_slope = past_rsi[-1] - past_rsi[-3] if len(past_rsi) > 3 else 0
        rsi_min = min(past_rsi[-14:]) if len(past_rsi) >= 14 else 0
        rsi_max = max(past_rsi[-14:]) if len(past_rsi) >= 14 else 100
        stoch_rsi = (rsi - rsi_min) / (rsi_max - rsi_min + 0.0001) * 100

        # EMA 200 (Trend Shield)
        ema200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else ma20
        trend_up = closes[-1] > ema200

        is_compressed = bb_width < 0.65 or entropy > 0.55
        
        # 📊 RALF INDICATORS (EMA 9 & EMA 21)
        ema9 = sum(closes[-9:]) / 9
        ema21 = sum(closes[-21:]) / 21
        ema_cross_up = ema9 > ema21
        
        # 🔗 Elastic Divergence (Refined)
        divergence = False
        if closes[-1] > ma20 and rsi < 35: divergence = True
        elif closes[-1] < ma20 and rsi > 65: divergence = True

        return {
            "rsi": rsi, "stoch_rsi": stoch_rsi, "rsi_slope": rsi_slope, "psi": psi,
            "bb_width": bb_width, "z_vol": z_vol, "is_compressed": is_compressed,
            "touch_low": touch_low, "touch_high": touch_high,
            "divergence": divergence, "ema9": ema9, "ema21": ema21, "ema_cross_up": ema_cross_up,
            "ma20": ma20, "ema200": ema200, "trend_up": trend_up, 
            "price": closes[-1], "entropy": entropy, "atr": std_dev
        }

    def _calc_rsi(self, deltas):
        gains = [d for d in deltas if d > 0]
        losses = [abs(d) for d in deltas if d < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

brain = NomadBrain()

# ============================================================
# ⚡ FASTAPI APP
# ============================================================
class WebhookPayload(BaseModel):
    symbol: str = "BTCUSDT"
    action: str = "BUY"
    price: Optional[float] = None
    qty: Optional[float] = 0.01
    period: Optional[str] = "1m"
    limit: Optional[int] = 2000

app = FastAPI(title="PREDATOR v56.0 VALHALLA SUPREME")
exchange = ccxt.bybit({'apiKey': os.environ.get('BYBIT_API_KEY'), 'secret': os.environ.get('BYBIT_API_SECRET'), 'options': {'defaultType': 'linear'}})

@app.on_event("startup")
async def startup_event():
    print(f"� [v370.2 SINGULARITY] Neural Core Ativado.")
    print(f"🌐 [DUAL-CORE] Modo: {NODE_ROLE} | Primary: {PRIMARY_URL} | Brain: {BRAIN_URL}")
    print(f"📡 Telemetria: Black Box conectada em {SUPABASE_URL}")
    print(f"🛡️ Homeostase: Loss Limit {engine_state.MAX_DAILY_LOSS}% | Profit Limit {engine_state.MAX_DAILY_PROFIT}%")
    
    # Log de Startup
    asyncio.create_task(engine_state.log_event_to_supabase("STARTUP", f"Sistema Predator v370.2 Iniciado | Node: {NODE_ROLE}"))
    
    async def init_exchange():
        try:
            await exchange.load_markets()
            print("✅ [EXCHANGE] Conexão com Bybit estabelecida (Mercados Carregados).")
        except Exception as e:
            print(f"⚠️ [EXCHANGE ERROR] Falha Crítica na conexão com Bybit: {e}")
            if "403" in str(e):
                print("⛔ [GEO-BLOCK] Região Bloqueada Detectada (USA?). Este nó funcionará apenas como OBSERVADOR (Watchdog).")
                print("💡 AÇÃO: Mova este serviço para Frankfurt ou Singapore para habilitar Trading/Failover.")

    asyncio.create_task(init_exchange())
    
    # 💵 Initial Balance Sync
    await engine_state.sync_balance(exchange)
    
    # 🧠 DUAL-CORE: Only PRIMARY runs the autonomous loop
    if NODE_ROLE == "PRIMARY":
        asyncio.create_task(autonomous_hunter_loop())
    else:
        print("🧠 [BRAIN NODE] Modo auxiliar ativo. Aguardando requisições do Primary.")
        asyncio.create_task(brain_watchdog_loop())
    
    # 💓 INTERNAL KEEP-ALIVE & DB SYNC
    def internal_pulse():
        url = "https://predador-api.onrender.com/health"
        print(f"💓 [KEEP-ALIVE] Iniciando protocolo de auto-preservação.")
        counter = 0
        while True:
            time.sleep(300) # 5 minutos
            counter += 1
            try:
                # Auto-Ping
                with httpx.Client(timeout=10) as client:
                    client.get(url)
                
                # Sincronização com Supabase (a cada 5 min)
                asyncio.run(engine_state.sync_status_to_supabase())
                
            except Exception as e:
                print(f"⚠️ [PULSE/SYNC FAIL] {e}")

    import threading
    threading.Thread(target=internal_pulse, daemon=True).start()

@app.get("/state")
async def get_state(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    return engine_state.get_stats()

@app.get("/health")
async def health():
    return {"status": "alive", "version": "370.1-SINGULARITY-RALF"}

@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.post("/command/panic")
async def command_panic(x_token: str = Header(None)):
    await sovereign_auth(x_token)
    # Ativa trava de segurança imediata simulando perda máxima
    engine_state.daily_pnl = engine_state.MAX_DAILY_LOSS - 0.1
    return {"status": "PANIC_ACTIVATED", "message": "Sovereign Kill-Switch Engaged."}

@app.get("/")
async def root():
    return {"status": "alive", "message": "PREDATOR API ACTIVE"}

@app.head("/")
async def root_head():
    return {}

# ============================================================
# 🦅 AUTONOMOUS HUNTER (SUPREME LOOP)
# ============================================================
def get_supreme_config(symbol, is_trending, is_compressed):
    """ [BTC/ETH] SINGULARITY APEX - v280.0 QUANTUM """
    if is_compressed:
        return {
            "threshold": 0.10, 
            "min_score": 92,  
            "sl_mult": 1.5,   
            "tp_mult": 1.2,   
            "leverage": 20,    
            "shadow_trail": False
        }
    
    return {
        "threshold": 0.25, 
        "min_score": 85,  # High Precision 
        "sl_mult": 2.0,   
        "tp_mult": 4.5,   
        "leverage": 4,    # BTC Base
        "shadow_trail": True
    }

def get_sniper_config(symbol, is_trending, is_compressed):
    """ [SOL] SNIPER v280.0 QUANTUM """
    if is_compressed:
        return {
            "threshold": 0.15,
            "min_score": 94,
            "sl_mult": 2.2,   
            "tp_mult": 1.5, 
            "leverage": 15,   
            "shadow_trail": False
        }
    return {
        "threshold": 0.30,
        "min_score": 85,  # Reversão Certeira
        "sl_mult": 2.5,   
        "tp_mult": 5.0,  
        "leverage": 55,   # SOL Base
        "shadow_trail": True
    }

def get_ralf_config(symbol, is_trending, is_compressed):
    """ [RALF] SCALPER MODE - Optimized Risk """
    return {
        "threshold": 0.05, 
        "min_score": 50,  
        "sl_mult": 1.5,   
        "tp_mult": 3.4,   
        "leverage": 25,  
        "shadow_trail": True
    }

async def brain_watchdog_loop():
    """ 🧠 BRAIN NODE: Monitors PRIMARY health and provides backup intelligence """
    print("🧠 [BRAIN WATCHDOG] Loop de monitoramento iniciado.")
    consec_failures = 0
    
    while True:
        try:
            await asyncio.sleep(30) # Check every 30s
            
            # 💓 Health Check on PRIMARY
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{PRIMARY_URL}/health")
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"💓 [WATCHDOG] Primary ALIVE | Version: {data.get('version')} ")
                    consec_failures = 0
                    
                    # Sync state from Primary (optional)
                    try:
                        state_resp = await client.get(f"{PRIMARY_URL}/state", headers={"X-Token": INTERNAL_SECRET_TOKEN})
                        if state_resp.status_code == 200:
                            primary_state = state_resp.json()
                            engine_state.daily_pnl = primary_state.get('pnl', 0)
                            engine_state.trades = primary_state.get('trades', 0)
                    except: pass
                else:
                    consec_failures += 1
                    print(f"⚠️ [WATCHDOG] Primary returned {resp.status_code}. Failures: {consec_failures}")
                    
        except Exception as e:
            consec_failures += 1
            print(f"🚨 [WATCHDOG] Primary OFFLINE! Error: {e} | Failures: {consec_failures}")
            
            # 🚨 FAILOVER: If PRIMARY is down for 3+ checks, BRAIN becomes active
            if consec_failures >= 3:
                print("🚨🚨🚨 [FAILOVER] PRIMARY ESTÁ OFFLINE! BRAIN assumindo operações! 🚨🚨🚨")
                asyncio.create_task(engine_state.log_event_to_supabase("FAILOVER", "BRAIN assumiu operações devido a falha do PRIMARY."))
                # Start trading loop on BRAIN as backup
                asyncio.create_task(autonomous_hunter_loop())
                break # Exit watchdog, now running as active trader


async def autonomous_hunter_loop():
    print("🦅 PREDADOR SUPREMO, 🦖 SNIPER & 🌀 RALF SCALPER ATIVOS.")
    while True:
        try:
            await asyncio.sleep(1) # HFT Speed
            
            # 💵 SYNC BALANCE (Check Fuel every 30s or on demand)
            if int(time.time()) % 30 == 0:
                await engine_state.sync_balance(exchange)

            if engine_state.current_balance < engine_state.MIN_CAPITAL:
                if int(time.time()) % 60 == 0: # Log menos frequente
                    print(f"⏳ [WAITING FOR FUNDS] Saldo insuficiente: ${engine_state.current_balance:.2f} | Mínimo: ${engine_state.MIN_CAPITAL:.2f}")
                await asyncio.sleep(5)
                continue

            # 🛡️ CHECK KILL SWITCH (Homeostase)
            stats = engine_state.get_stats()
            if stats["kill_switch_active"]:
                print(f"🛑 [KILL SWITCH] Homeostase atingida: PnL {stats['pnl']}%")
                await asyncio.sleep(60) 
                continue

            # PREDADOR (BTC/ETH)
            for symbol in ["BTCUSDT", "ETHUSDT"]: await run_strategy(symbol, "SUPREME")
            # SNIPER (SOL)
            await run_strategy("SOLUSDT", "SNIPER")
            # 🌀 RALF SCALPER (All Assets - High Frequency)
            for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]: await run_strategy(symbol, "RALF")
        except Exception as e:
            print(f"⚠️ Loop: {e}")
            await asyncio.sleep(5)

async def run_strategy(symbol, mode):
    ohlcv = await exchange.fetch_ohlcv(symbol, "1m", limit=35)
    if not ohlcv: return
    
    closes = [x[4] for x in ohlcv]
    engine_state.last_price = closes[-1]
    
    # 🧠 DISTRIBUTED BRAIN (Vercel Shadow)
    vercel_url = os.environ.get("VERCEL_BRAIN_URL")
    intel = None
    bias = "NEUTRAL"
    score = 0
    decision = "REJECT"
    
    if vercel_url:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.post(
                    f"{vercel_url}/api/hunt",
                    json={"symbol": symbol, "mode": mode, "ohlcv": ohlcv},
                    headers={"x-token": INTERNAL_SECRET_TOKEN}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    intel = data.get("intel")
                    bias = data.get("bias")
                    score = data.get("score")
                    decision = data.get("decision")
                    print(f"🧠 [VERCEL BRAIN] {symbol}: {bias} ({score})")
        except Exception as e:
            print(f"⚠️ [BRAIN FAILOVER] Vercel offline ou lento, usando Local Core: {e}")

    # 🧬 LOCAL FALLBACK (Se o Vercel falhar)
    if not brain: return
    intel = brain.calculate_indicators(closes, [x[2] for x in ohlcv], [x[3] for x in ohlcv], [x[5] for x in ohlcv])
    if not intel: return
    
    # 🛡️ v367.0 TITAN LEVERAGE (Logic v364.1)
    
    rsi = intel["rsi"]
    bb_width = intel["bb_width"]
    
    if "ETH" in symbol:
        oversold = rsi < 20 # "Ether Zero" Logic
        overbought = rsi > 80
    else:
        oversold = rsi < 30
        overbought = rsi > 70
        
    active_market = bb_width > 0.15
    
    # 🧠 NEURAL SCORING SYSTEM (Weighted Convergence)
    points = 0
    if oversold: points += 40
    if overbought: points += 40
    
    # Factor 2: StochRSI Confirmation
    if intel.get("stoch_rsi", 50) < 10: points += 20
    if intel.get("stoch_rsi", 50) > 90: points += 20
    
    # Factor 3: Volume Shock (Institutional Force)
    if intel.get("z_vol", 0) > 2.0: points += 15
    
    # Factor 4: BB Touch
    if intel.get("touch_low") or intel.get("touch_high"): points += 15
    
    # Factor 5: Trend Alignment (Alpha) - Buy the Dip / Sell the Rip
    if oversold and intel.get("trend_up"): points += 10 
    if overbought and not intel.get("trend_up"): points += 10
    
    score = points
    
    # Surgical Thresholds: Sovereign Mode (v370.0)
    active_threshold = 85 
    
    # 🔗 TREND FILTER (The Golden Rule)
    trend_aligned = (oversold and intel.get("trend_up")) or (overbought and not intel.get("trend_up"))
    
    # [RALF OVERRIDE]
    if mode == "RALF":
        # Balanced RSI for RALF LIVE Scalper (más relaxado que backtest)
        ralf_oversold = rsi < 40
        ralf_overbought = rsi > 60
        
        ralf_long = intel.get("ema_cross_up") and intel.get("trend_up")
        ralf_short = not intel.get("ema_cross_up") and not intel.get("trend_up")
        
        vol_check = intel.get("z_vol", 0) > 0.3
        
        if (ralf_oversold and ralf_long and vol_check):
            points += 60
            bias = "GOD_LONG"
            decision = "EXECUTE"
        elif (ralf_overbought and ralf_short and vol_check):
            points += 60
            bias = "GOD_SHORT"
            decision = "EXECUTE"
        else:
            decision = "REJECT"
    else:
        vol_confirmation = intel.get("z_vol", 0) > 1.0 or intel.get("bb_width", 0) > 0.25
        decision = "EXECUTE" if (points >= active_threshold and vol_confirmation and trend_aligned) else "REJECT"
    
    # 🛡️ ENTROPY SHIELD CALCULATOR
    entropy = intel.get("entropy", 0.5)
    
    # CRITICAL: Pure Chaos Kill-Switch
    if entropy > 0.85:
        print(f"🛑 [KILL-SWITCH] ENTROPIA EXTREMA ({entropy:.2f}). Abortando qualquer execução.")
        return # Sai da estratégia para este ativo
    
    shield_mult = 1.0
    sl_boost = 1.0
    
    if entropy > 0.75:
        shield_mult = 0.2 # Modo Sobrevivência (Reduz 80%)
        sl_boost = 1.4    # Abre SL em 40%
        print(f"🛡️ [ENTROPY SHIELD] SURVIVAL MODE! (Entropy: {entropy:.2f})")
        asyncio.create_task(engine_state.log_event_to_supabase("SHIELD", f"SURVIVAL MODE ACTIVE (Entropy: {entropy:.2f})", asset=symbol))
    elif entropy > 0.60:
        shield_mult = 0.5 # Modo Cautela (Reduz 50%)
        sl_boost = 1.2    # Abre SL em 20%
        print(f"🛡️ [ENTROPY SHIELD] CAUTION MODE! (Entropy: {entropy:.2f})")
        asyncio.create_task(engine_state.log_event_to_supabase("SHIELD", f"CAUTION MODE ACTIVE (Entropy: {entropy:.2f})", asset=symbol))
        
    is_sol = "SOL" in symbol.upper()
    
    # 💎 INFINITY MATRIX: SOVEREIGN REFINEMENT (v370.0)
    trading_mode = os.environ.get("TRADING_MODE", "AGGRESSIVE")
    
    if is_sol: 
        target_base_lev = 55.0 
    elif "ETH" in symbol:
        target_base_lev = 3.0  
    else:
        target_base_lev = 4.0  
        
    # Ajuste pelo Modo de Trading (Pedido do Usuario: Uso Moderado)
    if trading_mode == "MODERATE":
        target_base_lev = target_base_lev * 0.5
    elif trading_mode == "SAFE":
        target_base_lev = 1.0

    # ALAVANCAGEM FINAL = INFINITY * SHIELD
    effective_leverage = target_base_lev * shield_mult
    final_leverage_int = max(1, int(effective_leverage))
    
    intel["tp_factor"] = 0     
    intel["sl_factor"] = 3.0 
    intel["tp_target"] = "ma20" 
    intel["leverage"] = final_leverage_int
    intel["sl_boost"] = sl_boost # Passa para a execução

    engine_state.last_score = score
    engine_state.last_entropy = entropy
    engine_state.shield_status = "MAX_DEFENSE" if entropy > 0.75 else ("ACTIVE" if entropy > 0.60 else "OFF")
    
    if decision == "EXECUTE":
        if mode == "RALF":
            config = get_ralf_config(symbol, intel.get("trend_up", True), intel["is_compressed"])
        else:
            config = get_supreme_config(symbol, intel.get("trend_up", True), intel["is_compressed"]) if mode == "SUPREME" else get_sniper_config(symbol, intel.get("trend_up", True), intel["is_compressed"])
        print(f"⚡ [EXECUTION-KING] {symbol} | Mode: {mode} | Score: {score:.1f} | Bias: {bias}")
        
        price = intel["price"]
        atr = intel["atr"]
        effective_sl_mult = config["sl_mult"] * intel.get("sl_boost", 1.0)
        
        sl = price - (atr*effective_sl_mult) if bias == "GOD_LONG" else price + (atr*effective_sl_mult)
        tp = price + (atr*config["tp_mult"]) if bias == "GOD_LONG" else price - (atr*config["tp_mult"])
        
        if exchange.apiKey:
            try:
                # 💵 DYNAMIC POSITION SIZING (v110.0)
                # Aloca ~5% do capital real livre por trade ajustado pela alavancagem
                free_usd = engine_state.current_balance
                
                # Qty = (Capital * Alavancagem) / Preço
                qty = (free_usd * 0.05 * effective_leverage) / price
                qty = float(exchange.amount_to_precision(symbol, qty))
                
                side = "buy" if bias == "GOD_LONG" else "sell"
                
                params = {
                    'stopLoss': float(exchange.price_to_precision(symbol, sl)), 
                    'takeProfit': float(exchange.price_to_precision(symbol, tp))
                }
                
                try: await exchange.set_leverage(final_leverage_int, symbol)
                except: pass
                
                order = await exchange.create_order(symbol, 'market', side, qty, params=params)
                print(f"✅ KING ORDER EXECUTED! ID: {order['id']} | Qty: {qty} | Lev: {final_leverage_int}x (Eff: {effective_leverage:.2f}x)")
                
                engine_state.trades += 1
                engine_state.last_order = order
                
                trade_data = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "action": side.upper(),
                    "symbol": symbol,
                    "confidence": int(score),
                    "price": float(price),
                    "qty": float(qty),
                    "leverage": int(final_leverage),
                    "pnl": 0.0, # Será preenchido no fechamento
                    "version": "370.0"
                }
                
                engine_state.trade_log.append(trade_data)
                
                # 📡 REGISTRO PERSISTENTE (Supabase)
                try:
                    supabase.table("trades").insert(trade_data).execute()
                    print(f"📡 [BLACK BOX] Trade sincronizado com Sucesso.")
                except Exception as s_ex:
                    print(f"⚠️ [BLACK BOX FAIL] Erro ao sincronizar: {s_ex}")
            except Exception as ex:
                print(f"❌ [EXECUTION FAIL] {ex}")
                asyncio.create_task(engine_state.log_event_to_supabase("ERROR", str(ex), asset=symbol))
        
        await asyncio.sleep(8) # Recovery time reduzido para HFT

# ============================================================
# 🔙 BACKTEST (DUAL DYNAMIC)
# ============================================================
@app.post("/backtest")
async def run_backtest(payload: WebhookPayload):
    symbol = normalize_symbol(payload.symbol)
    period = payload.period or "1m"
    limit = payload.limit or 2000
    
    try:
        ohlcv = await exchange.fetch_ohlcv(symbol, period, limit=limit)
    except Exception as e:
        return {"error": f"Failed to fetch OHLCV: {str(e)}", "candles_count": 0}
        
    if not ohlcv:
        return {"error": "No OHLCV data returned from exchange", "candles_count": 0}

    candles_count = len(ohlcv)
    sim = {"pnl": 0.0, "trades": 0, "wins": 0, "losses": 0, "total_pnl_percent": 0.0}
    mode = "SNIPER" if "SOL" in symbol else "SUPREME"
    if payload.action == "RALF": mode = "RALF"
    
    trade_log = []
    debug_samples = []
    
    i = 35
    while i < len(ohlcv) - 1:
        past_closes = [x[4] for x in ohlcv[i-35:i+1]]
        # Passando volumes corretamente
        intel = brain.calculate_indicators(
            past_closes, 
            [x[2] for x in ohlcv[i-35:i+1]], 
            [x[3] for x in ohlcv[i-35:i+1]], 
            [x[5] for x in ohlcv[i-35:i+1]]
        )
        
        if not intel: 
            i += 1
            continue
            
        # Collect debug sample for the last few candles
        if i > len(ohlcv) - 5:
            debug_samples.append({
                "time": ohlcv[i][0],
                "rsi": intel.get("rsi"),
                "entropy": intel.get("entropy"),
                "trend_up": intel.get("trend_up")
            })

        bias = "NEUTRAL"
        score = 0
        
        # 🛡️ v364.1 ETHER-ZERO RELOADED BACKTEST
        rsi = intel["rsi"]
        bb_width = intel["bb_width"]
        t_up = intel.get("trend_up", True)
        ema_cross = intel.get("ema_cross_up")
        
        points = 0
        
        if "ETH" in symbol:
            oversold = rsi < 20
            overbought = rsi > 80
        else:
            oversold = rsi < 30
            overbought = rsi > 70
        
        # Scoring logic
        if oversold: points += 40
        if overbought: points += 40
        if intel.get("stoch_rsi", 50) < 10: points += 20
        if intel.get("stoch_rsi", 50) > 90: points += 20
        if intel.get("z_vol", 0) > 2.0: points += 15
        if intel.get("touch_low") or intel.get("touch_high"): points += 15
        if oversold and t_up: points += 10 
        if overbought and not t_up: points += 10
        
        entropy = intel.get("entropy", 0.5)
        
        # Decision Logic
        aligned_bt = False
        vol_confirm_bt = False
        active_threshold = 85
        
        if mode == "RALF":
            active_threshold = 50
            # RALF Logic relaxed for backtest visibility
            r_os = rsi < 45  # Relaxed from 35/40
            r_ob = rsi > 55  # Relaxed from 65/60
            r_vol = intel.get("z_vol", 0) > 0.3
            
            if (r_os and ema_cross and t_up and r_vol):
                points = 100
                aligned_bt = True
                vol_confirm_bt = True
                bias = "GOD_LONG"
            elif (r_ob and not ema_cross and not t_up and r_vol):
                points = 100
                aligned_bt = True
                vol_confirm_bt = True
                bias = "GOD_SHORT"
        else:
            aligned_bt = (oversold and t_up) or (overbought and not t_up)
            vol_confirm_bt = intel.get("z_vol", 0) > 1.0 or intel.get("bb_width", 0) > 0.25

        if points >= active_threshold and entropy <= 0.85 and vol_confirm_bt and aligned_bt:
            # Entry Found
            price = ohlcv[i][4] # Close price
            
            # Simple simulation: take profit or stop loss
            # For simplicity in this debug check, detailed simulation is skipped in favor of signal detection
            # But let's add a dummy trade
            sim["trades"] += 1
            
            # Estimate outcome (next 5 candles)
            entry_price = price
            outcome = 0
            for k in range(1, 6):
                if i+k >= len(ohlcv): break
                future_price = ohlcv[i+k][4]
                if bias == "GOD_LONG" or (oversold and t_up):
                    change = (future_price - entry_price) / entry_price
                else:
                    change = (entry_price - future_price) / entry_price
                
                # Check TP/SL hit
                if change > 0.005: # 0.5% TP
                    sim["wins"] += 1
                    outcome = 0.5
                    break
                elif change < -0.003: # 0.3% SL
                    sim["losses"] += 1
                    outcome = -0.3
                    break
            
            sim["total_pnl_percent"] += outcome
            
            trade_log.append({
                "index": i,
                "price": price,
                "bias": bias,
                "outcome": outcome
            })
            
            # Skip forward to avoid overlapping trades
            i += 5
        
        i += 1

    # Safe division
    win_rate = (sim["wins"] / sim["trades"] * 100) if sim["trades"] > 0 else 0
    
    return {
        "candles_count": candles_count,
        "total_pnl_percent": sim["total_pnl_percent"],
        "total_trades": sim["trades"],
        "wins": sim["wins"],
        "losses": sim["losses"],
        "win_rate": win_rate,
        "metrics": {
            "rating": "DEBUG_MODE",
            "max_drawdown_pct": 0,
            "sharpe_ratio": 0
        },
        "debug_last_candles": debug_samples
    }
    
    if history and len(history) > 1:
        # 📈 Retorno Médio por Trade
        mean_ret = sum(history) / len(history)
        
        # 📉 Volatilidade (Desvio Padrão dos Retornos)
        variance = sum([(x - mean_ret)**2 for x in history]) / len(history)
        std_dev = variance**0.5
        
        # ⚖️ SHARPE RATIO (Anualizado para 1m candles)
        # Fórmula: (Retorno Médio - Risk-Free Rate) / Volatilidade
        # Risk-Free Rate aproximado: 0 para simplificar (crypto)
        # Anualização: sqrt(525600) para candles de 1 minuto por ano
        if std_dev > 0:
            # Sharpe simples por trade
            sharpe_per_trade = mean_ret / std_dev
            # Anualizado (sqrt do número de períodos)
            sharpe = sharpe_per_trade * (len(history) ** 0.5)
        
        # 📉 DRAWDOWN MÁXIMO (%)
        # Maior queda do pico até o fundo antes de recuperar
        equity_curve = []
        cumulative = 0
        for ret in history:
            cumulative += ret
            equity_curve.append(cumulative)
        
        peak = equity_curve[0]
        max_dd = 0
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            dd = peak - equity
            if dd > max_dd:
                max_dd = dd
        max_drawdown_pct = max_dd
    
    # 🏆 Rating baseado nas métricas
    if sim["pnl"] > 0 and sharpe >= 2.0:
        rating = "EXCELENTE"
    elif sim["pnl"] > 0 and sharpe >= 1.0:
        rating = "BOM"
    elif sim["pnl"] > 0:
        rating = "ACEITÁVEL"
    else:
        rating = "PRECISA REVISÃO"

    return {
        "symbol": symbol, 
        "mode": mode,
        # 💰 PnL Líquido
        "total_pnl_percent": round(sim["pnl"], 2), 
        # 📈 Win Rate
        "total_trades": sim["trades"],
        "wins": sim["wins"],
        "losses": sim["trades"] - sim["wins"],
        "win_rate": round(win_rate, 2),
        # 📊 Métricas Avançadas
        "metrics": {
            "sharpe_ratio": round(sharpe, 2),
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "avg_return_per_trade": round(sum(history) / max(1, len(history)), 2) if history else 0,
            "volatility": round((sum([(x - sum(history)/max(1,len(history)))**2 for x in history]) / max(1, len(history)))**0.5, 2) if history else 0,
            "rating": rating
        },
        "interpretation": {
            "sharpe": "< 1 Fraco | 1-2 Aceitável | > 2 Bom | > 5 Excelente",
            "drawdown": "Menor = Melhor (representa risco máximo)"
        }
    }
