import os
import sys
import subprocess
from loguru import logger

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar comando: {e}")
        return False

def setup():
    logger.info("🛠️ Iniciando Setup Automatizado: POLY-PREDATOR (v1.0)")

    # 1. Verifica Python
    logger.info(f"🐍 Python Detectado: {sys.version}")

    # 2. Instala Dependências
    logger.info("📦 Instalando/Atualizando dependências...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        logger.error("❌ Falha na instalação das dependências.")
        return

    # 3. Cria .env se não existir
    if not os.path.exists(".env"):
        logger.info("📝 Criando arquivo .env a partir do template...")
        try:
            with open(".env.example", "r") as f_in, open(".env", "w") as f_out:
                f_out.write(f_in.read())
            logger.success("✅ Arquivo .env criado! EDITE-O com suas chaves antes de rodar.")
        except Exception as e:
            logger.error(f"❌ Erro ao criar .env: {e}")
    else:
        logger.info("ℹ️ Arquivo .env já existe.")

    # 4. Verifica Estrutura
    for folder in ["src", "logs", "docs", "scripts"]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f"📁 Pasta criada: {folder}")

    logger.success("🚀 Setup concluído com sucesso! A DeepMachine está pronta para caçar Baleias.")
    print("\n--- PRÓXIMOS PASSOS ---")
    print("1. Abra o arquivo .env e coloque suas chaves (Polymarket e Polygon RPC).")
    print("2. Adicione os endereços das baleias que deseja seguir no campo WHALE_ADDRESSES.")
    print("3. Rode o comando: python main.py")

if __name__ == "__main__":
    setup()
