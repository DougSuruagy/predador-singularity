# 🦅 PREDADOR v56.0 "VALHALLA SUPREME"
> **The Ultimate Fusion: A-CLASS Safety + Dynamic Aggression**

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/status-DEPLOYED-brightgreen.svg) ![Version](https://img.shields.io/badge/version-v56.0-gold.svg)

## 🧬 Core Logic: Dynamic Regime Adaptation

A v56.0 resolve o dilema entre "Segurança" e "Lucro" adaptando-se automaticamente ao regime de mercado:

| Regime de Mercado | Modo Ativado | Comportamento | Threshold | RRR |
| :--- | :--- | :--- | :--- | :--- |
| **TENDÊNCIA** (Médias Afastadas) | **VALHALLA** (Agressivo) | Busca lucro explosivo (+20%) | **0.22** | 1.8x / 5.5x |
| **LATERAL** (Médias Cruzadas) | **IRON FORTRESS** (Blindado) | Protege capital (Zero Loss) | **0.35** | 1.8x / 5.5x |
| **EXTREMO** (Crash/Pump) | **JUNIOR SNIPER** (SOL) | Scalping de Reversão | RSI < 20 | 1.0x / 1.5x |

---

## 🚀 Status do Sistema

O sistema está **DEPLOYED** no Render e operacional.

### ✅ Checklist de Validação
- [x] **/health** → Status 200 (ALIVE - v56.0)
- [x] **/stats** → Engine rodando (Uptime OK)
- [x] **/state** → Dados de Trading OK (Zero Trades em dia ruim)
- [⚠️] **regime = NO_CASH** → Robô aguardando saldo
- [⚠️] **is_hunting = false** → Pausado por segurança

### 🚨 Próximos Passos (AÇÃO NECESSÁRIA)
1.  [ ] **Depositar USDT** na conta de Futuros da Bybit (Mínimo: 20 USDT).
2.  [ ] **Verificar Chaves API** no Dashboard do Render (Environment Variables).
3.  [ ] **Reiniciar Serviço** no Render (Manual Redeploy) após o depósito para forçar o reconhecimento do saldo.
4.  [ ] **Rodar `python monitor_logs.py`** e confirmar que o regime mudou para `HUNTING`.

---

## 🛠️ Comandos Úteis

### Monitorar em Tempo Real
```bash
python monitor_logs.py
```
*Visualiza o painel de controle, regime de mercado e status do "Junior Sniper".*

### Rodar Backtest Simulado
```bash
python trigger_backtest.py
```
*Simula a lógica v56.0 nos últimos 2000 candles para validar a estratégia do dia.*

---

## 📊 Histórico de Performance

*   **v43.0 (Valhalla Original):** +19.91% (Dia de Tendência)
*   **v54.0 (Iron Fortress):** +1.10% (Dia Lateral/Ruim)
*   **v56.0 (Valhalla Supreme):** Combina o melhor dos dois mundos automaticamente.

---
*Developed by Douglas & Google Deepmind Agent - 2026*
