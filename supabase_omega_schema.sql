-- ============================================================
-- �️ CORREÇÃO DEFINITIVA: SEGURANÇA E PERFORMANCE
-- ============================================================

-- 1. 🧹 LIMPEZA TOTAL DE POLÍTICAS ANTIGAS (Evita conflitos)
-- Removemos tudo para garantir que não sobrem regras duplicadas
DROP POLICY IF EXISTS "Service Role Full Access" ON polymarket_trades;
DROP POLICY IF EXISTS "Service Full Access Poly" ON polymarket_trades;
DROP POLICY IF EXISTS "Service Write Poly" ON polymarket_trades;
DROP POLICY IF EXISTS "Service Update Poly" ON polymarket_trades;
DROP POLICY IF EXISTS "Service Delete Poly" ON polymarket_trades;
DROP POLICY IF EXISTS "Public Read Poly" ON polymarket_trades;

DROP POLICY IF EXISTS "Service Role Full Access" ON whales;
DROP POLICY IF EXISTS "Service Full Access Whales" ON whales;
DROP POLICY IF EXISTS "Service Write Whales" ON whales;
DROP POLICY IF EXISTS "Service Update Whales" ON whales;
DROP POLICY IF EXISTS "Service Delete Whales" ON whales;
DROP POLICY IF EXISTS "Public Read Whales" ON whales;

-- 2. 🛡️ NOVAS POLÍTICAS OTIMIZADAS (Performance + Segurança)
-- Usamos (select auth.role()) para cachear o resultado e evitar re-avaliação por linha

-- Tabela: polymarket_trades
CREATE POLICY "Public Read Poly" ON polymarket_trades
    FOR SELECT USING (true);

CREATE POLICY "Service Write Poly" ON polymarket_trades
    FOR INSERT WITH CHECK ((select auth.role()) = 'service_role');

CREATE POLICY "Service Update Poly" ON polymarket_trades
    FOR UPDATE USING ((select auth.role()) = 'service_role');

CREATE POLICY "Service Delete Poly" ON polymarket_trades
    FOR DELETE USING ((select auth.role()) = 'service_role');

-- Tabela: whales
CREATE POLICY "Public Read Whales" ON whales
    FOR SELECT USING (true);

CREATE POLICY "Service Write Whales" ON whales
    FOR INSERT WITH CHECK ((select auth.role()) = 'service_role');

CREATE POLICY "Service Update Whales" ON whales
    FOR UPDATE USING ((select auth.role()) = 'service_role');

CREATE POLICY "Service Delete Whales" ON whales
    FOR DELETE USING ((select auth.role()) = 'service_role');

-- 3. 👁️ CORREÇÃO DA VIEW (Security Invoker)
DROP VIEW IF EXISTS public.omega_health_check;

CREATE VIEW public.omega_health_check 
WITH (security_invoker = true) -- Resolve o erro "Security Definer"
AS
SELECT 
    'PREDADOR-OMEGA'::text AS system_name,
    (SELECT COUNT(*) FROM polymarket_trades WHERE created_at > NOW() - INTERVAL '24 hours') AS poly_trades_24h,
    (SELECT COALESCE(SUM(pnl_usd), 0) FROM polymarket_trades WHERE created_at > NOW() - INTERVAL '24 hours') AS poly_pnl_24h,
    (SELECT COUNT(*) FROM whales WHERE is_active = TRUE) AS active_whales,
    NOW() AS checked_at;

-- 4. 🚀 CONFIRMAÇÃO
DO $$
BEGIN
    RAISE NOTICE '✅ Limpeza e Otimização de Segurança Concluídas com Sucesso!';
END $$;
