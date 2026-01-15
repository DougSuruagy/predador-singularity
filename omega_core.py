import asyncio
import os
import sys
from loguru import logger
from dotenv import load_dotenv

# 🔥 CORREÇÃO DE PATRIMÔNIO: Ensina o Python a achar a pasta src do Sniper
sys.path.append(os.path.join(os.getcwd(), "polymarket_sniper"))

# Importa o coração do Predador Bybit
from cloud_api import engine_state, autonomous_hunter_loop, exchange
# Importa o coração do Poly-Predator
from main import PolySniperOrchestrator

load_dotenv()

class PredatorOmega:
    def __init__(self):
        self.version = "v1.0-OMEGA-SINGULARITY"
        self.poly_orchestrator = PolySniperOrchestrator()
        
    async def boot_sequence(self):
        print(f"""
        {'-'*50}
        🧬 PREDADOR-OMEGA: SER ÚNICO VIVO ATIVADO
        Versão: {self.version}
        Hardware: DeepMachine (Xeon 24-Threads | GTX 1660 SUPER)
        Modo: HFT (Bybit) + Whale-Sniper (Polymarket)
        {'-'*50}
        """)
        
        # 1. Verificações de Conectividade
        logger.info("📡 Sincronizando Sistemas de Telemetria Interconectados...")
        
        # 2. Inicialização em Paralelo (Nuclear-Parallelism)
        # O Xeon vai distribuir essas tarefas entre seus núcleos
        tasks = [
            self.run_bybit_hft(),
            self.run_poly_sniper()
        ]
        
        await asyncio.gather(*tasks)

    async def run_bybit_hft(self):
        logger.info("🦅 BLOCO A: Iniciando Motor HFT Bybit (Nuclear Axon)...")
        try:
            await autonomous_hunter_loop()
        except Exception as e:
            logger.error(f"⚠️ Falha no Pulmão Bybit: {e}")

    async def run_poly_sniper(self):
        logger.info("🐋 BLOCO B: Iniciando Radar Sniper Polymarket...")
        try:
            # Sincroniza o loop do Poly-Sniper
            await self.poly_orchestrator.start()
        except Exception as e:
            logger.error(f"⚠️ Falha no Olho Polymarket: {e}")

if __name__ == "__main__":
    # Configuração de Log Unificado: Distingue os dois sistemas
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
    logger.add("logs/omega_history.log", rotation="50 MB")
    
    omega = PredatorOmega()
    try:
        asyncio.run(omega.boot_sequence())
    except KeyboardInterrupt:
        logger.warning("💤 ORE PREDADOR-OMEGA entrando em hibernação...")
