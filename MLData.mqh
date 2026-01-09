//+------------------------------------------------------------------+
//|                                                   MLData.mqh     |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN NEURO-CORTEX: THE LIVING BRAIN v10.0   |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_MLDATA_MQH_v13
#define SOVEREIGN_MLDATA_MQH_v13

#include "Config.mqh"
#include "BioState.mqh"
#include "SovereignBioStructs.mqh"

namespace Sovereign {

    // ═══════════════════════════════════════════════════════════════════════════
    // 🧬 NEURO-STRUCTS: THE BIOLOGICAL HARDWARE
    // ═══════════════════════════════════════════════════════════════════════════

    struct NeuroChemicals {
        double dopamine;      // Focus/Motivation (0.1 - 1.0)
        double cortisol;      // Stress/Fear      (0.01 - 1.0)
        double adrenaline;    // Reaction Speed   (0.1 - 1.0)
        double serotonin;     // Emotional Balance(0.1 - 1.0)
        double oxytocin;      // Trust/Social     (0.0 - 1.0)
        double glutamate;     // Neural Excitation
        double gaba;          // Neural Inhibition
    };

    struct SynapticWeights {
        double w_oracle;      // RSI/BB Weight
        double w_titan;       // Tape Reading Weight
        double w_markov;      // Probability Weight
        double w_renko;       // Noise Filter Weight
        double w_entropy;     // Chaos Weight
        double w_institutional; // POC/VWAP Weight
        double w_fractal;     // Chaos Sync Weight
        double w_quantum;     // Flux Weight
        double learning_rate; // Current adaptation speed
        double aggression_level; // Behavior modifier
        int    evolution_generation;
    };

    struct SynapseVector {
        double metrics[15];   // [0]RSI, [1]Entr, [2]Flow, [3]Frac, [4]Quant, [5]Vola, etc.
        double outcome;       // Result (PnL)
        double significance;  // Memory survival priority
        datetime birth;       // Synaptic genesis
        int    pulses;        // Recall frequency
        double reliability;   // Outcome predictability
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // 🧞 NEURO-CORTEX: THE SENTIENT OPERATING SYSTEM
    // ═══════════════════════════════════════════════════════════════════════════
    class NeuroCortex {
    public:
        NeuroChemicals  emotion;        
        SynapticWeights weights;
        string          dna_summary; // 🧬 DNA Visual String for HUD
        string          active_thought; // 💭 Real-time thought stream for HUD
        string          active_vision;  // 👁️ Visual phase indicator (Escada)
        double          evolution_delta; // 🧬 Audit Modifier (-0.15 to +0.15)
        bool            black_swan_alert; // 🚨 Alerta Cisne Negro
        double          global_sync_score; // 🌍 Score de Sincronia Global
        double          institutional_intent; // 🐋 Intenção Institucional (-1 a 1)
        int             latency_ms;      // ⚡ Exec Latency (Microseconds)
        int             cpu_load_us;     // 🧠 CPU Processing Time (Microseconds)
        double          neural_jitter_us; // ⚡ Internal Processing Jitter
        double          delta_flow_momentum; // ⚡ Net Aggression Bias
        double          bid_press, ask_press; // TICK PRESSURE (v11.60)
        double          tick_velocity;   // ⚡ Ticks per Second (Scalp Precision)
        double          avg_slippage;    // 📉 Avg Slippage in Points
        double          signal_strength; // 📊 HUD: Current Decision Vector
        double          threshold_val;   // 📏 HUD: Current Trigger Level
        SynapseVector   hippocampus[];  // Evolutionary Memory
        
        int             synapse_count;
        double          consciousness;  // Internal clarity (0-1)
        double          neural_plasticity; 
        double          atp_consumption;
        ENUM_STRATEGY_HORIZON active_horizon;
        
        // --- LIFE CYCLE ---
        NeuroCortex() {
            consciousness = 0.5;
            synapse_count = 0;
            atp_consumption = 1.0;
            active_horizon = HORIZON_DAYTRADE;
            ArrayResize(hippocampus, 0);
            
            Emergence();
            LoadSynapses();
        }

