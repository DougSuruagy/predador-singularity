//+------------------------------------------------------------------+
//|                                                CommandBridge.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|        MQTT COMMAND BRIDGE v2.0 - SOUL/BODY SYNC PROTOCOL        |
//+------------------------------------------------------------------+
#ifndef SOVEREIGN_COMMAND_BRIDGE_MQH
#define SOVEREIGN_COMMAND_BRIDGE_MQH

#include "SharedComm.mqh"
#include <Trade\Trade.mqh>

namespace Sovereign {
    // ================================================================
    // ESTRUTURA DE ORDEM MQTT (Recebida da Alma Python)
    // ================================================================
    struct MQTTOrder {
        string tipo;         // compra/venda
        string ativo;        // WINFUT, etc
        double quantidade;
        double preco;
        string ordem;        // market/limit
        string id;           // unique id
        string timeInForce;  // GTC/IOC
        int    sl_pts;       // Stop Loss em pontos
        int    tp_pts;       // Take Profit em pontos
        double signal_strength; // Força do sinal (0-1)
        string session_id;   // ID da sessão Python
    };
    
    // ================================================================
    // ESTADO DA ALMA (Recebido do Python)
    // ================================================================
    struct SoulState {
        string session_id;
        string version;
        double capital;
        double daily_pnl;
        string bio_state;
        double neural_drive;
        string market_regime;
        bool   is_hunting;
    };

    // ================================================================
    // PONTE DE COMUNICAÇÃO ALMA <-> CORPO
    // ================================================================
    class CommandBridge {
    private:
        static string    m_in_file;
        static string    m_out_file;
        static string    m_soul_state_file;
        static string    m_body_state_file;
        static datetime  m_last_soul_sync;
        static ulong      m_last_io_flush_ms;
        static double    m_last_transmitted_price;
        
    public:
        static SoulState soul;  // Estado atual da alma
        
        // ------------------------------------------------------------
        // RECEBE ORDEM DA ALMA PYTHON
        // ------------------------------------------------------------
        static bool GetNextOrder(MQTTOrder &ord) {
            // Leitura BINÁRIA para evitar problemas de encoding (UTF-8 vs ANSI vs UTF-16)
            int h = FileOpen(CommandBridge::m_in_file, FILE_READ|FILE_BIN|FILE_SHARE_READ|FILE_COMMON);
            if(h == INVALID_HANDLE) return false;
            
            // Check Modify Time (Ignorado no Backtest pois o tempo simulado é diferente do tempo real do arquivo)
            if(!MQLInfoInteger(MQL_TESTER)) {
                datetime mod_time = (datetime)FileGetInteger(h, FILE_MODIFY_DATE);
                if(TimeTradeServer() - mod_time > 30) {
                    FileClose(h);
                    FileDelete(m_in_file, FILE_COMMON);
                    return false;
                }
            }
            
            // Lê todo o conteúdo como array de bytes e converte 'na marra' de UTF-8 para String
            ulong size = FileSize(h);
            if(size == 0) { FileClose(h); return false; }
            
            uchar data[];
            ArrayResize(data, (int)size);
            FileReadArray(h, data);
            FileClose(h);
            FileDelete(m_in_file, FILE_COMMON);
            
            string json = CharArrayToString(data, 0, WHOLE_ARRAY, CP_UTF8);
            if(json == "") return false;
            
            return ParseOrderJSON(json, ord);
        }
        
        // ------------------------------------------------------------
        // ENVIA CONFIRMAÇÃO PARA A ALMA PYTHON
        // ------------------------------------------------------------
        static void SendConfirmation(string id, string status, double p_exec, double q_exec, double profit = 0.0, string reason = "") {
            string json = "{";
            json += "\"id\": \"" + id + "\",";
            json += "\"status\": \"" + status + "\",";
            if(reason != "") json += "\"motivo\": \"" + reason + "\",";
            json += "\"preco_exec\": " + DoubleToString(p_exec, 5) + ",";
            json += "\"quantidade_exec\": " + DoubleToString(q_exec, 2) + ",";
            json += "\"profit\": " + DoubleToString(profit, 2) + ",";
            json += "\"timestamp\": \"" + TimeToString(TimeTradeServer(), TIME_DATE|TIME_SECONDS) + "\"";
            json += "}";
            
            int h = FileOpen(CommandBridge::m_out_file, FILE_WRITE|FILE_TXT|FILE_SHARE_WRITE|FILE_COMMON);
            if(h != INVALID_HANDLE) {
                FileWrite(h, json);
                FileClose(h);
            }
        }
        
