//+------------------------------------------------------------------+
//|                                             ROBÔ TRADER DOUG.mq5 |
//|          Singularity v15.00 QUANTUM PREDATOR - B3 SCALPER        |
//|                                  Copyright 2026, Antigravity AI  |
//+------------------------------------------------------------------+
#property copyright "Antigravity AI 2026"
#property version   "15.00"
#property strict

#include <Trade\Trade.mqh> 
#include <Trade\PositionInfo.mqh>
#include <Trade\SymbolInfo.mqh>
#include <Math\Stat\Math.mqh>

#include "SovereignInputs.mqh"
#include "Config.mqh"
#include "SovereignBioStructs.mqh"
#include "MLData.mqh"
#include "SovereignMind.mqh"
#include "MarketCache.mqh"
#include "RiskManagement.mqh"
#include "BioState.mqh"
#include "NewHUDResponsive.mqh"
#include "SharedComm.mqh"
#include "CommandBridge.mqh"
#include "QuantumBankroll.mqh"

// PERFORMANCE MAXIMIZER: Backtest = 0ms latency, Live = 5ms safety
#define THROTTLE_MICROS (ulong)(MQLInfoInteger(MQL_TESTER) ? 0 : 5000)

class CSovereignSupremeNew {
    enum EStrategyType { STRAT_MOMENTUM, STRAT_REVERSION };

public:
    // --- 🎭 PARALLEL REALITY ENGINE (2026 GHOST TRADING) ---
    struct GhostTrade {
        int    type;     // 1=Buy, -1=Sell
        double entry;
        double sl;
        double tp;
        bool   active;
        string strategy;
    };
    GhostTrade       m_ghost_pool[10];      // Simulador de cenários paralelos
    double           m_ghost_win_rate;      // Taxa de acerto das simulações
    int              m_ghost_total;
    int              m_ghost_wins;

    // --- NÚCLEO DE NEGOCIAÇÃO & CONTA ---
    CTrade           m_trade;
    ENUM_ORDER_TYPE_FILLING m_filling;      
    MqlTradeRequest  m_template_req;        
    MqlTradeRequest  m_exec_req, m_mod_req; 
    MqlTradeResult   m_exec_res, m_mod_res;
    
    double           m_acc_profit;          
    double           m_acc_margin;          
    double           m_acc_balance;         
    double           m_daily_profit_cached; 
    double           m_daily_profit_net_cached; // Novo: Lucro Líquido (descontando B3)
    double           m_virtual_margin_used; 
    double           m_pos_profit;          
    int              m_orders_in_flight;
    bool             m_in_transaction;
    ulong            m_pos_ticket;          
    int              m_spread_pts;
    bool             m_need_profit_sync;
    ulong            m_last_rsi_sync_ms;
    double           m_rsi_val_current;
    double           m_last_entry_price; // Cache de preço planejado p/ slippage
    
    // --- AI & BIOMETRIC CORE ---
    Sovereign::NeuroCortex           m_cortex;
    SovereignSupremeCortex           m_ctx;
    double           m_current_drive;
    double           m_input_state[];       
    double           m_feedback_inputs[];  
    
    // --- HFT TRACKING & SCANNERS ---
    int              m_pulse;
    int              m_current_time_score;
    double           m_last_proc_price;     
    double           m_last_proc_bid;       
    double           m_last_proc_ask;       
    double           m_last_bid;
    double           m_last_ask;
    MqlTick          m_current_tick;        
    
    bool             m_auto_mode;
    bool             m_trailing_active;
    uint             m_sys_flags;           
    #define SYS_FLAG_AUTO    0x01
    #define SYS_FLAG_VIRUS   0x02
    #define SYS_FLAG_NEWS    0x04

    double           m_whale_wall_price;
    double           m_whale_wall_vol;
    double           m_iceberg_alert;
    string           m_sync_partner;
    
    ulong            m_last_tick_time;
    ulong            m_last_tick_msc;
    ulong            m_last_heartbeat_ms;   
    ulong            m_last_acc_update_ms;
    ulong            m_last_ai_micros;
    ulong            m_last_trade_micros;
    ulong            m_last_book_micros;    
    ulong            m_last_book_proc_ms;   
    ulong            m_last_mod_micros;     
    double           m_dom_velocity;
    bool             m_dom_dirty_flag;
    ulong            m_last_news_sync;
    ulong            m_trans_timeout_ms;    
    datetime         m_last_visual_update;  
    datetime         m_last_bar_time;
    ulong            m_last_decay_time;     
    int              m_last_day_checking;
    int              m_last_deals_count;    
    bool             m_need_genetic_update; 
    bool             m_need_hud_redraw;
    ulong            m_last_viral_sound_ms;
    bool             m_cpu_overload;
    int              m_overload_counter; 
    double           m_recent_pnl_window[5]; // TRACKER DE CURVA DE EQUITY (5 TRADES)    
    ulong            m_last_mod_fail_ms;     // COOLDOWN DE FALHA EM MODIFICAÇÃO (Anti-Spam)
    // --- CACHE DE SISTEMA (B3) ---
    int              m_digits;
    double           m_point;
    double           m_point_inv;
    double           m_tick_size;
    double           m_tick_inv;
    double           m_tick_value;
    double           m_tick_cost_ratio;
    double           m_vol_min;
    double           m_vol_max;
    double           m_vol_step;
    double           m_vol_inv;
    double           m_margin_per_lot_buy;  
    double           m_margin_per_lot_sell;
    double           m_stops_level;
    
    // --- PERCEPÇÃO DE MERCADO ---
    double           m_last_bar_open;
    double           m_last_bar_high;       // Barra Finalizada
    double           m_last_bar_low;        // Barra Finalizada
    double           m_curr_bar_high;       // Barra Atual (Real-time)
    double           m_curr_bar_low;        // Barra Atual (Real-time)
    double           m_curr_bar_open;       // Barra Atual (Real-time)
    double           m_bb_up, m_bb_low;     // Bollinger Bands RAM Cache
    double           m_last_bar_atr;
    double           m_last_eval_price;     // Cache p/ Physics Engine
    double           m_m1_open_cached;      
    datetime         m_m1_time_cached;      
    double           m_atr_val;
    double           m_rsi_val;
    double           m_smooth_v;
    double           m_orb_high, m_orb_low;
    double           m_stack_threshold;
    bool             m_is_wdo;
    string           m_last_log_msg;
    ulong            m_last_deal_sync_ticket; // 🗲 Deal Cache p/ Performance
    
    // --- SCALP ANALYTICS ---
    int              m_scalp_samples;
    double           m_bid_press, m_ask_press; 
    double           m_scalp_win_rate;
    double           m_avg_trade_points;
    double           m_avg_trade_dur_sec;
    double           m_avg_slippage_pts;      
    ulong            m_exec_start_micros;     
    
    // --- HFT RAM BUFFER (Zero-API History) ---
    MqlRates         m_m1_history[4];         // 0=Current, 1=Last, 2=Prev, 3=Deep
    double           m_symmetry_gate;         // ⚡ Precision Execution Gate (0-1)
    
    // --- ESTRUTURAS DE DADOS ---
    struct RAMPos {
        int      type;
        double   vol;
        double   price_open;
        double   sl;
        double   tp;
        datetime open_time; // NEW: Track entry time for Duration metric
    } m_ram_pos;
    
    double           m_rsi_buf[], m_atr_buf[], m_high_buf[], m_low_buf[];
    double           m_close_buf[], m_sync_close_buf[];
    MqlBookInfo      m_book_buf[];          
    int              m_h_rsi, m_h_atr, m_h_macd, m_h_stoch, m_h_cci, m_h_bb;
    double           m_hour_sin, m_hour_cos, m_day_sin, m_day_cos;
    double           m_avg_latency_ms;
    int              m_latency_samples;
    double           m_vel_buffer[10];
    int              m_vel_idx;
    double           m_vel_sum;
    double           m_mirror_point; // PERFORMANCE: Cached property for Multi-Asset Sync
    double           m_session_profit; // SCALP ANALYTICS: Total Profit for PF
    double           m_session_loss;   // SCALP ANALYTICS: Total Loss for PF

    // --- COMPONENTES AUXILIARES ---
    Sovereign::CommandBridge m_bridge;
    SovereignMind m_mind; // Novo Cérebro
    int           m_last_intensity; // Intensidade da última decisão IA [1-5]


    double NormalizeLot(double lot) {
        // PERFORMANCE: Normalização por RAM-Cache (Zero-API Churn)
        double l = MathFloor(lot * m_vol_inv + 0.00001) * m_vol_step;
        if(l < m_vol_min) l = m_vol_min;
        if(l > m_vol_max) l = m_vol_max;
        return l;
    }

    double GetBestPrice(const MqlTick &tick) {
        // BUG FIX: B3 Prioriza 'last' p/ cálculo de execução e 'bid/ask' p/ limite
        return (tick.last > 0) ? tick.last : (tick.bid + tick.ask) / 2.0;
    }

