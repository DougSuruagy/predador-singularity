import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def monitor_stats():
    url = "https://fun-calley-modelo-inteligente-85d8461c.koyeb.app"
    token = os.environ.get("INTERNAL_SECRET_TOKEN", "predador_secret_2026")
    headers = {"X-Token": token}
    
    print(f"📡 Buscando Estatísticas em: {url}")
    
    try:
        s = requests.get(f"{url}/stats", headers=headers, timeout=10)
        if s.status_code == 200:
            print("\n🧠 NEURAL STATS:")
            print(json.dumps(s.json(), indent=2))
        else:
            print(f"❌ Erro na API (Status {s.status_code}): {s.text}")
            
        # Also try /state (which the dashboard uses)
        st = requests.get(f"{url}/state", headers=headers, timeout=10)
        if st.status_code == 200:
            print("\n📊 SYSTEM STATE (Dashboard Feed):")
            data = st.json()
            # Filter some fields for brevity
            filtered = {k: v for k, v in data.items() if k in ["daily_pnl", "trades", "wins", "losses", "win_rate", "regime", "confidence", "bias", "is_hunting"]}
            print(json.dumps(filtered, indent=2))
            if data.get("is_shielded"):
                print("🚨 SHIELD STATUS: ACTIVE")
            else:
                print("🛡️ SHIELD STATUS: INACTIVE")
        else:
            print(f"❌ Erro na API State (Status {st.status_code}): {st.text}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    monitor_stats()
