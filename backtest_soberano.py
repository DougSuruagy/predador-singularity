import asyncio
import os
import random
from loguru import logger
from cloud_api import exchange, run_backtest, WebhookPayload
from polymarket_sniper.src.whale_researcher import WhaleResearcher
from polymarket_sniper.src.token_mapper import PolyMapper

class SovereignBacktest:
    def __init__(self):
        self.researcher = WhaleResearcher()
        self.mapper = PolyMapper()
        self.assets = ["SOLUSDT", "BTCUSDT", "ETHUSDT"]

    async def run_hft_phase(self):
        """Fase 1: Backtest HFT Bybit (Dados Reais)"""
        logger.info("🦅 FASE 1: Iniciando Backtest HFT (Bybit)...")
        hft_results = {}
        
        try:
            try:
                await asyncio.wait_for(exchange.load_markets(), timeout=10)
            except Exception as e:
                logger.warning(f"💡 Bybit Market Load Warning: {e}")

            for asset in self.assets:
                logger.info(f"📊 Processando {asset}...")
                try:
                    payload = WebhookPayload(symbol=asset, limit=1500)
                    result = await run_backtest(payload)
                    if result and "error" not in result:
                        hft_results[asset] = result
                except Exception as e:
                    logger.error(f"⚠️ Erro no processamento de {asset}: {e}")
        except Exception as e:
            logger.error(f"⚠️ Erro no Backtest HFT: {e}")
        return hft_results

    async def run_poly_phase(self):
        """Fase 2: Simulação de Performance das Baleias Polymarket"""
        logger.info("🐋 FASE 2: Analisando Potencial de Copy-Trading (Polymarket)...")
        poly_results = []
        
        try:
            # Busca baleias reais para projetar performance
            top_traders = self.researcher.get_elite_traders()
            for trader in top_traders[:5]:
                # Projeção baseada no lucro histórico da baleia
                # Simulamos que copiamos uma fatia proporcional
                pnl_str = str(trader.get('profit_loss', '0')).replace('$', '').replace(',', '')
                try:
                    pnl_float = float(pnl_str)
                except:
                    pnl_float = 0.0

                projected_pnl = pnl_float * 0.01 # Simulando cópia conservadora de 1% da força
                poly_results.append({
                    "trader": trader.get('address', 'Unknown'),
                    "historical_pnl": pnl_str,
                    "projected_profit_usd": round(projected_pnl, 2)
                })
        except Exception as e:
            logger.error(f"⚠️ Erro na Simulação Polymarket: {e}")
        return poly_results

    async def generate_unified_report(self):
        print(f"\n{'='*60}")
        print("🏛️ REPORT SOBERANO: PREDADOR-OMEGA (SimulaÃ§Ã£o Unificada)")
        print(f"{'='*60}\n")
        
        hft = await self.run_hft_phase()
        poly = await self.run_poly_phase()
        
        total_hft_pnl = 0
        print("\n📈 [BYBIT HFT PERFORMANCE]")
        for asset, res in hft.items():
            pnl = res['total_pnl_percent']
            total_hft_pnl += pnl
            status = "🟢 EXCELENTE" if pnl > 0 else "🔴 REVISAR"
            print(f"- {asset:10}: {pnl:>7.2f}% | WR: {res['win_rate']}% | {status}")

        total_poly_usd = 0
        print("\n🐋 [POLYMARKET WHALE-COPY PROJECTION]")
        for res in poly:
            total_poly_usd += res['projected_profit_usd']
            print(f"- Trader {res['trader'][:10]}...: +${res['projected_profit_usd']:>8.2f} (Projetado)")

        print(f"\n{'='*60}")
        print("💰 RESULTADO FINAL ESTIMADO (24H)")
        print(f"HFT Total: {total_hft_pnl:.2f}%")
        print(f"Polymarket Total: +${total_poly_usd:.2f}")
        print(f"Rating Global: {'💎 SOBERANO' if total_hft_pnl > 100 else '🛠️ EM CALIBRAÃ‡ÃƒO'}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    # Remove logs para nÃ£o poluir o report final
    logger.remove()
    logger.add("logs/sovereign_backtest.log", rotation="10 MB")
    
    backtest = SovereignBacktest()
    asyncio.run(backtest.generate_unified_report())
