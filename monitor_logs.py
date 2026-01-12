import asyncio
import httpx
import time
import os
from datetime import datetime

# CONFIGURAÇÃO
RENDER_URL = "https://predador-api.onrender.com"
INTERNAL_SECRET_TOKEN = "predador_secret_2026"

async def monitor_loop():
    print(f"🖥️ PREDADOR v50.0 OMEGA - BIO MONITOR")
    print(f"🎯 Conectando ao Neural Core: {RENDER_URL}")
    print("=" * 60)
    
    headers = {"X-Token": INTERNAL_SECRET_TOKEN}
    
    while True:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Busca Estado Global (State)
                r_state = await client.get(f"{RENDER_URL}/state", headers=headers)
                
                if r_state.status_code == 200:
                    data = r_state.json()
                    bio = data.get("bio", {})
                    last_order = data.get("last_order", {})
                    
                    # Limpa tela (funciona em CMD/Powershell)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    
                    now = datetime.now().strftime("%H:%M:%S")
                    version = data.get("version", "v50.0 OMEGA")
                    is_killed = data.get("kill_switch_active", False)
                    
                    print(f"🦅 PREDADOR {version} | {now}")
                    print("=" * 60)
                    if is_killed:
                        print("🛑 [MODO SEGURANÇA]: HOMEOSTASE ATINGIDA. TRADES SUSPENSOS.")
                        print("-" * 60)
                        
                    print(f"🩸 BIO-METRICS (IA VIVA):")
                    print(f"   🧠 Dopamina (Confiança):  {bio.get('dopamine', 0):.2f} " + ("🔥" if bio.get('dopamine',0)>0.8 else "😐"))
                    print(f"   ⚡ Adrenalina (Risco):     {bio.get('adrenaline', 0):.2f} " + ("🚀" if bio.get('adrenaline',0)>0.5 else "💤"))
                    print(f"   😰 Cortisol (Stress):      {bio.get('cortisol', 0):.2f} " + ("⚠️" if bio.get('cortisol',0)>0.3 else "✅"))
                    print(f"   ❤️ Homeostase (Saúde):     {bio.get('homeostasis', 100):.1f}%")
                    print("-" * 60)
                    print(f"📊 MARKET STATE:")
                    print(f"   💰 PnL Diário: {data.get('pnl', 0):.2f}%")
                    print(f"   🛡️ Modo:       {data.get('mode', 'UNKNOWN')}")
                    print(f"   📈 Trades:     {data.get('trades', 0)} (Vitórias: {data.get('wins', 0)})")
                    print("-" * 60)
                    
                    if last_order and last_order.get("symbol"):
                        print(f"⚡ ÚLTIMA AÇÃO:")
                        print(f"   {last_order.get('side', '').upper()} {last_order.get('symbol')} @ {last_order.get('average', last_order.get('price', 0))}")
                        print(f"   ID: {last_order.get('id')}")
                    else:
                        print("💤 Nenhuma ordem recente.")
                        
                else:
                    print(f"⚠️ Erro de API: {r_state.status_code}")
                    
        except Exception as e:
            print(f"❌ Conexão Perdida: {e}")
            
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