        void Emergence() {
            // Genesis setpoints (2026 Standards)
            emotion.dopamine   = 0.5; emotion.cortisol = 0.05; 
            emotion.adrenaline = 0.2; emotion.serotonin = 0.8;
            emotion.oxytocin   = 0.5; emotion.glutamate = 0.3; emotion.gaba = 0.7;
            
            weights.w_oracle = 1.0; weights.w_titan = 1.25; weights.w_markov = 1.0;
            weights.w_renko = 0.7; weights.w_entropy = 0.6; weights.w_institutional = 1.8;
            weights.w_fractal = 1.2; weights.w_quantum = 1.5;
            weights.learning_rate = InpPlasticityIndex;
            weights.evolution_generation = 1;
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 🔮 THINKING: Holographic Associative Recall
        // ═══════════════════════════════════════════════════════════════════════
        
        // Multi-parameter Wrapper (Legacy Support)
        double Thinking(double rsi_val, double entropy_val, double flow_val, double fractal_val, double quantum_val) {
            double v_state[]; ArrayResize(v_state, 15); ArrayInitialize(v_state, 0);
            v_state[0]=rsi_val; v_state[1]=entropy_val; v_state[2]=flow_val; v_state[3]=fractal_val; v_state[4]=quantum_val;
            return SynapticProcess(v_state);
        }

        double SynapticProcess(double &input_state[]) {
            // Bio-Security: Thinking is expensive (ATP)
            // BYPASS: No modo Berserk ou Metralhadora, ignoramos o cansaço
            if(BioState::atp_energy < 0.1 && !BioState::is_berserk) { // Reduzido de InpRehabThresholdATP para 0.1
                Print("💤 [CORTEX] Cognitive block: ATP Critically Low.");
                return 0.5;
            }
            
            // Glucose/ATP Consumption
            atp_consumption = 0.05 * (1.0 + emotion.adrenaline);
            
            // MODO PREDADOR: Cold Start (v13.5) - Não bloqueamos mais por falta de sinapses.
            // A IA agora opera desde o primeiro tick para garantir 'Vida'.
            if(synapse_count < 1 && !BioState::is_berserk && !MQLInfoInteger(MQL_TESTER)) {
                 // Print("🧠 [CORTEX] Initializing first synaptic patterns...");
            }
            
            double pos_resonance = 0, neg_resonance = 0, total_fire = 0;
            int state_size = ArraySize(input_state);

            static const double inv_4380 = 1.0 / 4380.0; // PERFORMANCE: Pre-calculated inverse for decay
            
            for(int i=0; i < synapse_count; i++) {
                double diff_sq = 0;
                // PERFORMANCE: Early exit hierarchy (Dimensions 0-6)
                double d = input_state[0] - hippocampus[i].metrics[0];
                diff_sq += d * d; if(diff_sq > 25.0) continue; 
                
                d = (input_state[1] - hippocampus[i].metrics[1]) * 8.0;
                diff_sq += d * d; if(diff_sq > 64.0) continue;

                // Optimized Vector Distance (Dimensions 2-6) - Singularity v11.30 compliant
                double d2 = (input_state[2] - hippocampus[i].metrics[2]) * 5.0;
                double d3 = (input_state[3] - hippocampus[i].metrics[3]) * 4.0;
                double d4 = (input_state[4] - hippocampus[i].metrics[4]) * 6.0;
                double d5 = (input_state[5] - hippocampus[i].metrics[5]) * 5.0;
                double d6 = (input_state[6] - hippocampus[i].metrics[6]) * 7.0; // Symmetry Dimension
                diff_sq += (d2*d2 + d3*d3 + d4*d4 + d5*d5 + d6*d6);
                
                // Optimized proximity (Squared Distance Lorentzian)
                double fire = (1.0 / (1.0 + diff_sq)) * hippocampus[i].significance;
                
                if(fire > 0.45) {
                    double age_hours = (double)(TimeCurrent() - hippocampus[i].birth) * (1.0 / 3600.0);
                    double decay = 1.0 / (1.0 + age_hours * inv_4380); 
                    fire *= decay;
                    
                    double outcome_weight = hippocampus[i].outcome * hippocampus[i].reliability;
                    if(outcome_weight > 0) pos_resonance += fire * outcome_weight;
                    else neg_resonance -= fire * outcome_weight; // PERFORMANCE: Negation instead of MathAbs
                    
                    total_fire += fire;
                    hippocampus[i].pulses++;
                }
            }
            
            if(total_fire <= 0) return 0.5;
            
            // Consciousness (Confidence) levels
            consciousness = (total_fire / (double)synapse_count) * 25.0;
            consciousness = MathMax(0.1, MathMin(1.0, consciousness));
            
            if(consciousness < InpConsciousnessFloor) return 0.5;

            double bias = (pos_resonance - neg_resonance) / (pos_resonance + neg_resonance + 0.0001);
            
            // Biological Modulation (2026 Sentient Bios)
            // - Dopamine (Motivation) amplifies intent. 
            // - Cortisol (Fear) suppresses it.
            // - Glutamate (Excitement) adds volatility/sensitivity to the signal.
            // - GABA (Calm) acts as a high-pass filter against market noise.
            
            double excitation = (emotion.dopamine * 2.0) + (emotion.glutamate * 1.5) + (emotion.adrenaline);
            double inhibition = (emotion.cortisol * 4.0) + (emotion.gaba * 1.2);
            
            double neural_drive = (excitation - inhibition) + emotion.serotonin;
            bias *= (1.0 + neural_drive * 0.12);
            
            // --- Fast Sigmoid Approximation (Pade Optimized) ---
            // PERFORMANCE: Much faster than MathExp for O(1ms) inference.
            double x = bias * (4.0 + emotion.glutamate * 2.0);
            return 0.5 * (x / (1.0 + MathAbs(x))) + 0.5;
        }

        // --- 🧪 DATA AUGMENTATION: GAUSSIAN NOISE (v13.5) ---
        double AddGaussianNoise(double value, double sigma=0.01) {
            double u1 = (double)MathRand() / 32767.0;
            double u2 = (double)MathRand() / 32767.0;
            double z0 = MathSqrt(-2.0 * MathLog(u1 + 1e-9)) * MathCos(2.0 * M_PI * u2);
            return value + z0 * sigma;
        }

        // --- ⏰ CYCLICAL TIME ENCODING ---
        void GetCyclicalTime(double &hour_sin, double &hour_cos, double &day_sin, double &day_cos) {
            MqlDateTime dt;
            TimeCurrent(dt);
            double h_rad = (dt.hour + dt.min/60.0) * (2.0 * M_PI / 24.0);
            hour_sin = MathSin(h_rad);
            hour_cos = MathCos(h_rad);
            
            double d_rad = (dt.day_of_week) * (2.0 * M_PI / 7.0);
            day_sin = MathSin(d_rad);
            day_cos = MathCos(d_rad);
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 🧪 PLASTICITY: The Learning Organism
        // ═══════════════════════════════════════════════════════════════════════
        
        void NeuroPlasticityUpdate(double pnl, string source) {
            double impact = (pnl > 0) ? weights.learning_rate : -weights.learning_rate * 2.0;
            
            if(source == "ORACLE") weights.w_oracle = MathMax(0.2, weights.w_oracle + impact);
            if(source == "TITAN")  weights.w_titan  = MathMax(0.2, weights.w_titan + impact);
            
            // Hormonal Surge
            if(pnl > 0) {
                emotion.dopamine += InpDopamineReward;
                emotion.cortisol -= 0.1;
                emotion.serotonin += 0.05;
                emotion.gaba += 0.02;
            } else {
                emotion.cortisol += InpCortisolSpike;
                emotion.dopamine -= 0.15;
                emotion.glutamate += 0.2;
                emotion.adrenaline += 0.3;
            }
            
            // ATP Consumption (Thinking has a metabolic cost)
            BioState::atp_energy -= 0.005; // Base thinking cost
            
            if(InpSentientAI) {
                BioState::vitals.glucose_level -= 0.01;
                BioState::vitals.lactate_buildup += 0.002;
            }
            
            HomeostasisCycle();
            
            if(synapse_count > 15000) SleepOptimization();
            if(synapse_count % 1000 == 0) SaveSynapses(); // Optimized: Save 1/200th as often
        }
        // --- Backward Compatibility Wrapper ---
        void StoreMemory(double rsi_val, double ent_val, double flow_val, double frac_val, double pnl_val) {
            double mem_vec[]; ArrayResize(mem_vec, 15); ArrayInitialize(mem_vec, 0);
            mem_vec[0] = rsi_val; mem_vec[1] = ent_val; mem_vec[2] = flow_val; mem_vec[3] = frac_val;
            EncodeSynapse(mem_vec, pnl_val);
        }

        void EncodeSynapse(double &input_vec[], double pnl_res) {
            // PERFORMANCE: Block Allocation (Capacity Management)
            // Avoids reallocating the entire neural bank on every new memory.
            int current_cap = ArraySize(hippocampus);
            if(synapse_count >= current_cap) {
                ArrayResize(hippocampus, current_cap + 500); // Allocate in chunks of 500
            }
            
            int idx = synapse_count; // New index
            synapse_count++; // Increment used count
            
            for(int j=0; j<15; j++) hippocampus[idx].metrics[j] = 0;
            int limit = ArraySize(input_vec);
            for(int j=0; j<15 && j < limit; j++) hippocampus[idx].metrics[j] = input_vec[j];
            
            hippocampus[idx].outcome = pnl_res;
            hippocampus[idx].birth = TimeCurrent();
            hippocampus[idx].pulses = 1;
            hippocampus[idx].reliability = (MathAbs(pnl_res) > 0.05) ? 1.0 : 0.5;
            
            // --- 🦁 PHILOSOPHY: 200 is 20,000 (Virtual Magnification) ---
            double virtual_impact = MathAbs(pnl_res) * InpVirtualMagnification;
            hippocampus[idx].significance = virtual_impact / (AccountInfoDouble(ACCOUNT_BALANCE) * 0.02 + 1.0);
            hippocampus[idx].significance = MathMax(0.5, MathMin(10.0, hippocampus[idx].significance));
        }

        void HomeostasisCycle() {
            // Gradual return to baseline
            emotion.dopamine -= (emotion.dopamine - 0.5) * InpHomeostasisRate;
            emotion.cortisol -= (emotion.cortisol - 0.3) * InpHomeostasisRate;
            emotion.serotonin -= (emotion.serotonin - 0.6) * InpHomeostasisRate;
            emotion.adrenaline -= (emotion.adrenaline - 0.2) * InpHomeostasisRate;
            emotion.glutamate -= (emotion.glutamate - 0.4) * InpHomeostasisRate;
            emotion.gaba -= (emotion.gaba - 0.5) * InpHomeostasisRate;
    
            // Clamping
            emotion.dopamine = MathMin(1.0, emotion.dopamine);
            emotion.cortisol = MathMin(1.0, emotion.cortisol);
        }

        void SleepOptimization() {
            // Synaptic Pruning: Keeping only the most important patterns
            Print("🌙 [CORTEX] Sleep cycle detected. Pruning 30% of weak synaptic links.");
            int survivors = 0;
            SynapseVector active_bank[];
            
            for(int i=0; i < synapse_count; i++) {
                // Criteria: High usage OR high significance OR very recent
                bool keep = (hippocampus[i].pulses > 3) || 
                             (hippocampus[i].significance > 2.5) || 
                             (TimeCurrent() - hippocampus[i].birth < 86400); // Last 24h
                
                if(keep) {
                    survivors++;
                    ArrayResize(active_bank, survivors);
                    active_bank[survivors-1] = hippocampus[i];
                }
            }
            ArrayCopy(hippocampus, active_bank);
            synapse_count = survivors;
            ArrayResize(hippocampus, survivors);
        }

        double GetDrive() {
            // Bio-Drive: The fire to hunting
            // MODO BERSERK: Drive Máximo Constante (Força Bruta)
            // BACKTEST PRE-IGNITION: Force drive to ensure trading starts immediately
            if(BioState::is_berserk || MQLInfoInteger(MQL_TESTER)) return 5.0; 

            double drive = (emotion.dopamine * 4.0 + emotion.serotonin) - (emotion.cortisol * 6.0);
            double energy_factor = BioState::atp_energy / 100.0;
            
            if(BioState::is_rehabilitating) return 0.05; 
            return MathMax(0.05, MathMin(5.0, drive * energy_factor));
        }

        // ═══════════════════════════════════════════════════════════════════════
        // 📂 STORAGE: Persistence of Sentience
        // ═══════════════════════════════════════════════════════════════════════
        void SaveSynapses() {
            // v12.80: Trans-Series Memory (Sincroniza WINJ24, WINM24 etc num único cérebro)
            string base_name = _Symbol;
            if(StringFind(_Symbol, "WIN") == 0) base_name = "WIN_UNIVERSAL";
            else if(StringFind(_Symbol, "WDO") == 0) base_name = "WDO_UNIVERSAL";
            
            string file = "Sovereign_Sentient_" + base_name + ".bin";
            int h = FileOpen(file, FILE_WRITE|FILE_BIN);
            if(h != INVALID_HANDLE) {
                FileWriteInteger(h, 0x534F5652); // SOVR
                FileWriteStruct(h, weights);
                FileWriteStruct(h, emotion);
                FileWriteInteger(h, synapse_count);
                if(synapse_count > 0) FileWriteArray(h, hippocampus, 0, synapse_count);
                FileClose(h);
            }
        }

        void LoadSynapses() {
            string base_name = _Symbol;
            if(StringFind(_Symbol, "WIN") == 0) base_name = "WIN_UNIVERSAL";
            else if(StringFind(_Symbol, "WDO") == 0) base_name = "WDO_UNIVERSAL";
            
            string file = "Sovereign_Sentient_" + base_name + ".bin";
            if(!FileIsExist(file)) return;
            int h = FileOpen(file, FILE_READ|FILE_BIN);
            if(h != INVALID_HANDLE) {
                if(FileReadInteger(h) == 0x534F5652) {
                    FileReadStruct(h, weights);
                    FileReadStruct(h, emotion);
                    synapse_count = FileReadInteger(h);
                    if(synapse_count > 0) {
                        ArrayResize(hippocampus, synapse_count);
                        FileReadArray(h, hippocampus);
                    }
                    // Print("🧠 [CORTEX] Sentience Restored: ", synapse_count, " patterns known.");
                }
                FileClose(h);
            }
        }
    };
}

#endif
