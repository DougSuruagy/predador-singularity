# GUIA: VPS NO GOOGLE CLOUD (Crédito de $300 / R$ 1.500)

Diferente da AWS (que dá 1 ano de máquina fraca), o Google Cloud te dá **$300 dólares (aprox. R$ 1.500)** de crédito para gastar como quiser por 90 dias.

Isso permite criar uma máquina **MUITO MAIS POTENTE** que a da AWS, ideal para rodar o robô sem travamentos.

---

## 🏗️ FASE 1: Criando a Máquina Potente

1.  **Acesse:** [cloud.google.com](https://cloud.google.com) e clique em "Comece agora gratuitamente".
2.  **Conta:** Faça login com seu Gmail e cadastre o cartão (verificação de identidade, não cobra se tiver crédito).
3.  **No Console:**
    *   Abra o menu lateral (três riscos) > **Compute Engine** > **Instâncias de VM**.
    *   Clique em **"CRIAR INSTÂNCIA"**.

### ⚙️ Configuração (Para usar o Crédito Grátis):

1.  **Nome:** `predator-gcp`
2.  **Região:** `us-central1 (Iowa)` ou `us-east1` (Carolina do Sul). São as mais baratas.
3.  **Configuração da Máquina:**
    *   Aqui está o pulo do gato. Como temos crédito, não use a "micro".
    *   Escolha **Série E2**.
    *   Tipo: **e2-medium** (2 vCPUs, 4 GB de memória).
    *   *Nota:* Essa máquina roda o MT5 liso, diferente da AWS que engasga.

4.  **Disco de Inicialização (Boot Disk):**
    *   Clique em "Alterar".
    *   Sistema Operacional: **Windows Server**.
    *   Versão: **Windows Server 2022 Datacenter** ( Desktop Experience).
    *   Tamanho: **50 GB**.
    *   Clique em "Selecionar".

5.  **Firewall:** Marque "Permitir tráfego HTTP" e "HTTPS".
6.  **CRIAR:** Role até em baixo e clique no botão azul.

---

## 🔌 FASE 2: Gerando a Senha e Conectando

Após 2 minutos, a máquina estará com um "check" verde ✅.

1.  Na lista de instâncias, clique na setinha ao lado de **RDP**.
2.  Clique em **"Configurar senha do Windows"**.
    *   O usuário será seu nome ou `douglas`.
    *   Copie a senha gigante que ele gerar. **SALVE ELA.**

**Conectando:**
1.  Clique na setinha do RDP novamente -> **"Fazer download do arquivo RDP"**.
2.  Abra o arquivo no seu PC.
3.  Cole a senha que você gerou.
4.  Pronto! Você está num PC Gamer na nuvem.

---

## 🛠️ FASE 3: Instalação (Igual AWS)

1.  Abra o Edge na VPS.
2.  Baixe o MT5 da corretora e instale.
3.  Copie seu robô (`.ex5`) do PC e cole na VPS (`Ctrl+C` / `Ctrl+V`).

---

## ⚠️ AVISO CRÍTICO (Diferença Google vs AWS)

*   **Google Cloud:** Máquina forte, roda liso. Mas dura apenas enquanto durar o crédito de $300 (geralmente 3 meses se deixar ligada direto).
*   **AWS:** Máquina fraca, mas dura 12 meses grátis.

**Minha Recomendação:** Comece no Google Cloud para testar o sistema com performance máxima. Quando o crédito acabar, se você já tiver lucrado, pague a máquina (aprox R$ 150/mês) ou migre pra AWS Free Tier.
