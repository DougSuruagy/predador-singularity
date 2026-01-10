"""
PREDATOR v21.2 APEX MUTATION - Cloud API (Render)
═══════════════════════════════════════════════════════════════
100% CLOUD | ZERO LOCAL | CUSTO ZERO

Fluxo:
  TradingView (Pine Script) → Webhook → Esta API → Dashboard (Vercel)

Características:
  ✅ Recebe sinais do TradingView via webhook
  ✅ Processa ordens com lógica de Estoque Zero
  ✅ Alimenta o Dashboard em tempo real
  ✅ 3-Strikes Rule para proteção
  ✅ Pronto para integrar com API de corretora
═══════════════════════════════════════════════════════════════
"""
from fastapi import FastAPI, HTTPException
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

# ============================================================
# ⚙️ GLOBAL UTILS & TIMEZONE (Fix: Douglas -03:00)
# ============================================================
def get_today_iso():
    # Douglas está em UTC-3. Forçamos a data para ser consistente com o dia dele.
    return (datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%d")

def get_now_br():
    return datetime.utcnow() - timedelta(hours=3)

# Carregar variáveis de ambiente locais (.env) se existirem
load_dotenv()

app = FastAPI(
    title="PREDATOR v21.2 - APEX MUTATION",
    version="21.2.0",
    description="A Máquina de Lucro Definitiva para o Mercado Cripto 2026"
)

# ============================================================
# 🧠 NEURAL CORE 2026 - PREDATOR APEX V16.0 (ANTI-INSTITUTIONAL)
# ============================================================
# ============================================================
# 🧠 NEURAL CORE 2026 - PREDATOR OMEGA-SINGULARITY V19.0
# 🚀 (PHYSICS + PURE MATH + QUANTUM STATS)
# ============================================================
# ============================================================
# 🧠 NEURAL CORE 2026 - PREDATOR v21.0 'NOMAD-INFINITY'
# 🚀 (AUTONOMOUS MARKET SCANNER + GOD-MODE EXECUTION)
# ============================================================
import math

class NomadBrain:
    def __init__(self):
        # 🟢 MULTI-OCULAR SYSTEM (OLHOS)
        self.eyes = {
            "DEFI": ["UNI/USDT", "AAVE/USDT", "LINK/USDT"],
            "L1": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "ADA/USDT"],
            "MEMES": ["DOGE/USDT", "PEPE/USDT", "WIF/USDT", "SHIB/USDT"],
            "AI": ["NEAR/USDT", "FET/USDT", "RENDER/USDT"]
        }
        self.market_watchlist = []
        for v in self.eyes.values(): self.market_watchlist.extend(v)
        
        # 🧠 MULTI-CEREBRAL CORTEX (CÉREBROS EXPANSORES)
        self.genes = {
            "frontal_weight": 0.35,   # Lógica/EMA
            "occipital_weight": 0.35, # Visão de Fluxo/OBP
            "amygdala_weight": 0.15,  # Emoção/Risco/Adrenalina
            "parietal_weight": 0.15   # Espacial/Liquidez (Depth)
        }
        
        # 🦴 CEREBELO (Memória Muscular / Execução)
        self.muscle_memory = {"avg_latency": 0.2, "success_rate": 0.0}
        
        self.restricted_symbols = set()
        
        # 🧬 BIO-QUANTUM LIFE SIGNS
        self.metabolism = 1.0           # Taxa de processamento biológico
        self.adrenaline = 0.0           # Resposta ao estresse de mercado
        self.homeostasis = 100.0        # Saúde do sistema (Banca R$ 100)
        self.quantum_entropy = 0.1      # Desordem quântica
        self.synaptic_firing = 0.0      # Intensidade de sinais neurais
        self.btc_momentum = 0.0
        self.btc_last_price = 0.0
        self.btc_last_fetch = 0.0
        self.kelly_fraction = 0.20
        self.leverage_cache = {} 
        self.last_balance = 0.0
        self.last_balance_time = 0.0

    async def scan_market(self):
        best_opportunity = None
        highest_score = 0
        best_intel = None
        
        try:
            # Seleciona os ativos mais quentes de cada "Olho" para análise
            all_tickers = await exchange.fetch_tickers()
            candidates = []
            
            for sector, symbols in self.eyes.items():
                for sym in symbols:
                    ticker = all_tickers.get(sym)
                    if ticker and ticker['quoteVolume'] > 5000000:
                        score_v = abs(ticker.get('percentage', 0))
                        candidates.append((sym, score_v, sector))
            
            # Ordena por volatilidade setorial
            candidates.sort(key=lambda x: x[1], reverse=True)
            discovery = [c[0] for c in candidates[:10]]
            
            # [PERFORMANCE-BOOST] Fetch BTC once for all symbols in this scan
            btc_intel = await exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=10)
            btc_closes = [c[4] for c in btc_intel]
            self.btc_momentum = (btc_closes[-1] - btc_closes[0]) / btc_closes[0]
            self.btc_last_price = btc_closes[-1]
            self.btc_last_fetch = time.time()
            
            # Escaneamento Paralelo Bio-Sincronizado
            tasks = [self.fetch_god_intelligence(symbol, btc_provided=True) for symbol in discovery]
            results = await asyncio.gather(*tasks)
            
            for intel in results:
                if not intel: continue
                # Score Neural: OBP + Cinética + RSI
                score = (abs(intel["obp"]) * 50) + (intel["kinetic"] * 50)
                if score > highest_score:
                    highest_score = score
                    best_opportunity = intel["symbol"]
                    best_intel = intel
                    
        except Exception as e:
            print(f"⚠️ [SCAN-ERROR] {e}")

        return best_opportunity, highest_score, best_intel

    def mutate(self, success: bool):
        """MOTOR DE MUTAÇÃO GENÉTICA: Evolui os pesos neurais baseados no lucro."""
        mutation_rate = 0.05
        if success:
            # Se deu lucro, reforça os lobos frontais e occipitais (Análise Fria)
            self.genes["frontal_weight"] += mutation_rate
            self.genes["occipital_weight"] += mutation_rate
            self.genes["amygdala_weight"] -= mutation_rate
        else:
            # Se deu prejuízo, reforça a Amígdala (Risco/Instinto)
            self.genes["amygdala_weight"] += mutation_rate
            self.genes["frontal_weight"] -= mutation_rate
            self.genes["occipital_weight"] -= mutation_rate
        
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
            target = f"{symbol}/USDT" if "/" not in symbol else symbol
            # ⚓ ÂNCORA BTC + ATIVO ALVO PARALELIZADO
            # Otimização: Se BTC já foi buscado no loop de scan, evita a chamada repetida
            if not btc_provided:
                tasks = [
                    exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=10),
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
            
            if not btc_provided:
                btc_ohlcv = results[0]
                btc_closes = [c[4] for c in btc_ohlcv]
                self.btc_momentum = (btc_closes[-1] - btc_closes[0]) / btc_closes[0]
                self.btc_last_price = btc_closes[-1]
            
            # 📊 ATIVO ALVO
            ob = results[1]
            bids_vol = sum([b[1] for b in ob['bids']])
            asks_vol = sum([a[1] for a in ob['asks']])
            obp = (bids_vol - asks_vol) / (bids_vol + asks_vol) if (bids_vol + asks_vol) > 0 else 0
            
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
            
            return {
                "obp": obp, 
                "kinetic": kinetic, 
                "z_score": z_score, 
                "symbol": symbol,
                "btc_corr": self.btc_momentum,
                "price": closes[-1],
                "rsi": rsi,
                "trend_aligned": trend_aligned
            }
            
        except Exception as e:
            if "451" in str(e):
                print(f"🚫 [RESTRICTED] {symbol} está bloqueado nesta região (Error 451). Use um PROXY_URL.")
                self.restricted_symbols.add(symbol)
            else:
                print(f"⚠️ INTEL FAILURE: {e}")
            return None

    def analyze_infinity(self, state, intel=None):
        # 🧠 LOBO OCCIPITAL (Visão de Fluxo)
        obp = intel["obp"] if intel else 0.0
        occipital_signal = (obp * self.genes["occipital_weight"])
        
        # 🧠 LOBO FRONTAL (Lógica de Tendência e Preço)
        kinetic = intel["kinetic"] if intel else 0.0
        trend_aligned = intel.get("trend_aligned", True) if intel else True
        rsi = intel.get("rsi", 50) if intel else 50
        frontal_signal = (kinetic * 0.5 + (1 if trend_aligned else -1) * 0.5) * self.genes["frontal_weight"]
        
        # 🧠 LOBO PARIETAL (Integração de Liquidez Espacial)
        # Se o preço está perto de uma parede de liquidez (OBP alto), o sinal parietal é forte
        parietal_signal = (abs(obp) * 2.0) * self.genes["parietal_weight"]
        
        # 🧠 AMÍGDALA (Resposta ao Risco e Adrenalina)
        z_score = intel["z_score"] if intel else 0.0
        vol_stress = abs(z_score) * 0.3
        self.adrenaline = max(0, min(1.0, vol_stress))
        amygdala_signal = (1.0 - self.adrenaline) * self.genes["amygdala_weight"]
        
        # ⚛️ COOPERAÇÃO SINÁPTICA: Um único sinal harmônico
        psi = (occipital_signal + frontal_signal + amygdala_signal + parietal_signal)
        self.quantum_entropy = abs(psi - obp)
        
        entropy = abs(z_score) / (kinetic + 0.0001)
        btc_corr = intel["btc_corr"] if intel else state.btc_momentum
        is_correlated = (psi > 0 and btc_corr > 0) or (psi < 0 and btc_corr < 0)
        
        # 🛡️ HOMEOSTASE (Estado de Saúde da Banca)
        pnl_impact = (state.daily_pnl / 100.0)
        self.homeostasis = max(0, min(100, 100 + (pnl_impact * 50)))
        
        # 🛡️ ESCUDO DE REALIDADE (BIO-QUANTUM SHIELD)
        rsi_trap = (psi > 0 and rsi > 70) or (psi < 0 and rsi < 30)
        reality_trap = (abs(z_score) > 2.8) or (not is_correlated) or (entropy > 6.0) or rsi_trap or (self.homeostasis < 40)
        
        bias = "NEUTRAL"
        consensus_threshold = 0.20
        if psi > consensus_threshold and is_correlated and trend_aligned: bias = "GOD_LONG"
        if psi < -consensus_threshold and is_correlated and trend_aligned: bias = "GOD_SHORT"
        
        # SINAPSE: Intensidade do disparo neural
        self.synaptic_firing = (abs(psi) * 100)
        confidence = min(100, self.synaptic_firing * (0.4 if not is_correlated else 1.0))
        
        # 🧬 MUTAÇÃO ALPHA: Ajuste de Potência Bio-Mecânica
        alpha = 4.0 if confidence > 92 and not reality_trap else 1.0
        if self.adrenaline > 0.7: alpha *= 1.5 
        
        # Otimização Kelly: Se banca está saudável (Homeostasis), arrisca mais para rendimento ICP
        kelly = 0.20 + (0.10 if self.homeostasis > 85 else 0.0)
        
        return {
            "score": confidence,
            "bias": bias,
            "trap": reality_trap,
            "alpha": alpha,
            "kelly": kelly,
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

# BINANCE CONNECTION (Custo Zero - Sem MT5)
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

# 🌐 CONFIGURAÇÃO DE PROXY (Opcional - Para contornar bloqueios regionais)
PROXY_URL = os.environ.get("PROXY_URL") # Ex: http://user:pass@host:port
proxies = {'http': PROXY_URL, 'https': PROXY_URL} if PROXY_URL and PROXY_URL.strip() else None

# Configurar Exchange (Modo Futures - Otimizado para Baixa Latência)
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True,
        'recvWindow': 5000,
    },
    'proxies': proxies
})

