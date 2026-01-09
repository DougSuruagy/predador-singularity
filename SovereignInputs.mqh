//+------------------------------------------------------------------+
//|                                              SovereignInputs.mqh |
//|                                  Copyright 2026, Antigravity AI  |
//|                 SOVEREIGN UNIFIED PARAMETERS: SINGULARITY v10.0  |
//+------------------------------------------------------------------+
#property strict

#ifndef SOVEREIGN_INPUTS_MQH
#define SOVEREIGN_INPUTS_MQH

// ═══════════════════════════════════════════════════════════════════════════
// 📜 TODOS OS PARÂMETROS UNIFICADOS (FUSION EDITION V1000)
// ═══════════════════════════════════════════════════════════════════════════

// --- SEÇÃO 1: FILOSOFIA NANO-PREDADOR & CONTROLE ---
input group "🔌 NÚCLEO SUPREMO (MASTER CONTROL)"
input bool     InpWakeUpSupreme      = true;           // Acordar o Predador? (B3 Supreme)
input bool     InpFullAutonomy       = true;           // Autonomia Total (AI Decision Mode)
input ulong    InpMagicNumber        = 2496797;        // 01 Assinatura Neural (Magic Number)
input double   InpInitialCapital     = 200.0;          // Capital Inicial Real (R$)
input double   InpDailyProfitTarget  = 500.0;          // 🎯 Meta de Lucro Diário (R$)
input double   InpDailyLossLimit     = 300.0;          // 🛑 Limite de Perda Diário (R$)
input double   InpVirtualMagnification = 100.0;        // 🦁 FILOSOFIA: Magnificação (200 = 20.000)
input double   InpLotScalingFactor   = 0.1;            // 🦁 FILOSOFIA: Escala de Lote (1 = 0.1)
input string   InpUniversalGrid      = "WIN$N,WDO$N";  // Grade de Ativos (Separados por vírgula)

// --- SEÇÃO 1.5: CONTROLE DE BANCA QUANTUM (JUROS COMPOSTOS) ---
input group "🏦 CONTROLE DE BANCA QUANTUM (Compound Interest)"
input bool     InpCompoundActive      = true;           // Ativar Juros Compostos?
input double   InpDailyTargetPct      = 2.0;            // Meta de Lucro Real p/ dia (%)
input double   InpB3CostPerLot        = 0.60;           // Custo Realista B3 (R$ 0.60/lote c/ taxas)
input double   InpLeveragePower       = 1.5;            // Poder de Alavancagem (1.0=Cons., 5.0+ Agressivo)
input double   InpMinCapitalPerLot    = 100.0;          // Capital Mínimo exigido por 1 Mini (R$)
input bool     InpAutoScalingActive   = true;           // Aumentar lotes automaticamente conforme banca cresce?

// --- SEÇÃO 2: GESTÃO DE CAPITAL (BANKROLL) ---
input group "💰 GESTÃO DE CAPITAL (Money)"
input double   InpDailyLossPct       = 100.0;          // 💀 LIBERADO: Risco Total
input double   InpProfitTargetPct    = 10.0;           // Meta de Lucro Diária (%)
input double   InpRiskPerTrade       = 5.0;            // 5% Risco por Trade
input double   InpBaseLotUnit        = 1.0;            // Lote Base = 1
input double   InpMaxLotSize         = 50.0;           // Lote Máximo (Teto Absoluto)
input double   InpCapitalPerLot      = 200.0;          // Capital por Lote (R$) - Para juros compostos
input double   InpTargetProfit       = 10.0;           // Meta de Lucro em R$ por Operação
input double   InpSatietyGoal        = 10000.0;        // Meta de Sobrevivência/Saciedade (R$)
input bool     InpForceBerserk       = true;           // 💀 FORÇAR MODO BERSERK (Sem Medo)
input bool     InpZeroBrokerage      = true;           // Corretagem Zero Ativa?
input bool     InpBioLeverageActive  = true;           // Alavancagem Biológica Ativa?
input double   InpWinStreakBonusTh   = 2.0;            // Threshold de Bonus (Facilitado)
input double   InpSwingTrendThresh   = 1.5;            // Threshold de Tendência (Mais sensível)
input bool     InpMLAdaptive         = true;           // Aprendizado Máquina Adaptativo?

