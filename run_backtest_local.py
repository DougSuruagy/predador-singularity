import asyncio
import os
from cloud_api import exchange, run_backtest, WebhookPayload

async def main():
    print("⏳ Carregando mercados para Simulação Quantum v371.1...")
    try:
        await exchange.load_markets()
    except Exception as e:
        print(f"Erro ao carregar exchange: {e}")
        return
    
    # Simula o payload para o backtest
    # 2000 velas de 1m (aprox 33 horas de histórico real)
    assets = ["SOLUSDT", "BTCUSDT", "ETHUSDT"]
    
    for asset in assets:
        print(f"\n🚀 Iniciando Simulação: {asset}")
        payload = WebhookPayload(symbol=asset)
        
        # Executa a lógica do backtest
        try:
            result = await run_backtest(payload)
            
            print("="*50)
            print(f"📊 RESULTADO: {asset}")
            print("="*50)
            print(f"Total de Trades: {result['total_trades']}")
            print(f"Win Rate:       {result['win_rate']}%")
            print(f"PnL Estimado:   {result['total_pnl_percent']}%")
            print(f"Sharpe Ratio:   {result['metrics']['sharpe_ratio']}")
            print(f"Max Drawdown:   {result['metrics']['max_drawdown']}%")
            print(f"Rating:         {result['metrics']['safety_rating']}")
            print("="*50)
        except Exception as e:
            print(f"Erro ao simular {asset}: {e}")
    
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
