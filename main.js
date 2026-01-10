/**
 * PREDATOR v23.0 SENTINEL AGILITY - Frontend Engine
 * 100% CLOUD | Zero Local | Custo Zero
 * 
 * Fluxo: TradingView → Render API → Este Dashboard
 */

// ============================================================
// CONFIGURAÇÃO CLOUD (Substitua pela URL real do Render)
// ============================================================
const CONFIG = {
    // Detecta se está rodando localmente (127.0.0.1 ou localhost)
    // Se sim, usa a API local. Se não, usa a API de Produção (Render)
    API_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? "http://127.0.0.1:8000"
        : "https://predador-api.onrender.com", // API REAL (Render)

    // Frequência de atualização do dashboard (ms)
    SYNC_INTERVAL_MS: 500,

    // Supabase (opcional - para persistência)
    SUPABASE_URL: "https://sua-url.supabase.co",
    SUPABASE_KEY: "sua-chave-anonima"
};

// ============================================================
// ESTADO GLOBAL
// ============================================================
let lastSyncTime = 0;
let isOnline = false;
let syncErrors = 0;

// Cache de elementos DOM (Performance)
const DOM = {};

// ============================================================
// INICIALIZAÇÃO
// ============================================================
// ============================================================
// chart.js integration
// ============================================================
let chart;
let series;
let currentCandle = null;
let candleInterval = 60; // 1 minuto por candle simulado no front (ou sincronizado)

function initChart() {
    const chartContainer = document.getElementById('main-chart');
    chartContainer.innerHTML = ''; // Limpar placeholder

    chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: chartContainer.clientHeight,
        layout: {
            background: { type: 'solid', color: 'transparent' },
            textColor: '#8b949e',
        },
        grid: {
            vertLines: { color: 'rgba(255, 255, 255, 0.05)' },
            horzLines: { color: 'rgba(255, 255, 255, 0.05)' },
        },
        timeScale: {
            timeVisible: true,
            secondsVisible: true,
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
    });

    // 🕯️ APEX SCALPER: Candlestick Series Real
    series = chart.addCandlestickSeries({
        upColor: '#00ff9d',
        downColor: '#ff0055',
        borderVisible: false,
        wickUpColor: '#00ff9d',
        wickDownColor: '#ff0055',
    });

    // Responsividade
    window.addEventListener('resize', () => {
        chart.resize(chartContainer.clientWidth, chartContainer.clientHeight);
    });
}

// ============================================================
// INICIALIZAÇÃO DOM
// ============================================================
function initDOM() {
    DOM.bigPrice = document.getElementById('big-price');
    DOM.probValue = document.querySelector('.prob-value');
    DOM.pnlValue = document.querySelector('.stats-grid .stat-box:nth-child(1) h3');
    DOM.winRate = document.querySelector('.stat-box:nth-child(2) h3');
    DOM.tradesCount = document.querySelector('.stat-box:nth-child(3) h3');
    DOM.flowBar = document.getElementById('flow-bar');
    DOM.statusPill = document.querySelector('.status-pill');
    DOM.feedLog = document.getElementById('feed');
    DOM.regimeLabel = document.querySelector('.regime-label');
    DOM.assetSymbol = document.getElementById('asset-symbol');
    DOM.inertiaVal = document.getElementById('inertia-val');
    DOM.entropyVal = document.getElementById('entropy-val');
    DOM.corrVal = document.getElementById('corr-val');
    DOM.hunterPill = document.getElementById('hunter-pill');
    DOM.homeostasisVal = document.getElementById('homeostasis-val');
    DOM.adrenalineVal = document.getElementById('adrenaline-val');
    DOM.firingVal = document.getElementById('firing-val');

    // Iniciar Gráfico
    initChart();
}

// ============================================================
// SYNC DASHBOARD - Conexão com API Cloud
// ============================================================
async function syncDashboard() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(`${CONFIG.API_URL}/state`, {
            method: 'GET',
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();
        isOnline = true;
        lastSyncTime = Date.now();
        syncErrors = 0;

        updateUI(data);

    } catch (e) {
        syncErrors++;
        isOnline = false;

        if (DOM.statusPill) {
            const statusText = syncErrors < 10 && syncErrors > 0
                ? `WAKING UP THE BEAST... (booting ${syncErrors})`
                : `CLOUD: OFFLINE (retry ${syncErrors})`;

            DOM.statusPill.innerHTML = `
                <div style="background:var(--neon-pink)" class="dot"></div> 
                ${statusText}
            `;
        }

        // Retry mais lento se muitos erros (evitar spam enquanto boota)
        const delay = syncErrors < 10 ? 1000 : 3000;
        await new Promise(r => setTimeout(r, delay));
    }
}

