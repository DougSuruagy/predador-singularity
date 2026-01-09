//+------------------------------------------------------------------+
//|                                              RiskManagement.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN RISK SHIELD: PREDATOR GUARDIAN v10.0   |
//+------------------------------------------------------------------+
#ifndef SOVEREIGN_RISK_MANAGEMENT_MQH_v6
#define SOVEREIGN_RISK_MANAGEMENT_MQH_v6

#include <Trade\Trade.mqh>
#include "Config.mqh"
#include "MarketCache.mqh"
#include "BioState.mqh"
#include "SovereignInputs.mqh"

namespace Sovereign {

    class RiskManagement {
    public:
        // -------------------------------------------------------------------
        // 1. DYNAMIC LOT SCALING (Bio-Sync)
        // -------------------------------------------------------------------
        static double CalculateBioLot(double base_lot, double intensity) {
            double modifier = (intensity / 100.0) * BioState::atp_energy / 100.0;
            if(BioState::is_berserk) modifier *= 1.5;
            if(BioState::is_rehabilitating) modifier *= 0.2;
            
            return base_lot * modifier;
        }

        // -------------------------------------------------------------------
        // 2. CIRCADIAN YIELD PROTECTION
        // -------------------------------------------------------------------
        static bool IsTradeAllowed() {
            if(BioState::circadian_sync < 0.2 && !InpAllowNightTrading) return false;
            if(BioState::vitals.system_integrity < 0.4) return false;
            return true;
        }

        // -------------------------------------------------------------------
        // 3. GAP PROTECTION (Anti-Slippage)
        // -------------------------------------------------------------------
        static bool IsGapRisky(const MqlTick &tick, double last_close) {
            double gap = MathAbs(tick.bid - last_close);
            if(gap > SymbolInfoDouble(_Symbol, SYMBOL_POINT) * 50) return true;
            return false;
        }

        static double NormalizeLot(double lot) {
            double step = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
            double min = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
            double max = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
            
            double res = MathFloor(lot/step)*step;
            if(res < min) res = min;
            if(res > max) res = max;
            return res;
        }

        static void PurgeAllPositions() {
            CTrade local_trade;
            local_trade.SetExpertMagicNumber(InpMagicNumber);
            for(int i = PositionsTotal() - 1; i >= 0; i--) {
                ulong ticket = PositionGetTicket(i);
                if(PositionSelectByTicket(ticket)) {
                    if(PositionGetInteger(POSITION_MAGIC) == InpMagicNumber) {
                        local_trade.PositionClose(ticket);
                        Print("🛡️ [TITAN-SHIELD] Closed Position (B3 Protocol): ", ticket);
                    }
                }
            }
             for(int i = OrdersTotal() - 1; i >= 0; i--) {
                ulong ticket = OrderGetTicket(i);
                if(OrderSelect(ticket)) {
                    if(OrderGetInteger(ORDER_MAGIC) == InpMagicNumber) {
                        local_trade.OrderDelete(ticket);
                    }
                }
            }
        }
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // 🧬 BIO-RISK MANAGEMENT: BIOLOGY DRIVEN SCALING
    // ═══════════════════════════════════════════════════════════════════════════
    class BioRiskManagement {
    public:
        // Added 'base_lot' parameter to match main code calls
        static double ScaleLotByBiology(double base_lot, NeuroCortex &cortex, const InstitutionalPillars &pillars) {
            // Fator base: Dopamina (Confiança) vs Cortisol (Medo)
            double drive = cortex.GetDrive(); // -1.0 a 1.0
            
            // Fator de integridade: Energia ATP
            double energy = pillars.atp_level / 100.0;
            
            // Multiplicador base (0.5x a 2.0x)
            double scale = 1.0 + (drive * 0.5);
            
            // Penalidade por fadiga
            if(energy < 0.3) scale *= 0.5;
            
            // Boost Berserk
            if(BioState::is_berserk) scale = MathMax(scale, 1.5);
            
            double final_lot = base_lot * scale;
            return MathMax(0.1, final_lot);
        }

        static bool GapStopCheck(NeuroCortex &cortex, const InstitutionalPillars &pillars) {
           // Checks if cortisol is too high or energy too low
           if(cortex.emotion.cortisol > 0.8) return false;
           if(pillars.atp_level < 20.0) return false;
           return true; 
        }

        static bool CheckEmergencyState() {
           // Basic equity check logic placeholder
           if(AccountInfoDouble(ACCOUNT_EQUITY) < AccountInfoDouble(ACCOUNT_BALANCE) * 0.5) return true;
           return false;
        }

        static void SyncBioMetrics(NeuroCortex &cortex) {
            // Sincroniza estado global estático com o córtex dinâmico
            cortex.emotion.serotonin = BioState::is_rehabilitating ? 0.8 : 0.5;
            
            // Atualiza latência percebida
            cortex.latency_ms = (int)TerminalInfoInteger(TERMINAL_PING_LAST);
        }

        static void InjectQuantumStress(NeuroCortex &cortex) {
            // Simula um choque de adrenalina via tecla 'S'
            cortex.emotion.adrenaline = 1.0;
            cortex.emotion.dopamine = 1.0;
            cortex.emotion.cortisol = 0.0;
            Print("💉 [BIO-RISK] INJEÇÃO DE ESTRESSE QUÂNTICO APLICADA!");
        }
    };

}
#endif
