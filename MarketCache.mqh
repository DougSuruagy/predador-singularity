//+------------------------------------------------------------------+
//|                                                MarketCache.mqh   |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN QUANTUM SENSORY GRID: PULSE v10.0      |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_MARKETCACHE_MQH_v4
#define SOVEREIGN_MARKETCACHE_MQH_v4

#include "Config.mqh"
#include "BioState.mqh"

namespace Sovereign {

    // ═══════════════════════════════════════════════════════════════════════════
    // 🌌 QUANTUM REGIMES: THE STATES OF MARKET MATTER
    // ═══════════════════════════════════════════════════════════════════════════
    enum MarketRegimeState {
        REGIME_UNKNOWN,
        REGIME_RANGING,         // Accumulation/Distribution
        REGIME_TRENDING_UP,     // Bullish Expansion
        REGIME_TRENDING_DOWN,   // Bearish Expansion
        REGIME_HYPER_VOLATILE,  // Chaotic Flux
        REGIME_LIQUIDITY_HOLE,  // Vacuum (High Slippage Risk)
        REGIME_QUANTUM_LEAP     // Sudden Structural Break
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // 🧪 MARKET CACHE: THE SENSORY NERVOUS SYSTEM
    // ═══════════════════════════════════════════════════════════════════════════
    class MarketCache {
    public:
        // --- 📡 RAW SENSORY DATA ---
        static double bid, ask, last;
        static double tick_history[200]; // PERFORMANCE: 200 ticks window (2-4s HFT horizon) is optimal
        static int    tick_ptr;
        static ulong  last_tick_ms;
        
        // --- 📊 SYMBOL CACHE (Performance) ---
        static double vol_min;
        static double vol_max;
        
        // --- 🌀 CHAOS & ENTROPY (Market Physics) ---
        static double entropy_index;      // Shanon Entropy (Order vs Chaos)
        static double fractal_dimension;  // Hurst-based complexity
        static double lyapunov_exponent;  // Predictability score
        static double hft_noise_filter;   // HFT Filtering level
        
        // --- ⚛️ QUANTUM METRICS (Flux & Energy) ---
        static double quantum_phase;      // Angular momentum of price
        static double flow_intensity;     // Tick-per-second acceleration
        static double liquidity_pressure; // Bid/Ask depth imbalance
        static double prob_bull_flux;     // Probability of upward drift
        static double prob_bear_flux;     // Probability of downward drift
        
        // --- 🦁 BIOMETRIC SYNC (Organism Awareness) ---
        static MarketRegimeState current_regime;
        static double market_heartbeat;   // Volatility-adjusted frequency
        static double sentiment_osmosis;  // Collective bias absorption
        
        // ═══════════════════════════════════════════════════════════════════════
        // ⚡ PULSE UPDATE: Processing Raw Ticks into Intelligence
        // ═══════════════════════════════════════════════════════════════════════
        static void Update(const MqlTick &tick) {
            bid = tick.bid; ask = tick.ask; last = tick.last;
            
            // Record Temporal Shift
            ulong now_ms = GetTickCount64();
            double delta_time = (double)(now_ms - last_tick_ms) / 1000.0;
            last_tick_ms = now_ms;
            
            // Pulse Heartbeat Calculation (Speed of Market Life)
            // BUG FIX: Ticks simultâneos (delta_time=0) agora geram pico de intensidade (HFT Burst)
            double dt_corrected = MathMax(0.0005, delta_time); // Assume 0.5ms p/ ticks em bloco
            flow_intensity = (flow_intensity * 0.9) + (0.1 / (dt_corrected + 0.001));
            
            // Update Synaptic Buffer
            tick_history[tick_ptr] = last;
            tick_ptr = (tick_ptr + 1) % 200;
            
            // --- 🧪 BIO-QUANTUM ANALYSIS (Throttled 100ms p/ Economia de CPU) ---
            static ulong last_analysis_ms = 0;
            if(now_ms - last_analysis_ms > 100) {
                AnalyzeMicrostructure();
                last_analysis_ms = now_ms;
            }
            SynchronizeOrganism(tick);
        }