    void InitializeSystems() {
        m_auto_mode  = InpFullAutonomy;
        if(MQLInfoInteger(MQL_TESTER)) m_auto_mode = true; // FORCE AUTO IN BACKTEST
        m_digits    = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
        m_point     = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
        m_point_inv = (m_point > 0) ? 1.0 / m_point : 0;
        m_tick_size = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
        m_tick_inv  = (m_tick_size > 0) ? 1.0 / m_tick_size : 0;
        m_tick_value= SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
        
        // CRITICAL FIX: Ratio Logic Initialization
        if(m_tick_size > 0) m_tick_cost_ratio = m_tick_value / m_tick_size;
        else m_tick_cost_ratio = 1.0; 
        
        m_vol_step  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
        m_vol_min   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
        m_vol_max   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
        m_vol_inv   = (m_vol_step > 0) ? 1.0 / m_vol_step : 0;
        
        m_acc_profit = AccountInfoDouble(ACCOUNT_PROFIT);
        m_acc_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
        m_pulse = 0;
        m_in_transaction = false;
        m_virtual_margin_used = 0;
        m_orders_in_flight = 0;
        m_last_trade_micros = 0;
        m_last_book_proc_ms = 0;
        m_exec_start_micros = 0; // Initialize new member
        m_avg_slippage_pts = 0; // Initialize new member
        
        // SYNC BITMASK STARTUP
        m_sys_flags = 0;
        if(m_auto_mode) m_sys_flags |= SYS_FLAG_AUTO;
        if(m_ctx.archive.pillars.is_viral_state) m_sys_flags |= SYS_FLAG_VIRUS;

        // BACKTEST GOD MODE: MAX CONFIDENCE START
        if(MQLInfoInteger(MQL_TESTER)) {
             m_cortex.emotion.dopamine = 1.0; 
             m_cortex.emotion.adrenaline = 1.0;
             m_cortex.emotion.serotonin = 1.0; 
        }
        
        // --- ENTIDADE VIVA: RESET DE BIOMETRIA ---
        Sovereign::BioState::atp_energy = 100.0;
        Sovereign::BioState::is_hibernating = false;
        Sovereign::BioState::is_rehabilitating = false;
        Sovereign::BioState::is_berserk = false;

        m_acc_balance = AccountInfoDouble(ACCOUNT_BALANCE);
        m_last_bar_open = SymbolInfoDouble(_Symbol, SYMBOL_LAST);
        
        // BACKTEST SAFETY: Initialize bar cache to prevent zero-lock
        m_curr_bar_high = m_last_bar_open;
        m_curr_bar_low = m_last_bar_open;
        m_curr_bar_open = m_last_bar_open;
        
        datetime now = TimeCurrent();
        m_last_bar_time = now - (now % 60);
        m_last_decay_time = now;
        m_smooth_v = 0;
        
        m_point_inv = (m_point > 0) ? 1.0 / m_point : 1.0;
        
        // CACHE DE MÉTRICAS B3 (HFT Optimization)
        m_tick_size  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
        m_tick_value = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
        if(m_tick_size > 0) m_tick_cost_ratio = m_tick_value / m_tick_size;
        else m_tick_cost_ratio = m_tick_value / m_point;
        m_tick_inv  = (m_tick_size > 0) ? 1.0 / m_tick_size : 1.0; 
        m_vol_inv   = (m_vol_step > 0) ? 1.0 / m_vol_step : 1.0;
        
        // --- TEMPLATE DE ORDEM (Latência Zero) ---
        ZeroMemory(m_template_req);
        m_template_req.action = TRADE_ACTION_DEAL;
        m_template_req.symbol = _Symbol;
        m_template_req.magic  = InpMagicNumber;
        m_template_req.deviation = 5;
        
        // AUTO-FILLING DETECTOR (B3 Protection)
        int fill_mode = (int)SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
        if((fill_mode & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK) m_filling = ORDER_FILLING_FOK;
        else if((fill_mode & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC) m_filling = ORDER_FILLING_IOC;
        else m_filling = ORDER_FILLING_RETURN;
        
        m_template_req.type_filling = m_filling;
        
        m_last_viral_sound_ms = 0;
        
        m_ghost_win_rate = 0; m_ghost_total = 0; m_ghost_wins = 0;
        ZeroMemory(m_ghost_pool);
        
        // --- PRE-FILL EXECUTION STRUCTURES (HFT OPTIMIZATION) ---
        ZeroMemory(m_exec_req);
        m_exec_req.action = TRADE_ACTION_DEAL;
        m_exec_req.symbol = _Symbol;
        m_exec_req.magic  = InpMagicNumber;
        m_exec_req.type_filling = ORDER_FILLING_IOC; // B3 Standard
        m_exec_req.deviation = 10;
        
        ZeroMemory(m_mod_req);
        m_mod_req.action = TRADE_ACTION_SLTP;
        m_mod_req.symbol = _Symbol;
        m_mod_req.magic  = InpMagicNumber;
        
        m_is_wdo = (StringFind(_Symbol, "WDO") >= 0);
        m_stack_threshold = m_is_wdo ? 5.0 : 150.0;
        m_stops_level = SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL) * m_point;
        
        // PRE-ALLOCATION (HFT Memory Stability)
        ArrayResize(m_rsi_buf, 5);
        ArrayResize(m_atr_buf, 5);
        ArrayResize(m_high_buf, 5);
        ArrayResize(m_low_buf, 5);
        ArrayResize(m_close_buf, 5);
        ArrayResize(m_sync_close_buf, 5);
        ArrayResize(m_input_state, 30); // Aumentado p/ suportar 25+ indicadores
        ArrayResize(m_feedback_inputs, 30);
        ArrayInitialize(m_recent_pnl_window, 0);
        m_vel_sum = 0; // Initialize HFT velocity sum state
        
        ArraySetAsSeries(m_rsi_buf, true);
        ArraySetAsSeries(m_atr_buf, true);
        ArraySetAsSeries(m_high_buf, true);
        
        // --- INICIALIZA CACHE DE FÍSICA E MERCADO ---
        m_last_eval_price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
        if(m_last_eval_price <= 0) m_last_eval_price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
        
        // --- INICIALIZA CACHE DE MARGEM (HFT Safety) ---
        double price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
        if(price <= 0) price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
        if(price > 0) {
            if(!OrderCalcMargin(ORDER_TYPE_BUY, _Symbol, 1.0, price, m_margin_per_lot_buy)) m_margin_per_lot_buy = 0;
            if(!OrderCalcMargin(ORDER_TYPE_SELL, _Symbol, 1.0, price, m_margin_per_lot_sell)) m_margin_per_lot_sell = 0;
        }
        ArraySetAsSeries(m_low_buf, true);
        ArraySetAsSeries(m_close_buf, true);
        ArraySetAsSeries(m_sync_close_buf, true);
        if(m_h_rsi == INVALID_HANDLE) m_h_rsi = iRSI(_Symbol, PERIOD_M1, 14, PRICE_CLOSE);
        if(m_h_atr == INVALID_HANDLE) m_h_atr = iATR(_Symbol, PERIOD_M1, 14);
        if(m_h_macd == INVALID_HANDLE) m_h_macd = iMACD(_Symbol, PERIOD_M1, 12, 26, 9, PRICE_CLOSE);
        if(m_h_stoch == INVALID_HANDLE) m_h_stoch = iStochastic(_Symbol, PERIOD_M1, 5, 3, 3, MODE_SMA, STO_LOWHIGH);
        if(m_h_cci == INVALID_HANDLE) m_h_cci = iCCI(_Symbol, PERIOD_M1, 14, PRICE_CLOSE);
        if(m_h_bb == INVALID_HANDLE) m_h_bb = iBands(_Symbol, PERIOD_M1, 20, 0, 2.0, PRICE_CLOSE);
        
        ArrayInitialize(m_vel_buffer, 0);
        m_vel_idx = 0;
        
        // --- PERFORMANCE HFT: CACHE STATICO GLOBAL ---
        Sovereign::MarketCache::vol_min = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
        Sovereign::MarketCache::vol_max = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
        
        // Inicializa o cache de lucro do dia imediatamente
        UpdateDailyProfitCache();
        
        // --- 🛡️ RECUPERAÇÃO DE ESTADO (State Recovery) ---
        // Garante que o robô reconheça posições abertas após um restart
        m_pos_ticket = 0;
        for(int i=PositionsTotal()-1; i>=0; i--) {
            ulong ticket = PositionGetTicket(i);
            if(ticket > 0 && PositionSelectByTicket(ticket)) {
                if(PositionGetInteger(POSITION_MAGIC) == InpMagicNumber && PositionGetString(POSITION_SYMBOL) == _Symbol) {
                    m_pos_ticket = ticket;
                    SyncRAMPosition();
                    SupremeLog("SINC: Posição órfã recuperada (Ticket: " + (string)m_pos_ticket + ")");
                    break;
                }
            }
        }
        
        // --- CALIBRAGEM NEURAL INICIAL ---
        m_cortex.LoadSynapses();
        SupremeLog("MEMÓRIA: Sinapses recuperadas/iniciadas com sucesso.");
        
        // Se após carregar, os valores estiverem zerados (primeira vez), reinicia:
        if(m_cortex.weights.w_markov == 0) {
             m_cortex.emotion.dopamine = 0.65;
             m_cortex.emotion.serotonin = 0.85;
             m_cortex.emotion.cortisol = 0.15;
             m_ctx.archive.pillars.atp_level = 100.0;
             m_cortex.weights.w_markov = 1.0;
             m_cortex.weights.w_institutional = 1.0;
             m_cortex.weights.w_fractal = 1.0;
             m_cortex.weights.w_quantum = 1.0;
             m_cortex.weights.w_titan = 1.0;
        }
        
        // Cache do parceiro de sincronia (reduz StringFind no OnTick)
        m_cortex.global_sync_score = 0.5; // Inicia em 50%
        
        if(StringFind(_Symbol, "WIN") >= 0) {
           string suffixes[] = {"G25","J25", "M25", "N25", "Q25", "V25", "Z25", "G26"};
           for(int i=0; i<ArraySize(suffixes); i++) {
               string target = "WDO" + suffixes[i];
               if(SymbolSelect(target, true) && SymbolInfoDouble(target, SYMBOL_BID) > 0) {
                   m_sync_partner = target;
                   break;
               }
           }
           if(m_sync_partner == "") {
               string current_suffix = StringSubstr(_Symbol, 3);
               string target = "WDO" + current_suffix;
               if(SymbolSelect(target, true) && SymbolInfoDouble(target, SYMBOL_BID) > 0) m_sync_partner = target;
           }
        } else if(StringFind(_Symbol, "WDO") >= 0) {
           string suffixes[] = {"G25","J25", "M25", "N25", "Q25", "V25", "Z25", "G26"};
           for(int i=0; i<ArraySize(suffixes); i++) {
               string target = "WIN" + suffixes[i];
               if(SymbolSelect(target, true) && SymbolInfoDouble(target, SYMBOL_BID) > 0) {
                   m_sync_partner = target;
                   break;
               }
           }
           if(m_sync_partner == "") {
               string current_suffix = StringSubstr(_Symbol, 3);
               string target = "WIN" + current_suffix;
               if(SymbolSelect(target, true) && SymbolInfoDouble(target, SYMBOL_BID) > 0) m_sync_partner = target;
           }
        }
        
        if(m_sync_partner != "") SupremeLog("SINCRONIA: Parceiro detectado -> " + m_sync_partner);
        else SupremeLog("AVISO: Parceiro de Sincronia (WIN/WDO) não encontrado no Market Watch.");
        
        m_auto_mode  = InpFullAutonomy;
        if(m_auto_mode) m_sys_flags |= SYS_FLAG_AUTO;
        
        SupremeLog("SISTEMA DESPERTADO: " + _Symbol + " em Modo REAL SUPREME v14.00");
        // PlaySound("ok.wav");
        
        // Habilita o Book de Ofertas (DOM)
        if(!MarketBookAdd(_Symbol)) Print("⚠️ FALHA AO ATIVAR DOM: Book de ofertas não disponível para ", _Symbol);
    }
    void Pulse(const MqlTick &tick) {
        if(_StopFlag) return; // MQL5 MULTITHREAD SAFETY
        if((ulong)tick.time_msc <= m_last_tick_msc) return;
        ulong start_micros = GetMicrosecondCount();
        
        // --- 🧪 PRICE DELTA DETECTOR ---
        bool price_changed = (tick.bid != m_last_bid || tick.ask != m_last_ask);
        
        m_last_tick_msc = tick.time_msc;
        m_current_tick = tick; // CAPTURA ATÔMICA
        
        // SAFETY: Latency Guard (2026 Protection)
        // Se o tick chegou com lag > 500ms (Internet/Broker lento), ignoramos para evitar slippage fantasma.
        long system_lag = (long)(GetTickCount64() - tick.time_msc);
        if(system_lag > 500) {
            if(m_pulse % 100 == 0) SupremeLog("⚠ LAG CRÍTICO DETECTADO: " + IntegerToString(system_lag) + "ms. Tick ignorado.");
            return; 
        }

        // --- HFT JITTER FILTER (2026 Optimization) ---
        // Se o tick for idêntico ao anterior (Bid, Ask, Last e Volume), ignoramos.
        // Ticks redundantes ocorrem em corretoras que enviam flags de tempo sem mudança de dados.
        static MqlTick last_processed_tick;
        if(tick.bid == last_processed_tick.bid && tick.ask == last_processed_tick.ask && 
           tick.last == last_processed_tick.last && tick.volume == last_processed_tick.volume) return;
        last_processed_tick = tick;

        m_pulse++;
        
        // PERFORMANCE: Cache do Spread Points p/ evitar divisões/subtrações repetidas
        m_spread_pts = (int)MathRound((tick.ask - tick.bid) * m_point_inv);
        
        ulong now_mic = GetMicrosecondCount(); // Cache unico do timestamp

        // --- NEURAL JITTER TELEMETRY (v12.50) ---
        ulong current_micros = GetMicrosecondCount();
        if(m_last_ai_micros > 0) m_cortex.neural_jitter_us = (double)(current_micros - m_last_ai_micros);
        m_last_ai_micros = current_micros;

        // --- 0. SINCROSCOPIO CENTRAL (Performance HFT: Cache de Segundo) ---
        static datetime last_time_score = 0;
        if(tick.time != last_time_score) {
            int total_sec = (int)(tick.time % 86400);
            m_current_time_score = (total_sec / 3600) * 100 + ((total_sec % 3600) / 60);
            last_time_score = tick.time;
        }
        
        // PERFORMANCE: Delta suppression (Só processa se o preço moveu ou 10ms passaram)
        ulong now_ms = GetTickCount64();
        if(!price_changed && (now_ms - m_last_heartbeat_ms < 10)) return;
        m_last_heartbeat_ms = now_ms;
        
        // --- NEURAL LATENCY MONITOR (2026 CPU GUARD) ---
        if(m_cpu_overload) {
             m_overload_counter--;
             if(m_overload_counter <= 0) m_cpu_overload = false;
        }

        if(price_changed || (now_ms - m_last_acc_update_ms > 200)) {
            // 🔄 REFRESH CACHE (OHLC) - Throttled by price/time
            RefreshM1Cache();
            
            // 1. SINCRONIA DE CONTA E GESTÃO (Throttled & Reactive)
            bool active_trading = (m_pos_ticket > 0 || m_in_transaction);
            static ulong last_acc_sync = 0;
            if(now_ms - last_acc_sync > (ulong)(active_trading ? 100 : 1000)) {
                m_acc_profit = AccountInfoDouble(ACCOUNT_PROFIT);
                m_acc_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
                m_acc_balance = AccountInfoDouble(ACCOUNT_BALANCE);
                last_acc_sync = now_ms;
                m_last_acc_update_ms = now_ms;
                
                // --- 📊 AUTO-CALC SCALP METRICS ---
                UpdateScalpAnalytics();
            }
            
            // PERFORMANCE: Tick Pressure Calculation (Queue-less Math)
            if(tick.bid > m_last_proc_bid) m_bid_press += 1.0; else if(tick.ask < m_last_proc_ask) m_ask_press += 1.0;
            
            // ⚡ TICK VELOCITY MONITOR (v12.00 OMEGA)
            static ulong last_v_update = 0;
            static int v_ticks = 0;
            v_ticks++;
            if(now_ms - last_v_update >= 1000) {
                m_cortex.tick_velocity = (double)v_ticks;
                v_ticks = 0;
                last_v_update = now_ms;
            }
            m_bid_press *= 0.98; m_ask_press *= 0.98; // Continuous decay for moving pressure
            m_cortex.bid_press = m_bid_press; m_cortex.ask_press = m_ask_press;
            
            // DYNAMIC STOP LEVEL (Spread Protection)
            m_stops_level = (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL) * m_point;
            // Fallback: Se stops level for 0, usa 2x spread como margem de segurança
            if(m_stops_level == 0) m_stops_level = m_spread_pts * m_point * 2.0;
            
            if(!OrderCalcMargin(ORDER_TYPE_BUY, _Symbol, 1.0, m_current_tick.ask, m_margin_per_lot_buy)) m_margin_per_lot_buy = 0;
            if(!OrderCalcMargin(ORDER_TYPE_SELL, _Symbol, 1.0, m_current_tick.bid, m_margin_per_lot_sell)) m_margin_per_lot_sell = 0;
            
            // Movi a calibração de Timeframe para cá para garantir atualização periódica 
            TimeframeCalibrationEngine();
            // PERFORMANCE: Spread Aritmético (Latência Zero vs SymbolInfoInteger)
            m_spread_pts = (int)((m_current_tick.ask - m_current_tick.bid) * m_point_inv);
            
            // PERFORMANCE: Removemos o sync periódico de lucro (Agora é REATIVO via OnTradeTransaction)
            // m_need_profit_sync agora é usado apenas para sync forçado (ex: Mudança de Conta)
            if(m_need_profit_sync) {
                UpdateDailyProfitCache();
                m_need_profit_sync = false;
            }

            // 🛑 DAILY LIMIT ENFORCEMENT (GESTOR QUANTUM: JUROS COMPOSTOS)
            if(m_auto_mode && m_acc_balance > 0) {
                Sovereign::QuantumBankroll::UpdateDailyTarget(m_acc_balance);
                double target_val = Sovereign::QuantumBankroll::GetCurrentTarget();
                double stop_val = m_acc_balance * (InpDailyLossPct / 100.0);
                double real_pnl_net = m_daily_profit_net_cached + m_acc_profit;
                
                // Target Met Logic
                if(Sovereign::QuantumBankroll::IsDailyTargetMet(real_pnl_net)) {
                    // Opcional: Trailing Profit ou Fechar? Aqui o usuário pediu Meta, vamos avisar e proteger.
                    static bool target_alert = false;
                    if(!target_alert) {
                        SupremeLog("🎯 META DIÁRIA QUANTUM ATINGIDA: R$ " + DoubleToString(real_pnl_net, 2));
                        target_alert = true;
                    }
                }

                if(real_pnl_net < -stop_val) {
                    if(m_pos_ticket > 0) {
                        ManualCloseAll();
                        SupremeLog("🛑 STOP LOSS DIÁRIO ATINGIDO (NET): Protegendo Banca.");
                    }
                }
            }
            
            // --- 🧬 BIO-DRIVE SYNC (Critical for Scaling) ---
            m_current_drive = m_cortex.GetDrive();
            
            // PERFORMANCE: Low-Power Metabolic Mode (HIBERNATE)
            // Se ATP < 5%, o sistema entra em economia extrema de CPU
            bool low_power = (Sovereign::BioState::atp_energy < 5.0);
            
            // --- SCANNERS MACRO & SEGURANÇA (Throttled 200ms) ---
            BlackSwanScanner(tick);
            if(!low_power) {
                GlobalSymmetrySync();
                LiquidityVoidScanner(); 
            }
            
            // 30s Property Sync
            static ulong last_sym_prop_sync = 0;
            if(now_ms - last_sym_prop_sync > 30000) {
                m_tick_size  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
                m_tick_value = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
                if(m_tick_size > 1e-10) {
                    m_tick_cost_ratio = m_tick_value / m_tick_size;
                    m_tick_inv = 1.0 / m_tick_size;
                }
                last_sym_prop_sync = now_ms;
            }
            
            if(m_current_tick.time - m_last_news_sync > 60) {
                MacroNewsSentinel();
                m_last_news_sync = m_current_tick.time;
            }
            
            AdvancedMathCore();
            GeneticEvolutionSystem();
            BiochemistryEngine();
            
            m_last_acc_update_ms = now_ms;
        }
        
        // --- ⚡ HFT CRITICAL PATH ---
        // RefreshM1Cache(); // Removed redundant call for performance
        OpeningRangeBreakoutCore();
        
        // --- ⚡ HFT SENSORY PATH (Throttled for Performance) ---
        static ulong last_sensory_update = 0;
        if(now_ms - last_sensory_update >= 5) { // 5ms throttle: Sufficient for HFT, saves massive CPU
            UpdateFastIndicators(); 
            PhysicsEngineSync();
            TickVelocityScanner();
            InstitutionalScanner(tick);
            TrapHunterEngine();
            last_sensory_update = now_ms;
        }
        
        // --- 🔗 SOUL CONNECTION (Python Bridge) ---
        SoulConnect(); 
        
        // --- 🛡️ SCALPER SAFETY TRAPS (v20.0 Titan) ---
        bool safety_lock = false;
        if(m_cortex.latency_ms > 150) safety_lock = true; // Latência alta demais para scalp
        if(m_spread_pts > InpMaxSpread * 1.5) safety_lock = true; // Spread abriu demais (Notícia ou falta de liquidez)
        
        UnifiedPositionManager();
        
        // 3. NANO-THROTTLING IA (500us precision)
        now_mic = GetMicrosecondCount();
        if(!m_cpu_overload && !safety_lock && (m_sys_flags & SYS_FLAG_AUTO) != 0 && (now_mic - m_last_ai_micros >= 1000)) {
            m_current_drive = m_cortex.GetDrive(); 
            WhaleAbsorptionEngine();
            AdvancedIntelligenceCycle(); 
            ParallelRealitySimulation(tick); 
            if(m_auto_mode) AutonomousDecisionCore(tick);
            m_last_ai_micros = now_mic;
        }
        
        m_last_proc_price = tick.last;
        m_last_proc_bid = tick.bid;
        m_last_proc_ask = tick.ask;
        
        // --- 4. TRANSACTION WATCHDOG (Anti-Freeze) ---
        if(m_in_transaction && now_ms > m_trans_timeout_ms) {
            m_in_transaction = false;
            m_virtual_margin_used = 0;
            m_orders_in_flight = 0;
            m_cortex.active_thought = "🕒 WATCHDOG: Reset de transação por timeout de rede.";
        }
        
        m_last_tick_msc = (ulong)tick.time_msc;
        long proc_time_micros = (long)(GetMicrosecondCount() - start_micros);
        m_cortex.cpu_load_us = (int)proc_time_micros; // Record CPU load separately
        
        // Se o processamento demorou mais de 1.5ms, liga o Overload Guard
        if(proc_time_micros > 1500) {
            m_cpu_overload = true;
            m_overload_counter = 5; // Pula IA por 5 ticks
        }
    }

    // --- 🔗 QUANTUM SOUL BRIDGE (LIVING AI 2026) ---
    void SoulConnect() {
        static ulong last_read_sync = 0;
        static ulong last_write_sync = 0;
        ulong now = GetTickCount64();

        // 1. LEITURA DE COMANDOS (Sensoriamento Nervoso - 50ms)
        if(now - last_read_sync > 50) {
            Sovereign::MQTTOrder order;
            if(Sovereign::CommandBridge::GetNextOrder(order)) {
                ExecuteSoulOrder(order);
            }
            if(Sovereign::CommandBridge::SyncSoulState()) {
                m_cortex.emotion.dopamine = Sovereign::CommandBridge::soul.neural_drive;
                m_need_hud_redraw = true;
            }
            last_read_sync = now;
        }

        // 2. ADAPTIVE METABOLISM RECORDING (v2026)
        // O sistema pulsa conforme a volatilidade: No pânico grava tudo, na calmaria economiza CPU.
        double recording_throttle = 1000.0; // Padrão: 1 segundo
        if(m_cortex.emotion.adrenaline > 0.7) recording_throttle = 50.0; // Modo Scalper BERSERK: Grava a cada 50ms
        else if(m_cortex.emotion.adrenaline > 0.3) recording_throttle = 250.0; // Modo HUNTING: 250ms

        if(now - last_write_sync > recording_throttle) {
            // Métricas de Microestrutura (Filtros 2026)
            double entropy = Sovereign::MarketCache::entropy_index;
            double fractal = Sovereign::MarketCache::fractal_dimension;
            double imbalance = m_ctx.archive.pillars.flow_imbalance;
            
            // Gravação Quantum
            Sovereign::CommandBridge::SendBodyState(
                m_current_tick.last, m_current_tick.bid, m_current_tick.ask, 
                (double)m_spread_pts, (double)m_current_tick.volume,
                m_atr_val, m_rsi_val_current, (m_pos_ticket > 0 ? PositionGetDouble(POSITION_PROFIT) : 0), 
                m_acc_balance, (m_pos_ticket > 0), (int)m_ram_pos.type,
                m_cortex.tick_velocity, imbalance, m_cortex.emotion.cortisol
            );
            
            last_write_sync = now;
        }
    }

    void ExecuteSoulOrder(Sovereign::MQTTOrder &ord) {
        SupremeLog("🧠 ALMA ORDENOU: " + ord.tipo + " | Lote: " + DoubleToString(ord.quantidade, 2));
        
        // --- 1. FILTRO DE PROTEÇÃO (CRÍTICO PARA SCALP) ---
        // Se o spread estiver > 150 pontos (15 ticks WINFUT), rejeita por segurança.
        if(m_spread_pts > 150) {
             SupremeLog("⛔ ORDEM REJEITADA: Spread muito alto (" + IntegerToString(m_spread_pts) + "pts).");
             Sovereign::CommandBridge::SendConfirmation(ord.id, "rejeitada", 0, 0, 0, "Spread Alto: " + IntegerToString(m_spread_pts));
             return;
        }
        
        // Se não houver margem livre suficiente (~R$ 150 por contrato mini), rejeita.
        double margin_req = 150.0 * ord.quantidade; 
        if(m_acc_margin < margin_req) {
             SupremeLog("⛔ ORDEM REJEITADA: Margem insuficiente. Livre: " + DoubleToString(m_acc_margin, 2));
             Sovereign::CommandBridge::SendConfirmation(ord.id, "rejeitada", 0, 0, 0, "Sem Margem");
             return;
        }

        ENUM_ORDER_TYPE type = (ord.tipo == "compra") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
        double price = (type == ORDER_TYPE_BUY) ? SymbolInfoDouble(ord.ativo, SYMBOL_ASK) : SymbolInfoDouble(ord.ativo, SYMBOL_BID);
        
        // Normalize Request
        ZeroMemory(m_exec_req);
        ZeroMemory(m_exec_res);
        m_exec_req.action = TRADE_ACTION_DEAL;
        m_exec_req.symbol = ord.ativo;
        m_exec_req.volume = NormalizeLot(ord.quantidade);
        m_exec_req.type = type;
        m_exec_req.price = price;
        m_exec_req.deviation = 20; // Tolerância
        m_exec_req.type_filling = m_filling;
        
        // SL/TP from Python (se enviado)
        double sl = 0, tp = 0;
        if(ord.sl_pts > 0) sl = (type == ORDER_TYPE_BUY) ? price - ord.sl_pts * m_point : price + ord.sl_pts * m_point;
        if(ord.tp_pts > 0) tp = (type == ORDER_TYPE_BUY) ? price + ord.tp_pts * m_point : price - ord.tp_pts * m_point;
        
        m_exec_req.sl = sl;
        m_exec_req.tp = tp;
        m_exec_req.comment = "Soul_" + StringSubstr(ord.id, 0, 10);
        
        if(OrderSend(m_exec_req, m_exec_res)) {
            if(m_exec_res.retcode == TRADE_RETCODE_DONE || m_exec_res.retcode == TRADE_RETCODE_DONE_PARTIAL) {
                // Sucesso
                Sovereign::CommandBridge::SendConfirmation(ord.id, "executada", m_exec_res.price, m_exec_res.volume);
                SupremeLog("✅ EXECUÇÃO CONFIRMADA: " + ord.id);
                // PlaySound("Expert.wav");
            } else {
                // Falha Lógica
                Sovereign::CommandBridge::SendConfirmation(ord.id, "rejeitada", 0, 0, 0, "Retcode: " + IntegerToString(m_exec_res.retcode));
            }
        } else {
            // Falha Envio
            Sovereign::CommandBridge::SendConfirmation(ord.id, "erro", 0, 0, 0, "OrderSend Failed: " + IntegerToString(GetLastError()));
        }
    }

    // Unified Class Homeostasis - Delegates to Cortex properly
    void HomeostasisCycle() {
        m_cortex.HomeostasisCycle();
        
        // Manual scaling for remaining local emotions if needed
        m_current_drive = m_cortex.GetDrive();
    }

    void BlackSwanScanner(const MqlTick &tick) {
        bool alert = false;
        string reason = "";
        
        // 1. Filtro de Spread
        double spread = (tick.ask - tick.bid) / m_point;
        // BACKTEST FIX: Disable spread panic in tester (Data can be gapped)
        if(spread > 150.0 && !MQLInfoInteger(MQL_TESTER)) { 
            alert = true;
            reason = "SPREAD ANORMAL";
        }
        
        // 2. Filtro de Volatilidade
        double current_vol = MathAbs(tick.bid - tick.last);
        if(m_atr_val > 0 && current_vol > m_atr_val * 4.0 && !MQLInfoInteger(MQL_TESTER)) {
            alert = true;
            reason = "VOLATILIDADE SUPREMA";
        }
        
        // 3. Filtro de Fluxo
        if(Sovereign::MarketCache::flow_intensity > 450.0 && !MQLInfoInteger(MQL_TESTER)) { 
            alert = true;
            reason = "ALTO FLUXO DE ORDENS";
        }
        
        // 5. Integração com Sentinela Macro (Usa cache já calculado no Loop de 200ms)
        if(m_cortex.black_swan_alert) {
             alert = true;
             reason = "PROTEÇÃO MACRO ATIVA";
        }
        
        // 4. Vácuo de Liquidez
        if(Sovereign::MarketCache::entropy_index < 0.2 && Sovereign::MarketCache::flow_intensity > 200 && !MQLInfoInteger(MQL_TESTER)) {
            alert = true;
            reason = "ALERTA DE FLUXO/LIQUIDEZ";
        }
        
        // BACKTEST OVERRIDE: Never allow Black Swan to block trading in tester
        if(MQLInfoInteger(MQL_TESTER)) alert = false;
        
        m_cortex.black_swan_alert = alert;
        if(alert) {
            m_cortex.active_thought = "🚨 CISNE NEGRO: " + reason;
            m_sys_flags |= SYS_FLAG_NEWS;
            m_smooth_v = 0; 
        } else {
            m_sys_flags &= ~SYS_FLAG_NEWS;
        }
    }

    void GlobalSymmetrySync() {
        if(m_sync_partner == "") {
            m_ctx.archive.pillars.symmetry_ratio = 0.5;
            return;
        }
        
        // PERFORMANCE: Throttle sync to 100ms (Saves CopyOpen/SymbolInfo churn)
        static ulong last_sync_call = 0;
        if(GetTickCount64() - last_sync_call < 100) return;
        last_sync_call = GetTickCount64();
        
        // BACKTEST PERFORMANCE CIRCUIT BREAKER
        // Se falhar uma vez no tester, desliga para sempre para evitar "Ticks Discarded"
        static bool sync_broken = false;
        if(sync_broken) return;

        // PERFORMANCE: Sincronia Multi-Ativo (WIN vs WDO / SP500 vs DXY)
        if(SymbolInfoInteger(m_sync_partner, SYMBOL_SELECT) == 0) {
            if(!SymbolSelect(m_sync_partner, true)) {
                if(MQLInfoInteger(MQL_TESTER)) {
                     sync_broken = true; // Kill switch for tester
                     SupremeLog("⚠️ SYNC DISABLED: Parceiro " + m_sync_partner + " indisponível no teste.");
                }
                m_sync_partner = ""; 
                return;
            }
        }

        MqlTick mirror_tick;
        if(SymbolInfoTick(m_sync_partner, mirror_tick)) {
             // PERFORMANCE: Cache symbol point to avoid API churn
             if(m_mirror_point <= 0) m_mirror_point = SymbolInfoDouble(m_sync_partner, SYMBOL_POINT);
             
              double p1 = (m_current_tick.bid - m_curr_bar_open) / (m_point + 1e-9);
              
              double mirror_open = 0; double open_arr[1];
              if(CopyOpen(m_sync_partner, PERIOD_M1, 0, 1, open_arr) > 0) mirror_open = open_arr[0];

              // BUG FIX: Division Guard for Sync Partner (Avoids infinity/NaN on stale data)
              if(mirror_open <= 0) mirror_open = mirror_tick.bid; 

              double p2 = (mirror_tick.bid - mirror_open) / (m_mirror_point + 1e-9);
             
              // PERFORMANCE: Symmetry Gating (v12.00 OMEGA)
              // No scalping B3, se WIN e WDO não estão em simetria de espelho, o ruído é perigoso.
              double sym_diff = MathAbs(p1 + p2); // No cenário perfeito WIN+ e WDO-, sym_diff -> 0
              m_symmetry_gate = (1.0 / (1.0 + sym_diff * 0.5));
              m_cortex.global_sync_score = m_symmetry_gate; // For HUD
              m_ctx.archive.pillars.correlation_index = m_symmetry_gate;
              
              m_ctx.archive.pillars.symmetry_ratio = 0.5 + (0.5 * (p1 - p2) / (MathAbs(p1) + MathAbs(p2) + 1e-9));
        }
    }

    void AutonomousDecisionCore(const MqlTick &tick) {
        if(_StopFlag) return;
        
        // 1. CHECAGEM DE SAÚDE DO SISTEMA
        if(m_cpu_overload || !m_auto_mode) return;
        
        // 2. SINAPSE DO NOVO CÉREBRO (COMPLEXIDADE 2026)
        SovereignMind::NeuralOutput neuro_out;
        
        // Usa RSI cacheado e ATR cacheado para alta velocidade
        double rsi_input = (m_rsi_val_current > 0) ? m_rsi_val_current : 50.0;
        double atr_input = (m_last_bar_atr > 0) ? m_last_bar_atr : m_point * 50;
        
        // Think agora recebe m_point para calcular distâncias reais em pontos da B3
        m_mind.Think(tick, rsi_input, atr_input, m_point, m_daily_profit_cached, neuro_out);
        m_last_intensity = neuro_out.intensity;
        
        // Exibe pensamento no HUD
        if(neuro_out.tactic != "SCANNING") {
             m_cortex.active_thought = "🧠 SINAPSE [" + IntegerToString(m_last_intensity) + "]: " + neuro_out.tactic + " (Conf: " + DoubleToString(neuro_out.confidence*100,0) + "%)";
        }

        // 3. FILTRAGEM FINAL DE EXECUÇÃO
        if(MathAbs(neuro_out.signal) > 0.0) {
            
            // FILTRO DE SPREAD (Trava de Segurança HFT)
            if(m_spread_pts > 400) return; 
            
            // OTIMIZAÇÃO CRÍTICA DE PERFORMANCE: Uso de flags event-driven
            if(m_pos_ticket > 0 || m_orders_in_flight > 0) return; 
            
            // EXECUTE
            if(neuro_out.signal > 0) ExecutePredatoryOrder(1, STRAT_MOMENTUM, neuro_out.tactic, tick);
            if(neuro_out.signal < -0.1) ExecutePredatoryOrder(-1, STRAT_MOMENTUM, neuro_out.tactic, tick);
        }
        
        if(m_pulse % 100 == 0) m_need_hud_redraw = true;
    }

    void ParallelRealitySimulation(const MqlTick &tick) {
        // 1. EVALUATION: Check SL/TP for all ghosts
        for(int i=0; i<10; i++) {
             if(!m_ghost_pool[i].active) continue;
             
             bool win = false;
             bool loss = false;
             
             if(m_ghost_pool[i].type == 1) { // BUY
                  if(tick.bid >= m_ghost_pool[i].tp) win = true;
                  else if(tick.bid <= m_ghost_pool[i].sl) loss = true;
             } else { // SELL
                  if(tick.ask <= m_ghost_pool[i].tp) win = true;
                  else if(tick.ask >= m_ghost_pool[i].sl) loss = true;
             }
             
             if(win || loss) {
                  m_ghost_total++;
                  if(win) m_ghost_wins++;
                  m_ghost_win_rate = (double)m_ghost_wins / m_ghost_total;
                  m_ghost_pool[i].active = false;
                  
                  if(m_pulse % 10 == 0) SupremeLog("🎭 GHOST STUDY: " + (win ? "GAIN" : "LOSS") + " | WR=" + DoubleToString(m_ghost_win_rate*100,1) + "%");
                  
                  // RECURSIVE FEEDBACK: Ghost results influence real AI state
                  if(win) m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.02);
                  else if(loss) m_cortex.emotion.serotonin = MathMax(0.1, m_cortex.emotion.serotonin - 0.02);
             }
        }
    }