# Task para manter a sessão da exchange viva e evitar reconexões lentas
async def maintain_exchange_session():
    while True:
        try:
            if exchange.apiKey:
                await exchange.fetch_balance()
            await asyncio.sleep(60)
        except:
            pass

# Se as chaves estiverem presentes, testa conexão e configura alavancagem
if BINANCE_API_KEY and BINANCE_API_SECRET:
    try:
        print("⚡ CONECTANDO À BINANCE FUTURES...")
        async def setup_account():
            try:
                await exchange.load_markets()
                print("✅ MERCADOS CARREGADOS E AMBIENTE BINANCE PRONTO.")
            except Exception as e:
                print(f"⚠️ ERRO AO CARREGAR MERCADOS: {e}")
        asyncio.create_task(setup_account())
    except Exception as e:
        print(f"⚠️ ERRO BINANCE: {e}")
else:
    print("⚠️ BINANCE API KEYS AUSENTES: Execução real bloqueada. Apenas Simulação.")

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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# VARIÁVEIS DE CONFIGURAÇÃO (Ajuste conforme necessário)
# ============================================================
MAX_CONSECUTIVE_LOSSES = 3      # 3-Strikes Rule
POSICAO_ZERO_HOUR = 17          # Hora limite (Day Trade Only)
POSICAO_ZERO_MIN = 30           # Minuto limite
STALE_TIMEOUT_SEC = 120         # Tempo sem update = offline
INITIAL_PRICE = 0.0             # Preço inicial (0 para aguardar dados reais)

