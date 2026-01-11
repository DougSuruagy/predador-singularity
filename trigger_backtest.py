import requests
import json
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do PREDATOR API (Render)
# Substitua pela sua URL real do Render se necessário
API_URL = "https://predador-api.onrender.com" 
# Seu token configurado no INTERNAL_SECRET_TOKEN
SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

def run_remote_backtest(symbol="SOLUSDT", period="1d"):
    """
    Dispara o motor de Backtest Quantum diretamente no servidor Render.
    """
    print(f"🚀 Iniciando Backtest Remoto no Render: {symbol} ({period})")
    print(f"🔗 Conectando a: {API_URL}")
    
    endpoint = f"{API_URL}/backtest"
    headers = {
        "X-Token": SECRET_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "symbol": symbol,
        "period": period,
        "limit": 2000   # Dobramos a amostra para validação estatística real
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"❌ Erro reportado pela IA: {result['error']}")
                return

            print("\n" + "═"*50)
            print(f"🏆 RESULTADO DOS SONHOS DA IA (BACKTEST)")
            print("═"*50)
            print(f"Ativo: {result.get('symbol')}")
            print(f"Velas Analisadas (1m): {result.get('candles_analyzed')}")
            print(f"Total de Trades: {result.get('total_trades')}")
            print(f"Win Rate: {result.get('win_rate')}%")
            print(f"PnL Líquido Simulado: {result.get('total_pnl_percent')}%")
            
            metrics = result.get('metrics', {})
            if metrics:
                print("\n📊 MÉTRICAS DE PERFORMANCE:")
                print(f"  - Drawdown Máximo:  {metrics.get('max_drawdown')}%")
                print(f"  - Sharpe Ratio:     {metrics.get('sharpe_ratio')}")
                print(f"  - SAFETY RATING:    {metrics.get('safety_rating')}")
                print(f"  - Expectativa/Trade: {metrics.get('expectancy')}%")
                print(f"  - Relação RRR:      {metrics.get('rrr')}:1")
                print(f"  - Ganho Médio:      {metrics.get('avg_win')}%")
                print(f"  - Perda Média:      {metrics.get('avg_loss')}%")

            print("\n📜 Últimos 5 Trades da Simulação:")
            for t in result.get('history', [])[-5:]:
                color = "🟢" if t['pnl'] > 0 else "🔴" if t['pnl'] < 0 else "⚪"
                print(f"  {color} Trade @ {t['t']}: PnL {t['pnl']:.2f}%")
            print("═"*50)
        else:
            print(f"❌ Erro na API (Status {response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"⚠️ Erro de Conexão: {e}")

if __name__ == "__main__":
    # Testando os Pilares do Mercado com a Genética v26.4
    assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    
    for asset in assets:
        print(f"\n--- Iniciando Ciclo para {asset} ---")
        run_remote_backtest(symbol=asset, period="1d")