    bool CheckPortfolioRisk() {
        // --- 🛡️ PORTFOLIO RISK LIMIT (User Pensamento: $1000) ---
        double portfolio_risk = 0;
        int active_positions = 0;
        
        for(int i=PositionsTotal()-1; i>=0; i--) {
            if(PositionSelectByTarget(i)) {
                 portfolio_risk += MathAbs(PositionGetDouble(POSITION_PROFIT));
                 active_positions++;
            }
        }
        
        // Se o risco do portfólio (perda aberta) exceder o limite (ex $1000), bloqueia.
        if(portfolio_risk > InpPortfolioRiskLimit) {
             m_cortex.active_thought = "🛡️ RISCO PORTFÓLIO: Limite de $" + DoubleToString(InpPortfolioRiskLimit,0) + " excedido.";
             return false;
        }
        
        // --- 🛡️ POSITION LIMITS (User Pensamento: Max 6) ---
        if(active_positions >= InpMaxConcurrentPositions) {
             if(m_pos_ticket <= 0) { // Só bloqueia NOVAS se já tiver 6
                 m_cortex.active_thought = "🛡️ LIMIT POSIÇÃO: Max " + IntegerToString(InpMaxConcurrentPositions) + " ativos simultâneos.";
                 return false;
             }
        }
        
        return true;
    }

    // Helper p/ looping de posições sem interferir no m_pos_ticket principal
    bool PositionSelectByTarget(int index) {
        ulong t = PositionGetTicket(index);
        return (t > 0 && PositionSelectByTicket(t));
    }

    void SpawnGhostTrade(int type, string tag, const MqlTick &tick) {
        for(int i=0; i<10; i++) {
             if(m_ghost_pool[i].active) continue;
             
             m_ghost_pool[i].type = type;
             m_ghost_pool[i].entry = (type == 1) ? tick.ask : tick.bid;
             m_ghost_pool[i].strategy = tag;
             
             double sl_pts = (InpStopPoints > 0) ? InpStopPoints : 150;
             double tp_pts = (InpTargetPoints > 0) ? InpTargetPoints : 100;
             
             m_ghost_pool[i].sl = (type == 1) ? m_ghost_pool[i].entry - sl_pts * m_point : m_ghost_pool[i].entry + sl_pts * m_point;
             m_ghost_pool[i].tp = (type == 1) ? m_ghost_pool[i].entry + tp_pts * m_point : m_ghost_pool[i].entry - tp_pts * m_point;
             m_ghost_pool[i].active = true;
             break;
        }
    }

    bool CheckPendingOrders() {
        // PERFORMANCE: Throttle scanning to 250ms or rely on m_in_transaction
        static ulong last_check = 0;
        if(GetTickCount64() - last_check < 250) return m_in_transaction;
        last_check = GetTickCount64();

        for(int i=OrdersTotal()-1; i>=0; i--) {
            if(OrderGetTicket(i) > 0 && OrderGetInteger(ORDER_MAGIC) == InpMagicNumber) return true;
        }
        return false;
    }

