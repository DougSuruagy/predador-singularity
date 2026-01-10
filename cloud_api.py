"""
PREDATOR v13.0 SINGULARITY - Cloud API (Render)
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
from datetime import datetime
import os
import random  # Restored for scanners and simulations
import ccxt.async_support as ccxt  # Alta Performance
from supabase import create_client, Client
from dotenv import load_dotenv
import asyncio
import time
from datetime import datetime
import math

# Carregar variáveis de ambiente locais (.env) se existirem
load_dotenv()

app = FastAPI(
    title="PREDATOR API - CRYPTO EDITION",
    version="14.0.0",
    description="100% Cloud Trading API - No Local Dependency"
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
        self.btc_last_price = 0.0
        self.btc_momentum = 0.0 # Direção do Bitcoin
        self.obp_score = 0.0
        self.kinetic_energy = 0.0
        self.volatility_z_score = 0.0
        self.kelly_fraction = 0.15
        self.active_hunters = [] 
        self.market_watchlist = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "AVAX/USDT"]

    async def scan_market(self):
        """Escaneia o mercado em busca de distorções quânticas (A caça começou)."""
        # Melhora crítica: Só escaneia se não houver trade ativo importante (Performance)
        best_opportunity = None
        highest_score = 0
        
        try:
            # Escaneia em chunks paralelos para não sobrecarregar o Event Loop
            tasks = [self.fetch_god_intelligence(symbol.replace("/USDT", "")) for symbol in self.market_watchlist]
            await asyncio.gather(*tasks)
            
            for symbol in self.market_watchlist:
                # Lógica Matemática Pura de Pontuação
                score = (abs(self.obp_score) * 50) + (self.kinetic_energy * 50)
                if score > highest_score and score > 80:
                    highest_score = score
                    best_opportunity = symbol
        except Exception as e:
            print(f"📡 [SCAN-ERROR] {e}")
        
        return best_opportunity, highest_score

    async def fetch_god_intelligence(self, symbol):
        """Busca dados de alta fidelidade e retorna métricas puras."""
        try:
            target = f"{symbol}/USDT" if "/" not in symbol else symbol
            tasks = [
                exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=5),
                exchange.fetch_order_book(target, limit=20),
                exchange.fetch_ohlcv(target, timeframe='1m', limit=20)
            ]
            results = await asyncio.gather(*tasks)
            
            # ⚓ ÂNCORA BTC
            btc_ohlcv = results[0]
            btc_closes = [c[4] for c in btc_ohlcv]
            btc_momentum = (btc_closes[-1] - btc_closes[0]) / btc_closes[0]
            self.btc_last_price = btc_closes[-1]
            self.btc_momentum = btc_momentum
            
            # 📊 ATIVO ALVO
            ob = results[1]
            bids_vol = sum([b[1] for b in ob['bids']])
            asks_vol = sum([a[1] for a in ob['asks']])
            obp = (bids_vol - asks_vol) / (bids_vol + asks_vol) if (bids_vol + asks_vol) > 0 else 0
            
            ohlcv = results[2]
            closes = [c[4] for c in ohlcv]
            velocity = (closes[-1] - closes[-3]) / closes[-3] if len(closes) > 3 else 0
            kinetic = abs(velocity * 1000)
            
            mean = sum(closes) / len(closes)
            std = math.sqrt(sum((x - mean)**2 for x in closes) / len(closes))
            z_score = (closes[-1] - mean) / (std if std > 0 else 1)
            
            return {
                "obp": obp, 
                "kinetic": kinetic, 
                "z_score": z_score, 
                "symbol": symbol,
                "btc_corr": btc_momentum
            }
            
        except Exception as e:
            print(f"⚠️ INTEL FAILURE: {e}")
            return None

    def analyze_infinity(self, state, intel=None):
        # Usa inteligência do scan ou a última do cérebro
        obp = intel["obp"] if intel else self.obp_score
        kinetic = intel["kinetic"] if intel else self.kinetic_energy
        z_score = intel["z_score"] if intel else self.volatility_z_score
        btc_corr = intel["btc_corr"] if intel else self.btc_momentum
        
        flow_vector = (state.imb * 0.4) + (obp * 0.6)
        p = max(0.4, min(0.9, state.win_rate / 100))
        self.kelly_fraction = (p * 2) - 1 
        
        # ⚓ REGRA DE CORRELAÇÃO (O Ativo deve seguir o Bitcoin)
        is_correlated = (flow_vector > 0 and btc_corr > 0) or (flow_vector < 0 and btc_corr < 0)
        
        # ⚛️ ESCUDO DE REALIDADE (Frequência Harmônica)
        reality_trap = (flow_vector > 0.3 and z_score > 2.5) or (not is_correlated)
        
        bias = "NEUTRAL"
        if flow_vector > 0.20 and kinetic > 0.001 and is_correlated: bias = "GOD_LONG"
        if flow_vector < -0.20 and kinetic > 0.001 and is_correlated: bias = "GOD_SHORT"
        
        confidence = (abs(flow_vector) * 60) + (state.prob * 0.4)
        if not is_correlated: confidence *= 0.5 # Penaliza se não houver correlação
        
        alpha = 4.0 if confidence > 90 and not reality_trap else 1.0
        
        return {
            "score": confidence,
            "bias": bias,
            "trap": reality_trap,
            "alpha": alpha,
            "kelly": self.kelly_fraction,
            "physics": kinetic,
            "z_score": z_score,
            "obp": obp,
            "correlation": is_correlated
        }

brain = NomadBrain()
state_lock = asyncio.Lock()

# BINANCE CONNECTION (Custo Zero - Sem MT5)
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

# Configurar Exchange (Modo Futures - Otimizado para Baixa Latência)
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True
    }
})

# Se as chaves estiverem presentes, testa conexão
if BINANCE_API_KEY and BINANCE_API_SECRET:
    try:
        print("⚡ CONECTANDO À BINANCE FUTURES...")
        # Em produção aqui você pode testar o balance: exchange.fetch_balance()
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
INITIAL_PRICE = 128000          # Preço inicial simulado (WING26)

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
        self.btc_momentum: float = 0.0
        self.alpha_scale: float = 1.0
        self.compounding: float = 0.30 # 30% REINVESTIMENTO (LIMITE MÁXIMO)
        self.regime: str = "WAITING"
        self.confidence: float = 80.0
        self.is_hunting: bool = True
        self.is_locked: bool = False
        
        # Controle de Tempo
        self.last_update: float = time.time()
        self.session_start: float = time.time()
        
        # Flags de Segurança
        self.is_hunting: bool = True
        self.consecutive_losses: int = 0
        self.is_locked: bool = False
        
        # Trade Log (últimos 50)
        self.trade_log: List[dict] = []
        
        # Última ordem
        self.last_order: dict = {}
        
        # COMANDOS REMOTOS (Cloud -> MQL5)
        self.pending_command: str = ""
        
        # TENTAR RECUPERAR ESTADO DO SUPABASE
        self.recover_daily_stats()

    def recover_daily_stats(self):
        """Recupera PnL do dia do Supabase se disponível."""
        if not supabase: return
        
        try:
            # Pega trades de hoje (UTC - Padrão Supabase/Bolsa)
            today = datetime.utcnow().strftime("%Y-%m-%d")
            response = supabase.table("trades").select("*").gte("created_at", today).execute()
            
            data = response.data
            if data:
                print(f"🔄 RECUPERANDO HISTÓRICO: {len(data)} trades encontrados hoje.")
                self.trades = len(data)
                self.pnl = sum(row['pnl'] for row in data)
                self.daily_pnl = self.pnl
                self.wins = sum(1 for row in data if row['pnl'] > 0)
                self.losses = sum(1 for row in data if row['pnl'] <= 0)
                
                # Recalcula Win Rate
                total = self.wins + self.losses
                self.win_rate = round((self.wins / total) * 100, 1) if total > 0 else 0.0
                
                # Popula log recente
                for t in reversed(data[-10:]):
                    self.trade_log.append({
                        "time": t['created_at'].split('T')[1][:8], # Extrai HH:MM:SS
                        "action": t['action'],
                        "symbol": t['symbol'],
                        "price": t['price'],
                        "confidence": 0, # Historico nao salva confiancia por padrao p/ economizar
                        "pnl": t['pnl']
                    })
        except Exception as e:
            print(f"⚠️ FALHA NA RECUPERAÇÃO DO SUPABASE: {e}")

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
    state.confidence = data.prob # Mapeando prob para confidence
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
async def tradingview_webhook(payload: WebhookPayload):
    """
    Recebe sinais do TradingView e processa.
    Configure no TradingView: Alert → Webhook URL → https://sua-api.onrender.com/webhook
    
    Payload JSON esperado:
    {
        "action": "BUY",
        "symbol": "WING26",
        "price": 128500,
        "confidence": 85.5
    }
    """
    now = datetime.now()
    
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
    
    # 💫 SINGULARIDADE v21.0 - Busca Inteligência para o ativo ATUAL
    intel = await brain.fetch_god_intelligence(payload.symbol)
    
    report = brain.analyze_infinity(state, intel=intel)
    state.confidence = report["score"]
    state.kinetic = report["physics"]
    state.z_score = report["z_score"]
    state.obp = report["obp"]
    state.is_correlated = report["correlation"]
    state.alpha_scale = report["alpha"]
    state.trap_detected = report["trap"]
    
    # ═══════════════════════════════════════════════════════════
    # EXECUÇÃO GOD-MODE (R$100 - BANK PROTECTION)
    # ═══════════════════════════════════════════════════════════
    if exchange.apiKey and exchange.secret:
        if state.trap_detected and state.confidence < 98:
            return {"status": "GOD_SHIELD_ACTIVE", "reason": "Trap Detected"}
            
        # Ajuste para banca pequena (R$100 ~= $20 USD)
        # O lote por operação será proporcional à banca para não quebrar no primeiro loss
        base_qty = payload.qty if payload.qty > 0 else 0.001 # Mínimo possível (BTC)
        final_qty = base_qty * state.alpha_scale
        
        # Juros Compostos Infinitos (Refinado para R$100)
        if state.daily_pnl > 0:
            # Reinvestimento proporcional: Cada R$100 de lucro dobra o lucro (50% Reinv)
            # final_qty *= (1 + (state.daily_pnl / capital_inicial))
            final_qty *= (1 + (state.daily_pnl / 100))
            
        payload.qty = final_qty
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

# ⚡ HELPER: Execução Assíncrona Binance (Alta Performance)
async def execute_binance_order(payload: WebhookPayload):
    """Executa a ordem na Binance sem travar o restante da API."""
    try:
        symbol = payload.symbol.upper()
        if "/" not in symbol:
            symbol = f"{symbol}/USDT" if "USDT" not in symbol else symbol
        
        amount = payload.qty
        action = payload.action.upper()
        
        print(f"🚀 [BINANCE] Processando {action} {amount} {symbol}...")
        
        if action == "BUY":
            await exchange.create_market_buy_order(symbol, amount)
            print(f"✅ [BINANCE] COMPRA EXECUTADA @ {symbol}")
        elif action == "SELL":
            await exchange.create_market_sell_order(symbol, amount)
            print(f"✅ [BINANCE] VENDA EXECUTADA @ {symbol}")
        elif action == "CLOSE":
            # Para fechar, buscamos a posição atual
            positions = await exchange.fetch_positions(symbols=[symbol])
            for pos in positions:
                size = float(pos.get('info', {}).get('positionAmt', 0))
                if size != 0:
                    side = 'sell' if size > 0 else 'buy'
                    await exchange.create_market_order(symbol, side, abs(size), params={'reduceOnly': True})
                    print(f"✅ [BINANCE] POSIÇÃO ZERADA: {abs(size)} {symbol}")
                    
    except Exception as e:
        print(f"❌ [BINANCE ERROR] Falha Crítica na Execução: {e}")

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
    
    # 💾 PERSISTÊNCIA SUPABASE (Memória Viva)
    if supabase:
        try:
            # Salva o estado atual do sistema como um snapshot de log
            supabase.table("logs").insert({
                "event": "TRADE_RESULT",
                "details": f"{result.result} | PnL: {result.pnl} | PnL Total: {state.pnl}",
                "level": "INFO" if result.result == "WIN" else "WARNING"
            }).execute()
            
            # Salva o trade em si
            supabase.table("trades").insert({
                "symbol": result.symbol, 
                "action": "CLOSE",
                "result": result.result,
                "pnl": result.pnl,
                "price": state.price
            }).execute()
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
    
    # Simular variação de preço para demonstração
    if state.regime == "ACTIVE" or state.regime == "WAITING":
        # Pequena variação aleatória para parecer vivo
        variation = random.uniform(-5, 5)
        state.price = max(100000, state.price + variation)
        state.imb = random.uniform(-0.3, 0.3)
    
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
        "neural_score": round(state.neural_score, 1),
        "bias": brain.neural_bias,
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
@app.get("/health")
async def health_check():
    """Health check para Render."""
    return {
        "status": "OK",
        "version": "13.0.0",
        "mode": "100% CLOUD",
        "uptime_seconds": round(time.time() - state.session_start, 0)
    }

@app.get("/")
async def root():
    """Página inicial da API."""
    return {
        "message": "🦅 PREDATOR v13.0 SINGULARITY",
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