# ============================================================
# ESTADO DO SISTEMA (Mantido em memória - Custo Zero)
# ============================================================
class MarketState:
    def __init__(self):
        # Preço e Métricas
        self.price: float = INITIAL_PRICE
        self.last_price: float = INITIAL_PRICE
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
        self.kinetic: float = 0.0
        self.z_score: float = 0.0
        self.kelly: float = 0.15
        self.is_correlated: bool = True
        self.alpha_scale: float = 1.0
        self.compounding: float = 0.30 
        self.regime: str = "WAITING"
        self.confidence: float = 80.0
        self.bias: str = "NEUTRAL"
        self.is_hunting: bool = True
        self.is_locked: bool = False
        self.trap_detected: bool = False
        self.entropy: float = 0.0
        self.rsi: float = 50.0
        self.trend_aligned: bool = True
        
        # 🧬 BIOMETRICS (LIVING ORGANISM v21.1)
        self.homeostasis: float = 100.0
        self.adrenaline: float = 0.0
        self.synaptic_firing: float = 0.0
        self.quantum_entropy: float = 0.0
        self.metabolism: float = 1.0
        
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
async def trigger_panic():
    """Aciona o modo PÂNICO: Fecha tudo e trava o sistema."""
    state.pending_command = "PANIC"
    state.is_locked = True
    state.regime = "PANIC_MODE"
    print("🚨 PÂNICO ACIONADO VIA DASHBOARD!")
    return {"status": "PANIC_TRIGGERED"}