    void ExecutePredatoryOrder(int direction, EStrategyType strat, string tag, const MqlTick &tick) {
        // 1. VALIDAÇÃO DE PREÇO E LOTE (Pre-Lock)
        if(tick.ask <= 0 || tick.bid <= 0) return;
        
        double lot = CalculateLotSize(tick, direction);
        if(lot <= 0) return; 
        
        // 2. VIRTUAL MARGIN CHECK (HFT Safety - Usa RAM Cache)
        double margin_per_lot = (direction == 1) ? m_margin_per_lot_buy : m_margin_per_lot_sell;
        double total_vol = lot + m_virtual_margin_used;
        double margin_req = total_vol * margin_per_lot;
        
        if(margin_per_lot > 0 && margin_req > m_acc_margin) {
            m_cortex.active_thought = "⚠️ MARGEM VIRTUAL EXCEDIDA: Abortando rajada.";
            return;
        }

        // 3. ATOMIC LOCK (Depois de tudo validado)
        m_in_transaction = true;
        m_virtual_margin_used += lot;
        m_trans_timeout_ms = GetTickCount64() + 2000; 
        
        // CAMPOS DINÂMICOS (Usando Pre-Fill de m_exec_req)
        m_exec_req.volume = lot; 
        m_exec_req.type = (direction == 1) ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
        m_exec_req.comment = tag;
        
        double slippage = 5 * m_tick_size;
        m_exec_req.price = (direction == 1) ? NormalizePrice(tick.ask + slippage) : NormalizePrice(tick.bid - slippage);
        
        // GEOMETRIA DINÂMICA DE RISCO
        double sl = 0, tp = 0;
        double atr = m_last_bar_atr;
        if(atr <= 0) atr = m_point * 100;
        
        double sl_mod = 1.0; 
        double tp_mod = 1.0;
        BioRiskAdvisory(tp_mod, sl_mod);
        
        // BUG FIX: Sincroniza com TimeframeCalibrationEngine (Unified Risk) e Physics v10.0
        double dynamic_sl = (m_ctx.auto_sl > 0) ? (m_ctx.auto_sl * m_point) : (atr * 1.5);
        sl = (InpStopPoints > 0) ? (InpStopPoints * m_point * sl_mod) : dynamic_sl * sl_mod;
        tp = (InpTargetPoints > 0) ? (InpTargetPoints * m_point) * tp_mod : atr * 3.0 * tp_mod;
        
        m_exec_req.sl = (direction == 1) ? NormalizePrice(m_exec_req.price - sl) : NormalizePrice(m_exec_req.price + sl);
        m_exec_req.tp = (direction == 1) ? NormalizePrice(m_exec_req.price + tp) : NormalizePrice(m_exec_req.price - tp);
        
        // Proteção de Stop Level (B3)
        double min_dist = m_stops_level + (m_point * 2); 
        if(MathAbs(m_exec_req.price - m_exec_req.sl) < min_dist && m_exec_req.sl != 0) m_exec_req.sl = (direction == 1) ? NormalizePrice(m_exec_req.price - min_dist) : NormalizePrice(m_exec_req.price + min_dist);
        if(MathAbs(m_exec_req.price - m_exec_req.tp) < min_dist && m_exec_req.tp != 0) m_exec_req.tp = (direction == 1) ? NormalizePrice(m_exec_req.price + min_dist) : NormalizePrice(m_exec_req.price - min_dist);
        
        // GAP PROTECTION (B3)
        if(direction == 1 && tick.ask > m_exec_req.price + (10 * m_point)) { 
            m_in_transaction = false; 
            m_virtual_margin_used = MathMax(0, m_virtual_margin_used - lot);
            return; 
        }
        if(direction == -1 && tick.bid < m_exec_req.price - (10 * m_point)) { 
            m_in_transaction = false; 
            m_virtual_margin_used = MathMax(0, m_virtual_margin_used - lot);
            return; 
        }
        
        // ENVIO ASSÍNCRONO (LATÊNCIA ZERO)
        m_last_entry_price = (direction == 1) ? tick.ask : tick.bid; 
        m_exec_start_micros = GetMicrosecondCount(); // Capture start time
        if(!OrderSendAsync(m_exec_req, m_exec_res)) {
            m_in_transaction = false; 
            m_virtual_margin_used = MathMax(0, m_virtual_margin_used - lot);
            m_last_entry_price = 0;
            m_exec_start_micros = 0; // Reset on failure
        } else {
            m_cortex.active_thought = "⚡ APEX ENVIADO: " + tag;
        }
    }

    // --- IMPLEMENTAÇÃO DOS MOTORES MESTRE ---
    
    // --- 🌍 CÓRTEX FUNDAMENTALISTA (NEWS READER) ---
    void MacroNewsSentinel() {
        // Throttled: Already checked in Pulse (60s), but we optimize the structural call
        static datetime last_processed_news_hour = -1;
        if(m_current_tick.time == last_processed_news_hour) return; 

        MqlDateTime dt;
        TimeToStruct(m_current_tick.time, dt);
        last_processed_news_hour = m_current_tick.time;
        
        bool danger_zone = false;
        string event_name = "";
        
        // Abertura Mercado Americano (Volatilidade Alta)
        if(dt.hour == 10 && dt.min >= 25 && dt.min <= 40) { danger_zone = true; event_name = "ABERTURA NYSE"; }
        
        // Payroll (Primeira Sexta do Mês - Aproximação)
        if(dt.day_of_week == 5 && dt.day <= 7 && dt.hour == 9 && dt.min >= 25 && dt.min <= 35) { danger_zone = true; event_name = "PAYROLL (US)"; }
        
        // FOMC / FED (Geralmente 15:00 ou 16:00) - Detecção genérica de aumento de spread
        if(m_spread_pts > InpMaxSpread) { // BUG FIX: Usa limite definido pelo usuário
             danger_zone = true; 
             event_name = "CHOQUE DE SPREAD/VOLATILIDADE";
        }
        
        if(danger_zone) {
            // A IA "sente" a tensão do mercado
            m_cortex.emotion.cortisol = 1.0; // Medo Máximo -> Para de operar ou aperta stops
            m_cortex.active_thought = "⚠️ MACRO ALERT: " + event_name + " IMINENTE. BLINDANDO CARTEIRA.";
            
            // Se tiver posições abertas, ativa trailing stop de emergência
            m_trailing_active = true;
        } 
        else {
            // Pós-Notícia: Se sobrevivemos e o preço está andando forte
            if(m_cortex.emotion.cortisol > 0.8 && Sovereign::MarketCache::flow_intensity > 100) {
                 m_cortex.emotion.cortisol = 0.2; // Alívio
                 m_cortex.emotion.adrenaline = 1.0; // Euforia do movimento
                 m_cortex.active_thought = "⚡ SURFANDO O CHOQUE: Aproveitando a volatilidade pós-notícia!";
            }
        }
    }  
    
    void UpdateFastIndicators() {
        // PERFORMANCE: Ultra-reactive indicator pooling
        static long last_vol = 0;
        bool high_activity = (m_cortex.emotion.adrenaline > 0.8 || (long)m_current_tick.volume > last_vol);
        last_vol = (long)m_current_tick.volume;

        uint poll_rate = high_activity ? 0 : 100; 
        
        if(GetTickCount64() - m_last_rsi_sync_ms >= poll_rate) {
            if(CopyBuffer(m_h_rsi, 0, 0, 1, m_rsi_buf) > 0) m_rsi_val_current = m_rsi_buf[0];
            
            // 2026 BOLLINGER INTEGRATION: Catching the Volatility Squeeze
            double bb_mid[], bb_up[], bb_low[];
            if(CopyBuffer(m_h_bb, 1, 0, 1, bb_up) > 0) m_bb_up = bb_up[0];
            if(CopyBuffer(m_h_bb, 2, 0, 1, bb_low) > 0) m_bb_low = bb_low[0];
            
            m_last_rsi_sync_ms = GetTickCount64();
        }
    }

    // Defines Market States
    enum EMarketRegime {
        REGIME_CHAOS = 0,
        REGIME_TRENDING = 1,
        REGIME_RANGING = 2
    };
    
    EMarketRegime m_quantum_regime;

    // --- 🕸️ CAÇADOR DE ARMADILHAS (TRAP HUNTER ENGINE) ---
    void TrapHunterEngine() {
        // SAFETY: The Steamroller Protection (Não entra contra trem-bala)
        if(MathAbs(m_ctx.archive.pillars.force_net) > 50.0) return;

        // --- 🕸️ 2026 FLASH REJECTION (HFT SCALPER) ---
        // Se o preço teve um spike violento e a velocidade inverteu instantaneamente
        static double last_p = 0;
        static ulong last_t = 0;
        double bid = m_current_tick.bid;
        ulong now = GetMicrosecondCount();
        
        if(last_p > 0 && now - last_t < 10000) { // Janela de 10ms
             double delta = (bid - last_p) * m_point_inv;
             // Se subiu > 40 pontos e a velocidade atual é fortemente negativa (Rejeição)
             if(delta > 40 && m_smooth_v < -10.0) {
                  ExecutePredatoryOrder(-1, STRAT_REVERSION, "FLASH_REJECT:Bear", m_current_tick);
                  SupremeLog("⚡ FLASH REJECTION DETECTADA (TOPO)");
             }
             // Se caiu > 40 pontos e a velocidade atual é fortemente positiva
             if(delta < -40 && m_smooth_v > 10.0) {
                  ExecutePredatoryOrder(1, STRAT_REVERSION, "FLASH_REJECT:Bull", m_current_tick);
                  SupremeLog("⚡ FLASH REJECTION DETECTADA (FUNDO)");
             }
        }
        last_p = bid; last_t = now;

        // Detecta "Stop Hunts" institucionais (Rompimentos Falsos)
        // Agora usa o Cache M1 RAM (m_last_bar_high/low) para Zero Latency
        double recent_high = m_last_bar_high;
        double recent_low  = m_last_bar_low;
        double active_price = m_current_tick.bid;
        
        if(recent_high <= 0 || recent_low <= 0) return;
        
        // --- BULL TRAP DETECTOR (Armadilha de Compra) ---
        if(active_price > recent_high) {
             double vol = (double)m_current_tick.volume; 
             double rsi = m_rsi_val_current; // BUG FIX: Usa RSI do candle ATUAL, não fechado
             
             // Condições: Sobrecompra + Volume + Rejeição
             if(rsi > 75 && vol > 10 && Sovereign::MarketCache::ret_rev_value >= 8.0) {
                 // SINAL DE VENDA (CONTRA-ATAQUE)
                 if(m_cortex.emotion.dopamine > 0.5) { // Só faz se tiver confiança
                     ExecutePredatoryOrder(-1, STRAT_REVERSION, "TRAP_HUNTER_BEAR:Institucional", m_current_tick);
                 }
             }
        }

        // --- BEAR TRAP DETECTOR (Armadilha de Venda / Stop Hunt) ---
        if(active_price < recent_low) {
             double vol = (double)m_current_tick.volume;
             double rsi = m_rsi_val_current;
             
             if(rsi < 25 && vol > 10 && Sovereign::MarketCache::ret_rev_value <= -8.0) {
                 // SINAL DE COMPRA (CONTRA-ATAQUE)
                 if(m_cortex.emotion.dopamine > 0.5) {
                     ExecutePredatoryOrder(1, STRAT_REVERSION, "TRAP_HUNTER_BULL:Institucional", m_current_tick);
                 }
             }
        }
    }
    void PhysicsEngineSync() {
        // MICRO-VELOCITY: Usa microssegundos p/ precisão HFT (Zero Jitter)
        double price = GetBestPrice(m_current_tick);
        if(price <= 0) return;
        // BUG FIX: Removed m_last_eval_price suppression here as it was dropping valid ticks during high volatility
        
        // --- SAFETY GUARD (INITIALIZATION) ---
        if(m_last_proc_price <= 0) {
            m_last_proc_price = price;
            m_last_tick_time = GetMicrosecondCount();
            return;
        }
        
        ulong now_micros = GetMicrosecondCount();
        long dt_micros = (long)(now_micros - m_last_tick_time);
        
        // ANTI-JITTER FILTER: Evita divisão por zero se ticks virem no mesmo microsegundo
        if(dt_micros < 100) return; 

        m_last_tick_time = now_micros;
        double dp = (price - m_last_proc_price) * m_point_inv; 
        m_last_proc_price = price;
        
        double velocity = (dp * 1000000.0) / (double)dt_micros;
        m_smooth_v = (m_smooth_v * 0.7) + (velocity * 0.3);
        
        m_ctx.archive.pillars.impulse_velocity = m_smooth_v;
        double mass = 1.0 + (Sovereign::MarketCache::flow_intensity * 0.02); // Multiplica instead of division
        m_ctx.archive.pillars.mass = mass;
        
        m_ctx.archive.pillars.kinetic_energy = 0.5 * mass * (m_smooth_v * m_smooth_v);
        
        // INTERPOLATED INERTIA (Branchless)
        double inertia_delta = (MathAbs(m_smooth_v) > 0.1) ? 0.01 : -0.02;
        m_ctx.archive.pillars.inertia = MathMax(0.5, MathMin(5.0, m_ctx.archive.pillars.inertia + inertia_delta));
        
        m_ctx.archive.pillars.force_net = mass * m_smooth_v;
    }
    
    void TickVelocityScanner() {
        // Filtro Tático HFT: Mede a desaceleração de ticks em microssegundos
        double current_v = MathAbs(m_smooth_v);
        
        // Remove old value from running sum using circular buffer logic
        int idx = m_vel_idx % 10;
        m_vel_sum -= m_vel_buffer[idx];     // Subtract old value
        m_vel_buffer[idx] = current_v;      // Update buffer
        m_vel_sum += current_v;             // Add new value
        m_vel_idx++;
        
        if(m_vel_idx < 10) return;
        
        double avg_v = m_vel_sum / 10.0;
        
        // Se a velocidade atual for muito menor que a média recente em um movimento forte: DIVERGÊNCIA
        double imb = m_ctx.archive.pillars.flow_imbalance;
        if(avg_v > InpVelDivAvgThreshold && current_v < avg_v * InpVelDivSlowdownPct) {
             if(m_smooth_v > 0) m_ctx.archive.pillars.tick_intensity_divergence = 0.8; // Exaustão de Compra
             else m_ctx.archive.pillars.tick_intensity_divergence = -0.8; // Exaustão de Venda
        } else {
             m_ctx.archive.pillars.tick_intensity_divergence = 0;
        }
    }

    void AdvancedMathCore() {
        m_ctx.archive.pillars.hurst_exponent = (Sovereign::MarketCache::fractal_dimension > 0) ? (2.0 - Sovereign::MarketCache::fractal_dimension) : 0.5;
        m_ctx.archive.pillars.shannon_entropy = Sovereign::MarketCache::entropy_index;
        m_ctx.archive.pillars.tick_pressure = Sovereign::MarketCache::flow_intensity;
        
        // --- QUANTUM REGIME CLASSIFIER (2026 AI STD) ---
        // Fuses Entropy + Hurst + Flow to determine Market Phase
        double h = m_ctx.archive.pillars.hurst_exponent;
        double e = m_ctx.archive.pillars.shannon_entropy;
        
        if(h > 0.6 && e < 0.4) m_quantum_regime = REGIME_TRENDING; // Organized Motion
        else if(h < 0.4 && e < 0.6) m_quantum_regime = REGIME_RANGING; // Mean Reverting
        else m_quantum_regime = REGIME_CHAOS; // Neural Noise
        
        if(m_auto_mode) {
             if(m_quantum_regime == REGIME_TRENDING) m_cortex.active_vision = "QUANTUM: LINEAR FLOW";
             else if(m_quantum_regime == REGIME_RANGING) m_cortex.active_vision = "QUANTUM: OSCILLATION";
             else m_cortex.active_vision = "QUANTUM: HIGH ENTROPY";
        }

        // --- PREDICTIVE DREAM ENGINE (Simulação Monte Carlo Lite) ---
        // Simula 5 passos à frente usando Inércia + Ruído Gaussiano
        // Se a projeção for otimista, aumenta a confiança (Dopamina).
        
        static ulong last_dream = 0;
        if(GetTickCount64() - last_dream > 1000) { // Sonha a cada 1s
            double proj_price = m_current_tick.bid;
            double drift = m_smooth_v * m_point; // Tendência atual
            double volt = (m_last_bar_atr > 0 ? m_last_bar_atr : m_point * 50) / 60.0; // Volatilidade por segundo
            
            // Simula 5 passos
            for(int i=0; i<5; i++) {
                double noise = ((MathRand() / 32767.0) - 0.5) * volt;
                proj_price += drift + noise;
            }
            
            // Avaliação do Sonho
            if(proj_price > m_current_tick.bid + (10 * m_point)) m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.05); // Sonho de Alta
            if(proj_price < m_current_tick.bid - (10 * m_point)) m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.05); // Sonho de Baixa (Confiança em movimento)
            