        // ------------------------------------------------------------
        // LÊ ESTADO DA ALMA (SINCRONIZAÇÃO ROBUSTA)
        // ------------------------------------------------------------
        // ------------------------------------------------------------
        // LÊ ESTADO DA ALMA (SINCRONIZAÇÃO ROBUSTA - UTF8 FIX)
        // ------------------------------------------------------------
        static bool SyncSoulState() {
            static ulong last_try = 0;
            if(GetTickCount64() - last_try < 500) return false;
            last_try = GetTickCount64();
            
            // Abre como BINÁRIO para ler bytes crus
            int h = FileOpen(CommandBridge::m_soul_state_file, FILE_READ|FILE_BIN|FILE_SHARE_READ|FILE_COMMON);
            if(h == INVALID_HANDLE) {
                // Silencioso para não spammar logs
                return false;
            }
            
            ulong size = FileSize(h);
            if(size == 0) { FileClose(h); return false; }
            
            uchar data[];
            ArrayResize(data, (int)size);
            FileReadArray(h, data);
            FileClose(h);
            
            // Converte bytes UTF-8 para String MQL5 (Unicode)
            string json = CharArrayToString(data, 0, WHOLE_ARRAY, CP_UTF8);
            
            if(json == "") return false;
            
            bool parsed = ParseSoulJSON(json);
            if(parsed) {
                // Sincronia de Tempo Estabilizada
                m_last_soul_sync = (datetime)TimeLocal();
            }
            return parsed;
        }
        
        // ------------------------------------------------------------
        // ENVIA ESTADO DO CORPO PARA A ALMA
        // ------------------------------------------------------------
        // ------------------------------------------------------------
        // QUANTUM PULSE STREAMER (v2026 HFT Standard)
        // ------------------------------------------------------------
        static void SendBodyState(double last_price, double bid, double ask, double spread, 
                                   double volume, double open, double high, double low, double close,
                                   double rsi, double pos_profit,
                                   double balance, double daily_profit, bool has_position,
                                   double tick_intensity, double imbalance, double cortisol,
                                   double bb_delta) { // Novo
            
            static ulong last_io_flush_ms = 0;
            static double last_p = 0;
            static bool last_pos = false;
            static double last_dp = 0;
            static ulong last_write_time = 0;
            
            ulong now = GetTickCount64();
            
            bool heartbeat = (now - last_write_time > 5000);
            bool price_move = (MathAbs(last_price - last_p) >= _Point);
            bool state_change = (has_position != last_pos) || (MathAbs(daily_profit - last_dp) > 0.01);

            // Throttle se nada mudou
            if(!heartbeat && !price_move && !state_change) return;
            
            last_p = last_price;
            last_pos = has_position;
            last_dp = daily_profit;
            last_write_time = now;

            string json = "{";
            json += "\"last_price\": " + DoubleToString(last_price, _Digits) + ",";
            json += "\"bid\": " + DoubleToString(bid, _Digits) + ",";
            json += "\"ask\": " + DoubleToString(ask, _Digits) + ",";
            json += "\"spread\": " + DoubleToString(spread, 0) + ",";
            json += "\"rsi\": " + DoubleToString(rsi, 2) + ",";
            json += "\"bb_delta\": " + DoubleToString(bb_delta, 0) + ","; // Novo
            json += "\"pos_profit\": " + DoubleToString(pos_profit, 2) + ",";
            json += "\"balance\": " + DoubleToString(balance, 2) + ",";
            json += "\"daily_profit\": " + DoubleToString(daily_profit, 2) + ",";
            json += "\"has_position\": " + (has_position ? "true" : "false") + ",";
            json += "\"tick_intensity\": " + DoubleToString(tick_intensity, 2) + ",";
            json += "\"flow_imbalance\": " + DoubleToString(imbalance, 3) + ",";
            json += "\"cortisol\": " + DoubleToString(cortisol, 2) + ",";
            json += "\"ativo\": \"" + _Symbol + "\",";
            json += "\"timestamp\": \"" + TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS) + "\"";
            json += "}";
            
            // DEBUG EXTREMO PARA DIAGNÓSTICO
            Print("CORE_DUMP >> Balance: ", balance, " | DailyProfit: ", daily_profit, " | HasPos: ", has_position);
            
            int h = FileOpen(CommandBridge::m_body_state_file, FILE_WRITE|FILE_BIN|FILE_SHARE_READ|FILE_COMMON);
            if(h != INVALID_HANDLE) {
                uchar data[];
                StringToCharArray(json, data, 0, WHOLE_ARRAY, CP_UTF8);
                FileWriteArray(h, data);
                FileClose(h);
                CommandBridge::m_last_transmitted_price = last_price;
            }
        }
        
