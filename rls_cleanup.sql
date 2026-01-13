-- ============================================================
-- 🧹 LIMPEZA DE POLÍTICAS DUPLICADAS - PREDATOR v370.3
-- Remove políticas "Unified_*" antigas e mantém apenas "SOVEREIGN_*"
-- ============================================================

-- SYSTEM_LOGS: Remover duplicata
DROP POLICY IF EXISTS "Unified_Logs_Write" ON public.system_logs;
DROP POLICY IF EXISTS "Unified_Logs_Read" ON public.system_logs;

-- SYSTEM_STATUS: Remover duplicatas (ALL é redundante)
DROP POLICY IF EXISTS "Unified_Status_Write" ON public.system_status;
DROP POLICY IF EXISTS "Unified_Status_Read" ON public.system_status;

-- TRADES: Remover duplicata
DROP POLICY IF EXISTS "Unified_Trades_Write" ON public.trades;
DROP POLICY IF EXISTS "Unified_Trades_Read" ON public.trades;

-- DAILY_STATS: Padronizar leitura
DROP POLICY IF EXISTS "APEX_READ_STATS" ON public.daily_stats;
CREATE POLICY "SOVEREIGN_READ_STATS" ON public.daily_stats 
FOR SELECT USING (true);

-- Adicionar políticas de leitura que podem estar faltando
DROP POLICY IF EXISTS "SOVEREIGN_READ_TRADES" ON public.trades;
CREATE POLICY "SOVEREIGN_READ_TRADES" ON public.trades 
FOR SELECT USING (true);

DROP POLICY IF EXISTS "SOVEREIGN_READ_LOGS" ON public.system_logs;
CREATE POLICY "SOVEREIGN_READ_LOGS" ON public.system_logs 
FOR SELECT USING (true);

-- VERIFICAÇÃO FINAL (deve mostrar apenas políticas SOVEREIGN_*)
SELECT tablename, policyname, cmd 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, cmd;