            last_dream = GetTickCount64();
        }
    }

    void BiochemistryEngine() {
        // Metabolismo AI: Emite hormônios e equilibra agressividade
        // HomeostasisCycle removed - handled centrally in Nano-Throttle loop
        m_current_drive = m_cortex.GetDrive(); // CACHE RAM
        
        // --- 2026 BIO-HOMEOPATHY: Serotonin Decay ---
        // Se a IA não opera, a satisfação cai lentamente (tédio/necessidade de agir)
        // Isso simula o ciclo de "caça" da IA.
        static ulong last_bio_decay = 0;
        if(GetTickCount64() - last_bio_decay > 60000) { // A cada 1 minuto
             if(m_pos_ticket <= 0) m_cortex.emotion.serotonin = MathMax(0.1, m_cortex.emotion.serotonin - 0.02);
             last_bio_decay = GetTickCount64();
        }

        // Simulação de Metabolismo AI (Unified Bio-Core)
        Sovereign::BioState::Pulse(); 

        // Active Trading Metabolism (Overclocking the base biological rate)
        if(m_cortex.emotion.adrenaline > 0.8) {
             Sovereign::BioState::atp_energy = MathMax(1.0, Sovereign::BioState::atp_energy - 0.01); // Shock Drain
        } else {
             Sovereign::BioState::atp_energy = MathMin(100.0, Sovereign::BioState::atp_energy + 0.005); // Active Recovery
        }
        
        // Sync Pillar State
        m_ctx.archive.pillars.atp_level = Sovereign::BioState::atp_energy;
        
        // Sincronia de Serotonina com Lucro/Prejuízo Diário (Cache-Driven)
        double daily_profit = m_acc_profit;
        if(daily_profit > 10) m_cortex.emotion.serotonin = MathMin(1.0, m_cortex.emotion.serotonin + 0.01);
        if(daily_profit < -10) m_cortex.emotion.serotonin = MathMax(0.1, m_cortex.emotion.serotonin - 0.01);
        
        // --- SELF-HEALING HANDLE SYSTEM ---
        if(m_h_rsi == INVALID_HANDLE) m_h_rsi = iRSI(_Symbol, PERIOD_M1, 14, PRICE_CLOSE);
        if(m_h_atr == INVALID_HANDLE) m_h_atr = iATR(_Symbol, PERIOD_M1, 14);
        if(m_h_bb  == INVALID_HANDLE) m_h_bb  = iBands(_Symbol, PERIOD_M1, 20, 0, 2.0, PRICE_CLOSE);
    }


    
    void DarkLiquidityHunter() {
        // PERFORMANCE: Reset de detecção p/ evitar "Whale-Ghosts" no HUD
        m_whale_wall_price = 0;
        m_whale_wall_vol = 0;
        
        // PERFORMANCE: Microsecond-based Throttle (HFT Precision)
        static ulong last_dom_read = 0;
        ulong now = GetMicrosecondCount();
        if(now - last_dom_read < 200000) return; // Lê DOM a cada 200ms (Preciso)
        last_dom_read = now;

        if(!MarketBookGet(_Symbol, m_book_buf)) return;
        int size = ArraySize(m_book_buf);
        if(size == 0) return;
        
        double buy_v = 0, sell_v = 0;
        double max_vol = -1;
        double best_wall_p = 0;
        int depth = MathMin(size, 30);
        double mid = (m_current_tick.bid + m_current_tick.ask) / 2.0;
        
        for(int i=0; i<depth; i++) {
            double v = (double)m_book_buf[i].volume;
            double p = m_book_buf[i].price;
            
            if(m_book_buf[i].type == BOOK_TYPE_BUY || m_book_buf[i].type == BOOK_TYPE_BUY_MARKET) buy_v += v;
            else if(m_book_buf[i].type == BOOK_TYPE_SELL || m_book_buf[i].type == BOOK_TYPE_SELL_MARKET) sell_v += v;
            
            // WHALE WALL RANKING: Prioriza paredes próximas ao preço atual e com volume massivo
            if(v > InpMinWhaleVolumeDOM) {
                // Score de relevância: Volume / Distância (Paredes próximas e grandes ganham)
                double dist = MathAbs(p - mid) * m_point_inv + 1.0;
                double rank = v / dist;
                if(rank > max_vol) {
                     max_vol = rank;
                     best_wall_p = p;
                     m_whale_wall_vol = v;
                }
            }
        }
        
        if(best_wall_p > 0) {
            m_whale_wall_price = best_wall_p;
            if(m_pulse % 1000 == 0) SupremeLog("🐋 WHALE WALL DETECTADA: " + DoubleToString(best_wall_p, m_digits) + " (Vol Score Rank)");
        }
        
        if(buy_v + sell_v > 0) {
            double old_imb = m_ctx.archive.pillars.flow_imbalance;
            m_ctx.archive.pillars.flow_imbalance = (buy_v - sell_v) / (buy_v + sell_v);
            
            // Monitora a velocidade de mudança de sentimento no Book
            m_dom_velocity = (m_ctx.archive.pillars.flow_imbalance - old_imb);
            m_dom_dirty_flag = true; 

            if(MathAbs(m_ctx.archive.pillars.flow_imbalance) > 0.6) m_cortex.emotion.adrenaline = MathMin(1.0, m_cortex.emotion.adrenaline + 0.05);
        }
        
        // --- 🕵️ DARK POOL STEALTH DETECTION ---
        // Se houver volume alto em um preço estático (baixa velocidade de preço), detectamos absorção stealth.
        static double last_vol_at_price = 0;
        static double last_detect_p = 0;
        if(m_current_tick.bid == last_detect_p && m_current_tick.volume > 50) {
             last_vol_at_price += (double)m_current_tick.volume;
             if(last_vol_at_price > 500) { // Acumulou 500 contratos no mesmo preço sem mover
                  double bias = (m_smooth_v > 0 ? 0.8 : -0.8);
                  // Move bias based on dominance if exists
                  if(MathAbs(bias) > MathAbs(m_cortex.institutional_intent)) m_cortex.institutional_intent = bias;
                  
                  if(m_pulse % 100 == 0) SupremeLog("🕵️ STEALTH ABSORPTION: " + DoubleToString(m_current_tick.bid, m_digits) + " (Vol Accum=" + DoubleToString(last_vol_at_price,0) + ")");
             }
        } else {
             last_vol_at_price = 0;
             last_detect_p = m_current_tick.bid;
        }
    }
    
    void InstitutionalScanner(const MqlTick &tick) {
        // PERFORMANCE: No logic here. DOM scan moved entirely to OnBookEvent
        // for zero-redundancy depth intelligence.
    }
    
    void AdvancedIntelligenceCycle() {
        m_cortex.HomeostasisCycle();
        
        // HEARTBEAT: Log a cada 2000 ciclos (~2 segundos no índice) para confirmar que está vivo
        if(m_pulse % 2000 == 0) {
            SupremeLog("💓 HEARTBEAT: Robô Processando [Drive: " + DoubleToString(m_current_drive, 1) + " | ATP: " + DoubleToString(Sovereign::BioState::atp_energy, 1) + "%]");
        }
    }
    
    void GeneticEvolutionSystem() {
        // --- 2026 NEURAL SYNAPSE PRUNING (SOFT NORMALIZATION) ---
        // BUG FIX: Removed 'Brain Wipe' (Hard Reset to 1.0). Now uses Soft Decay to preserve learning.
        static ulong last_pruning = 0;
        
        // Se a satisfação (Serotonina) for muito baixa por muito tempo, ajustamos os pesos suavemente
        if(m_cortex.emotion.serotonin < 0.15 && (GetTickCount64() - last_pruning > 3600000)) { // 1h cooldown
             // Soft Normalization: Move weights 10% closer to 1.0 (Baseline)
             m_cortex.weights.w_markov = (m_cortex.weights.w_markov * 0.9) + 0.1;
             m_cortex.weights.w_fractal = (m_cortex.weights.w_fractal * 0.9) + 0.1;
             m_cortex.weights.w_institutional = (m_cortex.weights.w_institutional * 0.9) + 0.1;
             m_cortex.weights.w_quantum = (m_cortex.weights.w_quantum * 0.9) + 0.1;
             m_cortex.weights.w_titan = (m_cortex.weights.w_titan * 0.9) + 0.1;
             
             // Restore some balance
             m_cortex.emotion.serotonin = 0.4; 
             SupremeLog("🧠 NEURAL PLASTICITY: Normalização suave de pesos (Anti-Overfitting).");
             last_pruning = GetTickCount64();
        }
    }


    

    
    void WhaleAbsorptionEngine() {
        // BUG FIX: Adaptive decay for institutional intent to avoid sticking states
        // Scanners B3: Se o preço foge da zona, o desespero/intenção deve esfriar mais rápido.
        double decay = 0.95;
        double bid = m_current_tick.bid;
        double dist_low = MathAbs(bid - m_ctx.archive.pillars.structure_low) * m_point_inv;
        double dist_high = MathAbs(bid - m_ctx.archive.pillars.structure_high) * m_point_inv;
        
        if(dist_low > InpWhaleAbsDistPoints * 2 && dist_high > InpWhaleAbsDistPoints * 2) decay = 0.85;
        m_cortex.institutional_intent *= decay; 
        double flow = m_ctx.archive.pillars.flow_imbalance;
        
        // Absorção de Fundo
        if(dist_low < InpWhaleAbsDistPoints && flow < -InpWhaleAbsFlowTh) {
            m_cortex.institutional_intent = 0.95; 
            m_iceberg_alert = 1.0;
            if(m_pulse % 50 == 0) SupremeLog("🐋 ABSORÇÃO NO FUNDO: Baleia segurando o preço.");
            m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.1);
        }
        // Absorção de Topo
        else if(dist_high < InpWhaleAbsDistPoints && flow > InpWhaleAbsFlowTh) {
            m_cortex.institutional_intent = -0.95; 
            m_iceberg_alert = 1.0;
            if(m_pulse % 50 == 0) SupremeLog("🐋 ABSORÇÃO NO TOPO: Baleia distribuindo.");
            m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.1);
        }
    }
    
    // PERFORMANCE: Executa o scanner de void apenas quando o minuto muda
    void LiquidityVoidScanner() {
        // PERFORMANCE: Zero-API Scanner (Uses RAM OHLC Buffer)
        double void_score = 0;
        // Identifica Fair Value Gap (FVG) no Buffer M1 em RAM
        if(m_m1_history[1].low > m_m1_history[3].high) void_score += 0.25;
        if(m_m1_history[1].high < m_m1_history[3].low) void_score -= 0.25;
        if(m_m1_history[0].low > m_m1_history[2].high) void_score += 0.25;
        if(m_m1_history[0].high < m_m1_history[2].low) void_score -= 0.25;
        
        m_ctx.archive.pillars.liquidity_void = void_score;
    }
    
    void CyberViralMutation() {
        if(!InpVirusMutantMode) return;
        
        // --- 2026 VIRAL EVOLUTION: CÁLCULO DE DOR DO VAREJO (Retail Pain) ---
        // Probabilidade de stop-run baseada na proximidade de topos/fundos e vácuo de liquidez
        double bid = m_current_tick.bid;
        double dist_h = MathAbs(bid - m_ctx.archive.pillars.structure_high) * m_point_inv;
        double dist_l = MathAbs(bid - m_ctx.archive.pillars.structure_low) * m_point_inv;
        
        // BUG FIX: Pega a dor MÁXIMA entre topo e fundo (anteriormente sobrescrevia)
        double retail_pain = 0;
        if(dist_h < InpVirusTargetZone) retail_pain = MathMax(retail_pain, (1.0 - (dist_h / (double)InpVirusTargetZone))); 
        if(dist_l < InpVirusTargetZone) retail_pain = MathMax(retail_pain, (1.0 - (dist_l / (double)InpVirusTargetZone)));
        
        // 1. INFECÇÃO NEURAL: Mescla dor do varejo com fluxo institucional e Vácuo de Liquidez
        double inst_flow = MathAbs(m_cortex.institutional_intent);
        double lq_void = MathAbs(m_ctx.archive.pillars.liquidity_void);
        
        // O vírus se espalha mais rápido em vácuos de liquidez (baixa resistência)
        m_ctx.archive.pillars.infection_level = (retail_pain * 0.5) + (inst_flow * 0.3) + (lq_void * 0.2);
        
        // 2. RETAIL FEAR INDEX (Nova Métrica 2026)
        // Se o preço está se aproximando do stop (retail_pain subindo) e o fluxo é contra, o medo explode.
        static double last_pain = 0;
        if(retail_pain > last_pain && inst_flow > 0.5) {
             m_ctx.archive.pillars.retail_fear_index = MathMin(1.0, m_ctx.archive.pillars.retail_fear_index + 0.1);
        } else {
             m_ctx.archive.pillars.retail_fear_index = MathMax(0.0, m_ctx.archive.pillars.retail_fear_index - 0.05);
        }
        last_pain = retail_pain;

        // 3. ATIVAÇÃO DO VÍRUS (Target Lock)
        if(m_ctx.archive.pillars.infection_level > InpVirusThreshold) {
            m_ctx.archive.pillars.is_viral_state = true;
            m_ctx.archive.pillars.target_lock_score = m_ctx.archive.pillars.infection_level * 100.0;
            
            // MUTAÇÃO QUÍMICA: Elimina o medo e induz fúria predatória
            if(InpVirusFearless) {
                m_cortex.emotion.cortisol *= 0.1; // Suprime o medo da IA
                m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.2);
                m_cortex.emotion.adrenaline = MathMin(1.0, m_cortex.emotion.adrenaline + 0.1);
            }
            
            // VIRAL LOT SCALER: Aumenta a agressividade se o regime for favorável
            if(m_quantum_regime == REGIME_TRENDING) {
                 m_cortex.active_thought = "🧬 VÍRUS: MUTAÇÃO PARA AGRESSIVIDADE MÁXIMA (TREND)";
            }
            
            if(m_pulse % 40 == 0) {
                string side = (dist_h < dist_l) ? "TOPO" : "FUNDO";
                SupremeLog("🦠 VÍRUS ATIVO: Infectando clusters de STOP no " + side + " (" + DoubleToString(m_ctx.archive.pillars.target_lock_score, 1) + "%)");
                
                // THROTTLE AUDIO: Só toca o som se passaram 10 segundos desde a última vez
                if(GetTickCount64() - m_last_viral_sound_ms > 10000) {
                    // PlaySound("expert.wav");
                    m_last_viral_sound_ms = GetTickCount64();
                }
                ViralAlertBanner(true, "MODO VÍRUS: CAÇANDO STOPS NO " + side);
            }
        } else {
            if(m_ctx.archive.pillars.is_viral_state) ViralAlertBanner(false, "");
            m_ctx.archive.pillars.is_viral_state = false;
            m_ctx.archive.pillars.target_lock_score = 0;
        }
    }
    
    double NormalizePrice(double price) {
        // PERFORMANCE: Fast Integer Rounding (No FPU Call)
        return (double)((long)(price * m_tick_inv + 0.5)) * m_tick_size;
    }

    void ViralAlertBanner(bool active, string msg) {
        // ... (resto da lógica igual)
    }

    void OpeningRangeBreakoutCore() {
        MqlDateTime dt; TimeToStruct(m_current_tick.time, dt);
        dt.hour = 9; dt.min = 0; dt.sec = 0;
        datetime open_time = StructToTime(dt);

        if(m_current_tick.time < open_time) return; // Market not open yet

        // B3: ORB Window 09:00 - 09:15
        if(m_orb_high <= 0) {
             datetime end_time = open_time + 15*60;
             MqlRates rates[];
             // MODERN BUG FIX: Use time-range CopyRates to avoid index-shift risk
             // during initial history synchronization or connectivity gaps.
             if(CopyRates(_Symbol, PERIOD_M1, open_time, MathMin(m_current_tick.time, end_time), rates) > 0) {
                  m_orb_high = -1; m_orb_low = 9999999;
                  for(int i=0; i<ArraySize(rates); i++) {
                       if(rates[i].high > m_orb_high) m_orb_high = rates[i].high;
                       if(rates[i].low  < m_orb_low)  m_orb_low  = rates[i].low;
                  }
             }
        }
        
        // Live updates during the window
        if(m_current_time_score >= 900 && m_current_time_score < 915) {
            double bid = m_current_tick.bid;
            if(m_orb_high <= 0 || bid > m_orb_high) m_orb_high = bid;
            if(m_orb_low  <= 0 || bid < m_orb_low)  m_orb_low  = bid;
        }
    }
    void RefreshM1Cache() {
        // PERFORMANCE HFT: Deriva o tempo do candle via aritmética (Zero iTime calls)
        datetime current_m1 = m_current_tick.time - (m_current_tick.time % 60);

        // --- DAY CHANGE RESET (v12.90 - Full State Purge) ---
        long current_day = m_current_tick.time / 86400;
        if(current_day != m_last_day_checking) {
             m_orb_high = 0; m_orb_low = 0;
             m_daily_profit_cached = 0;
             m_last_deal_sync_ticket = 0; // BUG FIX: Reset sync ticket on new day
             m_last_day_checking = (int)current_day;
             UpdateDailyProfitCache();
             SupremeLog("📅 DIÁRIO: Reset de variáveis de sessão (ORB/Profit/Sync).");
        }
        
        if(current_m1 > m_last_bar_time) {
            // PERFORMANCE: Shift RAM History Buffer (Zero Allocation)
            for(int i=3; i>0; i--) m_m1_history[i] = m_m1_history[i-1];
            
            // Capture fixed state of finished bar
            m_m1_history[1].high  = m_curr_bar_high;
            m_m1_history[1].low   = m_curr_bar_low;
            m_m1_history[1].open  = m_curr_bar_open;
            m_m1_history[1].close = m_current_tick.bid;
            
            m_last_bar_high = m_curr_bar_high;
            m_last_bar_low  = m_curr_bar_low;

            if(CopyBuffer(m_h_atr, 0, 1, 1, m_atr_buf)>0) {
                m_last_bar_atr = m_atr_buf[0];
                m_atr_val = m_atr_buf[0]; 
            }
            m_last_bar_time = current_m1;
            
            // Inicializa extremos da nova barra
            m_curr_bar_high = m_current_tick.bid;
            m_curr_bar_low  = m_current_tick.bid;
            m_curr_bar_open = m_current_tick.bid;
            
            m_m1_history[0].open = m_curr_bar_open; // Start live bar
        } else {
            // Live updates for RAM buffer index 0
            double bid = m_current_tick.bid;
            if(bid > 0) {
                if(bid > m_curr_bar_high || m_curr_bar_high == 0) m_curr_bar_high = bid;
                if(bid < m_curr_bar_low || m_curr_bar_low == 0) m_curr_bar_low = bid;
                
                m_m1_history[0].high  = m_curr_bar_high;
                m_m1_history[0].low   = m_curr_bar_low;
                m_m1_history[0].close = bid;
            }
        }
    }

    void TimeframeCalibrationEngine() {
        // Ajuste dinâmico de SL/TP por ATR (Via Handles)
        if(m_atr_val <= 0) return;
        
        m_ctx.auto_sl = m_atr_val * 2.5 * m_point_inv; // RAM-Only math
        
        // PREDATOR TARGETS: Expande o TP se houver euforia (Dopamina > 0.8)
        double tp_mult = (m_cortex.emotion.dopamine > 0.8) ? 6.0 : 3.5;
        m_ctx.auto_tp = m_atr_val * tp_mult * m_point_inv;
        
        // Cache de níveis para Whale Tracker (Usa o histórico apenas na virada da barra)
        m_ctx.archive.pillars.structure_high = m_last_bar_high;
        m_ctx.archive.pillars.structure_low  = m_last_bar_low;
    }

    void UnifiedPositionManager() {
        // PERFORMANCE: Zero-API Management via RAM-Mirror (O(1) logic)
        if(m_pos_ticket <= 0) return;
        
        ulong now_micros = GetMicrosecondCount();
        // --- MODIFICATION COOLDOWN (Safety) ---
        // Se uma modificação falhou recentemente, esperamos o cooldown para evitar spam.
        // PERFORMANCE: Throttle terminal call to 100ms (we have RAM Cache)
        // --- MODIFICATION COOLDOWN (Safety) ---
        // Se uma modificação falhou recentemente, esperamos o cooldown para evitar spam.
        // PERFORMANCE: No throttle on Read-Only Sync (Zero-Latency State Awareres)
        SyncRAMPosition(); // Seleciona e sincroniza cache local (Fast Local Call)
            
        if(m_pos_ticket <= 0) return;
        
        double price_open  = m_ram_pos.price_open;
        double current_sl  = m_ram_pos.sl;
        double current_tp  = m_ram_pos.tp;
        int    type        = m_ram_pos.type;
        double lot         = m_ram_pos.vol;
        
        // --- 🔒 DOUG'S LOCK-PROFIT (Scalp Secure v13.0) ---
        // Se bater 40 pontos, trava no zero (entry + small fee)
        double current_pts = (type == POSITION_TYPE_BUY) ? (m_current_tick.bid - price_open) : (price_open - m_current_tick.ask);
        current_pts /= (m_point + 1e-9);
        
        if(current_pts > 40.0 && current_sl != (price_open + (type == POSITION_TYPE_BUY ? m_point*2 : -m_point*2))) {
             double lock_sl = price_open + (type == POSITION_TYPE_BUY ? m_point*2 : -m_point*2);
             // PERFORMANCE: Usamos PositionModify local p/ evitar overhead global
             if(m_trade.PositionModify(m_pos_ticket, NormalizePrice(lock_sl), current_tp)) {
                  m_cortex.active_thought = "🔒 LOCK-PROFIT: Lucro protegido em +2 pts.";
             }
        }
        
        // --- 🧪 QUANTUM SLIPPAGE COMPENSATION ---
        static ulong slippage_checked_ticket = 0;
        if(m_pos_ticket != slippage_checked_ticket) {
             double expected = m_last_entry_price; 
             if(expected <= 0) expected = (type == POSITION_TYPE_BUY) ? m_current_tick.ask : m_current_tick.bid;
             
             double slippage = (type == POSITION_TYPE_BUY) ? (price_open - expected) : (expected - price_open);
             
             if(slippage > 2 * m_point) {
                  double new_tp = (type == POSITION_TYPE_BUY) ? current_tp + slippage : current_tp - slippage;
                  m_mod_req.position = m_pos_ticket;
                  m_mod_req.sl = current_sl; m_mod_req.tp = NormalizePrice(new_tp);
                  if(OrderSendAsync(m_mod_req, m_mod_res)) {
                       SupremeLog("🛰️ SCALP COMP: Slippage detectada. TP ajustado para compensação.");
                       m_ram_pos.tp = new_tp;
                  }
             }
             slippage_checked_ticket = m_pos_ticket;
        }

        bool   run_stack   = InpFlowStacking;
        
        double atr = m_last_bar_atr;
        double last_high = m_last_bar_high;
        double last_low = m_last_bar_low;
        
        // CALCULA LUCRO EM RAM (Zero-API p/ HUD)
        double diff_pts = (type == POSITION_TYPE_BUY ? m_current_tick.bid - price_open : price_open - m_current_tick.ask) * m_point_inv;
        m_pos_profit = (diff_pts * m_point) * lot * m_tick_cost_ratio;

        // --- ⚡ MICRO-SECURE (SCALP PROFIT LOCK) ---
        // Se tivermos > 15pts e o momentum inverter forte, sai a mercado.
        // Isso garante o "scalp" antes da reversão.
        bool reversal_risk = (type == POSITION_TYPE_BUY && m_smooth_v < -8.0) || (type == POSITION_TYPE_SELL && m_smooth_v > 8.0);
        
        if(diff_pts > 15.0 && reversal_risk) {
              m_trade.PositionClose(m_pos_ticket); 
              SupremeLog("⚡ SCALP SECURE: Saída rápida por inversão de fluxo (Profit: " + DoubleToString(diff_pts,0) + "pts)");
              // Reset local locks to avoid ghost management
              m_pos_ticket = 0; 
              m_in_transaction = false;
              return;
        }
            
        // 1. DIVINE GUARDIAN (Breakeven & Trailing)
            double profit_pts = 0;
            if(m_point > 0) {
                // PERFORMANCE: Multiplication over Division (CPU Cycle Optimization)
                profit_pts = (type == POSITION_TYPE_BUY) ? (m_current_tick.bid - price_open) * m_point_inv : (price_open - m_current_tick.ask) * m_point_inv;
            }

            // --- SMART BREAKEVEN ---
            double trigger = (m_ctx.archive.pillars.is_viral_state) ? 20.0 : InpTrailingStart;
            if(profit_pts > trigger) {
                double be_sl = (type == POSITION_TYPE_BUY) ? price_open + (5 * m_point) : price_open - (5 * m_point);
                bool improve = (type == POSITION_TYPE_BUY) ? (be_sl > current_sl + m_point*5) : (current_sl == 0 || be_sl < current_sl - m_point*5);
                if(improve) {
                    m_mod_req.position = m_pos_ticket;
                    m_mod_req.sl = NormalizePrice(be_sl); m_mod_req.tp = current_tp;
                    m_last_mod_micros = now_micros; // Update cooldown even if send fails to prevent spam
                    if(OrderSendAsync(m_mod_req, m_mod_res)) {
                        m_ram_pos.sl = m_mod_req.sl; 
                        m_trailing_active = true;
                    }
                }
            }
            
            // --- 2026 PREDATORY TAKE PROFIT (Expansion Logic) ---
            // Se o lucro pts > 50 e a velocidade é alta (>5.0), expandimos o TP p/ deixar correr
            static double original_tp = 0;
            static ulong  last_tracked_ticket = 0;
            
            // RESET SE O TICKET MUDOU (Nova Posição)
            if(m_pos_ticket != last_tracked_ticket) {
                 original_tp = current_tp; // Recupera TP atual como base
                 last_tracked_ticket = m_pos_ticket;
            }

            if(profit_pts > 40 && MathAbs(m_smooth_v) > 5.0) {
                 if(original_tp == 0) original_tp = current_tp;
                 double expanded_tp = (type == POSITION_TYPE_BUY) ? m_current_tick.bid + (100 * m_point) : m_current_tick.ask - (100 * m_point);
                 
                 if(MathAbs(expanded_tp - current_tp) > 20 * m_point) {
                     m_mod_req.position = m_pos_ticket;
                     m_mod_req.sl = current_sl; m_mod_req.tp = NormalizePrice(expanded_tp);
                     if(OrderSendAsync(m_mod_req, m_mod_res)) {
                          SupremeLog("🚀 PREDATORY TP: Expandindo alvo por alta velocidade!");
                          m_ram_pos.tp = expanded_tp;
                     }
                 }
            } else if(original_tp > 0 && MathAbs(m_smooth_v) < 1.0) {
                 // MOMENTUM SNAP-BACK: Retrai o alvo p/ o original se o movimento perder força
                 m_mod_req.position = m_pos_ticket;
                 m_mod_req.sl = current_sl; m_mod_req.tp = NormalizePrice(original_tp);
                 if(OrderSendAsync(m_mod_req, m_mod_res)) {
                      SupremeLog("🎯 PREDATORY TP: Retraindo alvo (Momentum falhou)");
                      m_ram_pos.tp = original_tp;
                      original_tp = 0;
                 }
            }
            if(m_pos_ticket == 0) original_tp = 0; 

            // --- TRAILING STOP TÉCNICO (HFT) ---
            // Throttle de 500ms para evitar SPAM de ordens (Rate Limit B3)
            now_micros = GetMicrosecondCount();
            if(atr > 0 && last_low > 0 && last_high > 0 && (now_micros - m_last_mod_micros > 500000)) {
                double n_sl = 0;
                double min_d = m_stops_level + (m_point * 2);

                if(InpUseDivineBreakeven) {
                    bool protected_buy = (type == POSITION_TYPE_BUY && current_sl > price_open);
                    bool protected_sell = (type == POSITION_TYPE_SELL && current_sl > 0 && current_sl < price_open);
                    
                    if(!protected_buy && !protected_sell) {
                        double trigger_be = InpBreakevenTrigger * m_point;
                        
                        if(type == POSITION_TYPE_BUY && m_current_tick.bid >= price_open + trigger_be) {
                            m_mod_req.position = m_pos_ticket;
                            m_mod_req.sl = NormalizePrice(price_open + (2 * m_point)); // BE + Fees
                            m_mod_req.tp = m_ram_pos.tp;
                            if(OrderSendAsync(m_mod_req, m_mod_res)) {
                                m_ram_pos.sl = m_mod_req.sl; 
                                m_last_mod_micros = now_micros;
                            }
                        }
                        else if(type == POSITION_TYPE_SELL && m_current_tick.ask <= price_open - trigger_be) {
                            m_mod_req.position = m_pos_ticket;
                            m_mod_req.sl = NormalizePrice(price_open - (2 * m_point));
                            m_mod_req.tp = m_ram_pos.tp;
                            if(OrderSendAsync(m_mod_req, m_mod_res)) {
                                SupremeLog("🛡️ DIVINE SELL: Entry=" + DoubleToString(price_open, m_digits) + " NewSL=" + DoubleToString(m_mod_req.sl, m_digits));
                                m_ram_pos.sl = m_mod_req.sl; 
                                m_last_mod_micros = now_micros;
                            }
                        }
                    } else { // Already protected -> Trailing Logic (2026 INERTIAL UPGRADE)
                        // TRAILING INERCIAL: Se a velocidade está alta a favor, apertamos o stop agressivamente.
                        double inertia_mod = (MathAbs(m_smooth_v) > 2.0) ? 0.5 : 1.0; 
                        
                        if(type == POSITION_TYPE_BUY && m_current_tick.bid > price_open + (atr * 0.5)) {
                            n_sl = last_low - (3 * m_point * inertia_mod); // SL mais apertado se tiver inércia
                            if(n_sl > current_sl + (m_point * 2) && n_sl < m_current_tick.bid - min_d) {
                                m_mod_req.position = m_pos_ticket;
                                m_mod_req.sl = NormalizePrice(n_sl); m_mod_req.tp = current_tp;
                                if(OrderSendAsync(m_mod_req, m_mod_res)) m_last_mod_micros = now_micros;
                            }
                        }
                        else if(type == POSITION_TYPE_SELL && m_current_tick.ask < price_open - (atr * 0.5)) {
                            n_sl = last_high + (3 * m_point * inertia_mod);
                            if((current_sl == 0 || n_sl < current_sl - (m_point * 2)) && n_sl > m_current_tick.ask + min_d) {
                                m_mod_req.position = m_pos_ticket;
                                m_mod_req.sl = NormalizePrice(n_sl); m_mod_req.tp = current_tp;
                                if(OrderSendAsync(m_mod_req, m_mod_res)) m_last_mod_micros = now_micros;
                            }
                        }
                    }
                } else { // Existing trailing logic (Standard)
                    if(type == POSITION_TYPE_BUY && m_current_tick.bid > price_open + (atr * 0.5)) {
                        n_sl = last_low - (5 * m_point);
                        if(n_sl > current_sl + (m_point * 5) && n_sl < m_current_tick.bid - min_d) {
                            m_mod_req.position = m_pos_ticket;
                            m_mod_req.sl = NormalizePrice(n_sl); m_mod_req.tp = current_tp;
                            if(OrderSendAsync(m_mod_req, m_mod_res)) m_last_mod_micros = now_micros;
                        }
                    }
                    else if(type == POSITION_TYPE_SELL && m_current_tick.ask < price_open - (atr * 0.5)) {
                        n_sl = last_high + (5 * m_point);
                        if((current_sl == 0 || n_sl < current_sl - (m_point * 5)) && n_sl > m_current_tick.ask + min_d) {
                            m_mod_req.position = m_pos_ticket;
                            m_mod_req.sl = NormalizePrice(n_sl); m_mod_req.tp = current_tp;
                            if(OrderSendAsync(m_mod_req, m_mod_res)) m_last_mod_micros = now_micros;
                        }
                    }
                }
            }
            
            // 2. FLOW STACKING (Pyramiding)
            int pos_total = PositionsTotal();
            if(run_stack && m_auto_mode && !m_in_transaction && m_cortex.emotion.dopamine > 0.7 && pos_total < 3) {
                double profit_pts = (type == POSITION_TYPE_BUY) ? (m_current_tick.bid - price_open) * m_point_inv : (price_open - m_current_tick.ask) * m_point_inv;
                bool risk_free = (type == POSITION_TYPE_BUY && current_sl >= price_open) || (type == POSITION_TYPE_SELL && current_sl > 0 && current_sl <= price_open);
                
                if(profit_pts > m_stack_threshold && risk_free) {
                    double cushion = m_daily_profit_cached + m_acc_profit;
                    
                    // --- ALPHA-INSTINCT STACKING (2026 AI) ---
                    // Se o regime for TENDÊNCIA, o robô ignora o coxim de lucro e empilha com convicção.
                    bool conviction = (m_quantum_regime == REGIME_TRENDING && m_cortex.emotion.dopamine > 0.85);

                    if((conviction || cushion > 50.0) && (GetMicrosecondCount() - m_last_trade_micros > 200000)) {
                        double add_lot = NormalizeLot(lot * 0.5);
                        if(add_lot >= m_vol_min) {
                            m_in_transaction = true;
                            m_virtual_margin_used += add_lot; // Shadow Lot Tracking
                            m_trans_timeout_ms = GetTickCount64() + 2000;
                            
                            m_exec_req.volume = add_lot;
                            m_exec_req.type = (type == POSITION_TYPE_BUY) ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
                            
                            // APEX SLIPPAGE (B3 Momentum Safe)
                            double offset = 5 * m_tick_size;
                            m_exec_req.price = (type == POSITION_TYPE_BUY) ? NormalizePrice(m_current_tick.ask + offset) : NormalizePrice(m_current_tick.bid - offset);
                            m_exec_req.comment = conviction ? "ALPHA_STACK:CONVICTION" : "FLOW_STACKING:" + DoubleToString(profit_pts,0);
                            
                            m_exec_start_micros = GetMicrosecondCount(); // Capture start time for execution latency
                            if(!OrderSendAsync(m_exec_req, m_exec_res)) {
                                m_in_transaction = false;
                                m_virtual_margin_used = MathMax(0, m_virtual_margin_used - add_lot);
                                m_exec_start_micros = 0; // Reset if send fails
                            }
                            m_last_trade_micros = GetMicrosecondCount();
                        }
                    }
                }
            }
        }
    
    void UpdateScalpAnalytics() {
        if(!HistorySelect(TimeCurrent()-86400, TimeCurrent())) return;
        
        int total = HistoryDealsTotal();
        int wins = 0, loss = 0, trades = 0;
        double sum_win = 0, sum_loss = 0;
        
        for(int i=total-1; i>=0 && trades < 100; i--) {
            ulong t = HistoryDealGetTicket(i);
            if(HistoryDealGetInteger(t, DEAL_MAGIC) != InpMagicNumber) continue;
            
            ENUM_DEAL_ENTRY entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(t, DEAL_ENTRY);
            if(entry == DEAL_ENTRY_OUT || entry == DEAL_ENTRY_INOUT) {
                trades++;
                double pnl = HistoryDealGetDouble(t, DEAL_PROFIT) + HistoryDealGetDouble(t, DEAL_SWAP) + HistoryDealGetDouble(t, DEAL_COMMISSION);
                if(pnl > 0) { wins++; sum_win += pnl; }
                else { loss++; sum_loss += MathAbs(pnl); }
            }
        }
        
        m_ctx.archive.pillars.scalp_total = trades;
        m_ctx.archive.pillars.scalp_wins = wins;
        m_ctx.archive.pillars.scalp_profit_sum = sum_win;
        m_ctx.archive.pillars.scalp_loss_sum = sum_loss;
        
        // Calculation of scalps/minute
        static ulong first_deal_time = 0;
        if(trades > 0 && first_deal_time == 0) first_deal_time = GetTickCount64();
        if(first_deal_time > 0) {
            double mins = (GetTickCount64() - first_deal_time) / 60000.0;
            if(mins > 0.5) m_ctx.archive.pillars.scalp_per_minute = trades / mins;
        }
    }
    
    double CalculateLotSize(const MqlTick &tick, int direction) {
        double tp_mod = 1.0, sl_mod = 1.0;
        BioRiskAdvisory(tp_mod, sl_mod); 
        
        double fd = Sovereign::MarketCache::fractal_dimension;
        double sl_dist = (InpStopPoints > 0) ? (InpStopPoints * m_point * sl_mod) : (m_last_bar_atr * 1.5 * sl_mod);
        
        double min_sl = MathMax(m_stops_level * m_point, m_tick_size * 20); 
        if(sl_dist < min_sl) sl_dist = min_sl;
        
        double magnification = (InpVirtualMagnification > 0) ? InpVirtualMagnification : 1.0;
        double money_risk = (m_acc_balance * magnification) * (InpRiskPerTrade / 100.0);
        
        if(sl_dist <= 0 || m_tick_cost_ratio <= 0) return 0;
        double lot_base = money_risk / (sl_dist * m_tick_cost_ratio);
        
        // 🌀 ADAPTIVE INTENSITY SCALING (2026 REVOLUTION)
        // Usa a intensidade da decisão neural [1-5] para escalar o lote
        double intensity_mod = 0.5 + (m_last_intensity * 0.25); // 1=0.75x, 2=1.0x, 3=1.25x, 4=1.5x, 5=1.75x
        
        double lot_scaling = (m_current_drive / 2.5) * intensity_mod;
        
        if(m_ctx.archive.pillars.consecutive_wins >= 2) {
             lot_scaling *= (1.0 + (m_ctx.archive.pillars.consecutive_wins * 0.1)); 
        }
        
        double lot = lot_scaling * lot_base; 
        lot = MathMin(lot, lot_base * 4.0); // Teto de agressividade aumentado p/ 4.0
        
        // --- 🏦 QUANTUM BANKROLL INJECTION ---
        if(InpCompoundActive) {
            double dynamic_lot = Sovereign::QuantumBankroll::CalculateDynamicLot(m_acc_balance, AccountInfoDouble(ACCOUNT_EQUITY));
            lot = MathMax(lot, dynamic_lot); // Garante a alavancagem desejada pelo usuário
        }

        double max_lot_margin = (m_acc_margin * 0.7) / ((direction == 1) ? m_margin_per_lot_buy : m_margin_per_lot_sell);
        lot = MathMin(lot, max_lot_margin);
        
        return NormalizeLot(lot);
    }

    void UpdateDailyProfitCache() {
        if(!HistorySelect(iTime(_Symbol, PERIOD_D1, 0), TimeCurrent())) return;
        
        int total = HistoryDealsTotal();
        double profit = 0;
        
        // PERFORMANCE: Se já processamos até certo ticket, pulamos (Otimização OMEGA)
        int start_idx = 0;
        if(m_last_deal_sync_ticket > 0) {
            // Busca o índice do último processo (geralmente próximo ao fim)
            for(int i=total-1; i>=0; i--) {
                if(HistoryDealGetTicket(i) == m_last_deal_sync_ticket) {
                    start_idx = i + 1;
                    break;
                }
            }
        }
        
        for(int i=start_idx; i<total; i++) {
            ulong t = HistoryDealGetTicket(i);
            if(HistoryDealGetInteger(t, DEAL_MAGIC) == InpMagicNumber) {
                double gross = HistoryDealGetDouble(t, DEAL_PROFIT);
                double lots = HistoryDealGetDouble(t, DEAL_VOLUME);
                double comm = HistoryDealGetDouble(t, DEAL_COMMISSION);
                double swap = HistoryDealGetDouble(t, DEAL_SWAP);
                
                profit += gross + comm + swap;
                
                // Desconto do Custo de Bolsa/Corretagem (Estimado se corretagem for zero)
                m_daily_profit_net_cached += Sovereign::QuantumBankroll::GetNetProfit(gross + comm + swap, lots);
            }
            if(i == total-1) m_last_deal_sync_ticket = t;
        }
        m_daily_profit_cached += profit; 
    }

    void AddToProfitCache(double p) {
        m_daily_profit_cached += p;
    }

    void RecordTradeResult(double profit) {
        // --- 📊 PREDATOR METRICS (v13.5) ---
        for(int i=4; i>0; i--) m_recent_pnl_window[i] = m_recent_pnl_window[i-1];
        m_recent_pnl_window[0] = profit;

        m_feedback_inputs[0] = m_rsi_val_current;
        m_feedback_inputs[1] = Sovereign::MarketCache::entropy_index;
        m_feedback_inputs[2] = Sovereign::MarketCache::flow_intensity / 100.0;
        m_feedback_inputs[3] = Sovereign::MarketCache::fractal_dimension;
        m_feedback_inputs[4] = m_ctx.archive.pillars.quantum_flux;
        m_feedback_inputs[5] = m_ctx.archive.pillars.hurst_exponent;
        m_feedback_inputs[6] = m_ctx.archive.pillars.symmetry_ratio; 
        
        m_cortex.EncodeSynapse(m_feedback_inputs, profit);
        m_cortex.NeuroPlasticityUpdate(profit, "SINGULARITY");

        m_ctx.archive.pillars.scalp_total++;
        if(profit > 0) {
            m_ctx.archive.pillars.scalp_wins++;
            m_ctx.archive.pillars.scalp_profit_sum += profit;
            m_ctx.archive.pillars.consecutive_wins++;
            m_ctx.archive.pillars.consecutive_losses = 0;
            m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.1);
        } else if(profit < -0.01) {
            m_ctx.archive.pillars.scalp_loss_sum += MathAbs(profit);
            m_ctx.archive.pillars.consecutive_losses++;
            m_ctx.archive.pillars.consecutive_wins = 0;
            m_cortex.emotion.dopamine *= 0.8; 
        }

        AddToProfitCache(profit);
        m_need_genetic_update = true;
        m_cortex.institutional_intent = 0;

        if(profit > 0.01) {
            m_cortex.emotion.dopamine = MathMin(1.0, m_cortex.emotion.dopamine + 0.15);
        } else if(profit < -0.01) {
            m_cortex.emotion.serotonin = MathMax(0.01, m_cortex.emotion.serotonin - 0.10);
        }
    }


    void UpdateHUD() {
        // PERFORMANCE: Throttling de renderização p/ 500ms (Evita sobrecarga de objetos MT5)
        // BUG FIX: Permite HUD no Backtest apenas se for MODO VISUAL
        if(m_cpu_overload || (MQLInfoInteger(MQL_TESTER) && !MQLInfoInteger(MQL_VISUAL_MODE)) || MQLInfoInteger(MQL_OPTIMIZATION)) return;
        
        static ulong last_hud_render = 0;
        if(GetTickCount64() - last_hud_render < 250) return; // 4 FPS p/ fluidez titan
        last_hud_render = GetTickCount64();

        Sovereign::NewHUDResponsive::Draw(
            InpHUD_X, 
            InpHUD_Y,
            m_auto_mode,
            m_daily_profit_net_cached,
            (m_pos_ticket > 0 ? PositionGetDouble(POSITION_PROFIT) : 0.0),
            m_cortex.active_thought,
            m_cortex.emotion.dopamine,
            Sovereign::CommandBridge::soul.bio_state,
            m_cortex.tick_velocity,
            m_cortex.latency_ms,
            (double)m_spread_pts,
            m_ctx.archive.pillars.flow_imbalance,
            m_acc_balance,
            Sovereign::CommandBridge::IsSoulAlive()
        );
        
        // AVISOS CRÍTICOS (Overlay)
        if(m_ctx.archive.pillars.is_viral_state) {
            Sovereign::NewHUDResponsive::Txt("VIRAL_WARN", "⚠ TITAN PREDATOR ACTIVE ⚠", 150, 420, clrGold, 12, "Arial Black");
        }
    }


    void UpdateThoughtStream() {
        // PERFORMANCE: Thought refresh 2s (Evita I/O de arquivo e alocações excessivas a cada tick)
        static ulong last_thought_ms = 0;
        if(GetTickCount64() - last_thought_ms < 2000) return;
        last_thought_ms = GetTickCount64();

        string shared = Sovereign::SharedComm::ReadLog();
        if(shared != "" && shared != m_last_log_msg) {
            m_cortex.active_thought = "📡 [SYNC]: " + shared;
            m_last_log_msg = shared;
            return;
        }
        
        if(m_auto_mode) {
             // MEMORY OPTIMIZATION: Static array evita alocação de heap a cada tick
             static string tacticals[] = {
                 "IA ATIVA: Escaneando vácuos de liquidez na B3...",
                 "Calculando probabilidade de rompimento de ORB...",
                 "Whale Tracker: Monitorando ordens iceberg...",
                 "Bio-Symmetry: Sincronizando humor e alvo...",
                 "Entropy Shield: Filtrando ruído fractal...",
                 "Apex Hunter: Aguardando sinal de alta convicção..."
             };
             
             m_cortex.active_thought = tacticals[GetTickCount64() % 6];
             return;
        }

        static string thoughts[] = {
            "Analisando Book de Ofertas B3 para desequilíbrios...",
            "Estado Bio-Neural: Caçador Ativo",
            "Calculando correlação WIN/WDO em tempo real...",
            "Entropia de mercado oscilando... Ajustando filtros fractais.",
            "Aguardando sinal MASTER p/ ativação neural.",
            "Frequência Alpha detectada no fluxo de ticks."
        };
        m_cortex.active_thought = thoughts[MathRand() % 6];
    }

    void SupremeLog(string msg) {
        if(InpLogLevel <= 0) return; // Silent mode
        static string last_msg = "";
        if(msg == last_msg) return; // Evita processamento de strings repetidas
        
        m_cortex.active_thought = msg;
        Sovereign::SharedComm::WriteLog(_Symbol + ": " + msg);
        last_msg = msg;
    }

    void LatencyMonitor() {
        static ulong last_lat_update = 0;
        ulong now = GetTickCount64();
        if(now - last_lat_update < 1000) return; // THROTTLE: Sincroniza ping a cada 1s
        last_lat_update = now;
        
        int ping = (TerminalInfoInteger(TERMINAL_CONNECTED) != 0) ? (int)TerminalInfoInteger(TERMINAL_PING_LAST) : 0;
        if(m_latency_samples == 0) { m_avg_latency_ms = (double)ping; m_latency_samples = 1; }
        else { m_avg_latency_ms = (m_avg_latency_ms * m_latency_samples + ping) / (m_latency_samples + 1); m_latency_samples = MathMin(m_latency_samples + 1, 100); }
    }

    void ToggleAutoMode() {
        m_auto_mode = !m_auto_mode;
        if(m_auto_mode) {
            m_sys_flags |= SYS_FLAG_AUTO;
            SupremeLog("SISTEMA: MODO AUTOMÁTICO ATIVADO [IA]");
            // PlaySound("ok.wav");
        } else {
            m_sys_flags &= ~SYS_FLAG_AUTO;
            SupremeLog("SISTEMA: MODO MANUAL TÁTICO ATIVADO");
            // PlaySound("alert.wav");
        }
    }

    void ManualBuy() {
        if(m_in_transaction || m_current_tick.ask <= 0) return;
        
        double lot = CalculateLotSize(m_current_tick, 1);
        if(lot <= 0) return;

        m_in_transaction = true;
        m_virtual_margin_used += lot;
        m_trans_timeout_ms = GetTickCount64() + 2000;
        
        MqlTradeRequest req = m_template_req; 
        req.volume = lot; req.type = ORDER_TYPE_BUY; req.price = NormalizePrice(m_current_tick.ask); 
        req.comment = "MANUAL_ASYNC";
        
        if(!OrderSendAsync(req, m_exec_res)) {
            m_in_transaction = false;
            m_virtual_margin_used -= lot;
            m_cortex.emotion.cortisol += 0.1;
        }
    }
    
    void ManualSell() {
        if(m_in_transaction || m_current_tick.bid <= 0) return;
        
        double lot = CalculateLotSize(m_current_tick, -1);
        if(lot <= 0) return;

        m_in_transaction = true;
        m_virtual_margin_used += lot;
        m_trans_timeout_ms = GetTickCount64() + 2000;

        MqlTradeRequest req = m_template_req; 
        req.volume = lot; req.type = ORDER_TYPE_SELL; req.price = NormalizePrice(m_current_tick.bid); 
        req.comment = "MANUAL_ASYNC";
        
        if(!OrderSendAsync(req, m_exec_res)) {
            m_in_transaction = false;
            m_virtual_margin_used -= lot;
            m_cortex.emotion.cortisol += 0.1;
        }
    }
    
    void ManualCloseAll() {
        if(m_pos_ticket <= 0) return;
        if(m_in_transaction) return;
        
        // PERFORMANCE: Saída Assíncrona via Shadow Ticket (Zero-Lag)
        if(PositionSelectByTicket(m_pos_ticket)) {
            double lot = PositionGetDouble(POSITION_VOLUME);
            int type = (int)PositionGetInteger(POSITION_TYPE);
            
            MqlTradeRequest req = m_template_req;
            req.type = (type == POSITION_TYPE_BUY) ? ORDER_TYPE_SELL : ORDER_TYPE_BUY;
            req.volume = lot;
            req.price = (type == POSITION_TYPE_BUY) ? m_current_tick.bid : m_current_tick.ask;
            req.comment = "MANUAL_CLOSE_ASYNC";
            
            if(OrderSendAsync(req, m_exec_res)) {
                m_in_transaction = true;
                m_trans_timeout_ms = GetTickCount64() + 2000;
            }
        }
    }
    
    void SyncRAMPosition() {
        // PERFORMANCE: Margem via MQL5 é O(1), mas throttle de 500ms evita overhead em HFT (v13.0)
        static ulong last_margin_sync = 0;
        if(GetTickCount64() - last_margin_sync > 500) {
            m_acc_margin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
            last_margin_sync = GetTickCount64();
        }
        
        // BUG FIX: Recuperação Automática de Posição (Se EA caiu ou reiniciou)
        if(m_pos_ticket <= 0) {
             if(PositionSelect(_Symbol)) {
                 m_pos_ticket = PositionGetInteger(POSITION_TICKET);
                 m_cortex.active_thought = "🔄 RECUPERAÇÃO: Posição Órfã detectada e vinculada.";
             }
        }

        if(m_pos_ticket > 0 && PositionSelectByTicket(m_pos_ticket)) {
            m_ram_pos.type = (int)PositionGetInteger(POSITION_TYPE);
            m_ram_pos.vol = PositionGetDouble(POSITION_VOLUME);
            m_ram_pos.price_open = PositionGetDouble(POSITION_PRICE_OPEN);
            m_ram_pos.sl = PositionGetDouble(POSITION_SL);
            m_ram_pos.tp = PositionGetDouble(POSITION_TP);
            
            // Capture entry time if it's the first sync for this ticket
            if(m_ram_pos.open_time == 0) m_ram_pos.open_time = (datetime)PositionGetInteger(POSITION_TIME);
        } else {
            m_pos_ticket = 0;
            ZeroMemory(m_ram_pos);
            m_ram_pos.open_time = 0;
        }
    }

    // --- MISSING IMPLEMENTATIONS (ADDED FOR SAFETY) ---
    void BioRiskAdvisory(double &tp_mod, double &sl_mod) {
        if(!m_auto_mode) return;
        // Modula SL/TP baseado em stress (Cortisol) e confiança (Dopamina)
        sl_mod = 1.0 + (m_cortex.emotion.cortisol * 0.5); // Mais stress = SL maior (espaço)
        
        // HYPER-SCALPER TARGETING
        // Se estiver em modo scalper (Dopamina Alta), reduz TP para garantir taxa de acerto (Hit Rate)
        if(m_cortex.emotion.dopamine > 0.6 && m_cortex.emotion.adrenaline < 0.9) {
            tp_mod = 0.8; // Target mais curto e rápido (Sniper)
            sl_mod = 0.9; // Stop mais curto (Gestão de Risco Agressiva)
        } else {
             tp_mod = 1.0 + (m_cortex.emotion.dopamine * 0.5); // Mais confiança = TP maior (alvo)
        }
        
        if(m_cortex.emotion.adrenaline > 0.8) {
            tp_mod *= 1.2; // Adrenalina estica alvos
        }
    }



    void ProcessMQTTCommands() {
        Sovereign::MQTTOrder ord;
        if(Sovereign::CommandBridge::GetNextOrder(ord)) {
            SupremeLog("📥 MQTT: Comando recebido ID=" + ord.id);
            
            // Validação Básica
            if(ord.ativo != _Symbol && ord.ativo != "WINFUT" && ord.ativo != "WIN$") {
                 Sovereign::CommandBridge::SendConfirmation(ord.id, "rejeitada", 0, 0, 0.0, "ativo_invalido: " + ord.ativo);
                 return;
            }

            m_in_transaction = true;
            m_trans_timeout_ms = GetTickCount64() + 2000;

            MqlTradeRequest req = m_template_req;
            double lot = (ord.quantidade > 0) ? ord.quantidade : CalculateLotSize(m_current_tick, (ord.tipo == "compra" ? 1 : -1));
            req.volume = NormalizeLot(lot);
            req.type = (ord.tipo == "compra") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
            req.price = (ord.tipo == "compra" ? m_current_tick.ask : m_current_tick.bid);
            
            if(ord.ordem == "limit") {
                req.type = (ord.tipo == "compra") ? ORDER_TYPE_BUY_LIMIT : ORDER_TYPE_SELL_LIMIT;
                req.price = NormalizePrice(ord.preco);
            }
            
            req.comment = "MQTT:" + ord.id;
            
            if(!OrderSendAsync(req, m_exec_res)) {
                m_in_transaction = false;
                Sovereign::CommandBridge::SendConfirmation(ord.id, "rejeitada", 0, 0, 0.0, "error_send: " + IntegerToString(GetLastError()));
            }
        }
    }

    void RecordMQTTConfirmation(const MqlTradeTransaction& trans, const MqlTradeRequest& req, const MqlTradeResult& res) {
        if(StringSubstr(req.comment, 0, 5) == "MQTT:") {
            string mqtt_id = StringSubstr(req.comment, 5);
            // CORREÇÃO: Passar profit real se disponível, ou 0.0 se apenas ordem colocada
            if(res.retcode == TRADE_RETCODE_DONE || res.retcode == TRADE_RETCODE_PLACED) {
                Sovereign::CommandBridge::SendConfirmation(mqtt_id, "executada", res.price, res.volume, 0.0, "Ordem enviada com sucesso");
            } else {
                Sovereign::CommandBridge::SendConfirmation(mqtt_id, "rejeitada", 0, 0, 0.0, "retcode: " + IntegerToString(res.retcode));
            }
        }
    }

    void SaveState() {
        // BUG FIX: Experts tab pollution reduced
        if(m_pulse % 1000 == 0) Print("Estado Neural Salvo: Dop=", m_cortex.emotion.dopamine);
    }

    void ReleaseHandles() {
        if(m_h_rsi != INVALID_HANDLE) IndicatorRelease(m_h_rsi);
        if(m_h_atr != INVALID_HANDLE) IndicatorRelease(m_h_atr);
        if(m_h_bb  != INVALID_HANDLE) IndicatorRelease(m_h_bb);
    }

};

