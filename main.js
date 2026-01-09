/**
 * PREDATOR v13.0 SINGULARITY - Frontend Engine
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
        : "https://predator-api-SEU-ID.onrender.com", // <--- EDITE AQUI PARA PRODUÇÃO

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
let candleSeries;
let areaSeries; // Usar area para um visual mais "tech" se preferir, ou candle

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
    });

    // Criar uma série de área (Area Series) para um visual mais fluido/moderno
    areaSeries = chart.addAreaSeries({
        lineColor: '#00f2ff',
        topColor: 'rgba(0, 242, 255, 0.4)',
        bottomColor: 'rgba(0, 242, 255, 0.0)',
        lineWidth: 2,
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
            DOM.statusPill.innerHTML = `
                <div style="background:var(--neon-pink)" class="dot"></div> 
                CLOUD: OFFLINE (retry ${syncErrors})
            `;
        }

        // Retry mais lento se muitos erros
        if (syncErrors > 5) {
            await new Promise(r => setTimeout(r, 2000));
        }
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

        // Atualizar Gráfico
        if (areaSeries) {
            // Usar o timestamp do servidor ou local se falhar
            const time = data.last_update ? Math.floor(data.last_update) : Math.floor(Date.now() / 1000);

            // Pequeno hack para garantir timestamps únicos se o update for muito rápido
            // (Lightweight charts requer timestamps crescentes)
            const lastTime = areaSeries.data().length > 0 ? areaSeries.data()[areaSeries.data().length - 1].time : 0;

            if (time > lastTime) {
                areaSeries.update({ time: time, value: price });
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
        const imb = data.imb || 0;
        const width = Math.max(5, Math.min(95, 50 + (imb * 50)));
        DOM.flowBar.style.width = `${width}%`;
        DOM.flowBar.style.background = imb > 0 ? 'var(--neon-green)' : 'var(--neon-pink)';
    }

    // Status
    if (DOM.statusPill) {
        const lockIcon = data.is_locked ? ' 🔒' : '';
        const huntIcon = data.is_hunting ? ' 🎯' : '';
        DOM.statusPill.innerHTML = `
            <div class="dot"></div> 
            CLOUD: ${data.regime || 'ACTIVE'}${lockIcon}${huntIcon}
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
    console.log("🦅 PREDATOR v13.0 | 100% CLOUD ENGINE");
    console.log(`📡 API: ${CONFIG.API_URL}`);

    initDOM();

    // Primeira sync imediata
    syncDashboard();

    // Loop de alta frequência
    setInterval(syncDashboard, CONFIG.SYNC_INTERVAL_MS);

    console.log("✅ PREDATOR v13.0 | CLOUD SYSTEMS ONLINE");
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
