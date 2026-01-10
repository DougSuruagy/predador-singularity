
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

        // 4. Lógica de "Progeny" (O Junior gera descendentes)
        let evolutionStatus = "STABLE";
        let newDna = null;

        if (totalTrades >= 5 && winRate > 60) {
            console.log("🧬 JUNIOR_VERCEL: Condições ideais detectadas. Gerando descendente...");

            // Busca o DNA atual da última geração
            const { data: lastGen } = await supabase
                .from('genetics')
                .select('*')
                .order('generation', { ascending: false })
                .limit(1);

            const currentDna = lastGen?.[0]?.dna || {
                frontal_weight: 0.35,
                occipital_weight: 0.35,
                amygdala_weight: 0.15,
                parietal_weight: 0.15
            };

            // Mutação do Junior (Evolução por descendência)
            newDna = { ...currentDna };
            const mutationFactor = 0.05;
            newDna.frontal_weight += (Math.random() - 0.5) * mutationFactor;
            newDna.occipital_weight += (Math.random() - 0.5) * mutationFactor;

            // Normalização
            const total = Object.values(newDna).reduce((a, b) => a + b, 0);
            for (let key in newDna) newDna[key] /= total;

            await supabase.from('genetics').insert({
                generation: (lastGen?.[0]?.generation || 0) + 1,
                dna: newDna,
                fitness: winRate,
                parent_id: lastGen?.[0]?.id || null,
                origin: 'JUNIOR_VERCEL'
            });

            evolutionStatus = "NEW_GEN_BORN";
        }

        // 5. Inteligência de Recomendação
        let recommendation = "KEEP_HUNTING";
        if (criticalFailure) recommendation = "EMERGENCY_COOLDOWN";
        if (totalPnl < -20) recommendation = "RISK_REDUCTION";

        const report = {
            version: "21.3.0 APEX PROGENY",
            status: "ACTIVE",
            timestamp: new Date().toISOString(),
            evolution: {
                status: evolutionStatus,
                generation: newDna ? "NEW" : "CURRENT",
                junior_contribution: newDna ? "GENETIC_MUTATION_APPLIED" : "MONITORING"
            },
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
            message: "O Junior na Vercel está gerando descendentes baseados nos lucros do Senior no Render."
        };

        return res.status(200).json(report);

    } catch (err) {
        console.error("❌ SUPERVISOR ERROR:", err);
        return res.status(500).json({ error: "Supervisor Internal Failure", message: err.message });
    }
}
