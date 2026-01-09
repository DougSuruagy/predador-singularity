import { createClient } from '@supabase/supabase-js'

// --- CONFIGURAÇÃO CLOUD (CUSTO ZERO) ---
const CLOUD_API = "https://seu-predador-api.onrender.com";
const LOCAL_API = "http://localhost:8000"; // Prioridade Local se o Render estiver lento
const SUPABASE_URL = "https://sua-url.supabase.co";
const SUPABASE_KEY = "sua-chave-anonima";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

let activeApi = CLOUD_API;

async function checkFastestPath() {
    try {
        const start = performance.now();
        await fetch(`${LOCAL_API}/state`, { mode: 'no-cors' });
        const latency = performance.now() - start;
        if (latency < 100) activeApi = LOCAL_API;
    } catch (e) {
        activeApi = CLOUD_API;
    }
}

async function syncDashboard() {
    try {
        const response = await fetch(`${activeApi}/state`);
        const data = await response.json();

        if (data.price > 0 || data.last_price > 0) {
            const currentPrice = data.price || data.last_price;
            document.getElementById('big-price').innerText = currentPrice.toLocaleString();
            document.querySelector('.prob-value').innerText = `${(data.prob || 0).toFixed(1)}%`;

            const pnlEl = document.querySelector('.stats-grid .stat-box:nth-child(1) h3');
            pnlEl.innerText = `R$ ${(data.pnl || 0).toLocaleString()}`;
            pnlEl.style.color = (data.pnl || 0) >= 0 ? 'var(--neon-green)' : 'var(--neon-pink)';

            document.querySelector('.stat-box:nth-child(2) h3').innerText = `${(data.win_rate || 0)}%`;
            document.getElementById('flow-bar').style.width = `${50 + ((data.imb || 0) * 50)}%`;

            document.querySelector('.status-pill').innerHTML = `<div class="dot"></div> LINK: ${activeApi === LOCAL_API ? 'LOCAL' : 'CLOUD'}`;
        }
    } catch (e) {
        document.querySelector('.status-pill').innerHTML = '<div style="background:var(--neon-pink)" class="dot"></div> LINK: OFFLINE';
    }
}

// Inicia Sincronia de Alta Performance
setInterval(checkFastestPath, 5000);
setInterval(syncDashboard, 150);

console.log("🦅 PREDATOR v13.0 | SINGULARITY ENGINE ACTIVE");