        // ------------------------------------------------------------
        // VERIFICA SE A ALMA ESTÁ ATIVA
        // ------------------------------------------------------------
        static bool IsSoulAlive() {
            if(MQLInfoInteger(MQL_TESTER)) return true;
            
            // --- QUANTUM STABILIZER v16.3 ---
            // Aumentamos a tolerância para 30s se houver indício de Disk Lag do Windows,
            // mas mantemos a sinalização de batimento cardíaco ativa.
            return (TimeLocal() - CommandBridge::m_last_soul_sync < 30); 
        }
        
        // ------------------------------------------------------------
        // OBTÉM MODIFICADOR DE AGRESSIVIDADE DA ALMA
        // ------------------------------------------------------------
        static double GetSoulAggressionMultiplier() {
            double mult = 1.0;
            if(CommandBridge::soul.bio_state == "BERSERK") mult = 1.5;
            else if(CommandBridge::soul.bio_state == "HIBERNATING") mult = 0.3;
            else if(CommandBridge::soul.bio_state == "HUNTING") mult = 1.0;
            else if(CommandBridge::soul.bio_state == "ATTACKING") mult = 1.2;
            mult *= (0.7 + CommandBridge::soul.neural_drive * 0.6);
            return MathMin(2.0, MathMax(0.2, mult));
        }

    private:
        static bool ParseOrderJSON(string json, MQTTOrder &ord) {
            ord.tipo = GetVal(json, "tipo");
            ord.ativo = GetVal(json, "ativo");
            ord.quantidade = StringToDouble(GetVal(json, "quantidade"));
            ord.preco = StringToDouble(GetVal(json, "preco"));
            ord.ordem = GetVal(json, "ordem");
            ord.id = GetVal(json, "id");
            ord.timeInForce = GetVal(json, "timeInForce");
            ord.sl_pts = (int)StringToInteger(GetVal(json, "sl_pts"));
            ord.tp_pts = (int)StringToInteger(GetVal(json, "tp_pts"));
            ord.signal_strength = StringToDouble(GetVal(json, "signal_strength"));
            ord.session_id = GetVal(json, "session_id");
            return (ord.id != "");
        }
        
        static bool ParseSoulJSON(string json) {
            CommandBridge::soul.session_id = GetVal(json, "session_id");
            CommandBridge::soul.version = GetVal(json, "version");
            CommandBridge::soul.capital = StringToDouble(GetVal(json, "capital"));
            CommandBridge::soul.daily_pnl = StringToDouble(GetVal(json, "daily_pnl"));
            CommandBridge::soul.bio_state = GetVal(json, "bio_state");
            CommandBridge::soul.neural_drive = StringToDouble(GetVal(json, "neural_drive"));
            CommandBridge::soul.market_regime = GetVal(json, "market_regime");
            CommandBridge::soul.is_hunting = (GetVal(json, "is_hunting") == "true");
            return (CommandBridge::soul.session_id != "");
        }
        
        static string GetVal(string json, string key) {
            string search = "\"" + key + "\"";
            int pos = StringFind(json, search);
            if(pos < 0) return "";
            pos = StringFind(json, ":", pos + StringLen(search));
            if(pos < 0) return "";
            
            int start = pos + 1;
            int len = StringLen(json);
            while(start < len) {
                ushort c = StringGetCharacter(json, start);
                if(c != ' ' && c != '\t' && c != '\r' && c != '\n') break;
                start++;
            }
            if(start >= len) return "";
            
            if(StringGetCharacter(json, start) == '"') {
                int end = StringFind(json, "\"", start + 1);
                if(end > start) return StringSubstr(json, start + 1, end - start - 1);
            } else {
                int end_comma = StringFind(json, ",", start);
                int end_brace = StringFind(json, "}", start);
                int end = -1;
                if(end_comma >= 0 && end_brace >= 0) end = MathMin(end_comma, end_brace);
                else if(end_comma >= 0) end = end_comma;
                else end = end_brace;
                
                if(end > start) {
                    string v = StringSubstr(json, start, end - start);
                    StringTrimRight(v);
                    return v;
                }
            }
            return "";
        }
    };
    
// DEFINIÇÕES ESTÁTICAS MOVIDAS PARA O .MQ5 PARA EVITAR UNRESOLVED EXTERNAL
// string    CommandBridge::m_in_file         = "Sovereign_MQTT_In.json";
// ...
}
#endif