// --- SEÇÃO 3: PROTEÇÃO & RISCO (RISK SHIELD) ---
input group "🛡️ ESCUDO OMEGA (Defesa)"
input double   InpPortfolioRiskLimit = 5000.0;         // 💰 Limite de Risco Portfólio ($) - Aumentado
input int      InpMaxConcurrentPositions = 20;         // 🔢 Limite de Posições (PIRÂMIDE LIBERADA)
input double   InpStopLoss           = 300.0;          // 🛑 Stop Loss (Pips/Points)
input double   InpMaxDrawdownPercent = 95.0;           // 💀 Drawdown Máximo (Quase total)
input double   InpEquityStopFloor    = 50.0;           // Piso Mínimo (Sobrevibência final)
input int      InpConsecutiveLossLimit = 3;            // Limite de Erros Consecutivos (Cooldown)
input int      InpCooldownMinutes    = 30;             // Minutos de Pausa após Stop
input double   InpMaxSlippageAllowed = 5.0;            // Slippage Máximo (Deslizamento)
input double   InpMaxSpread          = 35.0;           // Spread Máximo Permitido (Pips/Points)
input bool     InpParanoidRisk       = true;           // Modo Paranóico (Proteção Extrema)
input bool     InpHolidayDodge       = false;          // Fugir de Feriados e Baixa Liquidez (Desativado p/ Teste)
input bool     InpNewsDodge          = true;           // Desvia de Notícias de Alto Impactos
input bool     InpAutoHibernate      = true;           // Hibernação Automática após Drawdown
input bool     InpAntiMartingale     = false;          // Anti-Martingale (Desativado: Mantém Pressão)
input double   InpMaxExposure        = 30.0;           // Exposição Máxima por Ativo (%)
input bool     InpAutoLiquidation    = true;           // Liquidação automática no fim do dia?
input bool     InpAllowNightTrading  = false;          // Permitir operações fora do horário core?
input int      InpMaxSlippagePoints  = 10;             // Slippage máximo em pontos

// --- SEÇÃO 4: ESTRATÉGIAS & EXECUÇÃO (STRATEGY ENGINE) ---
input group "🚀 NÚCLEO ESTRATÉGICO (Execution)"
input double   InpTargetPoints       = 800.0;          // Alvo Padrão (TP: 800)
input double   InpStopPoints         = 300.0;          // Stop Loss Padrão (SL: 300)
input bool     InpDynamicTrailing    = true;           // Trailing Stop Dinâmico (ATR)
input double   InpTrailingStart      = 50.0;           // Gatilho do Trailing (Pontos)
input double   InpTrailingStep       = 20.0;           // Passo do Trailing (Pontos)
input bool     InpUseDivineBreakeven = true;           // ⚡ Ativar Divine Breakeven (Lightning Fast)
input double   InpBreakevenTrigger   = 35.0;           // ⚡ Gatilho do Breakeven (Pontos)
input bool     InpFlowStacking       = true;           // 🚀 Habilitar Flow Stacking (Pirâmide)
input bool     InpSmartOrderSplit    = false;          // Fragmentação (Desativado: 1 Lote Indivisível)
input bool     InpMultipleTP         = false;          // Saídas Parciais (Desativado: Saída Única)
input double   InpTP1_Percent        = 30.0;           // % do Lote para TP1
input double   InpTP2_Percent        = 40.0;           // % do Lote para TP2
input double   InpTP3_Percent        = 30.0;           // % do Lote para TP3
input bool     InpProTrend           = false;          // Operar APENAS a favor da Tendência? (Não: Opera em tudo)
input bool     InpBreathingMode      = false;          // Modo Respiração (Desativado)
input bool     InpWaitPullback       = false;          // Aguardar Pullback (Desativado: Rompimento Direto)

// --- SEÇÃO 5: SENSORES DE MERCADO (MARKET SENSORS) ---
input group "🐋 SENSORES DE BALEIA (Flow & Volume)"
input bool     InpWhaleTracker       = false;           // Rastrear Grandes Players (Desativado p/ Scalp)
input bool     InpUseGlobalSensors   = true;           // Usar Sensores Globais (S&P500, DXY, VIX)?
input int      InpMinWhaleVolumeDOM  = 500;            // Volume Mínimo no Book (Lotes)
input double   InpAbsorptionThresh   = 2.0;            // Fator de Absorção (2x média)
input bool     InpCorrelationRealtime = true;           // Sincronia WIN x WDO (Real-time)
input bool     InpFootprintAnalysis  = true;           // Analisar Fluxo de Agressão
input bool     InpTickPressureGauge  = true;           // Gauge de Pressão de Ticks (HUD)
input int      InpTickPressureWindow = 50;             // Janela de Ticks p/ Pressão
input double   InpVolumeImbThreshold = 1.5;            // Threshold de Desequilíbrio de Volume