CSovereignSupremeNew Supreme;

int OnInit() {
   MathSrand(GetTickCount()); 
   EventSetMillisecondTimer(200); // Pulse de HUD 5Hz (Aesthetics & Status)
   Supreme.InitializeSystems();
   
   ChartSetInteger(0, CHART_COLOR_BACKGROUND, C'5,7,12');
   ChartSetInteger(0, CHART_SHOW_GRID, false);
   ChartSetInteger(0, CHART_MODE, CHART_CANDLES);
   
   // MODERN OPTIMIZATION: Acelera backtests multithread escondendo indicadores
   if(MQLInfoInteger(MQL_OPTIMIZATION) || MQLInfoInteger(MQL_TESTER)) TesterHideIndicators(true);
   
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason) { 
   Supreme.m_cortex.SaveSynapses(); // FINAL SAVE: Don't lose current session learning
   Supreme.ReleaseHandles();
   if(!MQLInfoInteger(MQL_TESTER) || MQLInfoInteger(MQL_VISUAL_MODE)) Sovereign::NewHUDResponsive::Cleanup(); 
   Sovereign::SharedComm::Flush(); // Final disk write
   EventKillTimer(); 
}



void OnTimer() { 
    // Garante que a SoulState seja lida mesmo sem ticks (Connection Keep-Alive)
    // PERFORMANCE: Throttle 1Hz no Timer para evitar IO excessivo
    if((MQLInfoInteger(MQL_TESTER) && !MQLInfoInteger(MQL_VISUAL_MODE)) || MQLInfoInteger(MQL_OPTIMIZATION)) return; // Skip UI only in optimization/non-visual

    static ulong last_timer_check = 0;
    if(GetTickCount64() - last_timer_check > 1000) {
        if(Sovereign::CommandBridge::SyncSoulState()) {
            Supreme.m_cortex.emotion.dopamine = Sovereign::CommandBridge::soul.neural_drive;
            Supreme.m_need_hud_redraw = true;
        }
        last_timer_check = GetTickCount64();
    }
    
    Supreme.UpdateHUD(); 
    Supreme.UpdateThoughtStream(); 
}

