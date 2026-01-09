//+------------------------------------------------------------------+
//|                                              QuantumBankroll.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|         GESTOR DE BANCA QUANTUM: JUROS COMPOSTOS & CUSTO B3      |
//+------------------------------------------------------------------+
#ifndef QUANTUM_BANKROLL_MQH
#define QUANTUM_BANKROLL_MQH

#include "SovereignInputs.mqh"
#include <Trade\AccountInfo.mqh>

namespace Sovereign {

    class QuantumBankroll {
    private:
        static double m_last_closed_balance;
        static double m_target_today;
        
    public:
        // --- 📊 CÁLCULO DE ALAVANCAGEM PROGRESSIVA (SNIPER MODE v16.0) ---
        static double CalculateDynamicLot(double balance, double equity) {
            if(!InpAutoScalingActive) return InpBaseLotUnit;

            // Define a banca base para o cálculo
            double base_capital = MathMax(balance, InpInitialCapital);
            
            // --- 🚀 SNIPER BOOSTER (ALAVANCAGEM SELETIVA) ---
            // Aumentamos o peso do lote para que poucos trades batam a meta, 
            // mas apenas se a conta não estiver em drawdown.
            double booster = 1.0;
            if(equity >= base_capital) {
                booster = 2.0; // Dobra o lote base para atingir a meta com metade dos trades
            }
            
            // Fórmula Alpha: (Capital / Min_por_Lote) * Alavancagem * Booster
            double raw_lots = ((base_capital / InpMinCapitalPerLot) * InpLeveragePower) * booster;
            
            // Teto de segurança para não explodir a conta (0.25 divisor = mais agressivo)
            double max_safety = base_capital / (InpMinCapitalPerLot * 0.25); 
            double lot = MathMin(raw_lots, max_safety);
            
            return MathMax(InpBaseLotUnit, lot);
        }

        // --- 💸 MONITOR DE CUSTOS OPERACIONAIS (B3 + XP + OUTROS) ---
        static double GetNetProfit(double gross_profit, double lots) {
            // Estima o custo de abertura + fechamento (Taxas B3 + Emolumentos + XP + ISS)
            // AXP/B3 cobram aprox R$ 0.15 a R$ 0.30 por mini contrato, 
            // mas o usuário quer lucro real, então usamos uma margem de segurança maior.
            double total_cost = lots * (InpB3CostPerLot + 0.20); // Adicionado +R$ 0.20 de margem p/ XP/Outros
            return gross_profit - total_cost;
        }

        // --- 🎯 CALCULADORA DE META DIÁRIA LÍQUIDA ---
        static void UpdateDailyTarget(double current_balance) {
            double target_base = 0;
            if(InpCompoundActive) {
                target_base = current_balance * (InpDailyTargetPct / 100.0);
            } else {
                target_base = InpDailyProfitTarget;
            }
            // A meta agora é LÍQUIDA. O lucro bruto precisa cobrir as despesas.
            // Estimamos 20% de despesas sobre o alvo para recalcular a meta bruta necessária.
            m_target_today = target_base * 1.25; // Adiciona margem p/ garantir o líquido no bolso
        }

        static bool IsDailyTargetMet(double daily_profit_net) {
            return (daily_profit_net >= m_target_today);
        }

        static double GetCurrentTarget() { return m_target_today; }
    };

    double QuantumBankroll::m_last_closed_balance = 0;
    double QuantumBankroll::m_target_today = 0;
}

#endif
