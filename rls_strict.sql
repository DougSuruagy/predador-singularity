-- ============================================================
-- 🔐 RLS STRICT - PREDATOR v370.3 "DUAL-CORE"
-- Políticas restritas para service_role (100% Linter Green)
-- ⚠️ REQUER: SUPABASE_KEY = Service Role Key nos servidores
-- ============================================================

-- Remover políticas permissivas
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_TRADES" ON public.trades;
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "SOVEREIGN_UPDATE_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_LOGS" ON public.system_logs;
DROP POLICY IF EXISTS "SOVEREIGN_UPSERT_STATUS" ON public.system_status;
DROP POLICY IF EXISTS "SOVEREIGN_UPDATE_STATUS" ON public.system_status;

-- Criar políticas restritas para service_role
CREATE POLICY "SOVEREIGN_INSERT_TRADES" ON public.trades 
FOR INSERT WITH CHECK ((SELECT auth.role()) = 'service_role');

CREATE POLICY "SOVEREIGN_INSERT_STATS" ON public.daily_stats 
FOR INSERT WITH CHECK ((SELECT auth.role()) = 'service_role');

CREATE POLICY "SOVEREIGN_UPDATE_STATS" ON public.daily_stats 
FOR UPDATE USING ((SELECT auth.role()) = 'service_role');

CREATE POLICY "SOVEREIGN_INSERT_LOGS" ON public.system_logs 
FOR INSERT WITH CHECK ((SELECT auth.role()) = 'service_role');

CREATE POLICY "SOVEREIGN_UPSERT_STATUS" ON public.system_status 
FOR INSERT WITH CHECK ((SELECT auth.role()) = 'service_role');

CREATE POLICY "SOVEREIGN_UPDATE_STATUS" ON public.system_status 
FOR UPDATE USING ((SELECT auth.role()) = 'service_role');

-- Verificação
SELECT tablename, policyname, cmd 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, cmd;
