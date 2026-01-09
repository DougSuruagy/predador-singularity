# GUIA: CRIANDO SUA VPS "ZERO CUSTO" NA AWS (AMAZON)

Para rodar o robô 24/7 sem deixar seu computador ligado, usaremos a **AWS Free Tier**, que oferece 12 meses grátis de um computador Windows na nuvem.

---

## 🏗️ FASE 1: Criando a Máquina (O "Corpo")

1.  **Acesse:** [aws.amazon.com/free](https://aws.amazon.com/free)
2.  **Crie uma conta:** Você precisará de um cartão de crédito (apenas para verificação, não será cobrado se seguir os limites grátis).
3.  **No Console AWS:** Pesquise por **"EC2"** na barra de busca e clique nele.
4.  **Botão Laranja:** Clique em **"Launch Instance"** (Lançar Instância).

### ⚙️ Configuração da Máquina (Siga EXATAMENTE para ser grátis):

*   **Name:** `Predator-VPS`
*   **AMI (Sistema Operacional):** Selecione **Windows**.
    *   *Importante:* Escolha "Windows Server 2022 Base" (Verifique se tem a etiqueta "Free tier eligible").
*   **Instance Type:** `t2.micro` ou `t3.micro`.
    *   *Verifique:* Deve ter a etiqueta "Free tier eligible".
*   **Key Pair (Chave de Acesso):**
    *   Clique em "Create new key pair".
    *   Nome: `ChavePredator`.
    *   O arquivo `.pem` vai baixar no seu PC. **GUARDE ESSE ARQUIVO, ELE É A SENHA.**

*   **Network Settings:** Deixe padrão.
*   **Storage:** Pode deixar 30GB (o limite grátis é 30GB).

*   **FINAL:** Clique em **"Launch Instance"**.

---

## 🔌 FASE 2: Conectando na Nuvem

Espere uns 5 minutos para a máquina "ligar".

1.  No painel EC2, clique na sua instância `Predator-VPS`.
2.  Clique em **Connect** (botão superior).
3.  Vá na aba **RDP Client**.
4.  Clique em **"Get Password"**.
    *   Faça upload daquele arquivo `ChavePredator.pem` que você baixou.
    *   O site vai te mostrar a senha do Windows da VPS.
5.  Clique em **"Download Remote Desktop File"**.

**Agora a mágica acontece:**
1.  Abra o arquivo que baixou.
2.  Coloque a senha que a AWS te mostrou.
3.  Uma janela vai abrir. **Você agora está dentro de um computador da Amazon.**

---

## 🛠️ FASE 3: Instalação do Robô (Dentro da VPS)

Agora que você está dentro da VPS (Janela Remota):

1.  Abra o Edge (Internet Explorer).
2.  Baixe o **MetaTrader 5** da sua corretora (XP, Rico, etc).
3.  Faça login na sua conta.
4.  **Transfira o Robô:**
    *   No seu PC pessoal, copie o arquivo `c_v15_Quantum.ex5`.
    *   Vá na janela da VPS e dê `Ctrl+V` (Colar) na área de trabalho. Sim, funciona!
5.  Coloque na pasta Experts, configure a URL da API e ative o robô.

---

## 💡 DICAS DE OURO (Performance na Máquina Grátis)

A máquina grátis (t2.micro) é fraca. Para o robô voar nela:

1.  **Feche TUDO que não for o MT5.** (Server Manager, Edge, etc).
2.  **No MT5:**
    *   Menu `Ferramentas` > `Opções` > `Servidor`: Desmarque "Notícias".
    *   Menu `Gráficos`: Coloque o máximo de barras no gráfico para `1000` (Economiza RAM).
    *   **MINIMIZE O MT5:** Não deixe o gráfico aberto desenhando candles. Minimize a janela. O robô continua rodando e gasta 90% menos CPU.

---

## ⚠️ AVISO DE CUSTO
A AWS é grátis por 750 horas/mês (o mês todo) se você usar SÓ UMA máquina. Se criar duas, você paga. Se passar de 1 ano, você paga.
*Lembre-se de colocar um alarme no celular para daqui a 11 meses.*
