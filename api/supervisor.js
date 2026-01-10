
import { createClient } from '@supabase/supabase-js';
import axios from 'axios';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const renderApiUrl = process.env.RENDER_API_URL || 'https://predador-api.onrender.com';

const supabase = createClient(supabaseUrl, supabaseKey);

export default async function handler(req, res) {
    // Configuração de CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    try {
        console.log("🕵️ SUPERVISOR VERCEL: Iniciando auditoria de lucros...");

        // 1. Verificar Integridade do Render (O Cérebro)
        let renderStatus = "OFFLINE";
        let uptime = 0;
        try {
            const health = await axios.get(`${renderApiUrl}/health`, { timeout: 3000 });
            if (health.status === 200) {
                renderStatus = "ONLINE";
                uptime = health.data.uptime_seconds;
            }
        } catch (e) {
            console.error("⚠️ RENDER OFFLINE:", e.message);
        }

        // 2. Analisar Lucros Recentes (Supabase)
        const today = new Date().toISOString().split('T')[0];
        const { data: trades, error } = await supabase
            .from('trades')
            .select('pnl, result, symbol, created_at')
            .gte('created_at', today)
            .order('created_at', { ascending: false });

        if (error) throw error;

        const totalTrades = trades.length;
        const wins = trades.filter(t => t.result === 'WIN').length;
        const losses = trades.filter(t => t.result === 'LOSS').length;
        const totalPnl = trades.reduce((acc, t) => acc + (t.pnl || 0), 0);
        const winRate = totalTrades > 0 ? (wins / totalTrades) * 100 : 0;

        // 3. Lógica de "Kill-Switch" Preventivo (Supervisor)
        // Se houver 3 perdas seguidas, o supervisor sinaliza alerta crítico
        const recentResults = trades.slice(0, 3).map(t => t.result);
        const criticalFailure = recentResults.length === 3 && recentResults.every(r => r === 'LOSS');

        // 4. Inteligência de Recomendação
        let recommendation = "KEEP_HUNTING";
        if (criticalFailure) recommendation = "EMERGENCY_COOLDOWN";
        if (totalPnl < -20) recommendation = "RISK_REDUCTION"; // Perda de 20% da banca base

        const report = {
            version: "21.2.0 APEX SUPERVISOR",
            status: "ACTIVE",
            timestamp: new Date().toISOString(),
            infrastructure: {
                render_bridge: renderStatus,
                render_uptime: uptime
            },
            performance_audit: {
                daily_trades: totalTrades,
                daily_pnl: totalPnl,
                win_rate: `${winRate.toFixed(2)}%`,
                streak_status: criticalFailure ? "CRITICAL_LOSS_STREAK" : "STABLE"
            },
            ai_recommendation: recommendation,
            message: "Monitoramento Serverless Vercel ativo. Escaneando integridade do Render e Binance."
        };

        return res.status(200).json(report);

    } catch (err) {
        console.error("❌ SUPERVISOR ERROR:", err);
        return res.status(500).json({ error: "Supervisor Internal Failure", message: err.message });
    }
}
