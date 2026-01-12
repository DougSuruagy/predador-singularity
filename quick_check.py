import requests, os, json

BASE = "https://predador-api.onrender.com"
TOKEN = os.getenv("INTERNAL_SECRET_TOKEN", "predador_secret_2026")
HEADERS = {"X-Token": TOKEN}

def fetch(endpoint: str, timeout: int = 30):
    url = f"{BASE}/{endpoint}"
    print(f"\n{'='*60}")
    print(f"🔎 GET {url}")
    print(f"{'='*60}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        print(f"⚡ Status: {r.status_code}")
        print("📦 Payload:")
        try:
            data = r.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(r.text[:1000])
    except Exception as exc:
        print(f"❌ Erro: {exc}")

if __name__ == "__main__":
    fetch("health")
    fetch("stats")
    fetch("state")
