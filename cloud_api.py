"""
PREDATOR v13.0 SINGULARITY - Cloud API (Render)
Custo Zero | Estoque Zero | Automação de Repasse
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import time
import os

app = FastAPI(title="PREDATOR API", version="13.0.0")

# CORS para Vercel e qualquer frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# VARIÁVEIS DE ESTADO (Mantidas em memória para performance)
# ============================================================
class MarketState:
    def __init__(self):
        # Preço e Métricas
        self.price: float = 0.0
        self.last_price: float = 0.0
        self.pnl: float = 0.0
        self.daily_pnl: float = 0.0
        self.trades: int = 0
        self.wins: int = 0
        self.losses: int = 0
        self.win_rate: float = 0.0
        
        # IA e Regime
        self.prob: float = 0.0
        self.imb: float = 0.0
        self.regime: str = "STABLE"
        self.confidence: float = 0.0
        
        # Controle de Tempo
        self.last_update: float = time.time()
        self.session_start: float = time.time()
        
        # Flags de Segurança
        self.is_hunting: bool = True
        self.consecutive_losses: int = 0
        self.is_locked: bool = False
        
        # Trade Log (últimos 50)
        self.trade_log: List[dict] = []

state = MarketState()

# ============================================================
# VARIÁVEIS DE CONFIGURAÇÃO (Custo Zero)
# ============================================================
MAX_CONSECUTIVE_LOSSES = 3  # 3-Strikes Rule
ESTOQUE_ZERO_HOUR = 17
ESTOQUE_ZERO_MIN = 30
STALE_TIMEOUT_SEC = 60

# ============================================================
# ENDPOINT: Receber Sinais do TradingView (Automação de Repasse)
# ============================================================
class WebhookPayload(BaseModel):
    action: str  # "BUY" ou "SELL"
    symbol: str
    price: Optional[float] = 0.0
    qty: Optional[int] = 1
    confidence: Optional[float] = 0.0

@app.post("/webhook")
async def tradingview_signal(payload: WebhookPayload):
    """
    Recebe sinais do TradingView e repassa para execução.
    Implementa ESTOQUE ZERO e 3-STRIKES RULE.
    """
    now = datetime.now()
    
    # [BUG FIX] Validação correta de ESTOQUE ZERO
    if now.hour > ESTOQUE_ZERO_HOUR or (now.hour == ESTOQUE_ZERO_HOUR and now.minute >= ESTOQUE_ZERO_MIN):
        return {"status": "REJECTED", "reason": "ESTOQUE_ZERO_PROTOCOL", "time": now.strftime("%H:%M:%S")}
    
    # [SEGURANÇA] 3-Strikes Rule
    if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        state.is_locked = True
        return {"status": "REJECTED", "reason": "3_STRIKES_LOCK", "losses": state.consecutive_losses}
    
    # [SEGURANÇA] Verificar se está em modo de caça
    if not state.is_hunting or state.is_locked:
        return {"status": "REJECTED", "reason": "SYSTEM_PAUSED"}
    
    # Registrar trade no log
    trade_entry = {
        "time": now.strftime("%H:%M:%S"),
        "action": payload.action,
        "symbol": payload.symbol,
        "price": payload.price,
        "qty": payload.qty,
        "confidence": payload.confidence
    }
    state.trade_log.insert(0, trade_entry)
    if len(state.trade_log) > 50:
        state.trade_log = state.trade_log[:50]
    
    state.trades += 1
    
    print(f"🔥 REPASSE: {payload.action} {payload.qty}x {payload.symbol} @ {payload.price} | CONF: {payload.confidence}%")
    
    return {
        "status": "EXECUTED",
        "order": payload.action,
        "symbol": payload.symbol,
        "price": payload.price,
        "timestamp": now.isoformat()
    }

# ============================================================
# ENDPOINT: Obter Estado Atual (Dashboard)
# ============================================================
@app.get("/state")
async def get_state():
    """
    Retorna o estado atual do sistema para o Dashboard.
    [PERFORMANCE] Detecta conexão stale automaticamente.
    """
    now = time.time()
    
    # [BUG FIX] Detectar conexão offline corretamente
    if now - state.last_update > STALE_TIMEOUT_SEC:
        state.regime = "OFFLINE"
        state.is_hunting = False
    else:
        state.regime = "ACTIVE" if state.is_hunting else "PAUSED"
    
    # Calcular win rate corretamente
    total = state.wins + state.losses
    state.win_rate = round((state.wins / total) * 100, 1) if total > 0 else 0.0
    
    return {
        "price": state.price,
        "last_price": state.last_price,
        "pnl": state.pnl,
        "daily_pnl": state.daily_pnl,
        "trades": state.trades,
        "wins": state.wins,
        "losses": state.losses,
        "win_rate": state.win_rate,
        "prob": state.prob,
        "imb": state.imb,
        "regime": state.regime,
        "confidence": state.confidence,
        "is_hunting": state.is_hunting,
        "is_locked": state.is_locked,
        "consecutive_losses": state.consecutive_losses,
        "last_update": state.last_update,
        "trade_log": state.trade_log[:10]  # Últimos 10 trades
    }

# ============================================================
# ENDPOINT: Atualizar Estado (MT5 / EA)
# ============================================================
class StateUpdate(BaseModel):
    last_price: Optional[float] = None
    pnl: Optional[float] = None
    daily_pnl: Optional[float] = None
    prob: Optional[float] = None
    imb: Optional[float] = None
    confidence: Optional[float] = None
    is_hunting: Optional[bool] = None
    trade_result: Optional[str] = None  # "WIN" ou "LOSS"

@app.post("/update")
async def update_state(data: StateUpdate):
    """
    Recebe atualizações do MT5/EA.
    [PERFORMANCE] Atualização atômica de estado.
    """
    if data.last_price is not None:
        state.last_price = data.last_price
        state.price = data.last_price
    
    if data.pnl is not None:
        state.pnl = data.pnl
    
    if data.daily_pnl is not None:
        state.daily_pnl = data.daily_pnl
    
    if data.prob is not None:
        state.prob = data.prob
    
    if data.imb is not None:
        state.imb = data.imb
    
    if data.confidence is not None:
        state.confidence = data.confidence
    
    if data.is_hunting is not None:
        state.is_hunting = data.is_hunting
    
    # [SEGURANÇA] Contagem de perdas consecutivas
    if data.trade_result == "WIN":
        state.wins += 1
        state.consecutive_losses = 0
        state.is_locked = False
    elif data.trade_result == "LOSS":
        state.losses += 1
        state.consecutive_losses += 1
        if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
            state.is_locked = True
            print(f"🔒 3-STRIKES LOCK ATIVADO após {state.consecutive_losses} perdas consecutivas")
    
    state.last_update = time.time()
    
    return {"status": "SYNCED", "timestamp": state.last_update}

# ============================================================
# ENDPOINT: Reset Diário (Novo Dia de Trading)
# ============================================================
@app.post("/reset")
async def reset_daily():
    """
    Reseta contadores para um novo dia de trading.
    """
    state.daily_pnl = 0.0
    state.trades = 0
    state.wins = 0
    state.losses = 0
    state.consecutive_losses = 0
    state.is_locked = False
    state.is_hunting = True
    state.trade_log = []
    state.session_start = time.time()
    
    print("🌅 RESET DIÁRIO EXECUTADO - Novo dia de trading iniciado!")
    return {"status": "RESET_OK", "timestamp": time.time()}

# ============================================================
# HEALTH CHECK (Render/Vercel)
# ============================================================
@app.get("/health")
async def health_check():
    return {"status": "OK", "version": "13.0.0", "uptime": time.time() - state.session_start}

@app.get("/")
async def root():
    return {"message": "🦅 PREDATOR v13.0 SINGULARITY - API Online", "docs": "/docs"}
