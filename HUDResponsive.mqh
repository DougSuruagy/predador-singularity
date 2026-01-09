//+------------------------------------------------------------------+
//|                                               HUDResponsive.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|                SOVEREIGN ORACLE v5.0 - ELITE SCALPER HUD         |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_HUDRESPONSIVE_MQH
#define SOVEREIGN_HUDRESPONSIVE_MQH

#include "MarketCache.mqh"
#include "Config.mqh"
#include "MLData.mqh"
#include "RiskManagement.mqh"
#include "BioState.mqh"

namespace Sovereign {
    class HUDResponsive {
        static string m_prefix;
        static int    m_last_chart_width;
        static long   m_server_offset;
        
    public:
        static void UpdateHUD(NeuroCortex &cortex) {
             m_prefix = "HUD_";
             
             if(m_server_offset == 0) {
                 m_server_offset = (long)TimeTradeServer() - (long)TimeLocal();
             }
             
             int w = (int)ChartGetInteger(0, CHART_WIDTH_IN_PIXELS);
             
             if(w != m_last_chart_width) {
                 Cleanup();
                 m_last_chart_width = w;
             }
             
             DrawElitePanel(cortex);
             ChartRedraw();
        }
        
        static void Cleanup() {
            ObjectsDeleteAll(0, m_prefix);
        }

