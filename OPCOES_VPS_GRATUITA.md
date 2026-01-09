# 🏆 GUIA DEFINITIVO: VPS GRATUITA PARA TRADER

Para rodar o MetaTrader 5 sem pagar nada, você tem **3 Grandes Opções**. Todas elas exigem um cartão de crédito apenas para verificar que você é humano (não cobram se você seguir as regras).

ATENÇÃO: Não existem VPS Windows "gratuitas para sempre" sem cadastro, pois a licença do Windows custa dinheiro. As opções abaixo são grandes empresas te dando um "período de teste longo".

---

## 🥇 OPÇÃO 1: AWS (Amazon) - A Melhor para Longo Prazo
*   **Quanto tempo de graça?** 12 Meses (1 Ano).
*   **Sistema:** Windows Server 2022.
*   **Potência:** Baixa (1 vCPU, 1GB RAM).
*   **Ideal para:** Quem quer esquecer o robô rodando por um ano.
*   **Como conseguir:** [Seguir Tutorial AWS que criei](TUTORIAL_VPS_AWS.md)

## 🥈 OPÇÃO 2: Google Cloud - A Melhor Performance
*   **Quanto tempo de graça?** Aprox. 3 Meses (Te dão $300 dólares de crédito).
*   **Sistema:** Windows Server Datacenter.
*   **Potência:** ALTA (2 vCPUs, 4GB RAM). Rodar liso!
*   **Ideal para:** Testar o sistema com força máxima e fazer dinheiro rápido para pagar uma VPS depois.
*   **Como conseguir:** [Seguir Tutorial Google que criei](TUTORIAL_VPS_GOOGLE.md)

## 🥉 OPÇÃO 3: Microsoft Azure
*   **Quanto tempo de graça?** 12 Meses.
*   **Sistema:** Windows.
*   **Potência:** Semelhante à AWS (B1s instance).
*   **Link:** [azure.microsoft.com/free](https://azure.microsoft.com/free)

---

## 🚫 OPÇÃO 4: Oracle Cloud (CUIDADO)
Você vai ouvir falar que a Oracle tem uma VPS "Grátis para Sempre" (Always Free) com 24GB de RAM.
*   **O Problema:** Ela usa processadores **ARM** (tipo de celular) e roda **Linux**.
*   **Serve pro Robô?** **NÃO.** O MetaTrader 5 da XP/Rico foi feito para Windows e processadores Intel/AMD. Tentar rodar lá é extremamente difícil e instável. Não recomendo para operar dinheiro real.

---

## 💡 RESUMO: QUAL ESCOLHER?

1.  **Quero rodar AGORA com potência máxima:** Escolha **Google Cloud** (Opção 2).
2.  **Quero rodar o ano todo sem me preocupar:** Escolha **AWS** (Opção 1 - Lembre de configurar o MT5 para economizar RAM).
3.  **Não tenho cartão de crédito:** Você não conseguirá pegar VPS gratuita nas gigantes.
    *   *Solução:* Deixe seu próprio computador ligado ou busque uma VPS brasileira barata (ex: iPlan, MetaQuotes VPS por $15).

---
**⚠️ DICA DE SEGURANÇA:**
Ao criar a VPS, anote a senha em um papel. Se perder o arquivo `.pem` (chave), você perde acesso à máquina e terá que criar outra.
