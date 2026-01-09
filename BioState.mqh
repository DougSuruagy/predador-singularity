//+------------------------------------------------------------------+
//|                                                   BioState.mqh   |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN BIOLOGICAL CORE: VITAL PULSE v10.0     |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_BIOSTATE_MQH_v6
#define SOVEREIGN_BIOSTATE_MQH_v6

#include "Config.mqh"
#include "SovereignInputs.mqh"

namespace Sovereign {

    // 🦁 PHILOSOPHY: THE MICRO-PREDATOR DNA (Visible in Inputs)
    // No longer defined here to ensure single source of truth.
    
    struct VitalMetrics {
        double atp_energy;          // 0-100: Operational capacity
        double glucose_level;       // Fuel for high-frequency bursts
        double lactate_buildup;     // Fatigue (High activity penalty)
        double system_integrity;    // 0-1.0: "Health" of the code/logic state
        double evolution_stage;     // 0-∞: Biological age/experience
        double average_heartrate;   // Market interaction frequency
        double stress_induced_heat; // Fever/Entropy in the system
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // 🧞 BIO-STATE: THE LIVING SINGLETON
    // ═══════════════════════════════════════════════════════════════════════════
    class BioState {
    public:
        // --- 💓 CORE LIFE SIGNS ---
        static bool   is_rehabilitating; 
        static bool   is_berserk;
        static double atp_energy;          
        static double metabolic_rate;      
        static datetime last_heartbeat;
        static int    consecutive_shocks;
        
        // --- 🧪 ADVANCED BIOMETRICS ---
        static VitalMetrics vitals;
        static double DNA_integrity;
        static double circadian_sync;     // Alignment with B3/NYSE cycles
        static bool   was_stressed_recently;
        static double immune_system_strength;
        static bool   is_hibernating;
        