        //+------------------------------------------------------------------+
        //|                    ELITE SCALPER HUD v5.1 (ADJUSTED)            |
        //+------------------------------------------------------------------+
        static void DrawElitePanel(NeuroCortex &cortex) {
            // ═══════════════════════════════════════════════════════════════
            // CONFIGURAÇÕES DO PAINEL
            // ═══════════════════════════════════════════════════════════════
            int x = 8;
            int y = 18;
            int W = 330;  // Adjusted width
            int H = 282;  // Reduced height from 310 to 282 to remove empty space
            int row = 14; 
            
            // CORES PROFISSIONAIS
            color C_BG       = C'12,14,18';      
            color C_BORDER   = C'35,45,60';      
            color C_HEADER   = C'18,22,30';      
            color C_TEXT     = C'180,185,195';   
            color C_DIM      = C'90,95,105';     
            color C_CYAN     = C'0,180,220';     
            color C_GREEN    = C'40,205,120';    
            color C_RED      = C'220,70,80';     
            color C_GOLD     = C'255,195,0';     
            color C_PURPLE   = C'160,100,255';   
            
            // HEADER
            // ═══════════════════════════════════════════════════════════════
            Box("MAIN", x, y, W, H, C_BG, C_BORDER);
            Box("HEAD", x+1, y+1, W-2, 20, C_HEADER, C_HEADER);
            
            Txt("TITLE", "SOVEREIGN v7", x+8, y+5, C_CYAN, 8, "Segoe UI Semibold");
            
            bool online = (bool)TerminalInfoInteger(TERMINAL_CONNECTED);
            Txt("DOT", online ? "●" : "○", x+110, y+5, online ? C_GREEN : C_RED, 7, "Consolas");
            
            datetime srv = (datetime)(TimeLocal() + m_server_offset);
            Txt("TIME", TimeToString(srv, TIME_SECONDS), x+125, y+6, C_DIM, 7, "Consolas");
            
            // Latency display
            color lat_c = (cortex.latency_ms < 50) ? C_GREEN : (cortex.latency_ms < 150 ? C_GOLD : C_RED);
            Txt("LAT", IntegerToString(cortex.latency_ms) + "ms", x+205, y+6, lat_c, 6, "Consolas");
            
            Txt("SYM", _Symbol, x+W-60, y+5, C_GOLD, 8, "Segoe UI Semibold");
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 1: PREÇO & SPREAD
            // ═══════════════════════════════════════════════════════════════
            int s1 = y + 24;
            
            double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
            long spread = SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
            
            Txt("L_PRICE", "PRICE", x+8, s1, C_DIM, 6, "Consolas");
            Txt("V_PRICE", DoubleToString(bid, _Digits), x+8, s1+10, C_CYAN, 11, "Consolas");
            
            Txt("L_SPREAD", "SPR", x+130, s1, C_DIM, 6, "Consolas");
            Txt("V_SPREAD", IntegerToString(spread), x+130, s1+10, C_TEXT, 9, "Consolas");
            
            string tf = GetTF();
            Txt("V_TF", tf, x+W-35, s1+8, C_TEXT, 8, "Consolas");
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 2: P&L
            // ═══════════════════════════════════════════════════════════════
            int s2 = s1 + 28;
            Line("DIV1", x+8, s2, W-16, C_BORDER);
            s2 += 4;
            
            double pnl = AccountInfoDouble(ACCOUNT_PROFIT);
            double bal = AccountInfoDouble(ACCOUNT_BALANCE);
            double eq  = AccountInfoDouble(ACCOUNT_EQUITY);
            color pnl_c = (pnl >= 0) ? C_GREEN : C_RED;
            string pnl_s = (pnl >= 0) ? "+" : "";
            
            Txt("L_PNL", "P&L", x+8, s2, C_DIM, 6, "Consolas");
            Txt("V_PNL", pnl_s + "R$ " + DoubleToString(pnl, 2), x+8, s2+10, pnl_c, 10, "Consolas");
            
            Txt("L_BAL", "BAL", x+130, s2, C_DIM, 6, "Consolas");
            Txt("V_BAL", "R$ " + DoubleToString(bal, 0), x+130, s2+10, C_TEXT, 8, "Consolas");
            
            Txt("L_EQ", "EQ", x+220, s2, C_DIM, 6, "Consolas");
            Txt("V_EQ", "R$ " + DoubleToString(eq, 0), x+220, s2+10, C_TEXT, 8, "Consolas");
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 3: BIO-NEURAL (Barras ajustadas)
            // ═══════════════════════════════════════════════════════════════
            int s3 = s2 + 28;
            Line("DIV2", x+8, s3, W-16, C_BORDER);
            s3 += 6;
            
            Txt("L_BIO", "BIO-NEURAL", x+8, s3, C_PURPLE, 6, "Segoe UI Semibold");
            s3 += 12;
            
            // Largura disponível ~300. Usaremos 145 para cada coluna
            MiniBar("ATP", x+8, s3, 140, BioState::atp_energy/100.0, C_CYAN);
            MiniBar("DOP", x+155, s3, 140, cortex.emotion.dopamine, C_GOLD);
            s3 += 14;
            MiniBar("SER", x+8, s3, 140, cortex.emotion.serotonin, C_GREEN);
            MiniBar("COR", x+155, s3, 140, cortex.emotion.cortisol, C_RED);
            s3 += 14;
            MiniBar("ADR", x+8, s3, 140, cortex.emotion.adrenaline, C_GOLD);
            MiniBar("CON", x+155, s3, 140, cortex.consciousness, C_PURPLE);
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 4: QUANTUM SENSORS
            // ═══════════════════════════════════════════════════════════════
            int s4 = s3 + 18;
            Line("DIV3", x+8, s4, W-16, C_BORDER);
            s4 += 6;
            
            Txt("L_QS", "QUANTUM", x+8, s4, C_PURPLE, 6, "Segoe UI Semibold");
            
            string regime = "OPTIMAL";
            color reg_c = C_GREEN;
            if(MarketCache::current_regime == REGIME_HYPER_VOLATILE) { regime = "VOLATILE"; reg_c = C_GOLD; }
            else if(MarketCache::current_regime == REGIME_LIQUIDITY_HOLE) { regime = "VACUUM"; reg_c = C_RED; }
            else if(MarketCache::current_regime == REGIME_TRENDING_UP) { regime = "BULL"; reg_c = C_GREEN; }
            else if(MarketCache::current_regime == REGIME_TRENDING_DOWN) { regime = "BEAR"; reg_c = C_RED; }
            
            Txt("V_REG", regime, x+80, s4, reg_c, 7, "Consolas");
            
            // v7: BLACK SWAN ALERT
            if(cortex.black_swan_alert) {
                Txt("V_SWAN", "🚨 BLACK SWAN", x+W-85, s4, C_RED, 6, "Segoe UI Semibold");
            }
            
            s4 += 14;
            // 3 barras dividindo ~300px = ~95px cada
            MiniBar("ENT", x+8, s4, 75, MarketCache::entropy_index, C_PURPLE);
            MiniBar("FLW", x+88, s4, 75, MathMin(1.0, MarketCache::flow_intensity/50.0), C_CYAN);
            MiniBar("FRC", x+168, s4, 75, (MarketCache::fractal_dimension-1.0), C_GOLD);
            MiniBar("SNC", x+248, s4, 75, cortex.global_sync_score, C_CYAN); // v7 Sync Bar
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 5: SCALP ENGINE
            // ═══════════════════════════════════════════════════════════════
            int s5 = s4 + 18;
            Line("DIV4", x+8, s5, W-16, C_BORDER);
            s5 += 6;
            
            Txt("L_SCALP", "SCALP ENGINE", x+8, s5, C_GOLD, 5, "Segoe UI Semibold");
            
            bool berserk = BioState::is_berserk;
            color mode_c = berserk ? C_RED : C_GREEN;
            string mode_t = "MODE: " + (berserk ? "BERSERK" : "TACTICAL");
            Txt("V_MODE", mode_t, x+80, s5, mode_c, 5, "Consolas");
            
            string phase_raw = cortex.active_vision;
            if(StringLen(phase_raw) < 1) phase_raw = "PIONEER";
            if(StringLen(phase_raw) > 18) phase_raw = StringSubstr(phase_raw, 0, 15) + "...";
            string phase_t = "PH: " + phase_raw;
            Txt("V_PHASE", phase_t, x+W-135, s5, C_CYAN, 5, "Segoe UI Semibold");
            
            s5 += 12;
            
            // Signal
            Txt("L_SIG", "SIG:", x+8, s5, C_DIM, 5, "Consolas");
            double bias = MarketCache::prob_bull_flux - MarketCache::prob_bear_flux;
            string sig_t = (bias > 0.1) ? "BUY" : (bias < -0.1 ? "SELL" : "WAIT");
            color sig_c = (bias > 0.1) ? C_GREEN : (bias < -0.1 ? C_RED : C_DIM);
            Txt("V_SIG", sig_t, x+30, s5, sig_c, 6, "Consolas");
            
            // Lot
            Txt("L_LOT", "LOT:", x+90, s5, C_DIM, 5, "Consolas");
            Txt("V_LOT", DoubleToString(InpBaseLotUnit * InpLotScalingFactor, 2), x+115, s5, C_TEXT, 6, "Consolas");
            
            // Risk
            Txt("L_RISK", "RISK:", x+W-70, s5, C_DIM, 5, "Consolas");
            Txt("V_RISK", DoubleToString(InpRiskPerTrade, 1) + "%", x+W-40, s5, C_RED, 6, "Consolas");
            
            s5 += 12;
            
            // Drive
            double drive = cortex.GetDrive();
            Txt("L_DRV", "DRV:", x+8, s5, C_DIM, 5, "Consolas");
            Txt("V_DRV", "x" + DoubleToString(drive, 2), x+30, s5, C_GOLD, 6, "Consolas");
            
            s5 += 14;
            
            // Aggression bar
            double agg = MathMin(1.0, cortex.weights.aggression_level / 5.0);
            MiniBar("AGG", x+8, s5, 140, agg, berserk ? C_RED : C_GOLD);
            
            // Evolution bar (Mapped from -0.15 to +0.15 normalized to 0-1)
            double evo_val = (cortex.evolution_delta + 0.15) / 0.30;
            MiniBar("EVO", x+175, s5, 140, evo_val, C_CYAN);
            
            // ═══════════════════════════════════════════════════════════════
            // SEÇÃO 6: THOUGHT STREAM
            // ═══════════════════════════════════════════════════════════════
            int s6 = s5 + 16;
            Line("DIV5", x+8, s6, W-16, C_BORDER);
            s6 += 4;
            
            string thought = cortex.active_thought;
            if(StringLen(thought) < 2) thought = "Scanning market...";
            if(StringLen(thought) > 48) thought = StringSubstr(thought, 0, 45) + "...";
            Txt("THOUGHT", thought, x+8, s6, C_CYAN, 5, "Consolas");
            
            Txt("GEN", "v7.0", x+W-35, s6, C_DIM, 6, "Consolas");
        }
        
