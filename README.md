# 🦅 PREDATOR v13.0 | SINGULARITY 🌌

![Status](https://img.shields.io/badge/Status-ONLINE-00ff9d?style=for-the-badge)
![Edition](https://img.shields.io/badge/Edition-2026_SINGULARITY-00f2ff?style=for-the-badge)
![Infrastructure](https://img.shields.io/badge/Infrastructure-HYBRID_CLOUD-bc00ff?style=for-the-badge)

> **Sistema HFT Híbrido: Python AI + MQL5 Quantum Execution.**
> Arquitetura distribuída "Estoque Zero" com Custo Operacional Inicial Zero.

---

## 📐 Arquitetura do Sistema (Tríade Cloud)

Este projeto opera uma arquitetura moderna de **Nuvem Híbrida**, separando a inteligência (Python), a visão (Web) e a execução (MetaTrader).

| Componente | Função | Hospedagem | Custo |
| :--- | :--- | :--- | :--- |
| **🧠 CÉREBRO** | API de Inteligência e Webhooks | **Render** (Python FastApi) | Grátis |
| **👁️ VISÃO** | Dashboard de Monitoramento Mobile | **Vercel** (Static Web) | Grátis |
| **⚡ MUSCULO** | Execução de Ordens HFT | **VPS** (MetaTrader 5 Windows) | Grátis (Google/AWS) |

---

## 📂 Estrutura de Arquivos

*   `cloud_api.py`: **O Cérebro.** Servidor Python que recebe sinais do TradingView e comanda o robô.
*   `render.yaml`: Blueprint para deploy automático "Zero Config" no Render.
*   `index.html` / `main.js`: **A Visão.** Dashboard PWA responsivo para celular.
*   `c_v15_Quantum.mq5`: **O Músculo.** Expert Advisor que roda no MT5 e obedece à API.
*   `GUIA_CLOUD_GRATUITA.md`: Tutorial completo de como colocar tudo no ar sem gastar nada.

---

## 🚀 Como Iniciar (Deploy Rápido)

Para detalhes completos, leia o arquivo **[GUIA_CLOUD_GRATUITA.md](./GUIA_CLOUD_GRATUITA.md)**. Resumo rápido:

### 1️⃣ CÉREBRO (API Python)
1.  Crie conta no **[Render.com](https://render.com)**.
2.  Conecte este repositório (New Web Service).
3.  O Render detectará o arquivo `render.yaml` e instalará tudo automaticamente.
4.  **Copie a URL gerada** (ex: `https://predator-api-xyz.onrender.com`).

### 2️⃣ VISÃO (Dashboard)
1.  Edite o arquivo `main.js`: Atualize `CONFIG.API_URL` com a URL do Render.
2.  Crie conta na **[Vercel.com](https://vercel.com)**.
3.  Importe este repositório. O deploy é instantâneo.

### 3️⃣ EXECUÇÃO (MetaTrader 5)
1.  Na sua VPS, abra o MT5 (XP/Genial/BTG).
2.  Vá em `Ferramentas > Opções > Expert Advisors`.
3.  **Adicione a URL do Render** na lista "Permitir WebRequest".
4.  Compile e inicie o `c_v15_Quantum.mq5`.

---

## 💎 Filosofia "Estoque Zero"
*   **Intraday Puro:** Zero posições abertas overnight.
*   **Liquidez Forçada:** Fechamento compulsório às 17h45.
*   **Caixa Livre:** Todo dia começa com 100% de margem disponível.

---

## ⚠️ Segurança & Comandos
*   **Panic Button:** No Dashboard Web, você pode encerrar todas as posições remotamente caso a VPS trave.
*   **3-Strikes Rule:** O sistema bloqueia automaticamente após 3 perdas consecutivas para preservação de capital.

---

*Desenvolvido pela Antigravity AI - Advanced Agentic Coding 2026*
