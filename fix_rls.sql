-- 🛡️ SOVEREIGN SECURITY PATCH - ENABLE RLS
-- ATENÇÃO: Rode este script no Editor SQL do Supabase para corrigir os erros de segurança.

-- 1. Ativa RLS na tabela trades
ALTER TABLE public.trades ENABLE ROW LEVEL SECURITY;

-- 2. Ativa RLS na tabela daily_stats
ALTER TABLE public.daily_stats ENABLE ROW LEVEL SECURITY;

-- 3. Ativa RLS na tabela system_logs
ALTER TABLE public.system_logs ENABLE ROW LEVEL SECURITY;

-- 4. Comentários para Auditoria
COMMENT ON TABLE public.trades IS 'PREDATOR v43.0: Core Trading Log (RLS Active)';
COMMENT ON TABLE public.daily_stats IS 'PREDATOR v43.0: Daily Performance (RLS Active)';
COMMENT ON TABLE public.system_logs IS 'PREDATOR v43.0: Neural Telemetry (RLS Active)';
