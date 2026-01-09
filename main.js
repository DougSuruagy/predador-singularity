/**
 * PREDATOR v13.0 SINGULARITY - Frontend Engine
 * Custo Zero | Performance Extrema | Automação de Repasse
 */

// ============================================================
// CONFIGURAÇÃO (Substitua pelas URLs reais após deploy)
// ============================================================
const CONFIG = {
    CLOUD_API: "https://predador-api.onrender.com",  // URL do Render
    LOCAL_API: "http://localhost:8000",               // API local (prioridade)
    SUPABASE_URL: "https://sua-url.supabase.co",      // Substitua após criar projeto
    SUPABASE_KEY: "sua-chave-anonima",                // Substitua após criar projeto
    SYNC_INTERVAL_MS: 200,                            // Frequência de atualização
    LATENCY_CHECK_MS: 5000,                           // Verificar melhor rota a cada 5s
    MAX_LATENCY_LOCAL: 150                            // Latência máxima para usar local (ms)
};

// ============================================================
// ESTADO GLOBAL
// ============================================================
let activeApi = CONFIG.CLOUD_API;
let lastSyncTime = 0;
let isOnline = false;

// Cache de elementos DOM (Performance)
const DOM = {
    bigPrice: null,
    probValue: null,
    pnlValue: null,
    winRate: null,
    flowBar: null,
    statusPill: null,
    feedLog: null,
    regimeLabel: null
};

// ============================================================
// INICIALIZAÇÃO
// ============================================================
function initDOM() {
    DOM.bigPrice = document.getElementById('big-price');
    DOM.probValue = document.querySelector('.prob-value');
    DOM.pnlValue = document.querySelector('.stats-grid .stat-box:nth-child(1) h3');
    DOM.winRate = document.querySelector('.stat-box:nth-child(2) h3');
    DOM.flowBar = document.getElementById('flow-bar');
    DOM.statusPill = document.querySelector('.status-pill');
    DOM.feedLog = document.getElementById('feed');
    DOM.regimeLabel = document.querySelector('[data-regime]');
}

// ============================================================
// FASTEST PATH - Priorização Local para Latência Zero
// ============================================================
async function checkFastestPath() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.MAX_LATENCY_LOCAL);

        const start = performance.now();
        const response = await fetch(`${CONFIG.LOCAL_API}/health`, {
            method: 'GET',
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        const latency = performance.now() - start;

        if (response.ok && latency < CONFIG.MAX_LATENCY_LOCAL) {
            if (activeApi !== CONFIG.LOCAL_API) {
                console.log(`⚡ Switching to LOCAL API (latency: ${latency.toFixed(0)}ms)`);
            }
            activeApi = CONFIG.LOCAL_API;
        } else {
            activeApi = CONFIG.CLOUD_API;
        }
    } catch (e) {
        // Fallback para Cloud se local não responder
        activeApi = CONFIG.CLOUD_API;
    }
}

// ============================================================
// SYNC DASHBOARD - Atualização de Alta Frequência
// ============================================================
async function syncDashboard() {
    try {
        const response = await fetch(`${activeApi}/state`);

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();
        isOnline = true;
        lastSyncTime = Date.now();

        // [PERFORMANCE] Atualizar apenas se houver dados válidos
        const price = data.price || data.last_price || 0;

        if (price > 0 && DOM.bigPrice) {
            DOM.bigPrice.innerText = price.toLocaleString('pt-BR');
        }

        if (DOM.probValue) {
            const prob = data.prob || data.confidence || 0;
            DOM.probValue.innerText = `${prob.toFixed(1)}%`;
            // Cor baseada na confiança
            DOM.probValue.style.color = prob >= 80 ? 'var(--neon-green)' :
                prob >= 60 ? 'var(--neon-blue)' : 'var(--neon-pink)';
        }

        if (DOM.pnlValue) {
            const pnl = data.pnl || data.daily_pnl || 0;
            DOM.pnlValue.innerText = `R$ ${pnl.toLocaleString('pt-BR')}`;
            DOM.pnlValue.style.color = pnl >= 0 ? 'var(--neon-green)' : 'var(--neon-pink)';
        }

        if (DOM.winRate) {
            DOM.winRate.innerText = `${(data.win_rate || 0)}%`;
        }

        if (DOM.flowBar) {
            const imb = data.imb || 0;
            DOM.flowBar.style.width = `${Math.max(5, Math.min(95, 50 + (imb * 50)))}%`;
            DOM.flowBar.style.background = imb > 0 ? 'var(--neon-green)' : 'var(--neon-pink)';
        }

        // Status do Link
        if (DOM.statusPill) {
            const linkType = activeApi === CONFIG.LOCAL_API ? 'LOCAL' : 'CLOUD';
            const lockStatus = data.is_locked ? ' 🔒' : '';
            DOM.statusPill.innerHTML = `<div class="dot"></div> ${linkType}: ${data.regime || 'ACTIVE'}${lockStatus}`;
        }

        // Atualizar Feed de Trades
        if (DOM.feedLog && data.trade_log && data.trade_log.length > 0) {
            DOM.feedLog.innerHTML = data.trade_log.slice(0, 5).map(t =>
                `[${t.time}] ${t.action} | ${t.symbol} | CONF: ${t.confidence}%`
            ).join('<br>');
        }

    } catch (e) {
        isOnline = false;
        if (DOM.statusPill) {
            DOM.statusPill.innerHTML = '<div style="background:var(--neon-pink)" class="dot"></div> LINK: OFFLINE';
        }
    }
}

// ============================================================
// SUPABASE - Persistência de Dados (Custo Zero)
// ============================================================
async function saveTradeToSupabase(trade) {
    // Implementar quando Supabase estiver configurado
    // const { data, error } = await supabase.from('trades').insert(trade);
}

// ============================================================
// INICIAR ENGINES
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    console.log("🦅 PREDATOR v13.0 | SINGULARITY ENGINE INITIALIZING...");

    initDOM();

    // Primeira verificação imediata
    checkFastestPath();
    syncDashboard();

    // Loops de alta performance
    setInterval(checkFastestPath, CONFIG.LATENCY_CHECK_MS);
    setInterval(syncDashboard, CONFIG.SYNC_INTERVAL_MS);

    console.log("✅ PREDATOR v13.0 | ALL SYSTEMS ONLINE");
});

// Export para uso externo
window.PREDATOR = {
    getConfig: () => CONFIG,
    getActiveApi: () => activeApi,
    isOnline: () => isOnline,
    forceSync: syncDashboard
};
