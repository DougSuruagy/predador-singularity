import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000" 
SECRET_TOKEN = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")

def run_remote_backtest(symbol="SOLUSDT", period="1m", mode="STD"):
    endpoint = f"{API_URL}/backtest"
    headers = {
        "X-Token": SECRET_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Se mode for RALF, envia action="RALF", senão envia "BUY" (Padrão)
    action = "RALF" if mode == "RALF" else "BUY"
    
    payload = {
        "symbol": symbol,
        "period": period,
        "limit": 2000,
        "action": action
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=180)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def print_metrics(asset, mode, res):
    """Exibe métricas profissionais do backtest"""
    candles = res.get("candles_count", "N/A")
    
    if "error" in res:
        print(f"❌ {asset} [{mode}]: {res['error']} (Candles: {candles})")
        return
    
    pnl = res.get('total_pnl_percent', 0)
    wins = res.get('wins', 0)
    losses = res.get('losses', 0)
    wr = res.get('win_rate', 0)
    metrics = res.get('metrics', {})
    
    # Debug Info
    print(f"   ℹ️  Candles Fetched: {candles}")
    if res.get("debug_last_candles"):
        last = res["debug_last_candles"][-1]
        print(f"   🐛 Last Debug: RSI={last.get('rsi',0):.1f} Entropy={last.get('entropy',0):.2f}")

    sharpe = metrics.get('sharpe_ratio', 0)
    dd = metrics.get('max_drawdown_pct', 0)
    if dd == 0: dd = metrics.get('max_drawdown', 0) # Fallback field name
    
    avg_ret = metrics.get('avg_return_per_trade', 0)
    rating = metrics.get('rating', 'N/A')
    
    # Emoji baseado no rating
    if rating == "EXCELENTE" or pnl > 10:
        emoji = "🏆"
    elif rating == "BOM" or pnl > 0:
        emoji = "✅"
    elif rating == "ACEITÁVEL" or pnl > -5:
        emoji = "⚠️"
    else:
        emoji = "❌"
    
    print(f"\n{emoji} {asset} ({mode}) [{rating}]")
    print("-" * 40)
    print(f"  💰 PnL Líquido:     {pnl:+.2f}%")
    print(f"  📈 Win Rate:        {wr:.1f}% ({wins}W / {losses}L)")
    print(f"  📉 Drawdown Máx:    {dd:.2f}%")
    print(f"  ⚖️  Sharpe Ratio:    {sharpe:.2f}")
    
if __name__ == "__main__":
    assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    
    print("=" * 70)
    print("🦅 PREDADOR v370.3 - DUAL BACKTEST SUITE (SUPREME vs RALF)")
    print("=" * 70)
    
    results_store = {}
    
    total_pnl_supreme = 0
    total_pnl_ralf = 0
    
    for asset in assets:
        # 1. Testar Modo SUPREME/SNIPER (Padrão)
        print(f"⏳ {asset} [SUPREME]...")
        res_std = run_remote_backtest(asset, mode="STD")
        print_metrics(asset, "SUPREME", res_std)
        if "error" not in res_std:
            total_pnl_supreme += res_std.get('total_pnl_percent', 0)
            results_store[f"{asset}_STD"] = res_std

        # 2. Testar Modo RALF
        print(f"⏳ {asset} [RALF]...")
        res_ralf = run_remote_backtest(asset, mode="RALF")
        print_metrics(asset, "RALF", res_ralf)
        if "error" not in res_ralf:
            total_pnl_ralf += res_ralf.get('total_pnl_percent', 0)
            results_store[f"{asset}_RALF"] = res_ralf
            
    # Save to file
    with open("backtest_results.json", "w") as f:
        json.dump(results_store, f, indent=2)
        
    print("\n" + "="*70)
    print(f"📊 PLACAR FINAL")
    print(f"🦅 MODO SUPREME/SNIPER: {total_pnl_supreme:+.2f}%")
    print(f"🌀 MODO RALF SCALPER:   {total_pnl_ralf:+.2f}%")
    print("="*70)
    
    if total_pnl_supreme > total_pnl_ralf:
        print("🏆 VENCEDOR: MODO SUPREME (Consistência)")
    else:
        print("🏆 VENCEDOR: MODO RALF (Agressividade)")
    print("="*70)
