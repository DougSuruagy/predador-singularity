import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://predador-api.onrender.com" 
SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

def run_remote_backtest(symbol="SOLUSDT", period="1d"):
    endpoint = f"{API_URL}/backtest"
    headers = {
        "X-Token": SECRET_TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "symbol": symbol,
        "period": period,
        "limit": 2000
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=180)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    
    results = {}
    for asset in assets:
        print(f"Testando {asset}...")
        results[asset] = run_remote_backtest(symbol=asset, period="1d")
    
    # Save to file
    with open("backtest_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResultados salvos em backtest_results.json")
    
    # Print summary
    print("\n" + "="*70)
    print("RESUMO DO BACKTEST v340.0 VALHALLA-REBORN")
    print("="*70)
    
    total_pnl = 0
    for asset, r in results.items():
        if "error" in r:
            print(f"{asset}: ERRO - {r['error']}")
            continue
            
        pnl = r.get('total_pnl_percent', 0)
        total_pnl += pnl
        wr = r.get('win_rate', 0)
        trades = r.get('total_trades', 0)
        metrics = r.get('metrics', {})
        rating = metrics.get('safety_rating', 'N/A')
        rrr = metrics.get('rrr', 0)
        sharpe = metrics.get('sharpe_ratio', 0)
        dd = metrics.get('max_drawdown', 0)
        
        status = "OK" if pnl > 0 else "RUIM"
        print(f"\n{asset} [{status}]:")
        print(f"  PnL:       {pnl:+.2f}%")
        print(f"  Win Rate:  {wr:.1f}%")
        print(f"  Trades:    {trades}")
        print(f"  RRR:       {rrr:.2f}:1")
        print(f"  Sharpe:    {sharpe:.2f}")
        print(f"  Drawdown:  {dd:.2f}%")
        print(f"  Rating:    {rating}")
    
    print("\n" + "-"*70)
    print(f"PnL TOTAL COMBINADO: {total_pnl:+.2f}%")
    
    if total_pnl > 0:
        print("STATUS: LUCRATIVO")
    else:
        print("STATUS: PRECISA AJUSTES")
    print("="*70)