@app.post("/command/clear")
async def clear_command():
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
async def tradingview_webhook(payload: WebhookPayload, intel_cache: dict = None):
    """
    Recebe sinais do TradingView e processa.
    O parâmetro intel_cache evita chamadas repetidas à API da Binance.
    """
    now = get_now_br()
    
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
    
    # [SEGURANÇA] Verificar se está em modo de caça
    if not state.is_hunting or state.is_locked:
        return {
            "status": "REJECTED",
            "reason": "SYSTEM_PAUSED",
            "message": "Sistema em pausa. Aguarde desbloqueio."
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
        
        # Valor da posição nominal (com alavancagem implícita)
        # v21.2: Multiplicamos pela 'adrenaline' para ordens maiores em momentos de alta confiança
        notional_value = capital_usd * risk_fraction * 15 * state.alpha_scale 
        
        final_qty = notional_value / (intel["price"] if intel else state.price)
        if final_qty <= 0: final_qty = 0.001 
            
        payload.qty = round(final_qty, 6)
        asyncio.create_task(execute_binance_order(payload))
    # ═══════════════════════════════════════════════════════════
    
    return {
        "status": "INFINITY_SINGULARITY_REACHED",
        "bias": report["bias"],
        "alpha": f"x{state.alpha_scale}",
        "kelly": f"{state.kelly * 100:.1f}%",
        "correlation": "SYNCED" if state.is_correlated else "DISCONNECTED",
        "message": "Predator NOMAD v21.1: Física e Correlação em Sintonia."
    }

# ⚡ HELPER: Gestão de Capital Auto-Compounding (Caixa Preta)
async def get_compounded_amount(symbol, kelly=0.20):
    """Calcula o tamanho do lote baseado no saldo real da Binance com alavancagem."""
    try:
        # Cache de saldo por 60 segundos para evitar Rate Limit
        now = time.time()
        if brain.last_balance == 0 or (now - brain.last_balance_time) > 60:
            balance = await exchange.fetch_balance()
            brain.last_balance = float(balance['total'].get('USDT', 0))
            brain.last_balance_time = now
            print(f"💰 [CAPITAL] Saldo Atualizado: ${brain.last_balance:.2f} USDT")
        
        capital = brain.last_balance
        if capital < 5: return 0 # Segurança mínima
        
        # Lógica de Lote: (Capital * Fração de Kelly * Alavancagem) / Preço Atual
        ticker = await exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        # Alavancagem agressiva de 15x
        leverage = 15
        risk_amount = capital * kelly * leverage
        amount = risk_amount / price
        
        return amount
    except Exception as e:
        print(f"⚠️ [CAPITAL-ERROR] {e}")
        return 0

# ⚡ HELPER: Execução Assíncrona Binance (Alta Performance)
async def execute_binance_order(payload: WebhookPayload, use_compounding=True):
    """Executa a ordem na Binance com Auto-Compounding."""
    try:
        symbol = payload.symbol.upper()
        if "/" not in symbol:
            symbol = f"{symbol}/USDT" if "USDT" not in symbol else symbol
        
        action = payload.action.upper()
        
        # Se for Black Box, ignora a quantidade do payload e calcula sozinho
        amount = payload.qty
        if use_compounding and action != "CLOSE":
            amount = await get_compounded_amount(symbol, kelly=brain.kelly_fraction)
            if amount == 0: return # Saldo insuficiente ou erro
        
        # Ajuste de Precisão (Lot Size)
        if symbol in exchange.markets:
            market = exchange.market(symbol)
            amount = exchange.amount_to_precision(symbol, amount)
            print(f"🎯 [PRECISION] Lote ajustado: {amount} {symbol}")
        
        print(f"🚀 [BINANCE] Processando {action} {amount} {symbol}...")
        
        # [PERFORMANCE-BOOST] Caching de Alavancagem para evitar chamadas de rede redundantes
        target_lev = 15
        if symbol not in brain.leverage_cache or brain.leverage_cache[symbol] != target_lev:
            try:
                await exchange.set_leverage(target_lev, symbol)
                brain.leverage_cache[symbol] = target_lev
                print(f"⚡ [LEVERAGE] {symbol} definido para {target_lev}x")
            except: pass

        if action == "BUY":
            await exchange.create_market_buy_order(symbol, amount)
            print(f"✅ [BINANCE] COMPRA EXECUTADA @ {symbol}")
        elif action == "SELL":
            await exchange.create_market_sell_order(symbol, amount)
            print(f"✅ [BINANCE] VENDA EXECUTADA @ {symbol}")
        elif action == "CLOSE":
            # Otimização: Uso de fetch_position_risk para precisão absoluta em futuros
            positions = await exchange.fetch_position_risk(symbols=[symbol])
            for pos in positions:
                size = float(pos.get('positionAmt', 0))
                if size != 0:
                    side = 'sell' if size > 0 else 'buy'
                    await exchange.create_market_order(symbol, side, abs(size), params={'reduceOnly': True})
                    print(f"✅ [BINANCE] POSIÇÃO ZERADA: {abs(size)} {symbol}")
                    await log_event_to_db("INFO", "EXECUTION", f"Posição zerada: {symbol}", {"size": size})
                    
    except Exception as e:
        print(f"❌ [BINANCE ERROR] Falha Crítica na Execução: {e}")

# 📊 HELPER: Atualizar Daily Stats no DB
async def log_event_to_db(level: str, module: str, message: str, data: dict = None):
    """Grava logs críticos no Supabase (Caixa-Preta 2026)."""
    try:
        if supabase:
            log_data = {
                "level": level,
                "module": module,
                "message": message,
                "data": data or {}
            }
            supabase.table("system_logs").insert(log_data).execute()
    except Exception as e:
        print(f"⚠️ [LOG-ERROR] {e}")

async def update_daily_stats_in_db():
    """
    Sincronia entre memória e Banco de Dados.
    BUG FIX: Agora utiliza agregação SQL para maior performance em escala.
    """
    if not supabase: return
    try:
        today = get_today_iso()
        
        # AGREGAÇÃO EM LADO SERVIDOR (Supabase): Mil vezes mais rápido que baixar todos os trades.
        # Buscamos os stats básicos para confirmar sincronia
        response = supabase.table("trades") \
            .select("pnl, result, kinetic_energy, confidence_score, is_correlated") \
            .gte("created_at", today) \
            .execute()
            
        trades_data = response.data
        if not trades_data: return
        
        total = len(trades_data)
        wins = sum(1 for t in trades_data if t.get('result') == 'WIN')
        losses = sum(1 for t in trades_data if t.get('result') == 'LOSS')
        pnl_sum = sum(float(t.get('pnl') or 0.0) for t in trades_data)
        
        # Upsert (Estratégia Ágil)
        supabase.table("daily_stats").upsert({
            "date": today,
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "total_pnl": pnl_sum,
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        
    except Exception as e:
        print(f"⚠️ [SYNC-ERROR] {e}")

# ============================================================
# ENDPOINT: Registrar Resultado de Trade
# ============================================================
@app.post("/trade-result")
async def register_trade_result(result: TradeResult):
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
async def get_state():
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
async def update_price(data: dict):
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
async def reset_daily():
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
async def unlock_system():
    """Desbloqueia o sistema após 3-strikes."""
    state.is_locked = False
    state.consecutive_losses = 0
    state.is_hunting = True
    state.regime = "ACTIVE"
    state.last_update = time.time()
    
    print("🔓 SISTEMA DESBLOQUEADO")
    return {"status": "UNLOCKED"}

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
            # Garante que os mercados estão carregados antes de caçar (Crucial para precisão de lotes)
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
                state.entropy = report["entropy"]
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
            
            if symbol and score >= 95:
                print(f"💎 OPORTUNIDADE GOD-LEVEL: {symbol} (SCORE: {score:.1f})")
                await log_event_to_db("INFO", "SCANNER", f"Oportunidade detectada: {symbol}", {"score": score, "bias": state.bias})
                
                intel = await brain.fetch_god_intelligence(symbol)
                report = brain.analyze_infinity(state, intel)
                
                if not report["trap"]:
                    # Cria payload simulado de webhook para reaproveitar execução
                    payload = WebhookPayload(
                        action="BUY" if report["bias"] == "GOD_LONG" else "SELL",
                        symbol=symbol,
                        price=intel["price"], 
                        qty=0.001, # Mínimo inicial p/ escala
                        confidence=report["score"]
                    )
                    # Dispara execução com AUTO-COMPOUNDING ativado
                    await execute_binance_order(payload, use_compounding=True)
            
            # Intervalo de scan (Alta Frequência mas respeitando limites de API)
            await asyncio.sleep(10) 
        except Exception as e:
            print(f"📡 [HUNTER-ERROR] {e}")
            await asyncio.sleep(30)

@app.on_event("startup")
async def startup_event():
    """Inicia a alma da máquina ao subir o servidor com Recuperação Rápida."""
    print("🔥 PREDATOR BOOT: Iniciando Motores...")
    
    # 1. Recuperação prioritária do estado (Garante Dashboard correto após hibernation)
    await state.recover_daily_stats_async()
    
    # 2. Carregamento de mercados em background para não travar o boot
    asyncio.create_task(exchange.load_markets())
    
    # 3. Loops perpétuos
    asyncio.create_task(maintain_exchange_session())
    asyncio.create_task(autonomous_hunter_loop())
    
    print("🚀 SISTEMA ONLINE E RECUPERADO.")

@app.get("/health")
async def health_check():
    """Health check para Render."""
    return {
        "status": "OK",
        "version": "21.2.0",
        "mode": "100% CLOUD | AUTONOMOUS",
        "uptime_seconds": round(time.time() - state.session_start, 0),
        "hunting": state.is_hunting
    }

@app.get("/")
async def root():
    """Página inicial da API."""
    return {
        "message": "🦅 PREDATOR v21.2 APEX MUTATION",
        "mode": "100% Cloud - Zero Local",
        "docs": "/docs",
        "status": "/state",
        "webhook": "POST /webhook"
    }

# ============================================================
# INFORMAÇÕES DE USO
# ============================================================
"""
═══════════════════════════════════════════════════════════════
COMO USAR (100% Cloud - Sem MetaTrader Local):
═══════════════════════════════════════════════════════════════

1. DEPLOY NO RENDER:
   - Conecte o repo GitHub ao Render
   - Render detectará o render.yaml automaticamente
   - Anote a URL: https://seu-app.onrender.com

2. CONFIGURAR TRADINGVIEW:
   - Crie/edite sua estratégia Pine Script
   - Configure Alert com Webhook URL:
     https://seu-app.onrender.com/webhook
   
   - Payload JSON:
     {
       "action": "{{strategy.order.action}}",
       "symbol": "WING26",
       "price": {{close}},
       "confidence": 85
     }

3. DASHBOARD NA VERCEL:
   - Conecte o repo GitHub à Vercel
   - Atualize CONFIG.API_URL no main.js com a URL do Render
   - Deploy automático!

4. TESTAR:
   - Acesse a API: https://seu-app.onrender.com/docs
   - Use o endpoint POST /webhook para simular sinais
   - Veja o Dashboard atualizar em tempo real!

═══════════════════════════════════════════════════════════════
"""
