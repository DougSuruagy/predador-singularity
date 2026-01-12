import requests
import time
import sys

URL = "https://predador-api.onrender.com" # URL padrão, ajuste se necessário

def keep_alive():
    print(f"🔌 INICIANDO PROTOCOLO KEEP-ALIVE PARA {URL}")
    print("♾️  SISTEMA RODARÁ EM LOOP INFINITO PARA EVITAR HIBERNAÇÃO DO RENDER.")
    
    fails = 0
    while True:
        try:
            r = requests.get(f"{URL}/health", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"✅ [{time.strftime('%H:%M:%S')}] PING OK | Version: {data.get('version')} | Status: {data.get('status')}")
                fails = 0
            else:
                print(f"⚠️ [{time.strftime('%H:%M:%S')}] PING ERROR: Status {r.status_code}")
                fails += 1
        except Exception as e:
            print(f"❌ [{time.strftime('%H:%M:%S')}] CONNECTION FAIL: {e}")
            fails += 1
            
        if fails > 5:
            print("🚨 ALERTA CRÍTICO: API PARECE FORA DO AR.")
            
        # Espera 10 minutos (Render dorme em 15min)
        time.sleep(600)

if __name__ == "__main__":
    try:
        keep_alive()
    except KeyboardInterrupt:
        print("\n🛑 Keep-Alive encerrado pelo usuário.")