async function syncSupervisor() {
    try {
        const response = await fetch('/api/supervisor');
        if (response.ok) {
            const data = await response.json();
            console.log("🛡️ SUPERVISOR REPORT:", data);

            if (DOM.statusPill) {
                const existing = DOM.statusPill.innerHTML;
                if (!existing.includes('🛡️')) {
                    DOM.statusPill.innerHTML += ` <span style="color:var(--neon-blue)">🛡️ SUP: ${data.ai_recommendation}</span>`;
                }
            }
        }
    } catch (e) {
        console.warn("Supervisor silent.");
    }
}

// ============================================================
// UPDATE UI - Atualização Visual
// ============================================================
function updateUI(data) {
    // Preço
    const price = data.price || data.last_price || 0;
    if (price > 0) {
        if (DOM.bigPrice) DOM.bigPrice.innerText = price.toLocaleString('pt-BR');

        // Atualizar Gráfico (Lógica de Candle Building)
        if (series) {
            const now = Math.floor(Date.now() / 1000);

            // Se não tem candle ou mudou o minuto, cria um novo
            if (!currentCandle || now >= currentCandle.time + 60) {
                currentCandle = {
                    time: Math.floor(now / 60) * 60, // Arredonda para o minuto exato
                    open: price,
                    high: price,
                    low: price,
                    close: price
                };
            } else {
                // Atualiza candle existente
                currentCandle.close = price;
                currentCandle.high = Math.max(currentCandle.high, price);
                currentCandle.low = Math.min(currentCandle.low, price);
            }

            series.update(currentCandle);

            // Plotar Trades como Marcadores
            if (data.trade_log && data.trade_log.length > 0) {
                const recentTrades = data.trade_log.filter(t => {
                    // Filtrar trades recentes (ex: últimos 5 minutos) para não poluir
                    // Assumindo que o timestamp vem no formato HH:MM:SS, teríamos que converter.
                    // Para simplificar, vou plotar o ÚLTIMO trade se ele acabou de acontecer.
                    return true;
                });

                // Mapear trades para marcadores
                const markers = [];
                // Por limitação de complexidade de tempo aqui, vamos adicionar apenas um marcador
                // se o last_order for recente.
                if (data.last_order && data.last_order.time) {
                    const isBuy = data.last_order.action === "BUY";
                    markers.push({
                        time: currentCandle.time,
                        position: isBuy ? 'belowBar' : 'aboveBar',
                        color: isBuy ? '#00ff9d' : '#ff0055',
                        shape: isBuy ? 'arrowUp' : 'arrowDown',
                        text: isBuy ? 'BUY' : 'SELL',
                    });
                    series.setMarkers(markers);
                }
            }
        }
    }

    // Confiança da IA
    if (DOM.probValue) {
        const prob = data.prob || data.confidence || 0;
        DOM.probValue.innerText = `${prob.toFixed(1)}%`;
        DOM.probValue.style.color = prob >= 80 ? 'var(--neon-green)' :
            prob >= 60 ? 'var(--neon-blue)' : 'var(--neon-pink)';
    }

    // Regime
    if (DOM.regimeLabel) {
        const regime = data.regime || 'WAITING';
        DOM.regimeLabel.innerText = regime;
        DOM.regimeLabel.style.color = regime === 'ACTIVE' ? 'var(--neon-green)' :
            regime === 'OFFLINE' ? 'var(--neon-pink)' : 'var(--neon-yellow)';
    }

    // PnL
    if (DOM.pnlValue) {
        const pnl = data.pnl || data.daily_pnl || 0;
        DOM.pnlValue.innerText = `R$ ${pnl.toLocaleString('pt-BR')}`;
        DOM.pnlValue.style.color = pnl >= 0 ? 'var(--neon-green)' : 'var(--neon-pink)';
    }

    // Win Rate
    if (DOM.winRate) {
        DOM.winRate.innerText = `${(data.win_rate || 0).toFixed(1)}%`;
    }

    // Trades
    if (DOM.tradesCount) {
        DOM.tradesCount.innerText = data.trades || 0;
    }

    // Flow Bar
    if (DOM.flowBar) {
        const obp = data.obp || 0; // Usar OBP real para o fluxo
        const width = Math.max(5, Math.min(95, 50 + (obp * 50)));
        DOM.flowBar.style.width = `${width}%`;
        DOM.flowBar.style.background = obp > 0 ? 'var(--neon-green)' : 'var(--neon-pink)';
    }

    if (DOM.inertiaVal) {
        DOM.inertiaVal.innerText = (data.kinetic || 0).toFixed(4);
    }

    if (DOM.entropyVal) {
        DOM.entropyVal.innerText = (data.entropy || 0).toFixed(2);
        DOM.entropyVal.style.color = (data.entropy || 0) > 3 ? 'var(--neon-pink)' : 'var(--neon-blue)';
    }

    if (DOM.corrVal) {
        const synced = data.is_correlated;
        DOM.corrVal.innerText = synced ? 'SYNCED' : 'DISC';
        DOM.corrVal.style.color = synced ? 'var(--neon-green)' : 'var(--neon-pink)';
    }

    if (DOM.hunterPill) {
        const hunting = data.is_hunting;
        DOM.hunterPill.innerText = hunting ? 'HUNTING' : 'IDLE';
        DOM.hunterPill.style.color = hunting ? 'var(--neon-purple)' : 'var(--text-dim)';
        DOM.hunterPill.style.borderColor = hunting ? 'var(--neon-purple)' : 'var(--text-dim)';
    }

    if (DOM.assetSymbol && data.last_order && data.last_order.symbol) {
        DOM.assetSymbol.innerText = `${data.last_order.symbol} • NOMAD-INFINITY HUNTER`;
    }

    // Neuro-Biometrics
    if (DOM.homeostasisVal) {
        DOM.homeostasisVal.style.width = `${data.homeostasis || 100}%`;
    }
    if (DOM.adrenalineVal) {
        DOM.adrenalineVal.style.width = `${(data.adrenaline || 0) * 100}%`;
    }
    if (DOM.firingVal) {
        DOM.firingVal.innerText = `${(data.synaptic_firing || 0).toFixed(0)}Hz`;
    }

    // Status e Escudo APEX V16.0
    if (DOM.statusPill) {
        const lockIcon = data.is_locked ? ' 🔒' : '';
        const huntIcon = data.is_hunting ? ' 🎯' : '';
        const whaleIcon = data.whale ? ' 🐋 W-ALERT' : '';
        const trapText = data.trap_detected ? ' <span style="color:var(--neon-pink)">[TRAP DETECTED]</span>' : ' [SHIELD ACTIVE]';

        DOM.statusPill.innerHTML = `
            <div class="dot" style="background:${data.is_locked ? 'var(--neon-pink)' : 'var(--neon-green)'}"></div> 
            APEX: ${data.regime || 'ACTIVE'}${lockIcon}${huntIcon}${whaleIcon}${trapText}
        `;
    }

    // Feed de Trades
    if (DOM.feedLog && data.trade_log && data.trade_log.length > 0) {
        DOM.feedLog.innerHTML = data.trade_log.slice(0, 8).map(t =>
            `<div style="margin-bottom:4px;">[${t.time}] <span style="color:${t.action === 'BUY' ? 'var(--neon-green)' : 'var(--neon-pink)'}">${t.action}</span> | ${t.symbol} | CONF: ${t.confidence}%</div>`
        ).join('');
    } else if (DOM.feedLog && (!data.trade_log || data.trade_log.length === 0)) {
        DOM.feedLog.innerHTML = `
            <div style="color: var(--text-dim);">
                🎯 Aguardando sinais do TradingView...<br>
                📡 API conectada: ${CONFIG.API_URL.split('//')[1]}
            </div>
        `;
    }
}