        // ═══════════════════════════════════════════════════════════════════════
        // HELPERS COMPACTOS (Fixed padding)
        // ═══════════════════════════════════════════════════════════════════════
        
        static void MiniBar(string id, int x, int y, int w, double val, color c) {
            val = MathMin(1.0, MathMax(0.0, val));
            int h = 8;
            int lbl_w = 25; // espaço reservado pro label (ex: "ATP")
            int val_w = 30; // espaço reservado pro valor (ex: "1.00")
            int bar_w = w - lbl_w - val_w; 
            
            Txt("MB_L_"+id, id, x, y, C'80,85,95', 6, "Consolas");
            
            int bx = x + lbl_w;
            Box("MB_BG_"+id, bx, y+1, bar_w, h-2, C'25,28,35', C'25,28,35');
            
            int fill = (int)(bar_w * val);
            if(fill > 0) Box("MB_F_"+id, bx, y+1, fill, h-2, c, c);
            
            Txt("MB_V_"+id, DoubleToString(val, 2), bx + bar_w + 3, y, c, 6, "Consolas");
        }
        
        static string GetTF() {
            ENUM_TIMEFRAMES tf = (ENUM_TIMEFRAMES)Period();
            switch(tf) {
                case PERIOD_M1:  return "M1";
                case PERIOD_M5:  return "M5";
                case PERIOD_M15: return "M15";
                case PERIOD_M30: return "M30";
                case PERIOD_H1:  return "H1";
                case PERIOD_H4:  return "H4";
                case PERIOD_D1:  return "D1";
                default: return "M1";
            }
        }
        
