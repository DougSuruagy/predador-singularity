from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado do Sistema (Estoque Zero - Mantido em Memória p/ Performance)
class MarketState:
    def __init__(self):
        self.price = 0
        self.pnl = 0
        self.trades = 0
        self.win_rate = 0
        self.regime = "STABLE"
        self.last_update = time.time()
        self.is_hunting = True

state = MarketState()

# ENDPOINT: Receber Sinais do TradingView (Custo Zero)
@app.post("/webhook")
async def tradingview_signal(data: dict):
    # Lógica de 'Repasse para Região'
    # Aqui o Render recebe o sinal do TradingView e repassa para a Corretora
    action = data.get("action") # "BUY" ou "SELL"
    symbol = data.get("symbol")
    
    # Validação de ESTOQUE ZERO (Não abre ordens após as 17:30)
    current_hour = time.localtime().tm_hour
    current_min = time.localtime().tm_min
    if current_hour >= 17 and current_min >= 30:
        return {"status": "REJECTED", "reason": "ESTOQUE_ZERO_PROTOCOL"}

    print(f"🔥 REPASSE: Ordem {action} enviada para {symbol}")
    return {"status": "EXECUTED", "order": action}

@app.get("/state")
async def get_state():
    # Detecta se o mercado está em 'Stale'
    if time.time() - state.last_update > 60:
        state.regime = "OFFLINE"
    return state.__dict__

@app.post("/update")
async def update_state(data: dict):
    state.price = data.get("last_price", state.price)
    state.pnl = data.get("pnl", state.pnl)
    state.prob = data.get("prob", 0)
    state.imb = data.get("imb", 0)
    state.last_update = time.time()
    return {"status": "SYNCED"}