// ============================================================
// INICIAR ENGINE
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    console.log("🦅 PREDATOR v21.2 | APEX MUTATION");
    console.log(`📡 API: ${CONFIG.API_URL}`);

    initDOM();

    // Primeira sync imediata
    syncDashboard();

    // Loop de alta frequência
    setInterval(syncDashboard, CONFIG.SYNC_INTERVAL_MS);

    // Supervisor a cada 30 segundos (Serverless economiza)
    setInterval(syncSupervisor, 30000);
    syncSupervisor();

    console.log("✅ PREDATOR v21.2 | CLOUD SYSTEMS ONLINE");
});

// ============================================================
// API PÚBLICA & ACTIONS
// ============================================================
window.PREDATOR = {
    getConfig: () => CONFIG,
    isOnline: () => isOnline,
    forceSync: syncDashboard,
    getLastSync: () => lastSyncTime
};

// Expor função de Pânico para o HTML
window.terminateAll = async function () {
    if (!confirm('⚠️ PERIGO: ISSO VAI FECHAR TODAS AS POSIÇÕES E PARAR O ROBÔ.\n\nDeseja continuar?')) return;

    const btn = document.querySelector('.btn-panic');
    const originalText = btn.innerText;
    btn.innerText = "ENVIANDO...";
    btn.style.background = "#555";

    try {
        const response = await fetch(`${CONFIG.API_URL}/command/panic`, {
            method: 'POST'
        });

        if (response.ok) {
            alert('🚨 COMANDO ENVIADO COM SUCESSO!\n\nO robô irá encerrar tudo na próxima sincronia (máx 1 seg).');
            btn.innerText = "ATIVA PÂNICO (ATIVADO)";
            btn.style.background = "var(--bg-deep)";
            btn.style.border = "2px solid var(--neon-pink)";
        } else {
            throw new Error('Falha no envio');
        }
    } catch (e) {
        alert('❌ ERRO AO ENVIAR COMANDO DE PÂNICO!\nVerifique sua internet ou a API.');
        btn.innerText = originalText;
        btn.style.background = ""; // Reset
    }
};