input group "🐋 SENSIBILIDADE BALEIAS (Whale Tuning)"
input double   InpWhaleIntentFilter  = 0.30;           // Filtro de Intenção (0.1 Sensível - 0.7 Conservador)
input double   InpWhaleImbalanceTh   = 0.45;           // Threshold de Desequilíbrio Tick Flow
input double   InpWhaleAbsFlowTh     = 0.40;           // Threshold de Fluxo p/ Absorção
input int      InpWhaleAbsDistPoints = 150;            // Distância Máxima p/ Detectar Absorção (Pts)

input group "⚡ VELOCITY DIVERGENCE (Exhaustion Tuning)"
input double   InpVelDivAvgThreshold = 2.0;            // Vel. Média Mínima p/ considerar Spike
input double   InpVelDivSlowdownPct  = 0.4;            // % de Slowdown p/ Gatilho (0.4 = 40% da média)
input double   InpVelDivSignalWeight = 1.0;            // Peso do Veto/Sinal de Exaustão (0.1 a 5.0)

// --- SEÇÃO 6: HARDWARE BIOLÓGICO & ML ---
input group "🧠 CÓRTEX E SETPOINTS (Biological BIOS)"
input bool     InpSentientAI         = true;           // Habilitar IA Senciente?
input double   InpDopamineReward     = 0.50;           // Recompensa de Dopamina (Vício em Vitória)
input double   InpCortisolSpike      = 0.10;           // Pico de Cortisol (Sem Medo)
input double   InpHomeostasisRate    = 0.001;          // Taxa de Retorno ao Equilíbrio
input double   InpRehabThresholdATP  = 30.0;           // Mínimo de Energia p/ Operar (ATP)
input double   InpPlasticityIndex    = 0.08;           // Velocidade de Aprendizado (ML)
input double   InpConsciousnessFloor = 0.30;           // Nível Mínimo de Clareza Neural
input bool     InpDreamPruning       = true;           // Poda Sináptica Automática (Sono)
input bool     InpVirusMutantMode    = true;           // Habilitar Mutação Viral (CRISPR Evolution)

input group "🦠 MODO VÍRUS (Stop-Loss Hunting)"
input double   InpVirusThreshold     = 0.75;           // Threshold de Ativação do Vírus (0-1)
input double   InpVirusAggression    = 3.0;            // Multiplicador de Lote em Modo Vírus
input int      InpVirusTargetZone    = 180;            // Raio de Caça (Pontos perto de Topo/Fundo)
input bool     InpVirusFearless      = true;           // Zerar Cortisol durante a Infecção?

input group "⚛️ FÍSICA E ENTROPIA (Quantum Engine)"
input double   InpEntropyMax          = 1.0;            // Entropia Máxima Permitida (Total)
input double   InpHurstThreshold      = 0.55;           // Filtro de Tendência (Dominância > 50%)
input double   InpFractalDimension    = 1.0;            // Mínima Complexidade
input double   InpHFTNoiseFilter      = 0.05;           // Filtro de Ruído (Mínimo)
input bool     InpQuantumAnalysis     = true;           // Análise de Fluxo Quântico Ativa

// --- SEÇÃO 7: FILTROS & INDICADORES (INDICATORS) ---
input group "📊 FILTROS TÉCNICOS (Oracle)"
input int      InpRSI_Period         = 2;              // Período RSI (Instântaneo)
input int      InpRSI_Overbought     = 70;             // Nível de Sobrecompra RSI (Conservador)
input int      InpRSI_Oversold       = 30;             // Nível de Sobrevenda RSI (Conservador)
input int      InpBB_Period          = 10;             // Período Bollinger (Rápido)
input double   InpBB_Deviation       = 1.0;            // Desvio Bollinger (Frenético)
input int      InpATR_Period         = 7;              // Período do ATR
input int      InpADX_Period         = 7;              // Período do ADX
input double   InpADX_Threshold      = 5.0;            // Limiar de ADX (Qualquer movimento opera)
input bool     InpUseRenkoFilter     = false;          // Filtro Renko (Desativado)
input double   InpRenkoBrickSize     = 10.0;           // Tamanho do Tijolo Renko
input bool     InpUseICTConcepts     = false;          // Usar ICT (Desativado p/ mais velocidade)
input bool     InpUsePivotPoints     = false;          // Usar Pivot Points (Desativado)
input bool     InpUseFibonacci        = false;          // Usar Níveis Fibonacci (Desativado)
input bool     InpDeltaDivergence     = false;          // Scanner de Divergência de Delta (Desativado)

