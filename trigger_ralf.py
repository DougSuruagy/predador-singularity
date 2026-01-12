
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
        "action": "RALF" # Aciona o modo RALF no backend
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=180)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    print(f"🌪️ INICIANDO BACKTEST MODO RALF (v370.1)")
    print("=" * 60)
    
    for asset in assets:
        print(f"Testando {asset} (RALF)...")
        res = run_ralf_backtest(asset)
        if "error" in res:
            print(f"❌ {asset}: {res['error']}")
        else:
            pnl = res.get('total_pnl_percent', 0)
            trades = res.get('trades', 0)
            wr = res.get('win_rate', 0)
            print(f"✅ {asset}: PnL {pnl}% | Trades: {trades} | WR: {wr}%")
    
    print("=" * 60)
