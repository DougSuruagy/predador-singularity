# 🦅 GUIA DE DEPLOY - PREDATOR v13.0 SINGULARITY
**Arquitetura 100% Cloud | Zero Custo Inicial | Alta Performance**

## 🚀 PREDATOR v14.0 - CRYPTO CLOUD EDITION
Esta versão permite rodar 100% na Nuvem (Render) sem precisar do MetaTrader 5 aberto.

### 📋 Pré-requisitos
1.  **Binance**: Crie uma chave de API (com permissão de Futuros se for operar alavancado).
2.  **Render**: Adicione `BINANCE_API_KEY` e `BINANCE_API_SECRET` nas Variáveis de Ambiente.
3.  **Supabase**: Configure `SUPABASE_URL` e `SUPABASE_KEY` para salvar o histórico.

### 🛠️ Como Funciona
-   Sua API no Render agora é o **Cérebro e o Músculo**.
-   Ela recebe sinais (via Webhook ou Dashboard) e envia ordens direto para a Binance.
-   **PC Local pode ficar desligado.**

---

## 🏗️ VISÃO GERAL DA ARQUITETURA

1.  **CÉREBRO (API Python)**: Hospedado no **Render**. Recebe sinais, gerencia risco e conecta tudo.
2.  **MEMÓRIA (Banco de Dados)**: Hospedado no **Supabase**. Guarda histórico de trades e stats do dia.
3.  **VISÃO (Dashboard)**: Hospedado na **Vercel**. Interface visual Cyberpunk para monitoramento.
4.  **GATILHO (Sinais)**: Originados no **TradingView** via Webhook.

---

## 🚀 PASSO 1: BANCO DE DADOS (Supabase)

1.  Crie uma conta gratuita em [supabase.com](https://supabase.com).
2.  Crie um novo projeto ("New Project").
3.  Vá em **SQL Editor** no menu lateral.
4.  Copie o conteúdo do arquivo `supabase_setup.sql` (que está na sua pasta) e cole no editor.
5.  Clique em **RUN**. Isso criará as tabelas necessárias.
6.  Vá em **Project Settings (engrenagem) > API**.
7.  Copie a **Project URL** e a **anon / public key**. Guarde-as.

---

## ☁️ PASSO 2: API BACKEND (Render)

1.  Crie uma conta em [render.com](https://render.com).
2.  Clique em **New +** e selecione **Web Service**.
3.  Conecte seu repositório do GitHub onde este código está.
4.  Dê um nome para o serviço (ex: `predator-api`).
5.  Configurações:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn cloud_api:app --host 0.0.0.0 --port 10000`
6.  Role para baixo até **Environment Variables** e adicione:
    *   `SUPABASE_URL`: (Cole a URL do passo 1)
    *   `SUPABASE_KEY`: (Cole a Key do passo 1)
    *   `PYTHON_VERSION`: `3.9.0` (Recomendado)
7.  Clique em **Create Web Service**.
8.  Aguarde o deploy. Quando terminar, copie a URL do seu serviço (ex: `https://predator-api-xyz.onrender.com`).

---

## 🖥️ PASSO 3: DASHBOARD FRONTEND (Vercel)

1.  **Antes de subir**: Edite o arquivo `main.js` na sua máquina.
    *   Procure por `const CONFIG`.
    *   Em `API_URL`, substitua pela URL que você copiou do Render no passo anterior.
2.  Crie uma conta em [vercel.com](https://vercel.com).
3.  Clique em **Add New... > Project**.
4.  Importe o mesmo repositório do GitHub.
5.  A Vercel geralmente detecta tudo automaticamente. Apenas clique em **Deploy**.
6.  Pronto! Seu dashboard está live. Copie o link (ex: `https://predator-dashboard.vercel.app`).

---

## 📈 PASSO 4: CONECTAR TRADINGVIEW

1.  No gráfico do TradingView, carregue seu script (`predator_astral.pine`).
2.  Crie um **Alerta** na estratégia/estudo.
3.  Em **Webhook URL**, cole: `https://[SUA-URL-DO-RENDER]/webhook`
4.  Na mensagem do alerta, cole **exatamente** este JSON:
    ```json
    {
      "action": "{{strategy.order.action}}",
      "symbol": "WING26",
      "price": {{close}},
      "qty": 1,
      "confidence": 85,
      "message": "{{strategy.order.comment}}"
    }
    ```
5.  Clique em **Create**.

---

## ✅ COMO TESTAR TUDO

1.  Abra seu Dashboard na Vercel (no PC ou Celular).
2.  Verifique se o status está "CLOUD: ACTIVE" (bolinha verde).
3.  Use uma ferramenta como Postman (ou envie um comando via terminal) para o Render simular um sinal, ou espere o TradingView disparar.
4.  Veja o **Gráfico Neon** atualizar e o PnL mudar em tempo real!

---

**DÚVIDAS?**
Se precisar reiniciar o sistema, basta fazer um Redeploy no Render. O histórico continuará salvo no Supabase.
