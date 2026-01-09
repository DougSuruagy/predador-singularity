import json
import time
import os
import uuid
import math
import threading
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datetime import datetime
from collections import deque
import re
import MetaTrader5 as mt5  # Integração MT5

# --- CONFIGURAÇÃO ULTRA-SENSÍVEL (2026 ALPHA) ---
# COLOR PALETTE - OMNISCIENCE ELITE
# COLOR PALETTE - SUPREME OMNISCIENCE (2026 ELITE)
BG_MAIN = "#020406"  # Deep Space
BG_CARD = "#0A0E14"  # Obsidian
BG_HUD = "#11171F"   # Shadow
FG_NEON_YELLOW = "#FFD700" 
FG_NEON_BLUE = "#00F2FF"
FG_NEON_GREEN = "#00FF9D"
FG_NEON_PINK = "#FF0055"
FG_NEON_PURPLE = "#BC00FF"
FG_TEXT_DIM = "#6A737D"
FONT_PRIMARY = "Segoe UI"
PULSE_HZ = 5 # Reduced for Debugging Stability
MAX_PRICE_POINTS = 120

if "Orbitron" not in [f.lower() for f in []]:
    FONT_PRIMARY = "Consolas"

def find_mt5_common():
    """Busca ultra-agressiva pela pasta Common do MT5"""
    # 1. Tentar caminho específico localizado no sistema do Douglas
    douglas_path = Path("C:/Users/Douglas/AppData/Roaming/MetaQuotes/Terminal/Common/Files")
    if douglas_path.exists(): 
        print(f"✅ PREDADOR: Caminho Douglas detectado: {douglas_path}")
        return douglas_path

    roots = [
        Path(os.getenv('APPDATA', '')),
        Path(os.getenv('LOCALAPPDATA', '')),
        Path.home() / "AppData" / "Roaming"
    ]
    
    for root in roots:
        if not root or not root.exists(): continue
        # 1. Tentar caminho direto
        direct = root / "MetaQuotes" / "Terminal" / "Common" / "Files"
        if direct.exists(): return direct
        
        # 2. Tentar busca em subpastas do Terminal
        mq_base = root / "MetaQuotes" / "Terminal"
        if mq_base.exists():
            for p in mq_base.iterdir():
                try:
                    target = p / "Common" / "Files"
                    if target.exists(): return target
                except: continue
                
    # 3. Busca recursiva limitada (último recurso)
    mq_root = Path(os.getenv('APPDATA', '')).parent
    for p in mq_root.rglob("Common/Files"):
        return p

    return Path("C:/MT5_NOT_FOUND") # Debug path

COMMON_PATH = find_mt5_common()
BODY_STATE_FILE = COMMON_PATH / "Sovereign_Body_State.json"
SOUL_PIPE_FILE = COMMON_PATH / "Sovereign_Soul_State.json"
MQTT_OUT_FILE = COMMON_PATH / "Sovereign_MQTT_Out.json"
MQTT_IN_FILE = COMMON_PATH / "Sovereign_MQTT_In.json"

print(f"🚀 PREDADOR OMNI: Ativando Data Pipe em {COMMON_PATH}")
print(f"📂 Arquivo esperado: {BODY_STATE_FILE}")

# Thread removida para estabilidade no Windows/Tkinter
# class NeuralProcessor(threading.Thread): ...

class PredatorDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.session_id = uuid.uuid4().hex[:6].upper()
        self.file_found = False
        self.pulse_phase = 0
        self.price_history = deque(maxlen=60)
        self.trade_history = deque(maxlen=15)
        self.candle_history = deque(maxlen=40) # Visible candles
        self.last_candle_minute = -1
        self.metrics = {
            "symbol": "---", "price": 0.0, "rsi": 50.0, "imb": 0.0,
            "intensity": 0.0, "pnl": 0.0, "balance": 0.0, 
            "has_position": False, "entropy": 0.0, "prob": 0.0,
            "atp": 100.0, "stress": 15.0, "spread": 0,
            "win_rate": 0.0, "trades": 0, "pf": 0.0,
            "open": 0.0, "high": 0.0, "low": 0.0, "close": 0.0, "vol": 0.0,
            "bid": 0.0, "ask": 0.0,
            "timestamp": "---"
        }
        self.last_sync_time = 0  
        self.last_file_mtime = 0 # OTIMIZAÇÃO I/O
        self.poll_debug_msg = "Init..."
        
        self.title(f"PREDATOR OMNISCIENCE v7.0 | SUPREME AI | ID: {self.session_id}")
        self.geometry("1100x750")
        self.configure(bg=BG_MAIN)
        
        self._init_styles()
        self._build_ui()
        
        # self.processor = NeuralProcessor(self) # Removido
        # self.processor.start() # Removido
        
        # Inicia loop de dados na MAIN THREAD (Tkinter Safety)
        print("🧠 Iniciando POLL DATA na main thread...")
        self.after(500, self.poll_data)
        self.update_gui()

    def _init_styles(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def _build_ui(self):
        # --- LAYOUT MASTER (3 COLUNAS) ---
        # Coluna 1: CONTROLES DE EXECUÇÃO (OPERACIONAL)
        op_panel = tk.Frame(self, bg=BG_CARD, width=280)
        op_panel.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        op_panel.grid_propagate(False)

        # 1.1 TÍTULO
        tk.Label(op_panel, text="EXECUÇÃO MANUAL", font=(FONT_PRIMARY, 8, "bold"), bg=BG_CARD, fg=FG_TEXT_DIM).pack(pady=(10, 5))
        
        # 1.2 BOTÕES BIG BUTTONS (SCALPING)
        btn_grid = tk.Frame(op_panel, bg=BG_CARD)
        btn_grid.pack(fill=tk.X, padx=10)
        
        # COMPRA
        btn_buy = tk.Button(btn_grid, text="COMPRAR\n(ASK)", font=(FONT_PRIMARY, 10, "bold"), bg="#004d26", fg="#00FF9D",
                           activebackground="#00FF9D", activeforeground="black", height=2, command=lambda: self._execute_mt5_order("ORDER_BUY"))
        btn_buy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # VENDA
        btn_sell = tk.Button(btn_grid, text="VENDER\n(BID)", font=(FONT_PRIMARY, 10, "bold"), bg="#4d0016", fg="#FF0055",
                            activebackground="#FF0055", activeforeground="black", height=2, command=lambda: self._execute_mt5_order("ORDER_SELL"))
        btn_sell.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # 1.3 GESTÃO DE RISCO E AUTO
        tk.Label(op_panel, text="SISTEMA AUTÔNOMO", font=(FONT_PRIMARY, 8, "bold"), bg=BG_CARD, fg=FG_TEXT_DIM).pack(pady=(15, 5))
        
        ctrl_f = tk.Frame(op_panel, bg=BG_CARD)
        ctrl_f.pack(fill=tk.X, padx=10)
        
        self._create_btn(ctrl_f, "ZERAR TUDO (PANIC)", FG_NEON_PINK, self.panic_close)
        self._create_btn(ctrl_f, "PAUSAR ROBÔ", FG_NEON_YELLOW, self.toggle_sniper)
        self._create_btn(ctrl_f, "MODO: AGRESSIVO", FG_NEON_PURPLE, self.bio_boost)

        # 1.4 GESTÃO DE BANCA & PERFORMANCE
        tk.Label(op_panel, text="GESTÃO DE BANCA", font=(FONT_PRIMARY, 8, "bold"), bg=BG_CARD, fg=FG_TEXT_DIM).pack(pady=(20, 5))
        
        fin_f = tk.Frame(op_panel, bg=BG_CARD, highlightthickness=1, highlightbackground="#1F242E")
        fin_f.pack(fill=tk.X, padx=10, pady=5)
        
        self.lbl_balance = self._create_row_val(fin_f, "SALDO CONTA:", "R$ 0.00", "white")
        self.lbl_equity = self._create_row_val(fin_f, "PATRIMÔNIO:", "R$ 0.00", "white")
        tk.Frame(fin_f, bg="gray", height=1).pack(fill=tk.X, padx=5, pady=5)
        self.lbl_pnl = self._create_row_val(fin_f, "LUCRO HOJE:", "R$ 0.00", FG_NEON_GREEN)
        
        # Barra de Meta (Visual)
        tk.Label(op_panel, text="META DIÁRIA", font=(FONT_PRIMARY, 7), bg=BG_CARD, fg="gray").pack(pady=(10, 2))
        self.meta_canvas = tk.Canvas(op_panel, height=8, bg="#1A1F2B", highlightthickness=0)
        self.meta_canvas.pack(fill=tk.X, padx=10)
        self.lbl_meta_pct = tk.Label(op_panel, text="0.0%", font=(FONT_PRIMARY, 7), bg=BG_CARD, fg=FG_NEON_BLUE)
        self.lbl_meta_pct.pack()

        # Coluna 2: MASTER ENGINE (GRÁFICOS E FLUXO)
        center_side = tk.Frame(self, bg=BG_MAIN)
        center_side.grid(row=0, column=1, sticky="nsew")
        center_side.grid_columnconfigure(0, weight=1)
        center_side.grid_rowconfigure(1, weight=1)

        # 2.1 HEADER: PREÇO E TICKER
        header = tk.Frame(center_side, bg=BG_MAIN, height=60)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.lbl_main_price = tk.Label(header, text="---", font=("Orbitron", 56, "bold"), bg=BG_MAIN, fg="white")
        self.lbl_main_price.pack(side=tk.LEFT)
        
        info_f = tk.Frame(header, bg=BG_MAIN)
        info_f.pack(side=tk.LEFT, padx=15)
        self.lbl_symbol_status = tk.Label(info_f, text="WDO | CONECTANDO...", font=(FONT_PRIMARY, 12, "bold"), bg=BG_MAIN, fg=FG_NEON_BLUE)
        self.lbl_symbol_status.pack(anchor="w")
        self.lbl_regime = tk.Label(info_f, text="REGIME: ---", font=(FONT_PRIMARY, 8, "bold"), bg=BG_MAIN, fg="gray")
        self.lbl_regime.pack(anchor="w")
        self.lbl_spread_info = tk.Label(info_f, text="SPREAD: 0pts | VOL: 0", font=(FONT_PRIMARY, 9), bg=BG_MAIN, fg="gray")
        self.lbl_spread_info.pack(anchor="w")

        # 2.2 CANVAS GRÁFICO (CANDLES)
        chart_frame = tk.Frame(center_side, bg="#05070A", highlightthickness=1, highlightbackground="#1F242E")
        chart_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        self.price_canvas = tk.Canvas(chart_frame, bg="#080B10", highlightthickness=0)
        self.price_canvas.pack(fill=tk.BOTH, expand=True)

        # 2.3 TAPE READING VISUAL (BARRA DE FLUXO)
        tape_frame = tk.Frame(center_side, bg=BG_MAIN, height=40)
        tape_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        tk.Label(tape_frame, text="FLUXO DE AGRESSÃO (1M)", font=(FONT_PRIMARY, 7), bg=BG_MAIN, fg="gray").pack(anchor="w")
        self.dom_canvas = tk.Canvas(tape_frame, height=20, bg="#1A1F2B", highlightthickness=0)
        self.dom_canvas.pack(fill=tk.X, pady=2)
        # Marcador central
        self.dom_canvas.update_idletasks()
        

        # Coluna 3: ANALYTICS QUANTITATIVO
        right_side = tk.Frame(self, bg=BG_CARD, width=240)
        right_side.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        right_side.grid_propagate(False)

        # 3.1 PROBABILIDADE IA
        tk.Label(right_side, text="PROBABILIDADE DIREÇÃO", font=(FONT_PRIMARY, 8, "bold"), bg=BG_CARD, fg=FG_NEON_BLUE).pack(pady=(10, 5))
        self.gauge_canvas = tk.Canvas(right_side, width=220, height=100, bg=BG_CARD, highlightthickness=0)
        self.gauge_canvas.pack()
        self.lbl_prob = tk.Label(right_side, text="50.0%", font=(FONT_PRIMARY, 22, "bold"), bg=BG_CARD, fg="white")
        self.lbl_prob.pack(pady=(0, 10))

        # 3.2 FATORES QUANTITATIVOS
        q_frame = self._create_card(right_side, "FATORES QUANT", 0, 0)
        q_frame.pack(fill=tk.X, padx=10)
        
        self.lbl_rsi = self._create_row_val(q_frame, "RSI (14)", "50.0", FG_NEON_PURPLE)
        self.lbl_imb = self._create_row_val(q_frame, "IMBALANCE", "0.00", FG_NEON_YELLOW)
        self.lbl_bb_delta = self._create_row_val(q_frame, "BB DELTA", "0", FG_NEON_BLUE) # Novo
        self.lbl_volat = self._create_row_val(q_frame, "VOLATILIDADE", "BAIXA", FG_NEON_BLUE)
        self.lbl_intensity = self._create_row_val(q_frame, "INTENSIDADE", "0/s", "white")

        # 3.3 LOG DE EVENTOS (CONSOLE)
        tk.Label(right_side, text="LOG DO SISTEMA", font=(FONT_PRIMARY, 7, "bold"), bg=BG_CARD, fg="gray").pack(anchor="w", padx=10, pady=(15, 2))
        self.log_list = tk.Listbox(right_side, bg="#030405", fg="#00FF00", font=("Consolas", 7), 
                                  borderwidth=0, highlightthickness=0, height=10)
        self.log_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Footer
        footer = tk.Frame(self, bg=BG_HUD, height=25)
        footer.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.lbl_status = tk.Label(footer, text="SISTEMA: ONLINE", font=(FONT_PRIMARY, 7), bg=BG_HUD, fg="#00FF00")
        self.lbl_status.pack(side=tk.LEFT, padx=10)
        
        self.lbl_latency = tk.Label(footer, text="LATÊNCIA: 0ms", font=(FONT_PRIMARY, 7), bg=BG_HUD, fg="gray")
        self.lbl_latency.pack(side=tk.RIGHT, padx=10)
        self.lbl_debug = tk.Label(footer, text="DEBUG: ---", font=("Consolas", 7), bg=BG_HUD, fg="orange")
        self.lbl_debug.pack(side=tk.RIGHT, padx=10)

    def _create_val_big(self, parent, label, default, color):
        f = tk.Frame(parent, bg=BG_CARD)
        f.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(f, text=label, font=(FONT_PRIMARY, 7), bg=BG_CARD, fg="gray").pack(anchor="w")
        v = tk.Label(f, text=default, font=(FONT_PRIMARY, 20, "bold"), bg=BG_CARD, fg=color)
        v.pack(anchor="w")
        return v
    
    def _create_row_val(self, parent, label, default, color):
        f = tk.Frame(parent, bg=BG_CARD)
        f.pack(fill=tk.X, pady=2)
        tk.Label(f, text=label, font=(FONT_PRIMARY, 8), bg=BG_CARD, fg="gray").pack(side=tk.LEFT)
        v = tk.Label(f, text=default, font=(FONT_PRIMARY, 8, "bold"), bg=BG_CARD, fg=color)
        v.pack(side=tk.RIGHT)
        return v

    def _create_stat(self, parent, label, default, color):
        f = tk.Frame(parent, bg=BG_CARD, pady=2)
        f.pack(fill=tk.X, padx=10)
        tk.Label(f, text=label, font=(FONT_PRIMARY, 7, "bold"), bg=BG_CARD, fg=FG_TEXT_DIM).pack(anchor="w")
        v = tk.Label(f, text=default, font=(FONT_PRIMARY, 11, "bold"), bg=BG_CARD, fg=color)
        v.pack(anchor="w")
        return v

    def _create_mini_val(self, parent, label, default, color):
        f = tk.Frame(parent, bg=BG_CARD)
        f.pack(fill=tk.X, padx=10, pady=2)
        tk.Label(f, text=label, font=(FONT_PRIMARY, 7, "bold"), bg=BG_CARD, fg=FG_TEXT_DIM).pack(anchor="w")
        v = tk.Label(f, text=default, font=(FONT_PRIMARY, 10, "bold"), bg=BG_CARD, fg=color)
        v.pack(anchor="w")
        return v

    def _create_btn(self, parent, text, color, cmd):
        btn = tk.Button(parent, text=text, font=(FONT_PRIMARY, 7, "bold"), bg="#1A1F2B", fg=color,
                       activebackground=color, activeforeground="black", borderwidth=0, 
                       cursor="hand2", padx=2, pady=4, command=cmd)
        btn.pack(fill=tk.X, pady=2)

    def panic_close(self):
        self.send_command("FECHAR_TUDO")
        self.add_trade_log({"status": "PANIC", "ativo": self.metrics["symbol"], "p_exec": 0, "profit": 0})

    def toggle_sniper(self):
        self.send_command("SNIPER_MODE")

    def bio_boost(self):
        self.send_command("BIO_BOOST")

    def send_command(self, cmd_type):
        """Envia comando ao MT5 via arquivo MQTT_IN e opcionalmente executa ordem direta."""
        try:
            cmd = {
                "id": uuid.uuid4().hex[:8],
                "ordem": cmd_type,
                "timestamp": time.time()
            }
            # Grava comando para o bridge MQTT
            with open(MQTT_IN_FILE, "w", encoding="utf-8") as f:
                json.dump(cmd, f)
            # Opcional: se o comando for de ordem, envia diretamente ao MT5
            if cmd_type.startswith("ORDER_"):
                self._execute_mt5_order(cmd_type)
        except Exception as e:
            print(f"Erro ao enviar comando {cmd_type}: {e}")

    def _execute_mt5_order(self, order_type):
        """Executa ordens simples no MT5 usando MetaTrader5 API.
        order_type pode ser 'ORDER_BUY' ou 'ORDER_SELL'."""
        symbol = self.metrics.get("symbol", "")
        if not symbol:
            print("Símbolo não definido, ordem abortada.")
            return
        price = mt5.symbol_info_tick(symbol).bid if order_type == "ORDER_SELL" else mt5.symbol_info_tick(symbol).ask
        volume = 0.01  # lote mínimo, pode ser parametrizado
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY if order_type == "ORDER_BUY" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": 202306,
            "comment": "PredatorAI",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Falha ao enviar ordem {order_type}: {result.comment}")
        else:
            print(f"Ordem {order_type} enviada com sucesso: {result.order}")

    def _create_card(self, parent, title, r, c):
        f = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground="#1F242E")
        f.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        tk.Label(f, text=title, font=(FONT_PRIMARY, 7, "bold"), bg=BG_CARD, fg="#5A6170").pack(anchor="w", padx=10, pady=4)
        return f

    def _create_val(self, parent, label, default, color):
        f = tk.Frame(parent, bg=BG_CARD)
        f.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(f, text=label, font=(FONT_PRIMARY, 8), bg=BG_CARD, fg=FG_TEXT_DIM).pack(anchor="w")
        v = tk.Label(f, text=default, font=(FONT_PRIMARY, 18, "bold"), bg=BG_CARD, fg=color)
        v.pack(anchor="w")
        return v

    def add_trade_log(self, data):
        # Format: STATUS | ASSET | PRICE | PROFIT
        status = str(data.get("status", "DONE")).upper()
        asset = str(data.get("ativo", "UNK"))
        price = data.get("p_exec", 0)
        profit = data.get("profit", 0)
        
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {status} | {asset} | {price:.0f}"
        self.trade_history.appendleft(entry)
        self.log_list.insert(0, entry)
        # Limita o número de linhas no Listbox para evitar consumo excessivo de memória
        if self.log_list.size() > 50:
            self.log_list.delete(50, tk.END)

        # ZERO-GATE: Ignore invalid initial syncs
        p = float(data.get("last_price", 0))
        if p <= 0: return

        self.metrics["symbol"] = data.get("ativo", "---")
        self.metrics["price"] = p
        self.metrics["bid"] = float(data.get("bid", p))
        self.metrics["ask"] = float(data.get("ask", p))
        self.metrics["open"] = float(data.get("open", 0))
        self.metrics["high"] = float(data.get("high", 0))
        self.metrics["low"] = float(data.get("low", 0))
        self.metrics["close"] = float(data.get("close", 0))
        self.metrics["vol"] = float(data.get("volume", 0))
        self.metrics["spread"] = int(float(data.get("spread", 0)))
        
        self.metrics["rsi"] = float(data.get("rsi", 50))
        self.metrics["imb"] = float(data.get("flow_imbalance", 0))
        self.metrics["intensity"] = float(data.get("tick_intensity", 0))
        
        # Mapeamento Inteligente de Lucro
        # Se 'daily_profit' vier do JSON, usamos ele para o PnL do dia
        # Se não, usamos pos_profit como fallback
        d_profit = float(data.get("daily_profit", -999999))
        if d_profit != -999999:
             self.metrics["pnl"] = d_profit
        else:
             self.metrics["pnl"] = float(data.get("pos_profit", 0))
             
        self.metrics["balance"] = float(data.get("balance", 0))
        self.metrics["has_position"] = data.get("has_position", False)
        self.metrics["atp"] = float(data.get("atp", 100))
        self.metrics["stress"] = float(data.get("cortisol", 15))
        self.metrics["timestamp"] = data.get("timestamp", "---")
        
        # Candle Control
        try:
            ts = self.metrics["timestamp"]
            cur_min = int(ts.split(":")[1]) if ":" in ts else -1
            if cur_min != self.last_candle_minute and self.metrics["open"] > 0:
                candle = {"o": self.metrics["open"], "h": self.metrics["high"], "l": self.metrics["low"], "c": self.metrics["close"], "v": self.metrics["vol"]}
                self.candle_history.append(candle)
                self.last_candle_minute = cur_min
        except: pass

        # Master Scalper Logic
        trades = list(self.trade_history)
        if trades:
            wins = sum(1 for t in trades if "R$" in t and float(t.split("R$")[-1]) > 0)
            self.metrics["trades"] = len(trades)
            self.metrics["win_rate"] = (wins / len(trades) * 100) if len(trades) > 0 else 0
            gross_p = sum(float(t.split("R$")[-1]) for t in trades if "R$" in t and float(t.split("R$")[-1]) > 0)
            gross_l = abs(sum(float(t.split("R$")[-1]) for t in trades if "R$" in t and float(t.split("R$")[-1]) < 0))
            self.metrics["pf"] = (gross_p / gross_l) if gross_l > 0 else (gross_p if gross_p > 0 else 0)

        self.metrics["entropy"] = abs(self.metrics["imb"] * 0.7) + (self.metrics["intensity"] * 0.05)
        self.metrics["prob"] = min(99.9, (abs(self.metrics["imb"]) * 65) + (self.metrics["intensity"] * 8))
        if self.metrics["price"] > 0: self.price_history.append(self.metrics["price"])
        self.last_sync_time = time.time()

    def update_metrics(self, data):
        """Atualiza métricas a partir dos dados do MT5 (Sovereign_Body_State.json)"""
        # ZERO-GATE: Ignora dados inválidos
        p = float(data.get("last_price", 0))
        if p <= 0:
            return

        self.metrics["symbol"] = data.get("ativo", "---")
        self.metrics["price"] = p
        self.metrics["bid"] = float(data.get("bid", p))
        self.metrics["ask"] = float(data.get("ask", p))
        self.metrics["open"] = float(data.get("open", 0))
        self.metrics["high"] = float(data.get("high", 0))
        self.metrics["low"] = float(data.get("low", 0))
        self.metrics["close"] = float(data.get("close", 0))
        self.metrics["vol"] = float(data.get("volume", 0))
        self.metrics["spread"] = int(float(data.get("spread", 0)))
        
        self.metrics["rsi"] = float(data.get("rsi", 50))
        self.metrics["bb_delta"] = float(data.get("bb_delta", 0)) # Novo
        self.metrics["imb"] = float(data.get("flow_imbalance", 0))
        self.metrics["intensity"] = float(data.get("tick_intensity", 0))
        self.metrics["pnl"] = float(data.get("pos_profit", 0))
        self.metrics["balance"] = float(data.get("balance", 0))
        self.metrics["has_position"] = data.get("has_position", False)
        self.metrics["stress"] = float(data.get("cortisol", 0.15)) * 100  # Normaliza para 0-100
        self.metrics["timestamp"] = data.get("timestamp", "---")
        
        # Candle Control
        try:
            ts = self.metrics["timestamp"]
            cur_min = int(ts.split(":")[1]) if ":" in ts else -1
            if cur_min != self.last_candle_minute and self.metrics["open"] > 0:
                candle = {"o": self.metrics["open"], "h": self.metrics["high"], "l": self.metrics["low"], "c": self.metrics["close"], "v": self.metrics["vol"]}
                self.candle_history.append(candle)
                self.last_candle_minute = cur_min
        except:
            pass

        # Cálculo de entropia e probabilidade
        self.metrics["entropy"] = abs(self.metrics["imb"] * 0.7) + (self.metrics["intensity"] * 0.05)
        self.metrics["prob"] = min(99.9, (abs(self.metrics["imb"]) * 65) + (self.metrics["intensity"] * 8))
        
        if self.metrics["price"] > 0:
            self.price_history.append(self.metrics["price"])
        self.last_sync_time = time.time()

    def broadcast_soul_state(self):
        """Informa ao MT5 que a alma está ativa"""
        try:
            state = {
                "session_id": self.session_id,
                "version": "3.2-OMNI",
                "neural_drive": 0.85,
                "bio_state": "HUNTING" if not self.metrics["has_position"] else "ATTACKING",
                "is_hunting": True
            }
            with open(SOUL_PIPE_FILE, "w") as f:
                json.dump(state, f)
        except:
            pass

    def update_gui(self):
        try:
            # 1. HEADER & STATUS
            self.lbl_main_price.config(text=f"{self.metrics['price']:.2f}")
            
            now_ts = time.time()
            lat = (now_ts - self.last_sync_time) * 1000 if self.last_sync_time > 0 else 0
            stale = (lat > 2000) or (self.last_sync_time == 0)

            status_txt = f"{self.metrics['symbol']} | {'CONECTADO' if not stale else 'CONEXÃO LENTA'}"
            status_color = FG_NEON_BLUE if not stale else "orange"
            self.lbl_symbol_status.config(text=status_txt, fg=status_color)
            
            # Spread Info
            vol = int(self.metrics['vol'])
            spread = self.metrics['spread']
            self.lbl_spread_info.config(text=f"SPREAD: {spread}pts | VOL: {vol}")

            # 2. CHART RENDER (CANDLES)
            self.price_canvas.delete("all")
            w = self.price_canvas.winfo_width()
            h = self.price_canvas.winfo_height()
            
            # Grid Pro
            for i in range(0, h, 40):
                self.price_canvas.create_line(0, i, w, i, fill="#12161C", width=1)
            for i in range(0, w, 60):
                self.price_canvas.create_line(i, 0, i, h, fill="#12161C", width=1)

            # Candles Logic
            if len(self.candle_history) > 0:
                p_values = [c['h'] for c in self.candle_history] + [c['l'] for c in self.candle_history]
                if p_values:
                    p_min, p_max = min(p_values), max(p_values)
                    p_range = max(1, p_max - p_min)
                    
                    c_w = 6 # Candle width
                    spacing = 4
                    start_x = w - 50
                    
                    for i, c in enumerate(reversed(self.candle_history)):
                        x = start_x - (i * (c_w + spacing))
                        if x < 0: break
                        
                        top = h - ((c['h'] - p_min) / p_range * (h - 60)) - 30
                        bot = h - ((c['l'] - p_min) / p_range * (h - 60)) - 30
                        open_y = h - ((c['o'] - p_min) / p_range * (h - 60)) - 30
                        close_y = h - ((c['c'] - p_min) / p_range * (h - 60)) - 30
                        
                        color = FG_NEON_GREEN if c['c'] >= c['o'] else FG_NEON_PINK
                        
                        self.price_canvas.create_line(x + c_w/2, top, x + c_w/2, bot, fill=color)
                        self.price_canvas.create_rectangle(x, open_y, x + c_w, close_y, fill=color, outline="")
                
                # Last Price Line
                last_y = h - ((self.metrics['price'] - p_min) / p_range * (h - 60)) - 30
                self.price_canvas.create_line(0, last_y, w, last_y, fill="white", dash=(2, 2))
                self.price_canvas.create_text(w-5, last_y-10, text=str(self.metrics['price']), fill="white", anchor="e", font=("Consolas", 8))

            # 3. TAPE READING (BARRA DE FLUXO)
            imb = self.metrics["imb"] # -1.0 a 1.0
            self.dom_canvas.delete("all")
            dw = self.dom_canvas.winfo_width()
            mid = dw / 2
            
            # Fundo neutro
            self.dom_canvas.create_rectangle(0, 5, dw, 15, fill="#0F1218", outline="")
            # Centro marcador
            self.dom_canvas.create_line(mid, 0, mid, 20, fill="gray")
            
            # Barra Ativa
            bar_len = abs(imb) * (mid * 0.9) # 90% da metade
            if imb > 0:
                self.dom_canvas.create_rectangle(mid, 5, mid + bar_len, 15, fill=FG_NEON_GREEN, outline="")
            else:
                self.dom_canvas.create_rectangle(mid - bar_len, 5, mid, 15, fill=FG_NEON_PINK, outline="")
            
            self.lbl_imb.config(text=f"{imb:+.3f}", fg=FG_NEON_GREEN if imb > 0 else FG_NEON_PINK)

            # 4. QUANT METRICS
            self.lbl_rsi.config(text=f"{self.metrics['rsi']:.1f}")
            
            intensity = self.metrics['intensity']
            self.lbl_intensity.config(text=f"{intensity:.1f}/s", fg="white" if intensity < 20 else FG_NEON_YELLOW)
            
            # Volatility State
            vol_state = "BAIXA"
            vol_color = FG_NEON_BLUE
            if intensity > 30: 
                vol_state = "MÉDIA"
                vol_color = FG_NEON_YELLOW
            if intensity > 60: 
                vol_state = "ALTA"
                vol_color = FG_NEON_PINK
            self.lbl_volat.config(text=vol_state, fg=vol_color)
            
            # BB Delta
            bb = self.metrics.get("bb_delta", 0)
            bb_color = FG_NEON_PINK if abs(bb) < 20 else "white" # Perto da banda = Alerta
            self.lbl_bb_delta.config(text=f"{bb:.0f} pts", fg=bb_color)

            # Regime
            self.lbl_regime.config(text=f"REGIME: {vol_state} MOMENTUM", fg=vol_color)

            # 5. GESTÃO DE BANCA
            pnl = self.metrics['pnl']
            balance = self.metrics['balance']
            equity = balance + pnl  # Simplificação, o ideal seria ler equity do JSON, mas PnL já ajuda
            
            self.lbl_pnl.config(text=f"R$ {pnl:,.2f}", fg=FG_NEON_GREEN if pnl >= 0 else FG_NEON_PINK)
            self.lbl_balance.config(text=f"R$ {balance:,.2f}")
            self.lbl_equity.config(text=f"R$ {equity:,.2f}", fg=FG_NEON_GREEN if equity >= balance else FG_NEON_PINK)
            
            # Meta Diária Simples (Ex: 3% do saldo ou R$ 500 fixo)
            # Vamos assumir uma meta baseada em 1% para visualização
            meta = balance * 0.01 if balance > 0 else 100
            if meta < 100: meta = 100 # Minimo R$ 100
            
            prog = min(1.0, max(0.0, pnl / meta)) if meta > 0 else 0
            if pnl < 0: prog = 0
            
            self.meta_canvas.delete("all")
            w_meta = self.meta_canvas.winfo_width()
            self.meta_canvas.create_rectangle(0, 0, w_meta * prog, 8, fill=FG_NEON_BLUE, outline="")
            self.lbl_meta_pct.config(text=f"{prog*100:.1f}% DA META (R$ {meta:.0f})")

            # Probabilidade
            prob = self.metrics["prob"]
            self.lbl_prob.config(text=f"{prob:.1f}%", fg=FG_NEON_GREEN if prob > 50 else FG_NEON_PINK)
            
            # Gauge Arc
            color = FG_NEON_GREEN if prob > 50 else FG_NEON_PINK
            start_angle = 180
            extent = -180 * (prob / 100)
            self.gauge_canvas.delete("all")
            self.gauge_canvas.create_arc(10, 10, 210, 150, start=180, extent=-180, outline="#1A1F2B", width=6, style=tk.ARC)
            self.gauge_canvas.create_arc(10, 10, 210, 150, start=180, extent=extent, outline=color, width=6, style=tk.ARC)


            # Footer Latency
            self.lbl_latency.config(text=f"LATÊNCIA: {int(lat)}ms")

        except Exception as e:
            # print(f"❌ UI CRASH: {e}") # Silent error
            pass
        
        # Garante que o loop continue mesmo com erro
        self.after(200, self.update_gui)

    
    def poll_data(self):
        """Nova função de leitura de dados rodando na main thread (sem threads)"""
        try:
            # 1. Heartbeat
            self.broadcast_soul_state()
            
            # 2. Leitura OTIMIZADA (Check Change Time)
            if BODY_STATE_FILE.exists():
                try:
                    current_mtime = BODY_STATE_FILE.stat().st_mtime
                    if current_mtime != self.last_file_mtime:
                        self.last_file_mtime = current_mtime
                        
                        with open(BODY_STATE_FILE, "rb") as f: # Leitura Binária Segura
                            raw = f.read()
                        
                        if raw:
                            clean = raw.rstrip(b'\x00').decode('utf-8', errors='ignore').strip()
                            match = re.search(r'\{.*\}', clean, re.DOTALL)
                            if match:
                                data = json.loads(match.group(0))
                                ts = data.get("timestamp", "?")
                                price = data.get("last_price", 0)
                                self.poll_debug_msg = f"LIDO: {ts} | P: {price}"
                                self.update_metrics(data)
                            else:
                                self.poll_debug_msg = "JSON FAIL"
                        else:
                            self.poll_debug_msg = "VAZIO"
                except Exception as e:
                    self.poll_debug_msg = f"IO ERR: {str(e)[:15]}"
            else:
                self.poll_debug_msg = "WAITING..."

            # 3. Leitura de Confirmações de Trade (MQTT Out)
            if MQTT_OUT_FILE.exists():
                try:
                    with open(MQTT_OUT_FILE, "r", encoding="utf-8") as f:
                        raw_conf = f.read().strip()
                    
                    if raw_conf:
                        try:
                            conf = json.loads(raw_conf)
                            # Processa confirmação
                            status = conf.get("status", "unknown")
                            if status == "executada":
                                msg = f"✅ EXEC: {conf.get('quantidade_exec')}x @ {conf.get('preco_exec')}"
                                self.log_list.insert(0, msg)
                                # Adiciona ao trade history para métricas (WinRate/PF - Aproximado)
                                # Nota: Isso é limitado pois não temos o resultado do trade, apenas a abertura.
                                # O cálculo real de WR/PF deve vir do MT5 (daily_profit e stats) futuramente.
                            elif status == "rejeitada":
                                msg = f"⛔ REJ: {conf.get('motivo')}"
                                self.log_list.insert(0, msg)
                            elif status == "erro":
                                msg = f"❌ ERRO: {conf.get('motivo')}"
                                self.log_list.insert(0, msg)
                            
                            # Limpa arquivo após ler para não reler
                            with open(MQTT_OUT_FILE, "w") as f: f.write("")
                            
                        except json.JSONDecodeError: pass
                except: pass

        except Exception as e:
            self.poll_debug_msg = f"CRITICAL: {e}"
        
        # Atualiza label de debug
        try:
            self.lbl_debug.config(text=self.poll_debug_msg)
        except: pass
        
        # Agenda próxima execução (5Hz = 200ms)
        self.after(200, self.poll_data)

if __name__ == "__main__":
    # Inicializa conexão MT5 antes de iniciar a UI
    if not mt5.initialize():
        print("Erro ao iniciar MetaTrader5. Verifique a instalação.")
        exit()
    app = PredatorDashboard()
    app.mainloop()
    mt5.shutdown()
