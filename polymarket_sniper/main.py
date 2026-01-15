import asyncio
import os
from loguru import logger
from dotenv import load_dotenv
from src.whale_radar import WhaleRadar
from src.execution_engine import PolyExecutionEngine
from src.whale_researcher import WhaleResearcher
from src.token_mapper import PolyMapper
from src.tx_decoder import PolyDecoder

load_dotenv()

class PolySniperOrchestrator:
    def __init__(self):
        self.radar = WhaleRadar()
        self.engine = PolyExecutionEngine()
        self.researcher = WhaleResearcher()
        self.mapper = PolyMapper()
        self.decoder = PolyDecoder(self.radar.w3) # Usa a mesma instância do Web3
        self.copy_ratio = float(os.getenv("DEFAULT_COPY_RATIO", 1.0))
        self.max_bet = float(os.getenv("MAX_BET_USDC", 10.0))

    async def handle_whale_tx(self, tx_hash, whale_address):
        """
        🔥 CONEXÃO REAL: Decodifica TX -> Traduz Token -> Executa
        """
        logger.warning(f"⚡ Analisando Blockchain Trade da Baleia {whale_address}...")
        
        try:
            # 1. Obtém o recibo da transação para ver os logs/eventos
            receipt = self.radar.w3.eth.get_transaction_receipt(tx_hash)
            trades = self.decoder.decode_trade_log(receipt)
            
            for trade in trades:
                # 2. Mapeia para Token ID
                token_id = self.mapper.get_token_id_by_condition(trade['conditionId'])
                
                if token_id:
                    # 3. Executa a Cópia Real
                    logger.info(f"💎 Copiando Baleia no Token: {token_id}")
                    await self.engine.execute_market_trade(token_id, self.max_bet)
                else:
                    logger.info(f"🔭 Mercado detectado na rede, mas não listado na Polymarket Gamma API.")
        except Exception as e:
            logger.error(f"⚠️ Falha no processamento da TX {tx_hash}: {e}")

    async def start(self):
        logger.info("🦅 INICIANDO ORQUESTRAÇÃO POLY-PREDATOR (v1.0)")
        
        # O cliente já é inicializado no __init__ do engine.
        # Caso queira testar a conexão, o engine faz isso internamente.
        try:
            # Teste rápido de leitura para validar as chaves
            self.engine.client.get_server_time()
            logger.success("✅ Conexão Polymarket CLOB Autenticada!")
        except Exception as e:
            logger.error(f"🚨 Falha ao conectar na Polymarket: {e}")
            return

        # 2. Pesquisa de Baleias (Opcional: Se não houver no .env, busca as do topo)
        whales = os.getenv("WHALE_ADDRESSES", "").split(",")
        if not whales or whales[0] == "":
            logger.info("🔎 Nenhuma baleia no .env. Buscando elite no Leaderboard...")
            top_traders = self.researcher.get_elite_traders()
            whales = [t['address'] for t in top_traders[:5]]
            self.radar.target_whales = whales
            logger.info(f"🐳 Seguindo {len(whales)} baleias do topo.")
        else:
            self.radar.target_whales = [w.strip() for w in whales]
            logger.info(f"🐳 Seguindo baleias configuradas no .env: {self.radar.target_whales}")

        # 3. Loop de Monitoramento e Execução
        logger.success("🚀 Sistema Online! Aguardando movimentação das baleias...")
        
        # Aqui integraríamos o radar com a execução real
        # Por enquanto, rodamos o radar em paralelo
        await asyncio.gather(
            self.radar.watch_loop(callback=self.handle_whale_tx),
        )

if __name__ == "__main__":
    # Configuração de Logs
    logger.add("logs/polymarket_sniper.log", rotation="10 MB", level="INFO")
    
    orchestrator = PolySniperOrchestrator()
    try:
        asyncio.run(orchestrator.start())
    except KeyboardInterrupt:
        logger.warning("👋 Sistema encerrado pelo usuário.")
