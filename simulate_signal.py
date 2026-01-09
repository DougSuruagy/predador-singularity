import urllib.request
import json
import time
import random

def send_signal(action, price, confidence):
    url = "http://127.0.0.1:8000/webhook"
    
    payload = {
        "action": action,
        "symbol": "WING26",
        "price": price,
        "confidence": confidence,
        "qty": 1,
        "message": "Sinal Simulado via Terminal"
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        print(f"📡 Enviando {action} @ {price} (Conf: {confidence}%)...")
        with urllib.request.urlopen(req) as response:
            resp_body = response.read().decode('utf-8')
            print(f"✅ RESPOSTA DA API: {resp_body}")
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    print("🦅 PREDATOR SIMULATION TOOL")
    print("---------------------------")
    
    # Preço base
    base_price = 128150.0
    
    # Simular 3 sinais rápidos para ver o gráfico mexer
    for i in range(3):
        variation = random.uniform(-50, 50)
        price = base_price + variation
        action = "BUY" if variation > 0 else "SELL"
        conf = round(random.uniform(80, 99), 1)
        
        send_signal(action, price, conf)
        time.sleep(2) # Pausa de 2s entre sinais para dar tempo de ver
    
    print("\nVerifique o Dashboard agora!")