// --- SEÇÃO 8: HORÁRIOS & CALENDÁRIO (TIME CONTROL) ---
input group "⏰ CONTROLE TEMPORAL (Time)"
input string   InpStartTime          = "09:05";        // Início das Operações
input string   InpEndTime            = "17:30";        // Fim das Operações
input string   InpLunchStart         = "12:00";        // Início do Almoço
input string   InpLunchEnd           = "13:00";        // Fim do Almoço
input bool     InpEconomicCalendarAware = false;        // Evitar Notícias (Desativado p/ Scalp)
input int      InpPreEventMinutes    = 10;             // Minutos antes da notícia
input bool     InpAvoidLunch         = false;           // Evitar Horário de Almoço (Desativado)
input bool     InpUSAOpenSync         = true;          // Sincronia com Abertura NYSE (10:30)
input bool     InpB3HolidayAware      = true;          // Detectar Feriados B3

// --- SEÇÃO 9: OPEN RANGE BREAKOUT (ORB CORE) ---
input group "🏹 OPEN RANGE BREAKOUT (ORB)"
input string   InpORBSessionMinutes  = "15";           // ORB: Minutos do Intervalo (5, 15, 30, ou 0=Custom)
input string   InpORBCustomTime      = "09:30-09:45";  // ORB: Horário Customizado (HH:MM-HH:MM)
input bool     InpORBAlertBreakOnly  = false;          // ORB: Alertar apenas Rompimento Confirmado
input bool     InpORBShowLabels      = true;           // ORB: Exibir Rótulos de Metas
input bool     InpORBShowPrevDay     = true;           // ORB: Exibir ORBs de Dias Anteriores
input bool     InpORBShowEntries     = true;           // ORB: Habilitar Marcadores de Entrada
input bool     InpORBShowTargets     = true;           // ORB: Exibir Metas (50% e 100%)
input bool     InpORBShowExtended    = false;          // ORB: Exibir Metas Estendidas (150%-500%)
input bool     InpORBShowMidpoint    = false;          // ORB: Exibir Ponto Médio (Pivô)
input bool     InpORBShowShadedBox   = true;           // ORB: Exibir Retângulo Sombreado
input color    InpORBShadeColor      = clrTeal;        // ORB: Cor do Box Sombreado
input color    InpORB50Color         = clrPurple;      // ORB: Cor Metas 50%
input color    InpORB100Color        = clrBlue;        // ORB: Cor Metas 100%
input color    InpORBOtherColor      = clrTeal;        // ORB: Cor Metas Estendidas
input int      InpORBLabelOffsetBars = 5;              // ORB: Offset dos Rótulos (Barras)
input int      InpORBMaxLineBars     = 500;            // ORB: Comprimento Máximo das Linhas

// --- SEÇÃO 10: VISUALIZAÇÃO (HUD & UX) ---
input group "🎨 SUPRA INTERFACE (Visual)"
input bool     InpShowHUD            = true;           // Exibir HUD 8K
input bool     InpHUDHalfHeight      = true;           // [Visual] HUD em Modo Compacto (50% do ecrã)
input bool     InpShowChartLevels    = true;           // Desenhar Níveis no Gráfico?
input int      InpUI_Transparency    = 220;            // Transparência (0-255)
input color    InpUI_ThemeColor      = C'0,255,100';   // Cor Tema (Neon Green)
input int      InpHUD_X              = 10;             // Posição X do HUD
input int      InpHUD_Y              = 50;             // Posição Y do HUD
input color    InpUI_Main            = C'0,255,100';   // Cor de Apex (Neon Green)
input color    InpUI_Accent          = C'255,0,50';    // Cor de Alerta (Cyber Red)
input color    InpUI_Background      = C'2,2,5';       // Vanta Black (Profundidade)

input group "📜 REGISTRO & LOGS (System)"
input bool     InpAutoBackupDNA       = true;           // Backup Automático do DNA
input bool     InpExpertInsight       = true;           // Insights de Especialista no Log
input int      InpLogLevel           = 2;              // Nível de Log (0-2)
input bool     InpSaveMLData         = true;           // Salvar Dados de ML
input string   InpDNAFilename        = "supreme_dna.bin"; // Arquivo de DNA

// --- SEÇÃO 7: SINGULARITY v7 (Black Swan & Global Sync) ---
input group "🛸 SINGULARIDADE v7 (Super-Sensores)"
input bool     InpBlackSwanProtection = true;          // Ativar Proteção contra Eventos Cisne Negro
input double   InpAnomalousVolatility = 3.5;           // Sensibilidade Cisne Negro (Multiplicador ATR)
input bool     InpGlobalSymbolSync    = true;          // Sincronia Multi-Ativos (Ex: WIN vs WDO)
input string   InpGlobalSyncSymbols   = "WDO$N";       // Ativo de Correlação Principal
input double   InpMinCorrelationReq   = 0.60;          // Correlação Mínima Necessária (-1 a 1)

#endif