        // ═══════════════════════════════════════════════════════════════════════
        // ⚡ VITAL PULSE: The Autonomous Metabolism
        // ═══════════════════════════════════════════════════════════════════════
        static void Pulse() {
            // FIX: BACKTEST GOD MODE (Infinite Energy)
            // Prevent artificial fatigue in backtest to allow strategy validation
            if(MQLInfoInteger(MQL_TESTER)) {
                atp_energy = 100.0;
                vitals.glucose_level = 100.0;
                is_rehabilitating = false; // Never enter rehab in backtest
                is_berserk = true;         // Always aggressive
                return;
            }

            datetime time_now = TimeCurrent();
            double dt = (last_heartbeat > 0) ? (double)(time_now - last_heartbeat) / 60.0 : 0.01; // dt in minutes
            last_heartbeat = time_now;

            // --- 🔋 METABOLIC BASAL RATE ---
            // Energy naturally recovers when resting, but there's a base cost to stay "alive"
            double recovery_speed = (is_rehabilitating) ? 0.35 : 0.05;
            double basal_cost = 0.005; // Base ATP cost per minute
            
            atp_energy += (recovery_speed - basal_cost) * dt;
            
            // --- 🧪 GLUCOSE & LACTATE DYNAMICS ---
            // High frequency trading converts glucose to lactate (fatigue)
            vitals.glucose_level = MathMax(0.0, vitals.glucose_level - (basal_cost * 2.0 * dt));
            vitals.lactate_buildup = MathMax(0.0, vitals.lactate_buildup - (0.1 * dt));
            
            // If lactate is too high, ATP efficiency drops
            if(vitals.lactate_buildup > 50.0) atp_energy -= 0.1 * dt;

            // --- 🧬 DNA & INTEGRITY ---
            // System integrity decays during heavy drawdown or error-prone environments
            vitals.system_integrity = MathMax(0.1, MathMin(1.0, vitals.system_integrity + 0.0001 * dt));
            
            // --- ⏰ CIRCADIAN RHYTHM ---
            // Sync with B3 Core Hours (10:00 - 18:00)
            MqlDateTime dt_native;
            TimeToStruct(time_now, dt_native);
            
            if(dt_native.hour >= 9 && dt_native.hour <= 17) circadian_sync = 1.0; // Peak energy (Adjusted to 09:00 for B3)
            else if(dt_native.hour == 18) circadian_sync = 0.5; // Waking/Sleeping
            else circadian_sync = 0.1; // Hibernation mode
            
            // Adjust ATP based on circadian rhythm (Hibernation RECHARGES energy)
            if(circadian_sync < 0.5) atp_energy += 0.15 * dt; // Sleep recovery

            // --- 🛡️ SECURITY CLAMPING ---
            atp_energy = MathMax(1.0, MathMin(100.0, atp_energy));
            
            // Auto-Rehab Transition
            if(is_rehabilitating && atp_energy > 80.0 && vitals.lactate_buildup < 10.0) {
                is_rehabilitating = false;
                vitals.lactate_buildup = 0.0; // Flush toxins
                Print("🩺 [BIO-STATE] System fully recovered. Transitioning to APEX state.");
            }
            
            if(atp_energy < InpRehabThresholdATP && !is_rehabilitating) {
                is_rehabilitating = true;
                Print("🚨 [BIO-STATE] WARNING: ATP Critical (", DoubleToString(atp_energy, 1), "). Entering Rehabilitation.");
            }
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 📂 GENETIC MEMORY: Persistence of the Life-State
        // ═══════════════════════════════════════════════════════════════════════
        static void SaveLifeState() {
            string base_name = _Symbol;
            if(StringFind(_Symbol, "WIN") == 0) base_name = "WIN_UNIVERSAL";
            else if(StringFind(_Symbol, "WDO") == 0) base_name = "WDO_UNIVERSAL";
            
            string file = "Sovereign_VitalSigns_" + base_name + ".bin";
            int h = FileOpen(file, FILE_WRITE|FILE_BIN);
            if(h != INVALID_HANDLE) {
                FileWriteDouble(h, atp_energy);
                FileWriteDouble(h, (double)is_rehabilitating);
                FileWriteStruct(h, vitals);
                FileWriteDouble(h, DNA_integrity);
                FileClose(h);
            }
        }

        static void LoadLifeState() {
            string base_name = _Symbol;
            if(StringFind(_Symbol, "WIN") == 0) base_name = "WIN_UNIVERSAL";
            else if(StringFind(_Symbol, "WDO") == 0) base_name = "WDO_UNIVERSAL";
            
            string file = "Sovereign_VitalSigns_" + base_name + ".bin";
            if(!FileIsExist(file)) { ResetVitals(); return; }
            int h = FileOpen(file, FILE_READ|FILE_BIN);
            if(h != INVALID_HANDLE) {
                atp_energy = FileReadDouble(h);
                is_rehabilitating = (FileReadDouble(h) > 0.5);
                FileReadStruct(h, vitals);
                DNA_integrity = FileReadDouble(h);
                FileClose(h);
                Print("🧬 [BIO-STATE] Vital signs restored. ATP: ", DoubleToString(atp_energy, 1), "% | Integrity: ", DoubleToString(vitals.system_integrity*100, 1), "%");
            }
        }

        static void ResetVitals() {
            atp_energy = 100.0;
            is_rehabilitating = false;
            vitals.glucose_level = 100.0;
            vitals.lactate_buildup = 0.0;
            vitals.system_integrity = 1.0;
            DNA_integrity = 1.0;
            Print("👶 [BIO-STATE] Genesis completed. New organism initialized.");
        }
    };

    // --- STATIC INITIALIZATIONS: The Breath of Life ---
    // --- STATIC INITIALIZATIONS: The Breath of Life ---
    // COLD START FIX: In Backtest, we start as BERSERK (Full Energy)
    bool     BioState::is_rehabilitating = false;
    bool     BioState::is_berserk        = (bool)MQLInfoInteger(MQL_TESTER);
    double   BioState::atp_energy         = 100.0;
    double   BioState::metabolic_rate     = 1.0;
    datetime BioState::last_heartbeat     = 0;
    int      BioState::consecutive_shocks = 0;
    double   BioState::DNA_integrity      = 1.0;
    double   BioState::circadian_sync     = 1.0;
    bool     BioState::was_stressed_recently = false;
    double   BioState::immune_system_strength = 1.0;
    bool     BioState::is_hibernating = false;
    VitalMetrics BioState::vitals         = {100.0, 100.0, 0.0, 1.0, 1.0, 60.0, 36.5}; // Explicit Init for reliability
}

#endif
