import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://predador-api.onrender.com" 
SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

def run_ralf_backtest(symbol="SOLUSDT", period="1m"):
    endpoint = f"{API_URL}/backtest"
    headers = {
        "X-Token": SECRET_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "symbol": symbol,
        "period": period,
        "limit": 2000,
        "action": "RALF"
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=180)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def print_metrics(asset, res):
    """Exibe métricas profissionais do backtest"""
    if "error" in res:
        print(f"❌ {asset}: {res['error']}")
        return
    
    pnl = res.get('total_pnl_percent', 0)
    trades = res.get('total_trades', 0)
    wins = res.get('wins', 0)
    losses = res.get('losses', 0)
    wr = res.get('win_rate', 0)
    metrics = res.get('metrics', {})
    
    sharpe = metrics.get('sharpe_ratio', 0)
    dd = metrics.get('max_drawdown_pct', 0)
    avg_ret = metrics.get('avg_return_per_trade', 0)
    rating = metrics.get('rating', 'N/A')
    
    # Emoji baseado no rating
    if rating == "EXCELENTE":
        emoji = "🏆"
    elif rating == "BOM":
        emoji = "✅"
    elif rating == "ACEITÁVEL":
        emoji = "⚠️"
    else:
        emoji = "❌"
    
    print(f"\n{emoji} {asset} [{rating}]")
    print("-" * 40)
    print(f"  💰 PnL Líquido:     {pnl:+.2f}%")
    print(f"  📈 Win Rate:        {wr:.1f}% ({wins}W / {losses}L)")
    print(f"  📉 Drawdown Máx:    {dd:.2f}%")
    print(f"  ⚖️  Sharpe Ratio:    {sharpe:.2f}")
    print(f"  📊 Retorno/Trade:   {avg_ret:.2f}%")

if __name__ == "__main__":
    assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    
    print("=" * 60)
    print("🌀 BACKTEST RALF SCALPER (v370.3)")
    print("=" * 60)
    
    total_pnl = 0
    total_trades = 0
    
    for asset in assets:
        print(f"\n⏳ Testando {asset}...")
        res = run_ralf_backtest(asset)
        print_metrics(asset, res)
        
        if "error" not in res:
            total_pnl += res.get('total_pnl_percent', 0)
            total_trades += res.get('total_trades', 0)
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO TOTAL")
    print("-" * 60)
    print(f"  💰 PnL Combinado:   {total_pnl:+.2f}%")
    print(f"  📈 Total Trades:    {total_trades}")
    print("=" * 60)
    
    # Interpretação
    print("\n📖 INTERPRETAÇÃO SHARPE RATIO:")
    print("   < 1  → Fraco (risco não compensa)")
    print("   1-2  → Aceitável")
    print("   > 2  → Bom")
    print("   > 5  → Excelente consistência")
