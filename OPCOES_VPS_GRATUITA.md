# GUIA: VPS GRATUITA PARA TRADING HFT (2026)
# PREDATOR V13.0 SINGULARITY

Este documento orienta sobre como obter e configurar uma VPS (Virtual Private Server) Windows GRATUITA para rodar seu MetaTrader 5 24/7.

---

## ☁️ OPÇÃO 1: AWS EC2 (Amazon Web Services)
**A mais confiável, gratuita por 12 meses.**

1. **Crie uma conta na AWS:**
   - Acesse: https://aws.amazon.com/free/
   - Crie uma conta (exige cartão de crédito para verificação, debita $1 estorno).

2. **Crie a Instância (VM):**
   - No Console AWS, procure por **"EC2"**.
   - Clique em **"Launch Instance"**.
   - **Nome:** `Predator-VPS`
   - **OS Image (AMI):** Selecione **Windows Server 2022 Base** (Importante: procure a tag "Free tier eligible").
   - **Instance Type:** `t2.micro` ou `t3.micro` (Verifique qual tem a tag "Free tier eligible").
   - **Key Pair:** Crie um novo par de chaves `.pem`, baixe e guarde (você precisará para pegar a senha).
   - **Network Settings:** Deixe padrão.

3. **Inicie e Conecte:**
   - Clique em **Launch Instance**.
   - Espere o status ficar "Running".
   - Selecione a instância e clique em **Connect > RDP Client**.
   - Clique em **Get Password**, faça o upload do seu arquivo `.pem`.
   - Copie a senha gerada e o "Public DNS".

4. **Acesse via Windows:**
   - No seu PC, abra "Conexão de Área de Trabalho Remota".
   - Cole o DNS Público em "Computador".
   - Usuário: `Administrator`.
   - Senha: (A senha que você copiou).

---

## ☁️ OPÇÃO 2: GOOGLE CLOUD PLATFORM (GCP)
**Grátis "para sempre" (com limitações), mas mais difícil de configurar Windows.**

1. Crie conta em https://cloud.google.com/free
2. Vá em **Compute Engine > VM Instances**.
3. Crie uma instância `e2-micro`.
4. **Desafio:** O Free Tier do Google geralmente é apenas para Linux. Rodar Windows consome os créditos de teste ($300) por 3 meses, depois cobra.
   - **Recomendação:** Use AWS para Windows. Google Cloud é melhor para Linux (API).

---

## ☁️ OPÇÃO 3: ORACLE CLOUD (Always Free)
**Muito potente, mas difícil de conseguir vaga (Ampere ARM).**

1. A Oracle oferece até 4 CPUs ARM e 24GB RAM grátis **para sempre**.
2. O problema: MetaTrader 5 é x86 (Intel/AMD). O Windows ARM roda MT5 por emulação, mas instalar Windows na Oracle Cloud é um processo avançado (hack).

---

## 🏆 RECOMENDAÇÃO FINAL DO PREDATOR: **AWS EC2**

A AWS é a escolha mais sólida para rodar o MT5 de graça por 1 ano.

### ⚙️ PÓS-INSTALAÇÃO (DENTRO DA VPS):

1. **Baixe o Chrome:** O Internet Explorer/Edge da VPS é bloqueado. Baixe o instalador do Chrome no seu PC, copie (Ctrl+C) e cole (Ctrl+V) dentro da janela da VPS.
2. **Instale o MetaTrader 5:** Baixe da sua corretora (XP, Genial, etc).
3. **Instale os Arquivos do PREDATOR:**
   - Copie sua pasta `MQL5` inteira do seu PC.
   - Cole na VPS.
4. **Configure a URL da API:**
   - No MT5 da VPS, vá em **Ferramentas > Opções > Expert Advisors**.
   - Adicione sua URL de produção: `https://predator-api-[SEU-ID].onrender.com` (NÃO use localhost na VPS, pois a API está na nuvem Render).

---

💡 **DICA DE OURO:**
Na AWS, lembre-se de configurar o MetaTrader para não atualizar gráficos pesados. Uma VPS `t2.micro` tem apenas 1GB de RAM.
- No MT5: Ferramentas > Opções > Gráficos > "Máximo de barras no gráfico" -> Coloque `1000`.
Isso fará o MT5 voar mesmo na VPS grátis fraca.
