# 🦅 PREDATOR v9.5 | SKYNET OMNISCIENCE 👑

![Status](https://img.shields.io/badge/Status-ONLINE-00ff9d?style=for-the-badge)
![Evolution](https://img.shields.io/badge/Edition-2026_SUPREME-00f2ff?style=for-the-badge)
![Cloud](https://img.shields.io/badge/Infrastructure-ZERO_LOCAL-bc00ff?style=for-the-badge)

> **Sistema HFT de Alta Performance para Scalping Intraday (XP/MT5).**
> Foco em Rendimento Imediato, Latência Zero e Automação de Repasse Regional.

---

## 💎 A Filosofia "ESTOQUE ZERO"
Diferente de sistemas comuns, o **PREDATOR v9.5** opera sob o protocolo de **Estoque Zero**. 
- **100% Intraday**: Nenhuma posição é carregada para o dia seguinte.
- **Liquidez Instantânea**: Todas as ordens são zeradas compulsoriamente às 17:45.
- **Risco Controlado**: Você acorda todos os dias com 100% de caixa e lucro no bolso.

## 🛠️ Arquitetura Cloudburst (Custo Zero)
O sistema foi desenhado para rodar sem depender do seu hardware local:
1.  **Vercel Cockpit**: Interface Web Premium para monitoramento global.
2.  **Render Engine**: Cérebro Neural em Python (FastAPI) que governa a lógica.
3.  **Oracle/AWS VPS**: Executor oficial MetaTrader 5 (Link direto XP).
4.  **TradingView Cloud**: Gerador de sinais via algoritmos proprietários.

---

## 🚀 Guia de Implementação (Passo a Passo)

### 1️⃣ Preparação das Contas (Custo Inicial R$ 0,00)
- **GitHub**: Crie sua conta para hospedar e versionar o código.
- **XP Investimentos**: Ative o **MetaTrader 5 (MT5)** no seu portal (Gratuito).
- **Vercel**: Conecte seu GitHub para hospedar o Dashboard Web.
- **Render**: Conecte seu GitHub para hospedar a API de Inteligência.
- **AWS/Oracle Cloud**: Crie uma conta para obter sua **VPS Windows Gratuita**.

### 2️⃣ Configuração do Cérebro (Render)
1. Crie um novo **Web Service** no Render apontando para este repositório.
2. No campo *Start Command*, use: `uvicorn cloud_api:app --host 0.0.0.0 --port $PORT`
3. Copie a URL gerada (ex: `https://seu-predador.onrender.com`).

### 3️⃣ Configuração do Cockpit (Vercel)
1. No seu `index.html`, atualize a constante `API_URL` com o endereço do seu Render.
2. Dê `git commit` e `git push`. A Vercel atualizará seu site em segundos.

### 4️⃣ Ativação na VPS (Repasse XP)
1. Instale o MT5 da XP na sua VPS.
2. Vá em `Ferramentas > Opções > Expert Advisors`. 
3. Marque "Permitir WebRequest" e adicione a URL do seu Render na lista.
4. Arraste o Expert Advisor `c_v15_Quantum.mq5` para o gráfico do **WING26** (1 Minuto).

### 5️⃣ Conexão TradingView (Gatilho)
1. Cole o script `predator_astral.pine` no Pine Editor do TradingView.
2. Crie um Alerta e, na aba **Notifications**, selecione **Webhook URL**.
3. Use a URL: `https://seu-predador.onrender.com/webhook`.

---

## 📊 Painel de Comandos
- **BUY/SELL**: Execução via fluxo de ordens (Tape Reading + AI).
- **TERMINATE ALL**: Botão de pânico para zerar todas as posições via Web.
- **BIO-BOOST**: Calibragem da agressividade do robô via nuvem.

---

## ⚖️ Aviso Legal
Este software é uma ferramenta tecnológica de automação. Operações em renda variável envolvem riscos. O desenvolvedor não se responsabiliza por resultados financeiros. **Teste sempre em conta simulada antes de ir para o real.**

---
*Desenvolvido pela Antigravity AI para Douglas - Elite Trading 2026*
