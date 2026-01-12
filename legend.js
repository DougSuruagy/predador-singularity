/**
 * PREDATOR LEGEND v320.0 - The Living UI
 */

const CONFIG = {
    API_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? "http://127.0.0.1:8000"
        : "https://predador-api.onrender.com",
    SYNC_INTERVAL: 1000,
    TOKEN: "predador_secret_2026"
};

let state = {
    last_price: 0,
    trades: [],
    online: false,
    chart: null,
    series: null,
    currentCandle: null
};

// --- INITIALIZATION ---
function init() {
    initChart();
    startSync();
    typewriterEffect("monitoring global markets... active hunters checking for wicks...", "command-text");
}

function initChart() {
    const container = document.getElementById('main-chart');
    state.chart = LightweightCharts.createChart(container, {
        width: container.clientWidth,
        height: container.clientHeight,
        layout: {
            background: { type: 'solid', color: 'transparent' },
            textColor: '#7982a9',
        },
        grid: {
            vertLines: { color: 'rgba(255, 255, 255, 0.03)' },
            horzLines: { color: 'rgba(255, 255, 255, 0.03)' },
        },
        timeScale: { borderColor: 'rgba(255, 255, 255, 0.1)' },
    });

    state.series = state.chart.addCandlestickSeries({
        upColor: '#9ece6a',
        downColor: '#f7768e',
        borderVisible: false,
        wickUpColor: '#9ece6a',
        wickDownColor: '#f7768e',
    });

    window.addEventListener('resize', () => {
        state.chart.resize(container.clientWidth, container.clientHeight);
    });
}

// --- SYNC ENGINE ---
async function startSync() {
    while (true) {
        try {
            const resp = await fetch(`${CONFIG.API_URL}/state`, {
                headers: { "x-token": CONFIG.TOKEN }
            });

            if (resp.ok) {
                const data = await resp.json();
                updateUI(data);
                updateConnection(true);
            } else {
                updateConnection(false);
            }
        } catch (e) {
            updateConnection(false);
            console.error("Sync Error:", e);
        }
        await new Promise(r => setTimeout(r, CONFIG.SYNC_INTERVAL));
    }
}

// --- UI UPDATES ---
function updateUI(data) {
    // Price & Ticker
    const price = data.price || 0;
    const priceDisplay = document.getElementById('price-display');
    const oldPrice = parseFloat(priceDisplay.innerText);

    priceDisplay.innerText = price.toLocaleString('en-US', { minimumFractionDigits: 2 });
    if (price > oldPrice) priceDisplay.style.color = 'var(--success)';
    else if (price < oldPrice) priceDisplay.style.color = 'var(--danger)';

    // Status Dots
    document.getElementById('render-dot').className = 'dot online';
    document.getElementById('render-status').innerText = 'OPERATIONAL';
    document.getElementById('brain-status').innerText = data.regime || 'ACTIVE';
    document.getElementById('brain-dot').className = 'dot online pulse-green';

    // Biometrics (Gauges)
    updateGauge('dopamine-fill', data.bio?.dopamine || 50);
    updateGauge('adrenaline-fill', (data.bio?.adrenaline || 0.5) * 100);

    document.getElementById('uptime').innerText = `UP ${formatUptime(data.uptime)}`;
    document.getElementById('efficiency').innerText = `${data.executive_efficiency || 100}%`;
    document.getElementById('firing').innerText = `${data.synaptic_firing || 12.0}Hz`;
    document.getElementById('homeostasis').innerText = `${data.homeostasis || 100}%`;

    // Bias & Score
    const biasEl = document.getElementById('current-bias');
    biasEl.innerText = `BIAS: ${data.mode || 'NEUTRAL'}`;
    document.getElementById('last-score').innerText = `SCORE: ${data.confidence || 0.0}`;

    // Asset Tickers
    if (data.symbol === "BTCUSDT") document.getElementById('btc-price').innerText = price.toLocaleString();
    if (data.symbol === "SOLUSDT") document.getElementById('sol-price').innerText = price.toLocaleString();

    // Chart Sync
    syncChart(price);

    // Trade Log
    if (data.trade_log && data.trade_log.length > 0) {
        updateTradesList(data.trade_log);
    }
}

function updateConnection(online) {
    if (!online) {
        document.getElementById('render-dot').className = 'dot offline';
        document.getElementById('render-status').innerText = 'ERROR';
        document.getElementById('brain-dot').className = 'dot offline';
        document.getElementById('brain-status').innerText = 'OFFLINE';
    }
}

function updateGauge(id, percent) {
    const el = document.getElementById(id);
    const offset = 126 - (126 * percent / 100);
    el.style.strokeDashoffset = offset;
}

function syncChart(price) {
    if (!state.series || price <= 0) return;
    const now = Math.floor(Date.now() / 1000);
    if (!state.currentCandle || now >= state.currentCandle.time + 60) {
        state.currentCandle = {
            time: Math.floor(now / 60) * 60,
            open: price, high: price, low: price, close: price
        };
    } else {
        state.currentCandle.close = price;
        state.currentCandle.high = Math.max(state.currentCandle.high, price);
        state.currentCandle.low = Math.min(state.currentCandle.low, price);
    }
    state.series.update(state.currentCandle);
}

function updateTradesList(trades) {
    const container = document.getElementById('trades-list');
    const terminal = document.getElementById('terminal');

    // Only update if new trades found
    if (trades.length > state.trades.length) {
        const newTrade = trades[trades.length - 1];

        // Add to terminal
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        const isLong = newTrade.action === "BUY";
        entry.innerHTML = `
            <span class="log-time">[${newTrade.time}]</span>
            <span class="log-tag trade">${newTrade.symbol}</span>
            <span style="color:${isLong ? 'var(--success)' : 'var(--danger)'}">
                ${newTrade.action} EXECUTION @ ${newTrade.price}
            </span>
        `;
        terminal.prepend(entry);
        state.trades = trades;

        // Play beep or visual pulse? 
        document.querySelector('.center-panel').style.borderColor = isLong ? 'var(--success)' : 'var(--danger)';
        setTimeout(() => {
            document.querySelector('.center-panel').style.borderColor = 'var(--border-dim)';
        }, 1000);
    }
}

// --- UTILS ---
function formatUptime(seconds) {
    if (!seconds) return "00:00:00";
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
}

function typewriterEffect(text, id) {
    const el = document.getElementById(id);
    let i = 0;
    el.innerText = "";
    function type() {
        if (i < text.length) {
            el.innerText += text.charAt(i);
            i++;
            setTimeout(type, 30);
        }
    }
    type();
}

window.onload = init;