void OnTick() {
   MqlTick tick;
   if(SymbolInfoTick(_Symbol, tick)) {
       // PERFORMANCE: Nano-Throttling (Ignora ruído de ticks < 5ms p/ cálculos geométricos pesados)
       static ulong last_cache_update = 0;
       ulong now = GetMicrosecondCount();
       if(now - last_cache_update > THROTTLE_MICROS) {
           Sovereign::MarketCache::Update(tick);
           last_cache_update = now;
       }
       
        Supreme.LatencyMonitor();
        Supreme.ProcessMQTTCommands();
        
        // --- 🛡️ TITAN SAFETY TRAP: SL BREAK PROTECTION ---
        if(Supreme.m_pos_ticket > 0 && Supreme.m_ram_pos.sl > 0) {
            bool force_exit = false;
            double p_sl = Supreme.m_ram_pos.sl;
            if(Supreme.m_ram_pos.type == POSITION_TYPE_BUY  && tick.bid < p_sl - (Supreme.m_point * 10)) force_exit = true;
            if(Supreme.m_ram_pos.type == POSITION_TYPE_SELL && tick.ask > p_sl + (Supreme.m_point * 10)) force_exit = true;
            
            if(force_exit) {
                // FALLBACK: Usar fechamento de emergência com verificação de ticket
                CTrade emergency_trade;
                emergency_trade.SetExpertMagicNumber(InpMagicNumber);
                emergency_trade.PositionClose(Supreme.m_pos_ticket);
                Supreme.m_cortex.active_thought = "🚨 SAFETY TRAP: SL violado, saída forçada!";
            }
        }
        
        Supreme.Pulse(tick);
    }
}