        static void Line(string id, int x, int y, int w, color c) {
            string obj = m_prefix + id;
            if(ObjectFind(0, obj) < 0) {
                ObjectCreate(0, obj, OBJ_RECTANGLE_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            }
            ObjectSetInteger(0, obj, OBJPROP_XDISTANCE, x);
            ObjectSetInteger(0, obj, OBJPROP_YDISTANCE, y);
            ObjectSetInteger(0, obj, OBJPROP_XSIZE, w);
            ObjectSetInteger(0, obj, OBJPROP_YSIZE, 1);
            ObjectSetInteger(0, obj, OBJPROP_BGCOLOR, (long)c);
            ObjectSetInteger(0, obj, OBJPROP_COLOR, (long)c);
        }

        static void Box(string id, int x, int y, int w, int h, color bg, color border) {
            string obj = m_prefix + id;
            if(ObjectFind(0, obj) < 0) {
                ObjectCreate(0, obj, OBJ_RECTANGLE_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj, OBJPROP_CORNER, CORNER_LEFT_UPPER);
                ObjectSetInteger(0, obj, OBJPROP_BORDER_TYPE, BORDER_FLAT);
            }
            ObjectSetInteger(0, obj, OBJPROP_XDISTANCE, x);
            ObjectSetInteger(0, obj, OBJPROP_YDISTANCE, y);
            ObjectSetInteger(0, obj, OBJPROP_XSIZE, w);
            ObjectSetInteger(0, obj, OBJPROP_YSIZE, h);
            ObjectSetInteger(0, obj, OBJPROP_BGCOLOR, (long)bg);
            ObjectSetInteger(0, obj, OBJPROP_COLOR, (long)border);
            ObjectSetInteger(0, obj, OBJPROP_BACK, false);
        }

        static void Txt(string id, string text, int x, int y, color c, int size, string font) {
            string obj = m_prefix + id;
            if(ObjectFind(0, obj) < 0) {
                ObjectCreate(0, obj, OBJ_LABEL, 0, 0, 0);
                ObjectSetInteger(0, obj, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            }
            ObjectSetInteger(0, obj, OBJPROP_XDISTANCE, x);
            ObjectSetInteger(0, obj, OBJPROP_YDISTANCE, y);
            ObjectSetString(0, obj, OBJPROP_TEXT, text);
            ObjectSetString(0, obj, OBJPROP_FONT, font);
            ObjectSetInteger(0, obj, OBJPROP_COLOR, (long)c);
            ObjectSetInteger(0, obj, OBJPROP_FONTSIZE, (long)size);
            ObjectSetInteger(0, obj, OBJPROP_BACK, false);
        }
    };
    
    string HUDResponsive::m_prefix = "HUD_";
    int    HUDResponsive::m_last_chart_width = 0;
    long   HUDResponsive::m_server_offset = 0;
}

#endif