        static void AnalyzeMicrostructure() {
            double sum_change = 0, sum_abs_change = 0;
            double high = -1, low = 9999999;
            int count = 0;
            
            double up_energy = 0, down_energy = 0;

            for(int i=0; i<200; i++) {
                if(tick_history[i] <= 0) continue;
                count++;
                if(tick_history[i] > high) high = tick_history[i];
                if(tick_history[i] < low)  low  = tick_history[i];
                
                if(i == tick_ptr) continue; // Skip wrap-around boundary (Oldest vs Newest artifact)
                
                int prev = (i == 0) ? 199 : i - 1;
                if(tick_history[prev] > 0) {
                    double diff = tick_history[i] - tick_history[prev];
                    sum_change += diff;
                    sum_abs_change += MathAbs(diff);
                    
                    if(diff > 0) up_energy += diff * (1.0 + flow_intensity * 0.1);
                    else down_energy += MathAbs(diff) * (1.0 + flow_intensity * 0.1);
                }
            }

            if(count < 50) return;

            double range = (high - low) + 0.000001;
            
            // 🧪 FRACTAL DIMENSION (Efficiency of price movement)
            // Using a simplified Katz Fractal Dimension for real-time speed
            double path_length = sum_abs_change;
            double d_fractal = 1.5; // Default random walk
            
            if(path_length > 0 && range > 0) {
                 double term2 = MathLog(range/path_length);
                 double denom = MathLog(count) + term2;
                 if(denom != 0) d_fractal = MathLog(count) / denom;
            }
            fractal_dimension = (fractal_dimension * 0.95) + (d_fractal * 0.05);
            
            // 🌀 ENTROPY (Chaos Index)
            entropy_index = MathMax(0.0, MathMin(1.0, (fractal_dimension - 1.0) / 0.5));
            
            // ⚛️ QUANTUM PROBABILITIES
            double total_energy = up_energy + down_energy + 0.0000001;
            prob_bull_flux = (up_energy / total_energy);
            prob_bear_flux = (down_energy / total_energy);
            quantum_phase = (prob_bull_flux - 0.5) * 2.0; // Normalized -1 to 1
            
            // 🛡️ NOISE FILTER (HFT Suppression)
            hft_noise_filter = 1.0 - (range / (sum_abs_change + 0.000001));
            
            // 🏛️ REGIME IDENTIFICATION
            if(hft_noise_filter > 0.85 && entropy_index > InpEntropyMax) current_regime = REGIME_HYPER_VOLATILE;
            else if(range > (sum_abs_change * 0.5)) current_regime = REGIME_LIQUIDITY_HOLE; // Vacuum
            else if(prob_bull_flux > InpHurstThreshold && prob_bull_flux > prob_bear_flux) current_regime = REGIME_TRENDING_UP;
            else if(prob_bear_flux > InpHurstThreshold && prob_bear_flux > prob_bull_flux) current_regime = REGIME_TRENDING_DOWN;
            else current_regime = REGIME_RANGING;
        }

        static void SynchronizeOrganism(const MqlTick &tick) {
            ulong now = GetTickCount64();
            // Adjust Organism Heartbeat based on volatility and HFT activity
            market_heartbeat = flow_intensity * (1.0 - entropy_index);
            
            // Sentiment Osmosis (The "feel" of the ticker tape)
            double tick_bias = (tick.last >= tick.ask) ? 1.0 : (tick.last <= tick.bid ? -1.0 : 0);
            sentiment_osmosis = (sentiment_osmosis * 0.99) + (tick_bias * 0.01);
            
            // Biological ATP Feedback (v12.90: dt-proportional to prevent HFT crash)
            if(current_regime == REGIME_HYPER_VOLATILE && flow_intensity > 50) {
                static ulong last_bio_loss = 0;
                if(now - last_bio_loss > 1000) { // Only once per second max
                    BioState::atp_energy -= 0.1; 
                    BioState::consecutive_shocks++;
                    last_bio_loss = now;
                }
            }
            
            // PERFORMANCE BUG FIX: Throttle Ret/Rev (CopyBuffer/History) para 100ms
            static ulong last_ret_rev_ms = 0;
            if(now - last_ret_rev_ms > 100) {
                CalculateRetRev();
                last_ret_rev_ms = now;
            }
        }
        