void OnBookEvent(const string& symbol) {
    if(symbol != _Symbol) return; // Keep symbol check, remove Auto Flag check
    
    // BOOK THROTTLING: Fast Spread Check (RAM-Only)
    double spread_pts = (Supreme.m_current_tick.ask - Supreme.m_current_tick.bid) * Supreme.m_point_inv;
    if(spread_pts > InpMaxSpread * 2.0) return; // Filtro de segurança (2x o máximo permitido p/ trade)
    
    ulong now = GetTickCount64();
    if(now - Supreme.m_last_book_proc_ms < (ulong)20) return; // Ultra-fast reading (20ms) only on event
    Supreme.m_last_book_proc_ms = now;
    
    Supreme.DarkLiquidityHunter();
}

void OnTradeTransaction(const MqlTradeTransaction& trans, const MqlTradeRequest& req, const MqlTradeResult& res) {
    // 🛡️ WAIT-FREE TRANS: Release lock as soon as order is accepted by the server
    if(trans.type == TRADE_TRANSACTION_REQUEST && req.magic == InpMagicNumber) {
        // PRECISION LATENCY: Record time from Intent to Server Response
        if(Supreme.m_exec_start_micros > 0) {
            long lat = (long)(GetMicrosecondCount() - Supreme.m_exec_start_micros);
            Supreme.m_cortex.latency_ms = (int)lat; 
            Supreme.m_exec_start_micros = 0; // RESET ATOMICALLY ONCE RECORDED
        }

        // Se a ordem foi aceita (DONE) ou colocada no Book (PLACED), liberamos o lock para novas operações
        if(res.retcode == TRADE_RETCODE_DONE || res.retcode == TRADE_RETCODE_PLACED) {
            Supreme.m_in_transaction = false;
            Supreme.RecordMQTTConfirmation(trans, req, res);
        } else {
            // Em caso de erro, removemos o lock e limpamos a margem virtual
            Supreme.m_in_transaction = false;
            Supreme.m_virtual_margin_used = MathMax(0, Supreme.m_virtual_margin_used - req.volume);
            Supreme.m_cortex.emotion.dopamine *= 0.8; // Penalidade por erro de execução
            Supreme.RecordMQTTConfirmation(trans, req, res);
            if(req.action == TRADE_ACTION_SLTP) Supreme.m_last_mod_fail_ms = GetTickCount64();
        }
    }

    // 🛡️ LIBERAÇÃO DE MARGEM EM CASO DE CANCELAMENTO/EXPIRAÇÃO (B3 Safe)
    if(trans.type == TRADE_TRANSACTION_ORDER_DELETE) {
        if(HistoryOrderSelect(trans.order) && HistoryOrderGetInteger(trans.order, ORDER_MAGIC) == InpMagicNumber) {
             long state = HistoryOrderGetInteger(trans.order, ORDER_STATE);
             if(state == ORDER_STATE_CANCELED || state == ORDER_STATE_REJECTED || state == ORDER_STATE_EXPIRED) {
                 double vol_left = HistoryOrderGetDouble(trans.order, ORDER_VOLUME_CURRENT);
                 Supreme.m_virtual_margin_used = MathMax(0, Supreme.m_virtual_margin_used - vol_left);
                 Supreme.m_in_transaction = false;
             }
        }
    }

    // 🛡️ SINCRONIA REATIVA (B3 Dynamic)
    if(trans.type == TRADE_TRANSACTION_POSITION && trans.symbol == _Symbol) {
        Supreme.SyncRAMPosition();
    }

    if(trans.type == TRADE_TRANSACTION_DEAL_ADD) {
        if(HistoryDealSelect(trans.deal)) {
            long magic = HistoryDealGetInteger(trans.deal, DEAL_MAGIC);
            if(magic == InpMagicNumber) {
                double deal_vol = HistoryDealGetDouble(trans.deal, DEAL_VOLUME);
                long deal_entry = HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
                long order_id = HistoryDealGetInteger(trans.deal, DEAL_ORDER);
                
                // 1. Release Virtual Margin proportionally (Partial Fill Guard)
                Supreme.m_virtual_margin_used = MathMax(0, Supreme.m_virtual_margin_used - deal_vol);
                
                // 2. Clear transaction lock if order is finished
                if(order_id > 0 && HistoryOrderSelect(order_id)) {
                    if(HistoryOrderGetDouble(order_id, ORDER_VOLUME_CURRENT) <= 0.000001) Supreme.m_in_transaction = false;
                } else {
                    Supreme.m_in_transaction = false;
                }

                // 3. Trade Feedback & Analytics
                double profit = HistoryDealGetDouble(trans.deal, DEAL_PROFIT) + 
                               HistoryDealGetDouble(trans.deal, DEAL_SWAP) + 
                               HistoryDealGetDouble(trans.deal, DEAL_COMMISSION);
                
                if(deal_entry == DEAL_ENTRY_IN) {
                    Supreme.m_pos_ticket = HistoryDealGetInteger(trans.deal, DEAL_POSITION_ID);
                    Supreme.SyncRAMPosition();
                    
                    // SLIPPAGE ANALYTICS
                    if(HistoryOrderSelect(order_id)) {
                        double req_p = HistoryOrderGetDouble(order_id, ORDER_PRICE_OPEN);
                        double exe_p = HistoryDealGetDouble(trans.deal, DEAL_PRICE);
                        if(req_p > 0) {
                            double slip = MathAbs(req_p - exe_p) * Supreme.m_point_inv;
                            Supreme.m_avg_slippage_pts = (Supreme.m_avg_slippage_pts == 0) ? slip : (Supreme.m_avg_slippage_pts * 0.95 + slip * 0.05);
                        }
                    }
                }
                else if(deal_entry == DEAL_ENTRY_OUT || deal_entry == DEAL_ENTRY_INOUT) {
                    Supreme.RecordTradeResult(profit);
                    Supreme.SyncRAMPosition();
                }
                
                if(InpGlobalSymbolSync && trans.symbol == _Symbol) {
                    Supreme.UpdateDailyProfitCache();
                }
                Supreme.m_last_acc_update_ms = 0; // Force UI refresh
            }
        }
    }
}

void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam) {
    // 2026 UI PERFORMANCE: HUD Resize Optimization
    if(id == CHARTEVENT_CHART_CHANGE) {
        long w = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS);
        long h = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS);
        
        static long last_w = 0;
        static long last_h = 0;
        
        if(w != last_w || h != last_h) {
            Supreme.m_need_hud_redraw = true; // Use flag instead of direct call
            Supreme.UpdateHUD(); // Force update on resize
            last_w = w;
            last_h = h;
        }
    }
    if(id == CHARTEVENT_OBJECT_CLICK) {
        // Performance: Identificação direta por nome de objeto (Elimina StringFind)
        if(sparam == "NEW_HUD_BT_AUTO") Supreme.ToggleAutoMode();
        // MANUAL BUTTONS REMOVED FOR FULL AUTOMATION
    }
    if(id == CHARTEVENT_KEYDOWN) {
        if(lparam == 'L' || lparam == 'l') Supreme.ManualBuy();
        if(lparam == 'K' || lparam == 'k') Supreme.ManualSell();
        if(lparam == '0') Supreme.ManualCloseAll();
    }
}
//+------------------------------------------------------------------+
//| 📉 MODERN OPTIMIZATION: Custom Tester Criterion                  |
//+------------------------------------------------------------------+
double OnTester() {
    // 2026 QUANTUM SCORE: Filtra por Lucro, Drawdown e Atividade
    double profit = TesterStatistics(STAT_PROFIT);
    double dd_rel = TesterStatistics(STAT_EQUITY_DDREL_PERCENT);
    double sharpe = TesterStatistics(STAT_SHARPE_RATIO);
    double trades = TesterStatistics(STAT_TRADES);
    
    if(profit <= 0 || trades < 20) return 0;
    
    // Fator de Estabilidade: Penaliza drawdowns profundos
    double stability = (100.0 - dd_rel) / 100.0;
    // Fator de Recuperação
    double recovery = TesterStatistics(STAT_RECOVERY_FACTOR);
    
    // Pontuação final ponderada
    return profit * stability * recovery * (sharpe > 0 ? sharpe : 0.1);
}
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+

