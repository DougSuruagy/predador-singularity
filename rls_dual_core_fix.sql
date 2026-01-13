-- ============================================================
-- 🦅 RLS FIX - PREDATOR v370.3 "DUAL-CORE"
-- Corrige políticas para permitir escrita de ambos os nós Render
-- ============================================================

-- 1. REMOVER TODAS AS POLÍTICAS (antigas e novas) para evitar conflitos
DROP POLICY IF EXISTS "APEX_WRITE_TRADES" ON public.trades;
DROP POLICY IF EXISTS "APEX_WRITE_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "APEX_UPDATE_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "APEX_WRITE_LOGS" ON public.system_logs;
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_TRADES" ON public.trades;
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "SOVEREIGN_UPDATE_STATS" ON public.daily_stats;
DROP POLICY IF EXISTS "SOVEREIGN_INSERT_LOGS" ON public.system_logs;

-- 2. CRIAR NOVAS POLÍTICAS

-- TRADES
CREATE POLICY "SOVEREIGN_INSERT_TRADES" ON public.trades 
FOR INSERT WITH CHECK (true);

-- DAILY_STATS
CREATE POLICY "SOVEREIGN_INSERT_STATS" ON public.daily_stats 
FOR INSERT WITH CHECK (true);

CREATE POLICY "SOVEREIGN_UPDATE_STATS" ON public.daily_stats 
FOR UPDATE USING (true);

-- SYSTEM_LOGS
CREATE POLICY "SOVEREIGN_INSERT_LOGS" ON public.system_logs 
FOR INSERT WITH CHECK (true);

-- 3. CRIAR/ATUALIZAR TABELA system_status
CREATE TABLE IF NOT EXISTS public.system_status (
    version TEXT PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    pnl NUMERIC(10, 2),
    trades INT,
    win_rate NUMERIC(5, 2),
    entropy NUMERIC(5, 2),
    shield TEXT,
    status TEXT,
    node_role TEXT
);

ALTER TABLE public.system_status ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "SOVEREIGN_READ_STATUS" ON public.system_status;
DROP POLICY IF EXISTS "SOVEREIGN_UPSERT_STATUS" ON public.system_status;
DROP POLICY IF EXISTS "SOVEREIGN_UPDATE_STATUS" ON public.system_status;

CREATE POLICY "SOVEREIGN_READ_STATUS" ON public.system_status 
FOR SELECT USING (true);

CREATE POLICY "SOVEREIGN_UPSERT_STATUS" ON public.system_status 
FOR INSERT WITH CHECK (true);

CREATE POLICY "SOVEREIGN_UPDATE_STATUS" ON public.system_status 
FOR UPDATE USING (true);

-- 4. VERIFICAÇÃO FINAL
SELECT tablename, policyname, cmd 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, cmd;
