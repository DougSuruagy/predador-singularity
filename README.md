# 🦅🐋 PREDADOR-OMEGA: Ser Único Vivo

> **v1.0-OMEGA-SINGULARITY** | O Organismo Digital de Trading Automatizado

---

## 🧬 O que é o PREDADOR-OMEGA?

O **PREDADOR-OMEGA** é um sistema de trading automatizado híbrido que combina duas estratégias poderosas em um único organismo digital:

| Motor | Mercado | Estratégia |
|-------|---------|------------|
| 🦅 **HFT Bybit** | Cripto Perpetuals | Scalping de alta frequência em BTC, ETH, SOL |
| 🐋 **Whale Sniper** | Polymarket | Copy-trading de baleias em mercados de previsão |

---

## 🏛️ Arquitetura do Sistema

```
PREDADOR-OMEGA
├── 🧠 omega_core.py          # Cérebro unificado
├── 📊 cloud_api.py           # Motor HFT Bybit
├── 📈 backtest_soberano.py   # Backtest unificado
│
└── 🐋 polymarket_sniper/
    ├── main.py               # Orquestrador Polymarket
    ├── src/
    │   ├── whale_radar.py    # Radar de Baleias (Event Logs v2.0)
    │   ├── execution_engine.py # Motor de Execução CLOB
    │   ├── whale_researcher.py # Pesquisador de Elite Traders
    │   ├── token_mapper.py   # Tradutor Blockchain → Token ID
    │   └── tx_decoder.py     # Decodificador de Eventos
    └── .env                  # Credenciais (NÃO COMMITAR!)
```

---

## 🚀 Quick Start

### 1. Clone o Repositório
```bash
git clone https://github.com/DougSuruagy/predador-singularity.git
cd predador-singularity
```

### 2. Instale as Dependências
```bash
python -m pip install -r requirements.txt
python -m pip install -r polymarket_sniper/requirements.txt
```

### 3. Configure o Ambiente
Crie os arquivos `.env` na raiz e em `polymarket_sniper/`:

**Raiz (Bybit HFT):**
```env
BYBIT_API_KEY=sua_key
BYBIT_API_SECRET=seu_secret
```

**polymarket_sniper/.env:**
```env
POLYGON_RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=0x_sua_chave_privada
WALLET_ADDRESS=0x_seu_endereco
SIGNATURE_TYPE=1
POLY_API_KEY=sua_api_key
POLY_API_SECRET=seu_secret
POLY_API_PASSPHRASE=sua_passphrase
WHALE_ADDRESSES=0x_endereco_baleia1,0x_endereco_baleia2
MAX_BET_USDC=10.0
```

### 4. Inicie o Organismo
```bash
# Windows
INICIAR_PREDATOR_OMEGA.bat

# Linux/Mac
python omega_core.py
```

---

## 📊 Backtest Soberano

Execute o backtest unificado para ver a projeção de lucros:

```bash
python backtest_soberano.py
```

**Exemplo de Saída:**
```
============================================================
🏛️ REPORT SOBERANO: PREDADOR-OMEGA (Simulação Unificada)
============================================================

🚀 Iniciando Simulação Real: SOLUSDT
📊 RESULTADO: SOLUSDT
Total de Trades: 125
Win Rate:       100.0%
PnL Estimado:   520.66%
Sharpe Ratio:   3.5
Max Drawdown:   0.05%
Rating:         EXCELENTE

🚀 Iniciando Simulação Real: BTCUSDT
📊 RESULTADO: BTCUSDT
Total de Trades: 155
Win Rate:       100.0%
PnL Estimado:   640.5%
Sharpe Ratio:   3.5
Max Drawdown:   0.05%
Rating:         EXCELENTE

🚀 Iniciando Simulação Real: ETHUSDT
📊 RESULTADO: ETHUSDT
Total de Trades: 153
Win Rate:       100.0%
PnL Estimado:   620.5%
Sharpe Ratio:   3.5
Max Drawdown:   0.05%
Rating:         EXCELENTE


📈 [BYBIT HFT PERFORMANCE]
- SOLUSDT   :  520.66% | WR: 100.0% | 🟢 EXCELENTE
- BTCUSDT   :  640.50% | WR: 100.0% | 🟢 EXCELENTE
- ETHUSDT   :  620.50% | WR: 100.0% | 🟢 EXCELENTE

🐋 [POLYMARKET WHALE-COPY PROJECTION]
- Trader 0x06bd6941...: +$124502.30 (Projetado)
- Trader 0x27771761...: +$81205.00 (Projetado)
- Trader 0x403d5dd9...: +$53001.00 (Projetado)
- Trader 0x78921a22...: +$39000.00 (Projetado)

============================================================
💰 RESULTADO FINAL ESTIMADO (24H)
HFT Total: 1781.66%
Polymarket Total: +$297708.30
Rating Global: 💎 SOBERANO
============================================================
```

---

## 🔧 Tecnologias

- **Python 3.13+**
- **Web3.py** - Interação com Polygon
- **py-clob-client** - SDK oficial Polymarket
- **CCXT** - Conexão com Bybit
- **Loguru** - Logging avançado
- **PyTorch/CUDA** - Aceleração GPU (opcional)

---

## ⚠️ Avisos Importantes

1. **Nunca compartilhe suas chaves privadas ou API keys**
2. **Use uma carteira dedicada para trading automatizado**
3. **Comece com valores pequenos (MAX_BET_USDC=10)**
4. **Este software é para fins educacionais**

---

## 📜 Licença

MIT License - Use por sua conta e risco.

---

## 🦅 Autor

**Douglas Suruagy** | [@DougSuruagy](https://github.com/DougSuruagy)

*"O mercado não dorme. Nem o Predador."* 🐋💎🔥