        // --- 📊 RET/REV ENGINE (Belkhayate Timing Logic) ---
        static double ret_rev_value;
        static int    ret_rev_signal; // 1=BUY, -1=SELL, 0=NEUTRAL

        static void CalculateRetRev() {
            int len = 5;
            static double highs[], lows[], closes[]; // Static Buffers (Zero Allocation)
            // No need to resize, Copy functions handle it or we resize once
            
            if(ArraySize(highs) == 0) { // First run init
               ArrayResize(highs, len); ArrayResize(lows, len); ArrayResize(closes, len);
               ArraySetAsSeries(highs, true); ArraySetAsSeries(lows, true); ArraySetAsSeries(closes, true);
            }
            
            if(CopyHigh(_Symbol, PERIOD_M1, 0, len, highs)<len || 
               CopyLow(_Symbol, PERIOD_M1, 0, len, lows)<len ||
               CopyClose(_Symbol, PERIOD_M1, 0, len, closes)<len) return;
            
            double sum_median = 0;
            double sum_range = 0;
            for(int i=0; i<len; i++) {
                sum_median += (highs[i] + lows[i]) / 2.0;
                sum_range  += (highs[i] - lows[i]);
            }
            
            double mba = sum_median / len;
            double lrange = (sum_range / len) * 0.2;
            
            // BUG FIX (STEP 499): EVITA STALE DATA SE VOLATILIDADE FOR ZERO
            if(lrange == 0) {
                 ret_rev_value = 0;
                 ret_rev_signal = 0;
                 return;
            }
            
            // vclose = (close - mba) / lrange
            ret_rev_value = (closes[0] - mba) / (lrange + 0.00000001);
            
            // Thresholds: +/- 9.0 (Significant Levels)
            if(ret_rev_value >= 9.0) ret_rev_signal = -1; // Overextended Up -> SELL
            else if(ret_rev_value <= -9.0) ret_rev_signal = 1; // Overextended Down -> BUY
            else ret_rev_signal = 0;
        }

        static string GetRegimeName() {
            switch(current_regime) {
                case REGIME_RANGING:         return "STABLE: Accumulation Cycle";
                case REGIME_TRENDING_UP:     return "ESTRUTURAL: Bullish Expansion";
                case REGIME_TRENDING_DOWN:   return "ESTRUTURAL: Bearish Expansion";
                case REGIME_HYPER_VOLATILE:  return "⚠️ CHAOS: High Entropy Phase";
                case REGIME_LIQUIDITY_HOLE:  return "☢️ VACUUM: Critical Slippage Risk";
                case REGIME_QUANTUM_LEAP:    return "⚡ QUANTUM LEAP: Structural Break";
                default:                     return "SYNAPSING: Market Awareness...";
            }
        }
        
        static double GetEntropy() { return entropy_index; }
    };

    // --- STATIC INITIALIZATIONS: The Physical Foundation ---
    double MarketCache::bid = 0;
    double MarketCache::ask = 0;
    double MarketCache::last = 0;
    double MarketCache::tick_history[200] = {0}; // OPT: 200
    int    MarketCache::tick_ptr = 0;
    ulong  MarketCache::last_tick_ms = 0;
    double MarketCache::entropy_index = 0.5;
    double MarketCache::fractal_dimension = 1.5;
    double MarketCache::lyapunov_exponent = 0.5;
    double MarketCache::hft_noise_filter = 0.0;
    double MarketCache::quantum_phase = 0.0;
    double MarketCache::flow_intensity = 0.0;
    double MarketCache::liquidity_pressure = 0.5;
    double MarketCache::prob_bull_flux = 0.5;
    double MarketCache::prob_bear_flux = 0.5;
    double MarketCache::market_heartbeat = 1.0;
    double MarketCache::sentiment_osmosis = 0.0;
    MarketRegimeState MarketCache::current_regime = REGIME_UNKNOWN;
    
    // Initialize New Members
    double MarketCache::ret_rev_value = 0.0;
    int    MarketCache::ret_rev_signal = 0;
    double MarketCache::vol_min = 0.01;
    double MarketCache::vol_max = 100.0;
}

#endif
