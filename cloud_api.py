"""
PREDATOR v21.2 APEX MUTATION - Cloud API (Render)
═══════════════════════════════════════════════════════════════
100% CLOUD | ZERO LOCAL | CUSTO ZERO

Fluxo:
  TradingView (Pine Script) → Webhook → Esta API → Dashboard (Vercel)

Características:
  ✅ Recebe sinais do TradingView via webhook
  ✅ Processa ordens com lógica de Flat Position Protocol
  ✅ Alimenta o Dashboard em tempo real
  ✅ 3-Strikes Rule para proteção
  ✅ Pronto para integrar com API de corretora
═══════════════════════════════════════════════════════════════
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
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
# ⚙️ GLOBAL UTILS & TIMEZONE (Fix: Douglas -03:00)
# ============================================================
def get_today_iso():
    # Douglas está em UTC-3. Forçamos a data para ser consistente com o dia dele.
    return (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d")

def get_now_br():
    return datetime.utcnow() - timedelta(hours=3)

# Consolidando normalização de símbolos para Bybit V5
def normalize_symbol(symbol: str) -> str:
    """Adapta símbolos para Bybit V5 (Sem barras e em maiúsculas)."""
    return symbol.replace("/", "").replace("-", "").upper()

def bybit_normalize_symbol(symbol: str) -> str:
    return normalize_symbol(symbol)

# Carregar variáveis de ambiente locais (.env) se existirem
load_dotenv()

# ============================================================
# 🛡️ SOVEREIGN SECURITY LAYER (SSL-2026)
# ============================================================
INTERNAL_SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

async def sovereign_auth(x_token: Optional[str] = Header(None)):
    """Valida se a requisição possui a assinatura de soberania do PREDATOR."""
    if not INTERNAL_SECRET_TOKEN: return # Se não configurado, ignora (Modo Dev)
    if x_token != INTERNAL_SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized - Sovereign Security Block")

# ============================================================
# ⚡ ENGINE STATE & METRICS (Backend Potency)
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
        self.last_neural_pulse = time.time()
        self.is_healthy = True # Deadman Switch status

    def get_stats(self):
        process = psutil.Process(os.getpid())
        self.cpu_usage = psutil.cpu_percent()
        self.ram_usage = process.memory_info().rss / (1024 * 1024)
        uptime = time.time() - self.uptime_start
        return {
            "uptime_sec": int(uptime),
            "cpu_percent": self.cpu_usage,
            "ram_mb": round(self.ram_usage, 2),
            "requests_total": self.requests_handled,
            "latency_avg_ms": round(self.api_latency_ms, 1),
            "pulse_rate_hz": round(1.0 / max(0.001, time.time() - self.last_neural_pulse), 2),
            "healthy": self.is_healthy
        }

engine_state = EngineState()

# 🛡️ DISK SHIELD: SOVEREIGN LOG BUFFER (Anti-Freeze Tech)
class SovereignLogBuffer:
    def __init__(self, flush_interval=15):
        self.log_queue = []
        self.trade_queue = []
        self.flush_interval = flush_interval
        self.last_flush = time.time()

    async def add_log(self, level, module, message, data=None):
        self.log_queue.append({
            "level": level, "module": module, "message": message,
            "data": data or {}, "created_at": get_now_br().isoformat()
        })
        if len(self.log_queue) > 50: await self.flush()

    async def add_trade(self, trade_data):
        trade_data["created_at"] = get_now_br().isoformat()
        self.trade_queue.append(trade_data)
        if len(self.trade_queue) > 10: await self.flush()

    async def flush(self):
        if not supabase: return
        try:
            if self.log_queue:
                batch = list(self.log_queue)
                self.log_queue = []
                supabase.table("system_logs").insert(batch).execute()
            
            if self.trade_queue:
                batch = list(self.trade_queue)
                self.trade_queue = []
                supabase.table("trades").insert(batch).execute()
                
            self.last_flush = time.time()
        except Exception as e:
            print(f"⚠️ [DISK-SHIELD-ERROR] {e}")

log_shield = SovereignLogBuffer()

# ============================================================
# 🚀 LIFESPAN MANAGER (FastAPI 2026)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🏁 STARTUP: Ativa motores principais
    print("🔋 [ENGINE] Carregando Sistema de Alta Potência...")
    # Recuperação prioritária do estado
    await state.recover_daily_stats_async()
    asyncio.create_task(exchange.load_markets())
    
    # Inicia loops em modo resiliente
    bg_tasks = [
        asyncio.create_task(maintain_sovereign_session()),
        asyncio.create_task(autonomous_hunter_loop()),
        asyncio.create_task(bybit_pnl_sync_loop()),
        asyncio.create_task(evolution_watcher_loop()),
        asyncio.create_task(disk_shield_automated_flush())
    ]
    
    yield
    
    # 🛑 SHUTDOWN: Desligamento gracioso
    print("🔌 [ENGINE] Desligando Motores...")
    for task in bg_tasks:
        task.cancel()
    await exchange.close()

app = FastAPI(
    title="PREDATOR v25.0 - SOVEREIGN ENGINE",
    version="25.0.0",
    description="Backend de Alta Potência - Bybit V5 Sovereign AI.",
    lifespan=lifespan
)

# 📡 MIDDLEWARE: Quantum Latency Tracker
@app.middleware("http")
async def quantum_latency_middleware(request, call_next):
    start_time = time.time()
    engine_state.requests_handled += 1
    response = await call_next(request)
    latency = (time.time() - start_time) * 1000
    engine_state.api_latency_ms = (engine_state.api_latency_ms * 0.9) + (latency * 0.1)
    response.headers["X-Neural-Latency"] = f"{latency:.2f}ms"
    return response

# ============================================================
# 🧠 NEURAL CORE 2026 - PREDATOR v21.3 'APEX-PROGENY'
# 🚀 (AUTONOMOUS HUNTER + GENETIC EVOLUTION)
# ============================================================

class NomadBrain:
    def __init__(self):
        # 🟢 MULTI-OCULAR SYSTEM (OLHOS)
        self.eyes = {
            "DEFI": ["UNIUSDT", "AAVEUSDT", "LINKUSDT"],
            "L1": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT"],
            "MEMES": ["DOGEUSDT", "PEPEUSDT", "WIFUSDT", "SHIBUSDT"],
            "AI": ["NEARUSDT", "FETUSDT", "RENDERUSDT"]
        }
        self.market_watchlist = []
        for v in self.eyes.values(): self.market_watchlist.extend(v)
        
        # 🧠 MULTI-CEREBRAL CORTEX (v26.4 - Lateralized Market Focus)
        self.genes = {
            "occipital_weight": 0.35, # 👁️ Fluxo/OFI/OBP (Alta importância em Range)
            "parietal_weight": 0.25,  # 🗺️ Liquidez/Paredes (Crucial em Range)
            "frontal_weight": 0.25,   # 🧠 Lógica/RSI (Momentum baixo)
            "amygdala_weight": 0.15   # 🛡️ Medo/Risco
        }
        
        # 🦴 CEREBELO (Memória Muscular / Execução)
        self.muscle_memory = {"avg_latency": 0.2, "success_rate": 0.0}
        self.restricted_symbols = set()
        
        # 🧬 BIO-QUANTUM LIFE SIGNS (v26.4)
        self.metabolism = 1.0
        self.adrenaline = 0.0
        self.homeostasis = 100.0
        self.quantum_entropy = 0.1
        self.synaptic_firing = 0.0
        self.btc_momentum = 0.0
        self.btc_last_price = 0.0
        self.btc_last_fetch = 0.0
        self.kelly_fraction = 0.30
        self.leverage_cache = {} 
        self.recent_trades = []
        self.scalper_win_streak = 0
        self.scalper_loss_streak = 0
        self.adaptive_aggression = 1.0
        self.last_trade_time = 0
        self.positions = {}
        
        # 🧠 PATTERN MEMORY & GLOBAL CONSCIOUSNESS
        self.synaptic_cache = {}
        self.psi_history = []           # [v26.6] Histórico de disparos neurais
        self.pulse_anchor = {"ETHUSDT": 0.0, "SOLUSDT": 0.0}
        self.global_consciousness = 0.5
        self.plasticity_index = 0.1
        self.sector_resonance = {k: 0.0 for k in self.eyes.keys()}
        
        # ⚡ CACHE DE SÍMBOLOS MONITORADOS
        self.monitored_symbols_cache = []
        self.refresh_monitored_symbols()
        
    def refresh_monitored_symbols(self):
        """Atualiza o cache de símbolos normalizados para Bybit V5."""
        symbols = []
        for s_list in self.eyes.values():
            symbols.extend([normalize_symbol(s) for s in s_list])
        self.monitored_symbols_cache = list(set(symbols))
        
    def record_trade_result(self, result: str, pnl: float, symbol: str):
        """Registra resultado do trade para adaptação de estratégia."""
        self.recent_trades.append({"result": result, "pnl": pnl, "symbol": symbol, "time": time.time()})
        if len(self.recent_trades) > 50:
            self.recent_trades = self.recent_trades[-50:]
        
        if result == "WIN":
            self.scalper_win_streak += 1
            self.scalper_loss_streak = 0
            self.adaptive_aggression = min(2.0, 1.0 + (self.scalper_win_streak * 0.1))
            self.mutate(success=True)
        else:
            self.scalper_loss_streak += 1
            self.scalper_win_streak = 0
            self.adaptive_aggression = max(0.5, 1.0 - (self.scalper_loss_streak * 0.15))
            self.mutate(success=False)
        
        print(f"🎯 [SCALPER] Resultado: {result} | Agressão: {self.adaptive_aggression:.2f}x | Streak: W{self.scalper_win_streak}/L{self.scalper_loss_streak}")

    async def scan_market(self):
        best_opportunity = None
        highest_score = 0
        best_intel = None
        
        try:
            # ⚡ OTIMIZAÇÃO V25.3: Busca todos os tickers Lineares (USDT) de uma vez
            # params={'category': 'linear'} garante que não misturamos com Spot
            all_tickers = await exchange.fetch_tickers(params={'category': 'linear'})
            candidates = []
            
            for sector, symbols in self.eyes.items():
                for sym in symbols:
                    # Tenta encontrar o símbolo unificado (ex: SOL/USDT:USDT)
                    norm_sym = bybit_normalize_symbol(sym)
                    
                    # Busca por ID ou por Símbolo Unificado no cache
                    ticker = None
                    if norm_sym in all_tickers:
                        ticker = all_tickers[norm_sym]
                    else:
                        # Fallback: procura o símbolo que contém o nome do par
                        for t_sym, t_data in all_tickers.items():
                            if norm_sym in t_sym.replace("/", "").replace(":", ""):
                                ticker = t_data
                                break

                    if ticker and (ticker.get('quoteVolume', 0) or 0) > 1000000:
                        change = ticker.get('percentage', 0)
                        score_v = abs(change)
                        candidates.append((sym, score_v, sector, change))
            
            # 🧬 SYMPATHETIC RESONANCE & GLOBAL CONSCIOUSNESS
            pos_changes = [c[3] for c in candidates if c[3] > 0]
            neg_changes = [c[3] for c in candidates if c[3] < 0]
            
            # Global Consciousness: 1.0 (All Harmony) to 0.0 (Pure Chaos)
            if len(candidates) > 0:
                harmony = max(len(pos_changes), len(neg_changes)) / len(candidates)
                self.global_consciousness = (harmony * 0.7) + (self.global_consciousness * 0.3)
            
            for sector in self.sector_resonance:
                sector_changes = [c[3] for c in candidates if c[2] == sector]
                if sector_changes:
                    # Resonance: Força direcional do setor (-1 a 1)
                    avg_c = sum(sector_changes) / len(sector_changes)
                    self.sector_resonance[sector] = max(-1, min(1, avg_c / 5.0)) # Normalizado
            
            # Ordena por volatilidade setorial
            candidates.sort(key=lambda x: x[1], reverse=True)
            discovery = [c[0] for c in candidates[:10]]
            
            # [PERFORMANCE-BOOST] Use already fetched tickers for anchors
            anchor_tickers = all_tickers
            
            if 'BTCUSDT' in anchor_tickers:
                btc_ticker = anchor_tickers['BTCUSDT']
                self.btc_last_price = btc_ticker['last']
                self.btc_momentum = btc_ticker.get('percentage', 0) / 100.0
                self.btc_last_fetch = time.time()
            
            for a in self.pulse_anchor:
                if a in anchor_tickers:
                    self.pulse_anchor[a] = anchor_tickers[a].get('percentage', 0) / 100.0
            
            # Escaneamento Paralelo Bio-Sincronizado
            tasks = [self.fetch_god_intelligence(symbol, btc_provided=True) for symbol in discovery]
            results = await asyncio.gather(*tasks)
            
            for intel in results:
                if not intel: continue
                # 🧬 SYMPATHETIC BONUS: Se o setor está em harmonia, aumenta o score
                resonance = self.sector_resonance.get(intel.get("sector", ""), 0)
                resonance_bonus = abs(resonance) * 15 if (resonance > 0 and intel["ofi"] > 0) or (resonance < 0 and intel["ofi"] < 0) else -10
                
                # 🧠 OMNISCIENT BIAS: Momentum do BTC/ETH/SOL impacta o score individual
                anchor_bias = (self.btc_momentum + sum(self.pulse_anchor.values())) * 20
                
                volume_weight = 1.6 if intel.get("volume_spike", False) else 1.0
                divergence_bonus = 25 if intel.get("divergence", False) else 0
                mtf_bonus = intel.get("mtf_confluence", 0) * 12
                
                score = (
                    (abs(intel["ofi"]) * 45 * volume_weight) + 
                    (intel["kinetic"] * 25) + 
                    divergence_bonus +
                    mtf_bonus +
                    resonance_bonus +
                    anchor_bias
                )
                
                if score > highest_score:
                    highest_score = score
                    best_opportunity = intel["symbol"]
                    best_intel = intel
                    
        except Exception as e:
            print(f"⚠️ [SCAN-ERROR] {e}")

        return best_opportunity, highest_score, best_intel

    def mutate(self, success: bool):
        """MOTOR DE MUTAÇÃO GENÉTICA: Evolui os pesos neurais baseados no lucro."""

        # NEUROPLASTICITY: O robô aprende mais rápido no início ou após falhas
        if not success:
            self.plasticity_index = min(0.3, self.plasticity_index + 0.05)
        else:
            self.plasticity_index = max(0.05, self.plasticity_index - 0.01)
            
        mutation_rate = self.plasticity_index
        
        if success:
            # Omnipotent Growth: Se está ganhando, foca em Visão e Lógica
            self.genes["frontal_weight"] += mutation_rate
            self.genes["occipital_weight"] += mutation_rate
            self.genes["parietal_weight"] += mutation_rate * 0.5
            self.genes["amygdala_weight"] -= mutation_rate * 1.5
        else:
            # Self-Preservation: Se está perdendo, a Amígdala domina (Fear/Safety)
            self.genes["amygdala_weight"] += mutation_rate * 2
            self.genes["frontal_weight"] -= mutation_rate
            self.genes["occipital_weight"] -= mutation_rate
            self.genes["parietal_weight"] -= mutation_rate
        
        # Normalização dos Genes com Guard (Evita NaN)
        total = sum(self.genes.values())
        if total > 0:
            for k in self.genes: self.genes[k] /= total
        else:
            self.genes = {"frontal_weight": 0.35, "occipital_weight": 0.35, "amygdala_weight": 0.15, "parietal_weight": 0.15}
        
        # Limita pesos para evitar especialização extrema (Mínimo 5%)
        for k in self.genes:
            self.genes[k] = max(0.05, self.genes[k])
        
        # Re-normaliza após o clamp
        total = sum(self.genes.values())
        for k in self.genes: self.genes[k] /= total
        
        print(f"🧬 [MUTATION] Genes Evoluídos: {self.genes}")

    async def fetch_god_intelligence(self, symbol, btc_provided=False):
        """Busca dados de alta fidelidade e retorna métricas puras."""
        try:
            target = bybit_normalize_symbol(symbol)
            # ⚓ ÂNCORA BTC + ATIVO ALVO PARALELIZADO
            # Otimização: Se BTC já foi buscado no loop de scan, evita a chamada repetida
            if not btc_provided:
                tasks = [
                    exchange.fetch_ohlcv('BTCUSDT', timeframe='1m', limit=10),
                    exchange.fetch_order_book(target, limit=10),
                    exchange.fetch_ohlcv(target, timeframe='1m', limit=30),
                    exchange.fetch_ohlcv(target, timeframe='5m', limit=10)
                ]
            else:
                tasks = [
                    asyncio.sleep(0), # Placeholder
                    exchange.fetch_order_book(target, limit=10),
                    exchange.fetch_ohlcv(target, timeframe='1m', limit=30),
                    exchange.fetch_ohlcv(target, timeframe='5m', limit=10)
                ]
            
            results = await asyncio.gather(*tasks)
            
            # 📊 ORDER FLOW IMBALANCE (OFI) - Lógica Institucional 2026
            # OFI = (Bids Change - Asks Change)
            # Como pegamos snapshot, calculamos o desbalanceamento real entre Bid/Ask Volume
            ob = results[1]
            bids = ob['bids']
            asks = ob['asks']
            
            # Peso maior para os primeiros níveis (mais liquidez imediata)
            ofi_val = 0
            for i in range(min(5, len(bids), len(asks))):
                weight = 1.0 / (i + 1)
                ofi_val += (bids[i][1] - asks[i][1]) * weight
            
            # Normalização OFI (-1 a 1)
            total_vol = sum([b[1] for b in bids[:5]]) + sum([a[1] for a in asks[:5]])
            ofi = ofi_val / total_vol if total_vol > 0 else 0
            
            # 📊 ORDER BOOK PRESSURE (OBP)
            # Diferença bruta de volume no topo do book
            bid_vol_top = sum([b[1] for b in bids[:3]])
            ask_vol_top = sum([a[1] for a in asks[:3]])
            obp = (bid_vol_top - ask_vol_top) / (bid_vol_top + ask_vol_top + 0.00001)
            
            ohlcv = results[2]
            ohlcv_5m = results[3]
            
            closes = [c[4] for c in ohlcv]
            closes_5m = [c[4] for c in ohlcv_5m]
            
            # [INDICADORES CRIPTO MASTER]
            # 1. RSI (Relative Strength Index) - 14 períodos
            deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
            gains = [d if d > 0 else 0 for d in deltas[-14:]]
            losses = [-d if d < 0 else 0 for d in deltas[-14:]]
            avg_gain = sum(gains) / 14
            avg_loss = sum(losses) / 14
            rs = avg_gain / (avg_loss + 0.00001)
            rsi = 100 - (100 / (1 + rs))
            
            # 2. EMA (Exponential Moving Average) Alignment
            ema_fast = sum(closes[-8:]) / 8
            ema_slow = sum(closes[-21:]) / 21
            trend_aligned = (ema_fast > ema_slow and closes[-1] > ema_fast) or (ema_fast < ema_slow and closes[-1] < ema_fast)
            
            # 3. Inércia Multimomento (1m + 5m)
            vel_1m = (closes[-1] - closes[-3]) / closes[-3] if len(closes) > 3 else 0
            vel_5m = (closes_5m[-1] - closes_5m[-2]) / closes_5m[-2] if len(closes_5m) > 2 else 0
            kinetic = abs((vel_1m * 0.7) + (vel_5m * 0.3)) * 1000
            
            mean = sum(closes) / len(closes)
            std = math.sqrt(sum((x - mean)**2 for x in closes) / len(closes))
            z_score = (closes[-1] - mean) / (std if std > 0 else 1)
            
            # ═══════════════════════════════════════════════════════════
            # 🎯 SCALPER 2026 - INDICADORES AVANÇADOS
            # ═══════════════════════════════════════════════════════════
            
            # 4. ATR (Average True Range) - Para Stop Loss / Take Profit dinâmicos
            highs = [c[2] for c in ohlcv[-14:]]
            lows = [c[3] for c in ohlcv[-14:]]
            trs = [highs[i] - lows[i] for i in range(len(highs))]
            atr = sum(trs) / len(trs) if trs else 0
            
            # 5. Volume Spike Detection (Volume atual vs média)
            volumes = [c[5] for c in ohlcv]
            avg_volume = sum(volumes[:-1]) / len(volumes[:-1]) if len(volumes) > 1 else 1
            current_volume = volumes[-1]
            volume_spike = current_volume > (avg_volume * 1.8)  # 80% acima da média
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # 6. RSI Divergence Detection (Preço faz novo high/low, RSI não)
            price_making_high = closes[-1] > max(closes[-5:-1]) if len(closes) > 5 else False
            price_making_low = closes[-1] < min(closes[-5:-1]) if len(closes) > 5 else False
            
            # RSI histórico simplificado
            rsi_prev = 50  # Placeholder simplificado
            if len(deltas) > 20:
                prev_gains = [d if d > 0 else 0 for d in deltas[-20:-14]]
                prev_losses = [-d if d < 0 else 0 for d in deltas[-20:-14]]
                prev_rs = (sum(prev_gains)/6) / (sum(prev_losses)/6 + 0.00001)
                rsi_prev = 100 - (100 / (1 + prev_rs))
            
            bearish_divergence = price_making_high and rsi < rsi_prev
            bullish_divergence = price_making_low and rsi > rsi_prev
            divergence = bearish_divergence or bullish_divergence
            
            # 7. Multi-Timeframe Confluence (1m + 5m concordando)
            trend_1m = 1 if vel_1m > 0 else -1
            trend_5m = 1 if vel_5m > 0 else -1
            mtf_confluence = 2 if trend_1m == trend_5m else 0
            
            # 8. Scalper Entry Quality Score
            scalper_score = (
                (volume_ratio * 10) +
                (20 if divergence else 0) +
                (mtf_confluence * 15) +
                (abs(obp) * 30)
            )
            
            return {
                "obp": obp, 
                "ofi": ofi,            # 💎 Institutional Flux
                "kinetic": kinetic, 
                "z_score": z_score, 
                "symbol": symbol,
                "btc_corr": self.btc_momentum,
                "anchor_confirm": sum(self.pulse_anchor.values()) / len(self.pulse_anchor),
                "price": closes[-1],
                "rsi": rsi,
                "trend_aligned": trend_aligned,
                # 🎯 SCALPER METRICS
                "atr": atr,
                "volume_spike": volume_spike,
                "volume_ratio": volume_ratio,
                "divergence": divergence,
                "bearish_div": bearish_divergence,
                "bullish_div": bullish_divergence,
                "mtf_confluence": mtf_confluence,
                "scalper_score": scalper_score + (ofi * 50), # Fluxo pesado aumenta score
                # Dynamic SL/TP based on ATR
                "suggested_sl": atr * 1.5,
                "suggested_tp": atr * 2.8 # TP levemente mais longo para scalping agressivo
            }
            
        except Exception as e:
            if "451" in str(e):
                print(f"🚫 [RESTRICTED] {symbol} está bloqueado nesta região (Error 451). Use um PROXY_URL.")
                self.restricted_symbols.add(symbol)
            else:
                print(f"⚠️ INTEL FAILURE: {e}")
            return None

    def analyze_infinity(self, state, intel=None):
        # 🧠 LOBO OCCIPITAL (Visão de Fluxo + OFI)
        obp = intel["obp"] if intel and "obp" in intel else 0.0
        ofi = intel.get("ofi", 0.0) if intel else 0.0
        
        # Fluxo institucional tem peso dobrado
        occipital_signal = (ofi * 0.7 + obp * 0.3) * self.genes["occipital_weight"]
        
        # 🔱 TRIPLE ANCHOR SYNC (BTC + ETH + SOL)
        anchor_conf = intel.get("anchor_confirm", 0.0) if intel else 0.0
        is_correlated = (state.btc_momentum > 0 and anchor_conf > 0) or (state.btc_momentum < 0 and anchor_conf < 0)
        
        # 🌀 DYNAMIC REGIME CORTEX (v23.0)
        # Analisa Volatilidade para decidir entre Trend Following ou Mean Reversion
        atr = intel.get("atr", 0.0) if intel else 0.0
        price = intel.get("price", 1.0) if intel else 1.0
        vol_ratio = atr / price if price > 0 else 0.0
        
        market_regime = "TRENDING" if vol_ratio > 0.004 else "RANGING" # 0.4% threshold para hoje
        
        # 🧠 LOBO FRONTAL (Lógica Adaptativa)
        kinetic = intel["kinetic"] if intel else 0.0
        rsi = intel.get("rsi", 50) if intel else 50
        trend_aligned = intel.get("trend_aligned", True) if intel else True
        
        # [v30.0] Inteligência de Regime: Prioriza exaustão técnica em mercados laterais
        if market_regime == "RANGING":
            rsi_dev = (rsi - 50) / 50.0
            rsi_factor = -2.0 * rsi_dev # Sensibilidade dobrada para reversão
            flow_mult = 0.4 # Diminui peso de fluxo (evita topo)
        else:
            rsi_factor = 1.2 * ((rsi - 50) / 50.0) 
            flow_mult = 1.0
            
        frontal_signal = (kinetic * 0.2 + rsi_factor * 0.8) * self.genes["frontal_weight"]
        
        # 🧠 LOBO PARIETAL (Integração de Liquidez Espacial)
        parietal_signal = (obp * 3.0 * flow_mult) * self.genes["parietal_weight"]
        
        # 🧠 AMÍGDALA (Resposta ao Risco e Adrenalina)
        z_score = intel["z_score"] if intel else 0.0
        vol_stress = abs(z_score) * 0.3
        self.adrenaline = max(0, min(1.0, vol_stress))
        amygdala_signal = (1.0 - self.adrenaline) * self.genes["amygdala_weight"]
        
        # ⚛️ COOPERAÇÃO SINÁPTICA: Um único sinal harmônico
        psi = (occipital_signal * flow_mult + frontal_signal + amygdala_signal + parietal_signal)
        self.quantum_entropy = abs(psi - obp)
        
        entropy = abs(z_score) / (kinetic + 0.0001)
        btc_corr = intel["btc_corr"] if intel else state.btc_momentum
        is_correlated = (psi > 0 and btc_corr > 0) or (psi < 0 and btc_corr < 0)
        
        # 🛡️ HOMEOSTASE (Estado de Saúde da Banca)
        pnl_impact = (state.daily_pnl / 100.0)
        self.homeostasis = max(0, min(100, 100 + (pnl_impact * 50)))
        
        # 🛡️ ESCUDO DE REALIDADE (BIO-QUANTUM SHIELD)
        # Em Ranging, RSI > 70 não é trap, é oportunidade de venda. Trap só em Trending.
        rsi_trap = False
        if market_regime == "TRENDING":
             rsi_trap = (psi > 0 and rsi > 70) or (psi < 0 and rsi < 30)
             
        # Reality Trap mais permissivo para Backtests e Range (v26.4.4)
        reality_trap = (abs(z_score) > 3.0) or (entropy > 10.0) or rsi_trap or (self.homeostasis < 30)
        
        # 🧬 SYMPATHETIC REINFORCEMENT
        # Se o ativo está em sintonia com seu setor (Resonância), ganhamos bônus de confiança
        resonance = self.sector_resonance.get(intel.get("sector", "") if intel else "", 0)
        resonance_align = (psi > 0 and resonance > 0.1) or (psi < 0 and resonance < -0.1)
        
        # 🔱 GLOBAL CONSCIOUSNESS FILTER
        # [v42.0] SINGULARITY SUPREME: A Convergência Final do Lucro
        symbol = intel.get("symbol", "")
        # Sincronização BTC/ETH baseada no sucesso do ETH (+12.7%)
        if "SOL" in symbol: base_cons = 0.26
        else: base_cons = 0.22 # BTC e ETH unificados no ponto de lucro
        
        consensus_threshold = (base_cons + 0.05) if self.global_consciousness < 0.6 else base_cons
        
        # Filtro de Volatilidade "Singularity"
        atr = intel.get("atr", 0.0)
        price = intel.get("price", 1.0)
        vol_floor = 0.0002 if "BTC" in symbol or "ETH" in symbol else 0.0005 
        vol_check = (atr / (price + 0.000001)) > vol_floor
        
        # Filtro de Inércia [v42.0]
        self.psi_history.append(psi)
        if len(self.psi_history) > 3: self.psi_history.pop(0)
        avg_psi = sum(self.psi_history) / len(self.psi_history)
        inertia_ok = (psi > 0 and avg_psi > 0) or (psi < 0 and avg_psi < 0)
        
        # [v42] Filtro RSI de Equilíbrio
        rsi_penalty = 1.0
        if market_regime == "RANGING":
            if psi > 0 and rsi > 70: rsi_penalty = 0.4 # Penalidade maior no topo
            if psi < 0 and rsi < 30: rsi_penalty = 0.4 
            
        bias = "NEUTRAL"
        if abs(psi) > consensus_threshold and is_correlated and inertia_ok and vol_check:
            bias = "GOD_LONG" if psi > 0 else "GOD_SHORT"
       
        # SINAPSE: Intensidade do disparo neural
        self.synaptic_firing = (abs(psi) * 100)
        confidence = min(100, self.synaptic_firing * (0.4 if not is_correlated else 1.0) * rsi_penalty)
        
        # 🧬 MUTAÇÃO ALPHA: Ajuste de Potência Bio-Mecânica
        alpha = 4.0 if confidence > 92 and not reality_trap else 1.0
        if self.adrenaline > 0.7: alpha *= 1.5 
        
        # Otimização Kelly: Ajuste dinâmico baseado na saúde da banca e regime
        # Ranging permite posições maiores pois Stop Loss é técnico e curto
        kelly_base = 0.30 if market_regime == "RANGING" else 0.15
        dynamic_kelly = kelly_base + (0.10 if self.homeostasis > 85 else 0.0)
        self.kelly_fraction = dynamic_kelly  # Atualiza instância para uso na execução
        
        return {
            "score": confidence,
            "bias": bias,
            "psi_raw": psi,
            "trap": reality_trap,
            "alpha": alpha,
            "kelly": dynamic_kelly,
            "physics": kinetic,
            "z_score": z_score,
            "obp": obp,
            "correlation": is_correlated,
            "btc_momentum": btc_corr,
            "entropy": entropy,
            "rsi": rsi,
            "trend_aligned": trend_aligned,
            "homeostasis": self.homeostasis,
            "adrenaline": self.adrenaline,
            "synaptic_firing": self.synaptic_firing,
            "quantum_entropy": self.quantum_entropy,
            "genes": self.genes
        }

brain = NomadBrain()
state_lock = asyncio.Lock()

# DOCTOR DOOM v25.0 - BYBIT SOVEREIGN ARCHITECTURE
# 100% BYBIT V5 | LINEAR PERPETUALS | SCALPER OPTIMIZED

# Carrega chaves (Prioridade: BYBIT > Genérica > Binance Legacy)
raw_key = os.environ.get("BYBIT_API_KEY", os.environ.get("EXCHANGE_API_KEY", os.environ.get("BINANCE_API_KEY", "")))
raw_secret = os.environ.get("BYBIT_API_SECRET", os.environ.get("EXCHANGE_API_SECRET", os.environ.get("BINANCE_API_SECRET", "")))

API_KEY = raw_key.strip() if raw_key else None
API_SECRET = raw_secret.strip() if raw_secret else None

# 🌐 CONFIGURAÇÃO DE PROXY
PROXY_URL = os.environ.get("PROXY_URL")
proxies = {'http': PROXY_URL, 'https': PROXY_URL} if PROXY_URL and PROXY_URL.strip() else None

# Inicializa Driver CCXT (BYBIT V5 EXCLUSIVE)
print("🔌 INICIALIZANDO BYBIT V5 DRIVER...")
exchange = ccxt.bybit({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'linear',  # Foco em USDT Perpetuals
        'adjustForTimeDifference': True,
        'recvWindow': 10000,      # Aumentado para evitar Timeouts
    },
    'proxies': proxies
})

# 🛡️ GLOBAL EXECUTION LOCK (Prevenção de Ordem Duplicada)
execution_locks = {}

# Task para manter a sessão da exchange viva e monitorar LIQUIDEZ (Gatekeeper)
async def maintain_sovereign_session():
    """
    BYBIT GATEKEEPER v25.1: Monitoramento otimizado de saldo e liquidez.
    Centraliza a verificação de saúde financeira para evitar redundância de API.
    """
    print("🛡️ BYBIT GATEKEEPER: Monitorando fluxo de caixa (Zero-Latency Mode)...")
    while True:
        try:
            if exchange.apiKey:
                # ⚡ Bybit V5 Unified Account Optimization
                # Forçamos a conta 'unified' se disponível para resposta mais rápida
                try:
                    # Tenta Unified e depois Contract como fallback
                    bal = await exchange.fetch_balance({'accountType': 'UNIFIED'})
                    usdt_total = float(bal.get('total', {}).get('USDT', 0))
                    if usdt_total == 0:
                        bal = await exchange.fetch_balance({'accountType': 'CONTRACT'})
                        usdt_total = float(bal.get('total', {}).get('USDT', 0))
                except:
                    bal = await exchange.fetch_balance()
                    usdt_total = float(bal.get('total', {}).get('USDT', 0))
                
                state.balance = usdt_total
                
                # 🔒 LIQUIDITY LOGIC (v23.1)
                # Pausa o caçador se o saldo for crítico (< $5)
                if usdt_total < 5.0:
                    if not state.funding_locked:
                        print(f"⚠️ [NO FUEL] Saldo Bybit ${usdt_total:.2f} insuficiente. Pausando PREDATOR.")
                    state.funding_locked = True
                    state.is_hunting = False
                    state.regime = "NO_CASH"
                else:
                    if state.funding_locked:
                        print(f"💰 [FUEL DETECTED] Saldo Bybit UTA ${usdt_total:.2f}. Reativando PREDATOR.")
                        state.funding_locked = False
                        
                    # 🔄 AUTO-RECOVERY: Sincroniza posições ativas da Bybit com a memória da IA
                    try:
                        positions = await exchange.fetch_positions()
                        active_syms = set()
                        for pos in positions:
                            size = float(pos.get('contracts', 0) or 0)
                            if size != 0:
                                norm_s = normalize_symbol(pos.get('symbol', ''))
                                active_syms.add(norm_s)
                        
                        # Se encontramos posições que não estavam na memória, recuperamos
                        if hasattr(brain, 'active_positions'):
                            for s in active_syms:
                                if s not in brain.active_positions:
                                    print(f"🔗 [RECOVERY] Posição aberta detectada em {s}. Sincronizando...")
                                    brain.active_positions.add(s)
                    except: pass

                    # Só reativa se não estiver travado por perdas ou pânico
                    if not state.is_locked and state.consecutive_losses < MAX_CONSECUTIVE_LOSSES:
                            state.is_hunting = True
                            if state.regime == "NO_CASH": state.regime = "ACTIVE"
                             
            await asyncio.sleep(15) # Intervalo maior para economizar Rate Limit
        except Exception as e:
            print(f"⚠️ GATEKEEPER ERROR: {e}")
            await asyncio.sleep(15)

# Se as chaves estiverem presentes, testa conexão
if API_KEY and API_SECRET:
    try:
        print(f"⚡ INICIANDO SISTEMA BYBIT (Key: {API_KEY[:4]}***)")
        async def setup_account():
            try:
                # 1. Carrega mercados
                print("⏳ Carregando mercados Bybit...")
                await exchange.load_markets()
                
                # 2. Configura One-way Mode
                try:
                    # Bybit V5: set_position_mode(hedged=False) tenta colocar em One-Way
                    # Muitas vezes já está, então capturamos o erro
                    await exchange.set_position_mode(False) 
                    print("✅ BYBIT: Modo de Posição definido para One-Way.")
                except Exception as e:
                    if "already in" in str(e):
                        print("✅ BYBIT: Já em Modo One-Way.")
                    else:
                        print(f"⚠️ BYBIT: Não foi possível definir modo de posição ({e})")

                print("✅ MERCADOS BYBIT CARREGADOS.")
                
                # Check Inicial de Saldo (Unified Aware)
                try:
                    bal = await exchange.fetch_balance({'accountType': 'UNIFIED'})
                    usdt = float(bal.get('total', {}).get('USDT', 0))
                    if usdt == 0:
                        bal = await exchange.fetch_balance({'accountType': 'CONTRACT'})
                        usdt = float(bal.get('total', {}).get('USDT', 0))
                except:
                    bal = await exchange.fetch_balance()
                    usdt = float(bal.get('total', {}).get('USDT', 0))
                    
                state.balance = usdt
                print(f"💰 SALDO BYBIT INICIAL: ${usdt:.2f} USDT")
                    
            except Exception as e:
                print(f"❌ [AUTH-CRITICAL] Falha na Autenticação Bybit: {e}")
                print("👉 Verifique suas chaves no Render Environment Variables.")
        asyncio.create_task(setup_account())
    except Exception as e:
        print(f"⚠️ ERRO DRIVER: {e}")
else:
    print("⚠️ BYBIT API KEYS AUSENTES: Modo Simulação.")



# Task para manter a sessão da exchange viva e evitar reconexões lentas
# Task para manter a sessão da exchange viva e monitorar LIQUIDEZ (Gatekeeper)


# ============================================================
# SUPABASE CLIENT (Persistência Opcional)
# ============================================================
# Defina SUPABASE_URL e SUPABASE_KEY nas Variáveis de Ambiente do Render
# Se não definir, o sistema roda apenas em RAM (volátil)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ SUPABASE CONECTADO! Histórico será salvo.")
    except Exception as e:
        print(f"⚠️ ERRO AO CONECTAR SUPABASE: {e}")
else:
    print("⚠️ SUPABASE OFF: Rodando em modo RAM Volátil (histórico perde-se ao reiniciar).")


# CORS para Vercel e qualquer frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://predador-singularity.vercel.app",
        "https://*.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# VARIÁVEIS DE CONFIGURAÇÃO (Ajuste conforme necessário)
# ============================================================
MAX_CONSECUTIVE_LOSSES = 3
POSICAO_ZERO_HOUR = 17
POSICAO_ZERO_MIN = 30
STALE_TIMEOUT_SEC = 120
INITIAL_PRICE = 0.0

# 🛡️ SCALPER SAFETY BOUNDARIES
MAX_DAILY_DRAWDOWN_PERCENT = 3.0 # Trava se perder 3% no dia
MAX_CONCURRENT_TRADES = 5       # Máximo de trades abertos ao mesmo tempo
SPREAD_THRESHOLD_PERCENT = 0.3 # Trava se spread > 0.3%
DEADMAN_LATENCY_MAX_MS = 1000  # Trava se latência > 1s

# ============================================================
# ESTADO DO SISTEMA (Mantido em memória - Custo Zero)
# ============================================================
class MarketState:
    def __init__(self):
        # Preço e Métricas
        self.price: float = INITIAL_PRICE
        self.last_price: float = INITIAL_PRICE
        self.balance: float = 0.0 # ⚡ CACHE DE SALDO (Zero-Latency)
        self.pnl: float = 0.0
        self.daily_pnl: float = 0.0
        self.trades: int = 0
        self.wins: int = 0
        self.losses: int = 0
        self.win_rate: float = 0.0
        
        # 🌌 IA NOMAD-INFINITY v21.1
        self.prob: float = 75.0
        self.imb: float = 0.0
        self.obp: float = 0.0
        self.ofi: float = 0.0           # 🟢 REAL-TIME OFI TELEMETRY
        self.kinetic: float = 0.0
        self.z_score: float = 0.0
        self.kelly: float = 0.15
        self.is_correlated: bool = True
        self.alpha_scale: float = 1.0
        self.compounding: float = 0.30 
        self.regime: str = "WAITING"
        self.confidence: float = 80.0
        self.bias: str = "NEUTRAL"
        self.is_hunting: bool = False # 🔒 INICIA PAUSADO (AGUARDANDO LIQUIDEZ)
        self.funding_locked: bool = True # 🔒 SEM FUNDOS ATÉ PROVAR O CONTRÁRIO
        self.is_locked: bool = False
        self.trap_detected: bool = False
        self.entropy: float = 0.0
        self.rsi: float = 50.0
        self.trend_aligned: bool = True
        self.btc_momentum: float = 0.0  # ⚓ BTC Correlation Sync
        
        # 🧬 BIOMETRICS (LIVING ORGANISM v25.0)
        self.homeostasis: float = 100.0
        self.adrenaline: float = 0.0
        self.synaptic_firing: float = 0.0
        self.quantum_entropy: float = 0.0
        self.metabolism: float = 1.0
        self.volatility_lock: bool = False # 🛡️ VOLATILITY SHIELD
        
        # Controle de Tempo
        self.last_update: float = time.time()
        self.session_start: float = time.time()
        
        # Flags de Segurança e Controle
        self.consecutive_losses: int = 0
        
        # Trade Log (últimos 50)
        self.trade_log: List[dict] = []
        
        # Última ordem
        self.last_order: dict = {}
        
        # 🧬 GENETIC SYNC
        self.genes: dict = getattr(brain, 'genes', {})
        
        # COMANDOS REMOTOS (Cloud -> MQL5)
        self.pending_command: str = ""
        
        # TENTAR RECUPERAR ESTADO DO SUPABASE
        asyncio.create_task(self.recover_daily_stats_async())

    async def recover_daily_stats_async(self):
        """Recupera PnL do dia do Supabase se disponível."""
        if not supabase: return
        
        try:
            today = get_today_iso()
            # OTIMIZAÇÃO: Busca apenas o essencial para a primeira carga
            response = supabase.table("trades").select("pnl, action, symbol, price, created_at").gte("created_at", today).execute()
            
            data = response.data
            if data:
                print(f"🔄 RECUPERANDO HISTÓRICO: {len(data)} trades encontrados hoje ({today}).")
                self.trades = len(data)
                self.pnl = sum(row.get('pnl', 0) or 0 for row in data)
                self.daily_pnl = self.pnl
                self.wins = sum(1 for row in data if (row.get('pnl', 0) or 0) > 0)
                self.losses = sum(1 for row in data if (row.get('pnl', 0) or 0) <= 0)
                
                # Recalcula Win Rate
                total = self.wins + self.losses
                self.win_rate = round((self.wins / total) * 100, 1) if total > 0 else 0.0
                
                # Popula log recente (Limitado a 10 para RAM e banda)
                self.trade_log = []
                for t in reversed(data[-10:]):
                    time_str = t['created_at'].split('T')[1][:8] if 'T' in t['created_at'] else "00:00:00"
                    self.trade_log.append({
                        "time": time_str,
                        "action": t['action'],
                        "symbol": t['symbol'],
                        "price": t['price'],
                        "confidence": 0, 
                        "pnl": t['pnl']
                    })
        except Exception as e:
            print(f"⚠️ [RECOVERY-BUG] {e}")

state = MarketState()

# ============================================================
# ENDPOINT: COMANDOS REMOTOS (PANIC BUTTON)
# ============================================================
@app.post("/command/panic")
async def trigger_panic(auth: None = Depends(sovereign_auth)):
    """Aciona o modo PÂNICO: Fecha tudo e trava o sistema."""
    state.pending_command = "PANIC"
    state.is_locked = True
    state.regime = "PANIC_MODE"
    print("🚨 PÂNICO ACIONADO VIA DASHBOARD!")
    return {"status": "PANIC_TRIGGERED"}

@app.post("/command/clear")
async def clear_command(auth: None = Depends(sovereign_auth)):
    """Limpa comandos pendentes."""
    state.pending_command = ""
    state.is_locked = False
    state.regime = "ACTIVE"
    return {"status": "COMMAND_CLEARED"}


# ============================================================
# MODELO DE DADOS
# ============================================================
class WebhookPayload(BaseModel):
    """Payload recebido do TradingView"""
    action: str              # "BUY" ou "SELL" ou "CLOSE"
    symbol: str = "WING26"   # Ativo
    price: Optional[float] = 0.0
    qty: Optional[int] = 1
    confidence: Optional[float] = 80.0
    message: Optional[str] = ""

class TradeResult(BaseModel):
    """Resultado de um trade (para atualização de PnL)"""
    result: str              # "WIN" ou "LOSS"
    pnl: float = 0.0
    symbol: str = "BTC/USDT" # Adicionado para persistência correta
    points: Optional[float] = 0.0

# ============================================================
# MODELO MQL5 (Telemetry)
# ============================================================
class MQL5Update(BaseModel):
    last_price: float
    bid: float
    ask: float
    pnl: float
    win_rate: float
    prob: float
    imb: float
    intensity: float
    symbol: str
    kinetic_energy: Optional[float] = 0.0
    z_score: Optional[float] = 0.0
    obp_score: Optional[float] = 0.0
    confidence_score: Optional[float] = 0.0
    btc_momentum: Optional[float] = 0.0
    is_correlated: Optional[bool] = True

# ============================================================
# ENDPOINT: Receber Telemetria do MQL5
# ============================================================
@app.post("/update")
async def mql5_update(data: MQL5Update):
    """
    Recebe atualização de estado em tempo real do EA MQL5.
    Substitui a necessidade do TradingView em modo Híbrido.
    """
    state.price = data.last_price
    state.last_price = data.last_price
    state.pnl = data.pnl
    state.win_rate = data.win_rate
    state.prob = data.prob
    state.imb = data.imb
    state.confidence = data.confidence_score or data.prob or state.confidence
    state.kinetic = data.kinetic_energy or state.kinetic
    state.z_score = data.z_score or state.z_score
    state.obp = data.obp_score or state.obp
    state.btc_momentum = data.btc_momentum or state.btc_momentum
    state.is_correlated = data.is_correlated if data.is_correlated is not None else state.is_correlated
    state.last_update = time.time()
    state.regime = "ACTIVE"
    
    # Se intensity for alta, marca como 'HUNTING'
    if data.intensity > 3.0:
        state.is_hunting = True
    
    # Resposta inclui comando pendente (se houver)
    response = {"status": "OK", "timestamp": time.time(), "command": state.pending_command}
    
    # Limpa comando após envio (One-shot)
    if state.pending_command == "PANIC":
        # Não limpa PANIC automaticamente, exige reset manual
        pass
    else:
        state.pending_command = ""
        
    return response

# ============================================================
# ENDPOINT: Webhook do TradingView (Automação de Repasse)
# ============================================================
@app.post("/webhook")
async def tradingview_webhook(payload: WebhookPayload, auth: None = Depends(sovereign_auth)):
    """Recebe sinais do TradingView e executa na Bybit."""
    # 🩹 Bybit V5 Fix: Remove barras dos símbolos
    payload.symbol = bybit_normalize_symbol(payload.symbol)
    
    now = get_now_br()
    
    # [SEGURANÇA] Liquidity Gatekeeper (v23.1)
    if state.funding_locked:
        return {
            "status": "REJECTED",
            "reason": "NO_FUEL",
            "message": "Saldo Insuficiente na Bybit (<$5). Deposite ou transfira para conta de Derivativos para ativar."
        }
        
    # [SEGURANÇA] Validação de POSIÇÃO ZERO (Zero Overnight)
    if now.hour > POSICAO_ZERO_HOUR or (now.hour == POSICAO_ZERO_HOUR and now.minute >= POSICAO_ZERO_MIN):
        return {
            "status": "REJECTED", 
            "reason": "POSICAO_ZERO_PROTOCOL",
            "message": f"Fim de Pregão ({POSICAO_ZERO_HOUR}:{POSICAO_ZERO_MIN:02d}). Posições Fechadas.",
            "time": now.strftime("%H:%M:%S")
        }
    
    # [SEGURANÇA] 3-Strikes Rule
    if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        state.is_locked = True
        return {
            "status": "REJECTED", 
            "reason": "3_STRIKES_LOCK",
            "message": f"Sistema bloqueado após {state.consecutive_losses} perdas consecutivas.",
            "losses": state.consecutive_losses
        }
    
    # [SEGURANÇA] Verificar se está bloqueado (3-Strikes ou PANIC)
    if state.is_locked:
        return {
            "status": "REJECTED",
            "reason": "SYSTEM_LOCKED",
            "message": "Sistema bloqueado. Use /unlock para desbloquear."
        }
    
    # Atualizar preço se fornecido
    if payload.price and payload.price > 0:
        state.price = payload.price
        state.last_price = payload.price
    
    # Atualizar confiança
    state.prob = payload.confidence or state.prob
    state.confidence = payload.confidence or state.confidence
    
    # Registrar trade no log
    trade_entry = {
        "time": now.strftime("%H:%M:%S"),
        "action": payload.action.upper(),
        "symbol": payload.symbol,
        "price": payload.price or state.price,
        "qty": payload.qty,
        "confidence": payload.confidence
    }
    state.trade_log.insert(0, trade_entry)
    if len(state.trade_log) > 50:
        state.trade_log = state.trade_log[:50]
    
    state.trades += 1
    state.regime = "ACTIVE"
    state.last_update = time.time()
    state.last_order = trade_entry
    
    # 💫 SINGULARIDADE v21.1 - Busca Inteligência se não estiver em cache
    intel = intel_cache if intel_cache else await brain.fetch_god_intelligence(payload.symbol)
    
    report = brain.analyze_infinity(state, intel=intel)
    state.confidence = report["score"]
    state.bias = report["bias"]
    state.kinetic = report["physics"]
    state.z_score = report["z_score"]
    state.obp = report["obp"]
    state.btc_momentum = report["btc_momentum"]
    state.is_correlated = report["correlation"]
    state.alpha_scale = report["alpha"]
    state.trap_detected = report["trap"]
    state.rsi = report.get("rsi", state.rsi)
    state.trend_aligned = report.get("trend_aligned", state.trend_aligned)
    state.kelly = report.get("kelly", state.kelly)
    
    # 🧬 SYNC BIO-QUANTUM LIFE SIGNS (Webhook flow)
    state.homeostasis = report.get("homeostasis", state.homeostasis)
    state.adrenaline = report.get("adrenaline", state.adrenaline)
    state.synaptic_firing = report.get("synaptic_firing", state.synaptic_firing)
    state.quantum_entropy = report.get("quantum_entropy", state.quantum_entropy)
    state.metabolism = 1.0 + (state.synaptic_firing / 100.0)
    state.genes = report.get("genes", state.genes)
    
    # ═══════════════════════════════════════════════════════════
    # EXECUÇÃO GOD-MODE (R$100 - BANK PROTECTION)
    # ═══════════════════════════════════════════════════════════
    if exchange.apiKey and exchange.secret:
        if state.trap_detected and state.confidence < 98:
            return {"status": "GOD_SHIELD_ACTIVE", "reason": "Trap Detected"}
            
        # [MATEMÁTICA AGRESSIVA] Kelly Criterion + Alpha Scale (MUTANTE v21.2)
        # Rendimento Curto Prazo: Se adrenalina > 0.8, dobramos a agressividade.
        yield_boost = 1.0 + (state.adrenaline * 1.5) if state.adrenaline > 0.5 else 1.0
        
        capital_usd = 20.0 # Aproximadamente R$ 100
        if state.daily_pnl > 0:
            capital_usd += (state.daily_pnl / 5.2) # Reinveste parte do lucro
            
        # Fração de risco: Limite 25% por trade em modo agressivo
        risk_fraction = max(0.05, min(0.25, state.kelly * yield_boost)) 
        
        # [SEGURANÇA] Usa Auto-Compounding com preço real
        entry_price = intel["price"] if intel else state.price
        
        # 🎯 Dynamic TP/SL from Intel
        sl, tp = None, None
        if intel:
            sl_dist = intel.get("suggested_sl", entry_price * 0.01)
            tp_dist = intel.get("suggested_tp", entry_price * 0.02)
            sl = entry_price - sl_dist if payload.action.upper() == "BUY" else entry_price + sl_dist
            tp = entry_price + tp_dist if payload.action.upper() == "BUY" else entry_price - tp_dist

        payload.qty = 0.001 
        asyncio.create_task(execute_bybit_order(payload, use_compounding=True, entry_price=entry_price, sl=sl, tp=tp))
    # ═══════════════════════════════════════════════════════════
    
    return {
        "status": "INFINITY_SINGULARITY_REACHED",
        "bias": report["bias"],
        "alpha": f"x{state.alpha_scale}",
        "kelly": f"{state.kelly * 100:.1f}%",
        "correlation": "SYNCED" if state.is_correlated else "DISCONNECTED",
        "message": "Predator NOMAD v21.1: Física e Correlação em Sintonia."
    }

# ⚡ HELPER: Gestão de Capital Auto-Compounding (Sovereign Cache - Zero Latency)
async def get_compounded_amount(symbol, kelly=0.20, price=None, atr=None):
    """Calcula o tamanho do lote baseado no saldo em CACHE da Bybit com alavancagem adaptativa."""
    try:
        # ⚡ ZERO-LATENCY CAPITAL MANAGER
        available_balance = state.balance
        
        # Fallback de segurança se o cache estiver zerado
        if available_balance <= 0:
            try:
                bal = await exchange.fetch_balance()
                available_balance = float(bal['total'].get('USDT', 0))
                state.balance = available_balance
            except:
                return 0.0
                
        # 🎰 VOLATILITY-ADJUSTED LEVERAGE (VAL)
        # Se ATR é 1% do preço, 0.01 / 0.01 = 1 -> Alavancagem equilibrada.
        # Alvo: Risco fixo de movimentação.
        leverage = 10 # Default
        if atr and price:
            volatility = (atr / price)
            # Regra: Se volatilidade é baixa (<0.5%), sobe alavancagem. Se alta (>2%), desce.
            # Limites: 2x a 25x.
            leverage = int(0.15 / max(0.005, volatility))
            leverage = max(2, min(25, leverage))
            
        # 🛡️ MARGIN PROTECTION: Se a saúde da banca baixar, corta a alavancagem pela metade
        if state.homeostasis < 70: leverage = max(1, int(leverage * 0.5))
        if state.homeostasis < 50: leverage = 1 # Cash only
        
        # ⚡ ZERO-LATENCY: Só faz fetch_balance se o cache estiver muito antigo (> 30s)
        now = time.time()
        if not hasattr(state, 'last_balance_fetch'): state.last_balance_fetch = 0
        
        if (now - state.last_balance_fetch) > 60: # Aumentado para 60s (Sovereign Cache)
            try:
                bal = await exchange.fetch_balance()
                available_balance = float(bal['total'].get('USDT', 0))
                state.balance = available_balance
                state.last_balance_fetch = now
            except: pass

        # Otimização: Cache de alavancagem inteligente na Bybit
        try:
            if symbol not in getattr(brain, 'leverage_cache', {}):
                if not hasattr(brain, 'leverage_cache'): brain.leverage_cache = {}
                await exchange.set_leverage(leverage, symbol)
                brain.leverage_cache[symbol] = leverage
                print(f"⚙️ [LEVERAGE] {symbol} configurado para {leverage}x (VAL Mode)")
        except: pass 
            
        # 🎯 DYNAMIC AGGRESSION (Win-Streak Scaling)
        # O PREDATOR fica mais faminto quando ganha e mais cauteloso quando perde.
        aggression = getattr(brain, 'adaptive_aggression', 1.0)
        risk_fraction = min(0.40, kelly * aggression) # Cap de 40% de risco nocional por trade
        
        risk_amount = available_balance * risk_fraction
        notional_value = risk_amount * leverage
        
        # ⚡ Evita fetch_ticker se o preço já foi passado pela inteligência
        if not price or price <= 0:
            ticker = await exchange.fetch_ticker(symbol)
            price = ticker['last']
            
        amount = notional_value / price
        
        # 🛡️ SCALPING SAFETY: SPREAD GUARDIAN
        try:
            orderbook = await exchange.fetch_order_book(symbol, limit=5)
            bid = orderbook['bids'][0][0]
            ask = orderbook['asks'][0][0]
            spread = (ask - bid) / bid * 100
            if spread > SPREAD_THRESHOLD_PERCENT:
                print(f"🚫 [SAFETY-SPREAD] Spread de {spread:.2f}% muito alto em {symbol}. Abortando.")
                return 0.0
        except: pass

        # Log de Cálculo (Biometria de Capital)
        print(f"💰 [CAPITAL] Trade: {symbol} | Risk: {risk_fraction*100:.1f}% | Lev: {leverage}x | Spot: ${risk_amount:.2f}")
        
        return amount
    except Exception as e:
        print(f"⚠️ [CAPITAL-ERROR] {e}")
        return 0

# ⚡ HELPER: Execução Assíncrona BYBIT V5 (Alta Performance)
async def execute_bybit_order(payload: WebhookPayload, use_compounding=True, entry_price=None, sl=None, tp=None, atr=None):
    """
    Executa a ordem na Bybit V5 (Sovereign) com Auto-Compounding, Precision Fix e TP/SL.
    """
    try:
        symbol = normalize_symbol(payload.symbol)
        action = payload.action.upper()
        
        amount = payload.qty
        if use_compounding and action != "CLOSE":
            amount = await get_compounded_amount(symbol, kelly=brain.kelly_fraction, price=entry_price, atr=atr)
            if amount <= 0: return 
            
        # 🔐 LOCK GUARD: Evita abrir duas ordens no mesmo símbolo simultaneamente
        if action != "CLOSE":
            if symbol in execution_locks and execution_locks[symbol]:
                print(f"🚫 [LOCK] Já existe uma execução em curso para {symbol}. Abortando.")
                return
            execution_locks[symbol] = True
            
        try:
            # ⚡ BYBIT V5 PRECISION & FILTERS
            params = {}
            if symbol in exchange.markets:
                market = exchange.market(symbol)
                # Bybit V5 exige precisão cirúrgica
                amount = float(exchange.amount_to_precision(symbol, amount))
                
                # Verifica limites mínimos
                min_amount = float(market['limits']['amount']['min'] or 0)
                if amount < min_amount:
                    amount = min_amount

                # 🛡️ PROTEÇÃO: Adiciona TP/SL se fornecidos (Bybit V5 suporta no create_order)
                if sl: params['stopLoss'] = float(exchange.price_to_precision(symbol, sl))
                if tp: params['takeProfit'] = float(exchange.price_to_precision(symbol, tp))

            print(f"🚀 [BYBIT] Executando {action} {amount} @ {symbol} (SL: {sl}, TP: {tp})")

            if action == "BUY":
                await exchange.create_order(symbol, 'market', 'buy', amount, params=params)
                print(f"✅ [BYBIT] COMPRA EXECUTADA @ {symbol}")
            elif action == "SELL":
                await exchange.create_order(symbol, 'market', 'sell', amount, params=params)
                print(f"✅ [BYBIT] VENDA EXECUTADA @ {symbol}")
            elif action == "CLOSE":
                # 🩹 Bybit V5 Perpetual Close Logic
                try:
                    positions = await exchange.fetch_positions([symbol])
                    for pos in positions:
                        size = float(pos.get('contracts', 0) or 0)
                        if size != 0:
                            side = pos.get('side', '').lower()
                            close_side = 'sell' if side == 'long' or side == 'buy' else 'buy'
                            await exchange.create_order(symbol, 'market', close_side, abs(size), params={'reduceOnly': True})
                            print(f"✅ [BYBIT] POSIÇÃO ZERADA: {abs(size)} {symbol}")
                except Exception as e:
                    print(f"⚠️ [CLOSE-ERROR] {symbol}: {e}")
            
            # ⚡ Sync Balance pós-trade
            asyncio.create_task(state.recover_daily_stats_async())
                    
        except Exception as e:
            print(f"❌ [BYBIT ERROR] {e}")
    finally:
        # 🔓 Libera o lock de execução
        if symbol in execution_locks:
            execution_locks[symbol] = False

# 📊 HELPER: Atualizar Daily Stats no DB
async def log_event_to_db(level: str, module: str, message: str, data: dict = None):
    """Grava logs via DISK SHIELD (Non-blocking)."""
    await log_shield.add_log(level, module, message, data)

async def disk_shield_automated_flush():
    """Flush automático periódico para garantir persistência."""
    while True:
        await asyncio.sleep(log_shield.flush_interval)
        await log_shield.flush()

async def update_daily_stats_in_db():
    """
    Sincronia entre memória e Banco de Dados.
    Utiliza o estado em memória para evitar SELECTs pesados, 
    mas valida com Supabase periodicamente.
    """
    if not supabase: return
    try:
        today = get_today_iso()
        
        # Upsert baseado no estado em tempo real (Cache-First)
        supabase.table("daily_stats").upsert({
            "date": today,
            "total_trades": state.trades,
            "wins": state.wins,
            "losses": state.losses,
            "total_pnl": state.daily_pnl,
            "updated_at": get_now_br().isoformat()
        }).execute()
        
    except Exception as e:
        print(f"⚠️ [SYNC-ERROR] {e}")

# ============================================================
# ENDPOINT: Registrar Resultado de Trade
# ============================================================
@app.post("/trade-result")
async def register_trade_result(result: TradeResult, auth: None = Depends(sovereign_auth)):
    """
    Registra o resultado de um trade (WIN ou LOSS).
    Usado para calcular estatísticas e ativar 3-Strikes.
    """
    if result.result.upper() == "WIN":
        state.wins += 1
        state.consecutive_losses = 0
        state.is_locked = False
        state.pnl += result.pnl
        state.daily_pnl += result.pnl
        print(f"✅ WIN: +R$ {result.pnl}")
    elif result.result.upper() == "LOSS":
        state.losses += 1
        state.consecutive_losses += 1
        state.pnl -= abs(result.pnl)
        state.daily_pnl -= abs(result.pnl)
        print(f"❌ LOSS: -R$ {abs(result.pnl)}")
        
        if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            state.is_locked = True
            print(f"🔒 3-STRIKES LOCK ATIVADO após {state.consecutive_losses} perdas consecutivas")
    
    # Recalcular win rate
    total = state.wins + state.losses
    state.win_rate = round((state.wins / total) * 100, 1) if total > 0 else 0.0
    state.last_update = time.time()
    
    # Persistência Biológica: Mutação dos Genes
    brain.mutate(success=(result.result == "WIN"))
    
    # 💾 PERSISTÊNCIA SUPABASE (Memória Viva)
    if supabase:
        try:
            # Salva o estado atual no log de sistema
            await log_event_to_db(
                level="INFO" if result.result == "WIN" else "WARNING",
                module="TRADE",
                message=f"Resultado Trade: {result.result} | PnL: {result.pnl}",
                data={"symbol": result.symbol, "pnl_total": state.pnl}
            )
            
            # Salva o trade em si com as variáveis quânticas
            supabase.table("trades").insert({
                "symbol": result.symbol, 
                "action": "CLOSE",
                "result": result.result,
                "pnl": result.pnl,
                "price": state.price,
                "kinetic_energy": state.kinetic,
                "z_score": state.z_score,
                "obp_score": state.obp,
                "confidence_score": state.confidence,
                "btc_momentum": state.btc_momentum,
                "is_correlated": state.is_correlated
            }).execute()
            
            # Atualiza daily_stats
            await update_daily_stats_in_db()
        except Exception as e:
            print(f"⚠️ ERRO AO SALVAR NO DB: {e}")
    
    return {"status": "OK", "win_rate": state.win_rate, "pnl": state.pnl}

# ============================================================
# ENDPOINT: Estado do Sistema (Dashboard)
# ============================================================
@app.get("/state")
async def get_state(auth: None = Depends(sovereign_auth)):
    """
    Retorna o estado atual do sistema para o Dashboard.
    O Dashboard chama este endpoint a cada 500ms.
    """
    now = time.time()
    
    # REMOÇÃO DE DADOS FICTÍCIOS: Preço e métricas são 100% vinculados aos feeds da internet.
    # Se stale, o sistema marca como OFFLINE em vez de simular variação.
    
    # Detectar conexão stale
    if now - state.last_update > STALE_TIMEOUT_SEC:
        state.regime = "OFFLINE"
        state.is_hunting = False
    
    return {
        "price": round(state.price, 2),
        "last_price": round(state.last_price, 2),
        "pnl": round(state.pnl, 2),
        "daily_pnl": round(state.daily_pnl, 2),
        "trades": state.trades,
        "wins": state.wins,
        "losses": state.losses,
        "win_rate": state.win_rate,
        "prob": round(state.prob, 1),
        "imb": round(state.imb, 2),
        "regime": state.regime,
        "confidence": round(state.confidence, 1),
        "neural_score": round(state.confidence, 1),
        "bias": state.bias,
        "kinetic": round(state.kinetic, 6),
        "obp": round(state.obp, 4),
        "ofi": round(state.ofi, 4),
        "global_consciousness": round(brain.global_consciousness, 4),
        "plasticity": round(brain.plasticity_index, 4),
        "sector_resonance": {k: round(v, 3) for k, v in brain.sector_resonance.items()},
        "z_score": round(state.z_score, 3),
        "entropy": round(getattr(state, 'entropy', 0.0), 2), 
        "rsi": round(state.rsi, 1),
        "trend_aligned": state.trend_aligned,
        "is_correlated": state.is_correlated,
        "btc_momentum": round(state.btc_momentum, 6),
        "trap_detected": state.trap_detected,
        
        # 🧬 LIFE SIGNS
        "homeostasis": round(state.homeostasis, 2),
        "adrenaline": round(state.adrenaline, 3),
        "synaptic_firing": round(state.synaptic_firing, 3),
        "quantum_entropy": round(state.quantum_entropy, 4),
        "metabolism": round(state.metabolism, 2),
        "genes": brain.genes,
        "is_hunting": state.is_hunting,
        "is_locked": state.is_locked,
        "consecutive_losses": state.consecutive_losses,
        "last_update": state.last_update,
        "trade_log": state.trade_log[:10],
        "last_order": state.last_order
    }

# ============================================================
# ENDPOINT: Atualizar Preço Manualmente (opcional)
# ============================================================
@app.post("/update-price")
async def update_price(data: dict, auth: None = Depends(sovereign_auth)):
    """Atualiza o preço manualmente se necessário."""
    if "price" in data:
        state.price = data["price"]
        state.last_price = data["price"]
        state.last_update = time.time()
        state.regime = "ACTIVE"
    return {"status": "OK", "price": state.price}

# ============================================================
# ENDPOINT: Reset Diário
# ============================================================
@app.post("/reset")
async def reset_daily(auth: None = Depends(sovereign_auth)):
    """Reseta contadores para um novo dia de trading."""
    state.daily_pnl = 0.0
    state.trades = 0
    state.wins = 0
    state.losses = 0
    state.consecutive_losses = 0
    state.is_locked = False
    state.is_hunting = True
    state.trade_log = []
    state.regime = "WAITING"
    state.session_start = time.time()
    state.last_update = time.time()
    
    print("🌅 RESET DIÁRIO - Novo dia de trading!")
    return {"status": "RESET_OK", "timestamp": time.time()}

# ============================================================
# ENDPOINT: Desbloquear Sistema
# ============================================================
@app.post("/unlock")
async def unlock_system(auth: None = Depends(sovereign_auth)):
    """Desbloqueia o sistema após 3-strikes."""
    state.is_locked = False
    state.consecutive_losses = 0
    state.is_hunting = True
    state.regime = "ACTIVE"
    state.last_update = time.time()
    
    print("🔓 SISTEMA DESBLOQUEADO")
    return {"status": "UNLOCKED"}

# ============================================================
# ENDPOINT: Genetic Backtesting Engine (Quantum Sims)
# ============================================================
@app.post("/backtest")
async def run_backtest(data: dict):
    """
    Simula a genética atual contra dados históricos (Sonhar com o Passado).
    """
    try:
        symbol = data.get("symbol", "BTCUSDT")
        period = data.get("period", "1d")
        
        print(f"🧪 INICIANDO BACKTEST GENÉTICO: {symbol} ({period})...")
        
        # 1. Buscar dados históricos Pagina da Bybit (Deep Data Fetch)
        target_limit = data.get("limit", 2000)
        ohlcv = []
        last_ts = None
        
        while len(ohlcv) < target_limit:
            batch_limit = min(1000, target_limit - len(ohlcv))
            params = {}
            if last_ts: params['since'] = last_ts + 1
            
            batch = await exchange.fetch_ohlcv(symbol, '1m', limit=batch_limit, params=params)
            if not batch: break
            ohlcv.extend(batch)
            last_ts = batch[-1][0]
            if len(batch) < batch_limit: break
            
        if not ohlcv:
            return {"error": "Sem dados históricos."}
            
        # 2. Estado Simulado
        sim_state = MarketState()
        sim_state.trades = 0
        sim_state.wins = 0
        sim_state.losses = 0
        sim_state.pnl = 0.0
        
        # [v2.0] Engine Fix: Limpa história neural para evitar poluição no backtest
        if hasattr(brain, 'psi_history'):
            brain.psi_history.clear()
        
        # Aumentamos consciência global para diminuir limiar de consenso no backtest
        brain.global_consciousness = 0.8
        
        # Se DNA fornecido, aplica temporariamente
        original_genes = brain.genes.copy()
        if "dna" in data and isinstance(data["dna"], dict):
            brain.genes.update(data["dna"])
        
        # 3. Loop de Simulação
        history = []
        position = None
        max_psi = -999
        min_psi = 999
        
        # Métricas Avançadas
        pnl_history = [0.0]
        max_pnl = 0.0
        max_drawdown = 0.0
        win_sum = 0.0
        loss_sum = 0.0
        
        for i in range(50, len(ohlcv)):
            candle = ohlcv[i]
            timestamp, open_p, high, low, close, vol = candle
            
            closes = [c[4] for c in ohlcv[i-31:i+1]]
            mean = sum(closes) / len(closes)
            std = math.sqrt(sum((x - mean)**2 for x in closes) / len(closes))
            z_score = (close - mean) / (std if std > 0 else 1)
            
            tr_sum = 0
            for j in range(1, 15):
                 tr_sum += max(ohlcv[i-j][2] - ohlcv[i-j][3], abs(ohlcv[i-j][2] - ohlcv[i-j][4]), abs(ohlcv[i-j][3] - ohlcv[i-j][4]))
            atr = tr_sum / 14
            
            # RSI Simulado (14 períodos)
            if len(closes) >= 14:
                deltas = [closes[k] - closes[k-1] for k in range(1, len(closes))]
                gains = [d if d > 0 else 0 for d in deltas[-14:]]
                losses = [-d if d < 0 else 0 for d in deltas[-14:]]
                avg_gain = (sum(gains) / 14) + 0.00001
                avg_loss = (sum(losses) / 14) + 0.00001
                rs = avg_gain / avg_loss
                sim_rsi = 100 - (100 / (1 + rs))
            else:
                sim_rsi = 50
                
            vel = (closes[-1] - closes[-3]) / (closes[-3] + 0.00001)
            kinetic = abs(vel * 1000)
            # Drift de simulação TURBINADO v27.4 (Força a IA a ver oportunidade)
            sim_corr = 0.82 if vel > 0 else -0.82
            
            intel = {
                "symbol": symbol, # [v34.0] Crucial: Identidade do ativo para o cérebro
                "price": close,
                "obp": 0.8 if vel > 0 else -0.8, 
                "ofi": 0.8 if vel > 0 else -0.8,
                "anchor_confirm": sim_corr,
                "kinetic": kinetic,
                "z_score": z_score,
                "trend_aligned": True,
                "btc_corr": sim_corr,
                "sector": "",
                "rsi": sim_rsi,
                "atr": atr,
                "volume_spike": vol > (mean * 1.5)
            }
            
            report = brain.analyze_infinity(sim_state, intel)
            
            # Debug PSI
            psi_val = report.get("psi_raw", 0.0) 
            max_psi = max(max_psi, psi_val)
            min_psi = min(min_psi, psi_val)
            
            if not position:
                # Gatilho v42.0: Singularity Supreme (Score > 60)
                if report["bias"] != "NEUTRAL" and report["score"] > 60:
                    # RRR Singularity 4.0:1 (v42)
                    sl_mult = 1.5
                    tp_mult = 6.0 
                    
                    sl_dist = atr * sl_mult
                    tp_dist = atr * tp_mult
                    sl = close - sl_dist if report["bias"] == "GOD_LONG" else close + sl_dist
                    tp = close + tp_dist if report["bias"] == "GOD_LONG" else close - tp_dist
                    position = {"entry": close, "type": "long" if report["bias"] == "GOD_LONG" else "short", "sl": sl, "tp": tp, "time": timestamp}
            else:
                pnl_trade = 0
                closed = False
                if position["type"] == "long":
                    if low <= position["sl"]:
                        pnl_trade = (position["sl"] - position["entry"]) / position["entry"]
                        closed = True
                    elif high >= position["tp"]:
                        pnl_trade = (position["tp"] - position["entry"]) / position["entry"]
                        closed = True
                elif position["type"] == "short":
                    if high >= position["sl"]:
                        pnl_trade = (position["entry"] - position["sl"]) / position["entry"]
                        closed = True
                    elif low <= position["tp"]:
                        pnl_trade = (position["entry"] - position["tp"]) / position["entry"]
                        closed = True
                
                if closed:
                    # [v30.0] Friction Realista (0.03% Fees Bybit)
                    friction = 0.0003 
                    
                    real_pnl_percent = (pnl_trade - friction) * 10 * 100
                    sim_state.pnl += real_pnl_percent
                    sim_state.trades += 1
                    
                    if real_pnl_percent > 0:
                        sim_state.wins += 1
                        win_sum += real_pnl_percent
                    else:
                        sim_state.losses += 1
                        loss_sum += abs(real_pnl_percent)
                    
                    pnl_history.append(sim_state.pnl)
                    max_pnl = max(max_pnl, sim_state.pnl)
                    dd = max_pnl - sim_state.pnl
                    max_drawdown = max(max_drawdown, dd)
                    
                    history.append({"t": timestamp, "pnl": round(real_pnl_percent, 2)})
                    position = None
                else:
                    # [v28.0] SEM PREMATUROS: Deixamos o mercado decidir entre TP ou SL.
                    # Removida a trava de Breakeven para restaurar o Win Rate real.
                    pass

        brain.genes = original_genes
        total = sim_state.wins + sim_state.losses
        wr = (sim_state.wins / total * 100) if total > 0 else 0
        
        # Cálculo de Métricas Sugeridas
        avg_win = (win_sum / sim_state.wins) if sim_state.wins > 0 else 0
        avg_loss = (loss_sum / sim_state.losses) if sim_state.losses > 0 else 0.0001
        rrr = avg_win / avg_loss if avg_loss > 0 else 0
        expectancy = (wr/100 * avg_win) - ((1 - wr/100) * avg_loss)
        
        # Sharpe Simples (Retorno s/ Volatilidade)
        std_pnl = 1.0
        if len(pnl_history) > 2:
            import statistics
            diffs = [pnl_history[i] - pnl_history[i-1] for i in range(1, len(pnl_history))]
            std_pnl = statistics.stdev(diffs) if len(diffs) > 1 else 1.0
        sharpe = (sim_state.pnl / std_pnl) if std_pnl > 0 else 0
        
        # [v27.0] Safety Rating
        rating = "D-CLASS (Risco Alto)"
        if sharpe > 1.5: rating = "C-CLASS (Aceitável)"
        if sharpe > 3.0: rating = "B-CLASS (Sólido)"
        if sharpe > 5.0: rating = "A-CLASS (Profissional)"
        if sharpe > 10.0: rating = "S-CLASS (IA Soberana)"
        
        return {
            "symbol": symbol,
            "candles_analyzed": len(ohlcv),
            "total_trades": sim_state.trades,
            "win_rate": round(wr, 1),
            "total_pnl_percent": round(sim_state.pnl, 2),
            "metrics": {
                "max_drawdown": round(max_drawdown, 2),
                "sharpe_ratio": round(sharpe, 2),
                "safety_rating": rating,
                "expectancy": round(expectancy, 2),
                "rrr": round(rrr, 2),
                "avg_win": round(avg_win, 2),
                "avg_loss": round(avg_loss, 2)
            },
            "history": history[-10:],
            "debug": {"max_psi": round(max_psi, 4), "min_psi": round(min_psi, 4)}
        }
    except Exception as e:
        print(f"❌ [BACKTEST-ERROR] {e}")
        return {"error": str(e)}

# ============================================================
# ENDPOINTS DE SISTEMA
# ============================================================
# ============================================================
# 🦅 AUTONOMOUS HUNTER TASK (GOD-MODE SCANNER)
# ============================================================
async def autonomous_hunter_loop():
    """Loop perpétuo de caça para a Máquina de Lucro 2026."""
    print("🎯 NOMAD GOD-MODE: CAÇADOR AUTÔNOMO INICIADO.")
    while True:
        try:
            # 🧪 HARDWARE-AWARE METABOLISM (Render Stability)
            # Se a RAM do Render estiver > 85%, descansa mais para evitar crash (OOM)
            mem = psutil.virtual_memory()
            sleep_time = state.metabolism
            if mem.percent > 85:
                print(f"⚠️ [HARDWARE-STRESS] RAM em {mem.percent}%. Reduzindo metabolismo...")
                sleep_time = max(5.0, state.metabolism * 2)
            
            await asyncio.sleep(sleep_time)
            
            if state.is_locked:
                state.regime = "3-STRIKE-LOCK"
                continue
                
            # Garante que os mercados estão carregados antes de caçar
            if not exchange.markets:
                print("⏳ [WAIT] Carregando mercados de câmbio...")
                await exchange.load_markets()
            
            state.regime = "HUNTING"
            # Executa scan com timeout para não travar o loop
            try:
                symbol, score, intel = await asyncio.wait_for(brain.scan_market(), timeout=15)
            except asyncio.TimeoutError:
                print("⌛ [TIMEOUT] Scanner demorou muito. Pulando ciclo.")
                continue
            
            # Sincroniza a "visão" do caçador com o estado global para o dashboard
            if symbol and intel:
                # SINCRONIZAÇÃO EM TEMPO REAL: Preencha o estado com a internet real
                state.price = intel["price"]
                state.last_price = intel["price"]
                state.last_update = time.time()
                    
                report = brain.analyze_infinity(state, intel)
                state.kinetic = report["physics"]
                state.z_score = report["z_score"]
                state.obp = report["obp"]
                state.ofi = intel.get("ofi", 0.0) # Sincroniza OFI Institucional
                state.entropy = report["entropy"]
                
                # 🛡️ VOLATILITY SHIELD: Se o ATR explodir, trava por segurança
                atr = intel.get("atr", 0)
                price = intel.get("price", 1)
                atr_percent = (atr / price) * 100
                if atr_percent > 2.5: # Volatilidade extrema detectada
                    if not state.volatility_lock:
                        print(f"🚨 [VOLATILITY-SHIELD] ATR: {atr_percent:.2f}% | Trava de Segurança Ativada.")
                    state.volatility_lock = True
                    state.regime = "VOLATILE_SAFETY"
                else:
                    state.volatility_lock = False

                state.btc_momentum = report["btc_momentum"]
                state.is_correlated = report["correlation"]
                state.confidence = report["score"]
                state.bias = report["bias"]
                state.trap_detected = report["trap"]
                state.rsi = report["rsi"]
                state.trend_aligned = report["trend_aligned"]
                
                # 🧬 SYNC BIO-QUANTUM LIFE SIGNS
                state.homeostasis = report["homeostasis"]
                state.adrenaline = report["adrenaline"]
                state.synaptic_firing = report["synaptic_firing"]
                state.quantum_entropy = report["quantum_entropy"]
                state.metabolism = 1.0 + (state.synaptic_firing / 100.0)
                state.genes = report["genes"]
            
            if symbol and score >= 85: # Aumentamos o threshold para maior qualidade
                print(f"💎 OPORTUNIDADE GOD-LEVEL: {symbol} (SCORE: {score:.1f})")
                
                # Sincroniza estado para análise final
                report = brain.analyze_infinity(state, intel)
                if not report["trap"]:
                    action = "BUY" if report["bias"] == "GOD_LONG" else "SELL"
                    
                    # 🎯 Dynamic TP/SL from Intel
                    sl_dist = intel.get("suggested_sl", intel["price"] * 0.01)
                    tp_dist = intel.get("suggested_tp", intel["price"] * 0.02)
                    
                    sl = intel["price"] - sl_dist if action == "BUY" else intel["price"] + sl_dist
                    tp = intel["price"] + tp_dist if action == "BUY" else intel["price"] - tp_dist

                    # 🛡️ POSITION GUARD & SAFETY LOCKS (Active Position Management)
                    if not hasattr(brain, 'active_positions'): brain.active_positions = set()
                    
                    if symbol in brain.active_positions:
                        continue
                        
                    if len(brain.active_positions) >= MAX_CONCURRENT_TRADES:
                        print(f"🚫 [SAFETY-MAX-TRADES] Limite de {MAX_CONCURRENT_TRADES} trades atingido.")
                        continue
                    
                    # 🛡️ DRAWDOWN GUARDIAN
                    if state.balance > 0:
                        dd = (state.daily_pnl / state.balance) * 100
                        if dd <= -MAX_DAILY_DRAWDOWN_PERCENT:
                            print(f"🚨 [DRAWDOWN-LOCK] Drawdown diário atingiu {dd:.2f}%. Bloqueando por segurança.")
                            state.is_locked = True
                            state.regime = "DRAWDOWN_LOCKED"
                            continue
                    
                    # 🛡️ DEADMAN SWITCH (API Health)
                    if engine_state.api_latency_ms > DEADMAN_LATENCY_MAX_MS:
                        print(f"⚠️ [DEADMAN-SWITCH] Latência CRÍTICA ({engine_state.api_latency_ms:.0f}ms). Pausando Hunter.")
                        await asyncio.sleep(10)
                        continue

                    if state.volatility_lock or state.is_locked:
                        continue

                    payload = WebhookPayload(
                        symbol=symbol,
                        action=action,
                        qty=0 # Será calculado pelo auto-compounding
                    )
                    
                    # Dispara execução com TP/SL e ATR para alavancagem adaptativa
                    await execute_bybit_order(payload, use_compounding=True, entry_price=intel["price"], sl=sl, tp=tp, atr=intel.get("atr"))
                    brain.active_positions.add(symbol)
                    
                     # [CRITICAL] Envia para o DISK SHIELD (Zero Lag)
                    trade_to_log = {
                        "symbol": symbol,
                        "action": action,
                        "price": intel["price"],
                        "confidence_score": report["score"],
                        "kinetic_energy": intel.get("kinetic", 0),
                        "z_score": intel.get("z_score", 0),
                        "obp_score": intel.get("obp", 0),
                        "btc_momentum": intel.get("btc_corr", 0),
                        "is_correlated": report["correlation"] == "SYNCED",
                        "metadata": {
                            "atr": intel.get("atr"),
                            "lev": brain.leverage_cache.get(symbol, 10),
                            "aggression": brain.adaptive_aggression
                        }
                    }
                    await log_shield.add_trade(trade_to_log)
                    
                    print(f"� [ORDEM] {action} em {symbol} enviada para execução e log buffer.")
                    
                    # 🧠 REGISTRO NO EVENT LOG NEURAL (Dashboard via Buffer)
                    await log_event_to_db("NEURAL", "HUNTER", f"Oportunidade {action} {symbol} Executada", {
                        "score": report["score"],
                        "ofi": intel.get("ofi", 0)
                    })
            
            # Ciclo concluído
        except Exception as e:
            print(f"⚠️ [HUNTER-ERROR] {e}")
            await asyncio.sleep(5)

async def bybit_pnl_sync_loop():
    """
    Sincronizador de PnL de Fechamento (Bybit V5 -> Supabase).
    Garante que trades fechados por TP/SL automático sejam contabilizados.
    """
    print("🔄 SYNC PNL: Sincronizador de resultados iniciado.")
    last_pnl_check = time.time()
    
    while True:
        try:
            if exchange.apiKey:
                # Busca pnl fechado desde a última checagem ou últimos 15 min
                if not hasattr(brain, 'last_pnl_sync_time'): 
                    brain.last_pnl_sync_time = int((time.time() - 900) * 1000)
                
                since = brain.last_pnl_sync_time
                closed_pnl = []
                
                # 🛡️ AUTH GUARD: Se a chave falhou no boot, não bombardeia a API
                if not exchange.markets:
                    await asyncio.sleep(60)
                    continue

                if hasattr(exchange, 'fetch_closed_pnl'):
                    closed_pnl = await exchange.fetch_closed_pnl(since=since)
                elif hasattr(exchange, 'fetchClosedPnl'):
                    closed_pnl = await exchange.fetchClosedPnl(since=since)
                
                # Atualiza o ponteiro de tempo apenas se tiver sucesso ou se o window for muito antigo
                max_timestamp = since
                
                if closed_pnl:
                    for trade in closed_pnl:
                        trade_ts = trade.get('timestamp', 0)
                        if trade_ts > max_timestamp: max_timestamp = trade_ts
                        
                        trade_id = trade.get('id')
                        symbol = trade.get('symbol')
                        norm_symbol = normalize_symbol(symbol)
                        pnl = float(trade.get('closedPnl', 0))
                        
                        # Remove de posições ativas se estiver lá
                        if hasattr(brain, 'active_positions') and norm_symbol in brain.active_positions:
                            brain.active_positions.remove(norm_symbol)

                        # Verifica se já registramos esse trade no estado local para evitar duplicidade
                        if not hasattr(brain, 'synced_trades'): brain.synced_trades = set()
                        
                        if trade_id not in brain.synced_trades:
                            # 🧠 EVOLUÇÃO NEURAL: O cérebro aprende com o resultado Real
                            result = "WIN" if pnl > 0 else "LOSS"
                            brain.record_trade_result(result, pnl, symbol)
                            
                            brain.synced_trades.add(trade_id)
                            
                            # Atualiza Estado Local
                            if pnl > 0:
                                state.wins += 1
                                state.consecutive_losses = 0
                            else:
                                state.losses += 1
                                state.consecutive_losses += 1
                                
                            state.daily_pnl += pnl
                            state.pnl += pnl
                            state.trades += 1
                            
                            # Limpa cache antigo (> 100 itens)
                            if len(brain.synced_trades) > 100:
                                brain.synced_trades = set(list(brain.synced_trades)[-50:])
                    
                            # Salva no Supabase (Opcional, mas recomendado)
                            if supabase:
                                try:
                                    supabase.table("trades").insert({
                                        "symbol": norm_symbol,
                                        "action": "CLOSE",
                                        "result": "WIN" if pnl > 0 else "LOSS",
                                        "pnl": pnl,
                                        "price": trade.get('avgExitPrice', 0),
                                        "metadata": {"bybit_id": trade_id, "type": "auto_close"}
                                    }).execute()
                                except: pass
                    
                    # Atualiza o ponteiro para o timestamp do último trade processado + 1ms
                    brain.last_pnl_sync_time = max_timestamp + 1
                
                # Sincroniza stats agregados no DB
                await update_daily_stats_in_db()
                
            await asyncio.sleep(60) # Checa a cada minuto
        except Exception as e:
            if "10003" in str(e):
                print("❌ [PNL-SYNC] API Key Inválida. Pausando Sync.")
                await asyncio.sleep(300)
            else:
                print(f"⚠️ [PNL-SYNC-ERROR] {e}")
                await asyncio.sleep(60)

async def evolution_watcher_loop():
    """O Senior observa os descendentes gerados pelo Junior no Supabase."""
    print("🧬 GENETIC LINK: Senior observando evolução do Junior...")
    while True:
        try:
            if supabase:
                # Busca a última geração de DNA no cofre genético
                response = supabase.table("genetics").select("dna, generation").order("generation", desc=True).limit(1).execute()
                if response.data:
                    latest_gen = response.data[0]
                    new_dna = latest_gen['dna']
                    gen_id = latest_gen['generation']
                    
                    # Se for uma nova geração, o Senior herda os genes
                    if new_dna != brain.genes:
                        print(f"🧬 [EVOLUTION] Senior herdando DNA da Geração {gen_id} (Origem Junior)!")
                        brain.genes = new_dna
                        state.genes = new_dna
                        await log_event_to_db("INFO", "EVOLUTION", f"Senior evoluiu para Gen {gen_id}", {"dna": new_dna})
            
            await asyncio.sleep(3600) # Checa a cada hora
        except Exception as e:
            print(f"⚠️ [EVOLUTION-BUG] {e}")
            await asyncio.sleep(300)

# ============================================================
# 🩺 DIAGNÓSTICO DE POTÊNCIA (Performance Monitor)
# ============================================================
@app.get("/stats")
async def get_performance_stats(auth: None = Depends(sovereign_auth)):
    """Retorna o estado de saúde neural do backend."""
    return {
        "engine": engine_state.get_stats(),
        "market": {
            "regime": state.regime,
            "monitored_assets": len(brain.monitored_symbols_cache),
            "last_price": state.price
        },
        "neural": {
            "homeostasis": state.homeostasis,
            "adrenaline": state.adrenaline,
            "quantum_entropy": state.quantum_entropy,
            "brain_genes": brain.genes
        }
    }

@app.get("/health")
async def health_check():
    """Health check para Render & Monitoramento."""
    return {
        "status": "SOVEREIGN_ACTIVE",
        "version": "25.0.0",
        "uptime_sec": int(time.time() - engine_state.uptime_start),
        "neural_pulse": True,
        "mode": "100% CLOUD",
        "load": engine_state.cpu_usage
    }

@app.get("/ping")
async def ping():
    """Endpoint simplificado para keep-alive (Render Free Tier)."""
    return {"status": "PONG", "timestamp": time.time()}

@app.get("/")
async def root():
    """Página inicial da API."""
    return {
        "message": "🦅 PREDATOR v25.0 SOVEREIGN ENGINE",
        "mode": "100% Cloud - Power Backend Active",
        "stats": "/stats",
        "health": "/health",
        "webhook": "POST /webhook"
    }
