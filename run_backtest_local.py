import asyncio
import os
from cloud_api import exchange, run_backtest, brain

async def main():
    # Carrega mercados para o backtest
    print("⏳ Carregando mercados para Simulação Quantum...")
    await exchange.load_markets()
    
    # Simula o payload para o backtest
    # Usando SOLUSDT que costuma ter boa volatilidade para scalping
    test_data = {
        "symbol": "SOLUSDT",
        "period": "1h", # 1 hora de dados (60 velas de 1m)
        "dna": brain.genes # Usa a genética atual v26.4
    }
    
    # Executa a lógica do backtest
    result = await run_backtest(test_data)
    
    print("\n" + "="*50)
    print(f"📊 RESULTADO DA SIMULAÇÃO (SOLUSDT)")
    print("="*50)
    print(f"Candles Analisados: {result['candles_analyzed']}")
    print(f"Total de Trades: {result['total_trades']}")
    print(f"Win Rate: {result['win_rate']}%")
    print(f"PnL Estimado: {result['total_pnl_percent']}%")
    print("="*50)
    
    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
