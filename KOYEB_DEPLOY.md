# 🚀 Guia de Deploy - PREDATOR no KOYEB

O Koyeb é uma alternativa excelente e gratuita ao Render. Siga os passos abaixo para colocar o sistema no ar.

## 1. Crie sua conta
Acesse [koyeb.com](https://www.koyeb.com/) e crie uma conta (pode usar o GitHub).

## 2. Crie o Serviço (App)
1. No dashboard, clique em **Create App**.
2. Selecione **GitHub** como fonte.
3. Escolha o repositório `predador-singularity`.

## 3. Configurações do Serviço
O Koyeb deve detectar automaticamente que é um projeto Python, mas confirme:
*   **Builder**: Buildpack (Padrão)
*   **Build Command**: `pip install -r requirements.txt`
*   **Run Command**: `uvicorn cloud_api:app --host 0.0.0.0 --port 8000`
    *   *(Se ele ler o arquivo `Procfile` que criamos, isso já virá preenchido)*

## 4. Variáveis de Ambiente (Environment Variables)
Clique em **"Add Variable"** e adicione as essenciais (copie da sua planilha ou do Render antigo):

| Key | Value |
| :--- | :--- |
| `App Name` | `predador-api` (Sugestão) |
| `PYTHON_VERSION` | `3.11` |
| `BYBIT_API_KEY` | *(Sua Key)* |
| `BYBIT_API_SECRET` | *(Seu Secret)* |
| `INTERNAL_SECRET_TOKEN` | `predador_secret_2026` |
| `SUPABASE_URL` | `https://xayaogxbjudpmwylaiuf.supabase.co` |
| `SUPABASE_KEY` | *(Sua Key)* |
| `NODE_ROLE` | `PRIMARY` |

## 5. Região
*   Escolha **Frankfurt (Germany)** para evitar o bloqueio da Bybit (Geo-Block) e ter baixa latência.

## 6. Deploy
Clique em **Deploy**. O Koyeb é muito rápido, em 2-3 minutos estará online.

---

### 🧠 E o Nó Brain (Dual-Core)?
Se quiser rodar o nó secundário (Brain):
1. Crie um **segundo serviço** no Koyeb (pode ser no mesmo App ou outro).
2. Use as mesmas configs, mas mude a variável:
    *   `NODE_ROLE` = `BRAIN`
3. A URL desse novo serviço será seu `BRAIN_URL`.
