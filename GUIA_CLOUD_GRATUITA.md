# ☁️ GUIA: CLOUD GRATUITA (API & SITE)

Além da VPS (que roda o MetaTrader), seu sistema usa serviços de **Nuvem Moderna (PaaS)** para o Cérebro (API) e a Visão (Site).

Diferente da VPS, esses serviços têm **Planos Gratuitos Ilimitados** para projetos pequenos como o seu.

---

## 1. RENDER.COM (Para a API Python)
É aqui que o `cloud_api.py` vai rodar.
*   **O que é:** Um computador Linux gerenciado que roda seu código Python.
*   **Custo:** **R$ 0,00 (Free Tier)**.
*   **Instalação:**
    1.  Crie conta no [render.com](https://render.com).
    2.  Clique "New Web Service".
    3.  Conecte seu GitHub.
    4.  Ele detecta o arquivo `render.yaml` e configura tudo sozinho.
*   **Limitação:** No plano grátis, se ninguém usar a API por 15 minutos, ela "dorme". Quando o robô mandar o primeiro sinal, ela demora uns 30 segundos para "acordar". Para nós, isso é aceitável.

## 2. VERCEL.COM (Para o Dashboard)
É aqui que o `index.html` e `main.js` vão ficar.
*   **O que é:** Hospedagem de sites super rápida (CDN).
*   **Custo:** **R$ 0,00 (Hobby Plan)**.
*   **Instalação:**
    1.  Crie conta no [vercel.com](https://vercel.com).
    2.  Clique "Add New Project".
    3.  Importe seu GitHub.
    4.  Clique Deploy.
*   **Limitação:** Nenhuma relevante para você. É extremamente rápido.

## 3. SUPABASE.COM (Banco de Dados - Opcional)
Se você quiser salvar o histórico de trades para sempre (hoje salvamos na memória RAM da API para ser simples).
*   **O que é:** Banco de Dados Postgres na nuvem.
*   **Custo:** **R$ 0,00 (500MB grátis)**.

---

## 📐 ARQUITETURA FINAL DO SISTEMA

Esta é a estrutura "Custo Zero" completa que montamos:

1.  **VPS (Google/AWS):** Roda o **MetaTrader 5** (Windows).
    *   *Você pegou grátis por 3-12 meses.*
2.  **RENDER:** Roda o **Cérebro Python** (Linux).
    *   *Grátis para sempre (dentro dos limites).*
3.  **VERCEL:** Mostra o **Painel no Celular**.
    *   *Grátis para sempre.*

**Vantagem:** Se a VPS cair ou travar, você consegue acessar o site (Vercel) e ver que o status mudou para "OFFLINE", pois a API (Render) parou de receber sinais. Você tem controle total.
