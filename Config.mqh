//+------------------------------------------------------------------+
//|                                                   Config.mqh     |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN NEURAL SYSTEM: CONFIG BIOS v10.0       |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_CONFIG_MQH_V4
#define SOVEREIGN_CONFIG_MQH_V4

// ═══════════════════════════════════════════════════════════════════════════
// 🌌 IDENTITY & CORE PROTOCOLS
// ═══════════════════════════════════════════════════════════════════════════
#define AI_NAME             "SOVEREIGN SINGULARITY"
#define AI_CODENAME         "LEGACY SUPREME v10.0"
#define AI_VERSION          "v10.0.0-TITAN-PRIME [GOD-MODE]"
#define ARCHITECTURE        "QUANTUM-GENETIC HYBRID (FLOW STACKING CORE)"

// ═══════════════════════════════════════════════════════════════════════════
// 🧠 NEURAL CORE CONSTANTS (Aggressive Geometry)
// ═══════════════════════════════════════════════════════════════════════════
#define SYNAPTIC_DENSITY      0.98    // Aumentado para maior sensibilidade a micro-padrões
#define FORGETTING_FACTOR     0.9998  // Mantém a memória institucional por mais tempo
#define YIELD_HUNGER_AGGR     0.85    // Multiplicador base de sede por lucro

// ═══════════════════════════════════════════════════════════════════════════
// ⚛️ PHYSICS & HFT TIMING (Atomic Execution)
// ═══════════════════════════════════════════════════════════════════════════
#define QUANTUM_TUNNEL_PROB   0.15    // Maior probabilidade de aceitar riscos calculados
#define TICK_EXHAUST_MS       250     // Janela atômica para sensor de exaustão
#define MAX_B3_LATENCY_MS     2000    // Latência máxima tolerada (B3 Tuning - ajustado para ambiente real)

// ═══════════════════════════════════════════════════════════════════════════
// 🛡️ SYSTEM SECURITY & DEFAULTS
// ═══════════════════════════════════════════════════════════════════════════
#define IMMUNE_RECOVERY_TIME  3600    // Reduzido para 1 hora (Recuperação rápida Berserker)
#define MAX_B3_SLIPPAGE       15.0    // Aumentado para garantir entrada em alta volatilidade

// ═══════════════════════════════════════════════════════════════════════════
// 🎨 CYBER-CORE AESTHETICS (PREDATOR UI TOKENS)
// ═══════════════════════════════════════════════════════════════════════════
#define CLR_NEON_GREEN        (color)C'0,255,160'
#define CLR_NEON_CYAN         (color)C'0,220,255'
#define CLR_NEON_RED          (color)C'255,20,60'  // Vermelho mais agressivo
#define CLR_PREDATOR_PINK      (color)C'255,0,180'  // Nova cor para Yield Predator
#define CLR_CYBER_VOLT        (color)C'200,255,0'  // Amarelo neon ultra-vibrante
#define CLR_GLOW_INTENSITY    220                  // Maior brilho nos sensores
#define CLR_VANTABLACK        (color)C'2,2,4'     
#define CLR_WARNING           (color)C'255,100,0' 
#define CLR_WHITE             (color)C'250,250,255'

// ═══════════════════════════════════════════════════════════════════════════
// ⏰ TEMPORAL CONSTRAINTS (B3 2026 SINC)
// ═══════════════════════════════════════════════════════════════════════════
#define B3_OPEN_TIME          "09:01" // Atraso de 1min para evitar leilão instável
#define B3_CLOSE_GUARD        "17:50"
#define NYSE_SYNC_OPEN        "10:30"
#define LUNCH_PAUSE_START     "12:00"
#define LUNCH_PAUSE_END       "13:00"

// NOTE: All Strategy, Biology, and Risk parameters are now Unified
// in the EA Input section for full real-time control.
// ═══════════════════════════════════════════════════════════════════════════
// 🌉 MQL4 COMPATIBILITY BRIDGE (ANTIGRAVITY v2026)
// Helpers to resolve MQL4-style calls in MQL5 environments.
// ═══════════════════════════════════════════════════════════════════════════
inline double   mql4_iHigh(string s, ENUM_TIMEFRAMES p, int i)   { double r[1]; return(CopyHigh(s,p,i,1,r)>0?r[0]:0); }
inline double   mql4_iLow(string s, ENUM_TIMEFRAMES p, int i)    { double r[1]; return(CopyLow(s,p,i,1,r)>0?r[0]:0); }
inline double   mql4_iClose(string s, ENUM_TIMEFRAMES p, int i)  { double r[1]; return(CopyClose(s,p,i,1,r)>0?r[0]:0); }
inline double   mql4_iOpen(string s, ENUM_TIMEFRAMES p, int i)   { double r[1]; return(CopyOpen(s,p,i,1,r)>0?r[0]:0); }
inline double   mql4_iVolume(string s, ENUM_TIMEFRAMES p, int i) { long r[1]; return(CopyTickVolume(s,p,i,1,r)>0?(double)r[0]:0); }
inline datetime mql4_iTime(string s, ENUM_TIMEFRAMES p, int i)   { datetime r[1]; return(CopyTime(s,p,i,1,r)>0?r[0]:0); }

#define iHigh(s,p,i)   mql4_iHigh(s,p,i)
#define iLow(s,p,i)    mql4_iLow(s,p,i)
#define iClose(s,p,i)  mql4_iClose(s,p,i)
#define iOpen(s,p,i)   mql4_iOpen(s,p,i)
#define iVolume(s,p,i) mql4_iVolume(s,p,i)
#define iTime(s,p,i)   mql4_iTime(s,p,i)

// Helper functions for Time extraction (MQL4 style)
inline int TimeHour(datetime t)   { MqlDateTime dt; TimeToStruct(t, dt); return dt.hour; }
inline int TimeMinute(datetime t) { MqlDateTime dt; TimeToStruct(t, dt); return dt.min; }
inline int TimeSeconds(datetime t) { MqlDateTime dt; TimeToStruct(t, dt); return dt.sec; }

// Helper function for RSI values (MQL4 style)
inline double mql4_iRSI(string s, ENUM_TIMEFRAMES p, int per, int price, int shift=0) {
   int h = iRSI(s,p,per,(ENUM_APPLIED_PRICE)price); double r[1]; 
   if(CopyBuffer(h,0,shift,1,r)>0) { IndicatorRelease(h); return r[0]; }
   IndicatorRelease(h); return 50.0;
}

// Helper function for ATR values (MQL4 style)
inline double mql4_iATR(string s, ENUM_TIMEFRAMES p, int per, int shift=0) {
   int h = iATR(s,p,per); double r[1];
   if(CopyBuffer(h,0,shift,1,r)>0) { IndicatorRelease(h); return r[0]; }
   IndicatorRelease(h); return 0.0;
}

#endif
