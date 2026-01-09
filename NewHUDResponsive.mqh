//+------------------------------------------------------------------+
//|                                           NewHUDResponsive.mqh   |
//|                                  Copyright 2026, Antigravity AI  |
//|            SOVEREIGN MASTER HUD - REVOLUTION v16.0         |
//+------------------------------------------------------------------+
#ifndef NEW_HUD_RESPONSIVE_MQH
#define NEW_HUD_RESPONSIVE_MQH

#include "CommandBridge.mqh"
#include "QuantumBankroll.mqh"

namespace Sovereign {
    
    class NewHUDResponsive {
    private:
        #define C_BG            C'10,12,18'    
        #define C_ACCENT        C'0,255,180'   
        #define C_BORD          C'40,45,60'    
        #define C_PROFIT        C'50,255,100'  
        #define C_LOSS          C'255,60,100'  
        #define C_TXT_MAIN      C'230,235,245' 
        #define C_TXT_DIM       C'110,120,140' 

        static void Box(string name, int x, int y, int w, int h, color bg, color border, int border_width=1) {
            if(ObjectFind(0, name) < 0) {
                ObjectCreate(0, name, OBJ_RECTANGLE_LABEL, 0, 0, 0);
                ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
            }
            ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
            ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
            ObjectSetInteger(0, name, OBJPROP_XSIZE, w);
            ObjectSetInteger(0, name, OBJPROP_YSIZE, h);
            ObjectSetInteger(0, name, OBJPROP_BGCOLOR, bg);
            ObjectSetInteger(0, name, OBJPROP_BORDER_TYPE, BORDER_FLAT);
            ObjectSetInteger(0, name, OBJPROP_WIDTH, border_width);
            ObjectSetInteger(0, name, OBJPROP_COLOR, border);
            ObjectSetInteger(0, name, OBJPROP_BACK, false);
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
        }

        static void Bar(string name, int x, int y, int w, int h, double pct, color c_fill) {
            Box(name + "_BG", x, y, w, h, C'20,25,35', C_BORD);
            int fill_w = (int)(w * MathMax(0.01, MathMin(1.0, pct)));
            Box(name + "_FILL", x, y, fill_w, h, c_fill, c_fill);
        }

    public:
        static void Txt(string name, string text, int x, int y, color c, int size, string font="Segoe UI", int anchor=0, int corner=CORNER_LEFT_UPPER) {
            if(ObjectFind(0, name) < 0) {
                ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
                ObjectSetInteger(0, name, OBJPROP_CORNER, corner);
                ObjectSetInteger(0, name, OBJPROP_ANCHOR, anchor);
            }
            ObjectSetString(0, name, OBJPROP_TEXT, text);
            if(corner == CORNER_LEFT_UPPER) {
                ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
                ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
            }
            ObjectSetInteger(0, name, OBJPROP_COLOR, c);
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size);
            ObjectSetString(0, name, OBJPROP_FONT, font);
            ObjectSetInteger(0, name, OBJPROP_BACK, false);
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
        }

        static void Draw(int X, int Y,
                         bool auto_mode, 
                         double daily_profit, 
                         double pos_profit,
                         string thought,
                         double dopamine, 
                         string bio_state, 
                         double tick_velocity, 
                         double latency_ms, 
                         double spread_points,
                         double imb_score,
                         double capital,
                         bool soul_alive,
                         int win_rate,     
                         double factor,    
                         double cost,      
                         double rsi,       // Novo
                         double bb_delta)  // Novo
        {
            int W = 260; 
            int H = 380; // Aumentado para novas métricas

            Box("MAIN_BG", X, Y, W, H, C_BG, C_BORD);
            Box("MAIN_TOP", X, Y, W, 25, C_BG, C_ACCENT); 
            Txt("H_TITLE", "🦅 QUANTUM SNIPER v16.2", X+(W/2), Y+4, C_ACCENT, 7, "Segoe UI Bold", ANCHOR_CENTER);
            
            int CY = Y + 30;

            // --- ⚡ EXECUÇÃO & ESTADO ---
            Txt("L_ST", "ESTADO:", X+12, CY, C_TXT_DIM, 6);
            color st_c = soul_alive ? C_PROFIT : C_LOSS;
            Txt("V_ST", (soul_alive ? "QUANTUM LINKED" : "OFFLINE"), X+W-12, CY, st_c, 6, "Segoe UI Bold", ANCHOR_RIGHT); CY+=12;

            Txt("L_LT", "LATÊNCIA:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_LT", DoubleToString(latency_ms, 0) + " ms", X+W-12, CY, C_TXT_MAIN, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=12;

            Txt("L_WR", "HIT RATE:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_WR", IntegerToString(win_rate) + "%", X+W-12, CY, C_PROFIT, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=16;

            Bar("N_BAR", X+12, CY, W-24, 4, dopamine, C_ACCENT); CY+=15;

            // --- 💰 FINANCEIRO LÍQUIDO (AUTOMÁTICO) ---
            Box("DIV_1", X+12, CY, W-24, 1, C_BORD, C_BORD); CY+=10;
            Txt("L_DI", "RESULTADO LÍQUIDO:", X+12, CY, C_TXT_DIM, 6);
            color pnl_c = (daily_profit >= 0) ? C_PROFIT : C_LOSS;
            Txt("V_DI", "R$ " + DoubleToString(daily_profit, 2), X+W-12, CY, pnl_c, 7, "Segoe UI Bold", ANCHOR_RIGHT); CY+=12;

            Txt("L_CS", "CUSTOS B3/XP:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_CS", "R$ " + DoubleToString(cost, 2), X+W-12, CY, C_LOSS, 6, "Consolas", ANCHOR_RIGHT); CY+=12;

            Txt("L_RF", "FATOR RECUP.:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_RF", DoubleToString(factor, 2), X+W-12, CY, clrCyan, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=15;

            // --- 🎯 MICROESTRUTURA SNIPER ---
            Box("DIV_2", X+12, CY, W-24, 1, C_BORD, C_BORD); CY+=10;
            Txt("L_VL", "TICK PRESSURE:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_VL", DoubleToString(tick_velocity, 0) + " t/s", X+W-12, CY, clrCyan, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=12;

            Txt("L_IB", "IMBALANCE:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_IB", DoubleToString(imb_score * 100, 1) + "%", X+W-12, CY, C_PROFIT, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=12;

            // --- ⚡ QUANTUM INDICATORS ---
            Txt("L_RSI", "RSI (2):", X+12, CY, C_TXT_DIM, 6);
            color rsi_c = C_TXT_MAIN;
            if(rsi < 30) rsi_c = C_PROFIT; 
            else if(rsi > 70) rsi_c = C_LOSS;
            Txt("V_RSI", DoubleToString(rsi, 1), X+W-12, CY, rsi_c, 6, "Consolas Bold", ANCHOR_RIGHT); CY+=12;
            
            Txt("L_BB", "DIST BANDA:", X+12, CY, C_TXT_DIM, 6);
            Txt("V_BB", DoubleToString(bb_delta, 0) + " pts", X+W-12, CY, (MathAbs(bb_delta) < 5 ? C_ACCENT : C_TXT_DIM), 6, "Consolas", ANCHOR_RIGHT); CY+=15;

            // --- 🧠 CORTEX Rodapé ---
            Box("DIV_3", X+8, CY, W-16, 40, C'15,18,25', C_BORD);
            string msg = thought;
            if(StringLen(msg) > 42) msg = StringSubstr(msg, 0, 39) + "...";
            Txt("V_THOUGHT", "» " + msg, X+14, CY+8, clrGold, 6, "Consolas");
            Txt("V_TIME", "UPTIME: " + TimeToString(TimeLocal(), TIME_SECONDS), X+14, CY+22, C_TXT_DIM, 5, "Consolas");
        }

        static void Cleanup() {
            ObjectsDeleteAll(0, "MAIN_");
            ObjectsDeleteAll(0, "H_");
            ObjectsDeleteAll(0, "L_");
            ObjectsDeleteAll(0, "V_");
            ObjectsDeleteAll(0, "N_");
            ObjectsDeleteAll(0, "DIV_");
            ChartRedraw();
        }
    };
}
#endif
