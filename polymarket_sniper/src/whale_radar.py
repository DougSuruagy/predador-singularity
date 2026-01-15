import asyncio
import os
from web3 import Web3
from loguru import logger
from dotenv import load_dotenv

# Carrega chaves do .env (Sempre use um .env separado para o Polymarket!)
load_dotenv()

class WhaleRadar:
    def __init__(self):
        self.rpc_url = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # 🐋 Endereços Alfa (Baleias)
        whales_raw = os.getenv("WHALE_ADDRESSES", "")
        self.target_whales = [w.strip().lower() for w in whales_raw.split(",") if w]
        
        # 🏛️ Polymarket Ecosystem Contracts (Polygon)
        self.POLYMARKET_CONTRACTS = {
            "0x4bFbB677051C65E5c48bA4486E77F30030aD602f": "Polymarket Proxy",
            "0x4D97dfbAf705A8935c6cd3FA995934FEf89Ad320": "Conditional Token Framework",
            "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174": "USDC (Polygon)",
            "0xC5d7332C0C17173ED6682fc399D36B5d79069F74": "CTF Exchange"
        }
        
    def check_connection(self):
        if self.w3.is_connected():
            logger.info(f"✅ Conectado ao Polygon RPC: {self.rpc_url}")
            return True
        else:
            logger.error("❌ Falha na conexão com o RPC do Polygon.")
            return False

    def is_polymarket_tx(self, tx):
        """Verifica se a transação envolve contratos da Polymarket"""
        target = tx['to'].lower() if tx['to'] else ""
        return target in [addr.lower() for addr in self.POLYMARKET_CONTRACTS.keys()]

    async def watch_loop(self, callback=None):
        logger.info("🔭 Iniciando Vigilância de Baleias (Modo Event Logs)...")
        
        if not self.target_whales:
            logger.warning("⚠️ Nenhuma baleia configurada no .env!")
        else:
            logger.success(f"🐋 Monitorando {len(self.target_whales)} baleias...")
        
        # Contratos Polymarket para filtrar
        polymarket_addrs = list(self.POLYMARKET_CONTRACTS.keys())
        
        last_block = self.w3.eth.block_number
        logger.info(f"📦 Bloco inicial: {last_block}")
        
        while True:
            try:
                current_block = self.w3.eth.block_number
                
                if current_block > last_block:
                    # Usa eth_getLogs para buscar eventos dos contratos Polymarket
                    for contract_addr in polymarket_addrs:
                        try:
                            logs = self.w3.eth.get_logs({
                                'fromBlock': last_block + 1,
                                'toBlock': current_block,
                                'address': contract_addr
                            })
                            
                            for log in logs:
                                tx_hash = log['transactionHash'].hex()
                                # Busca a transação para ver quem enviou
                                tx = self.w3.eth.get_transaction(log['transactionHash'])
                                sender = tx['from'].lower()
                                
                                if sender in self.target_whales:
                                    contract_name = self.POLYMARKET_CONTRACTS.get(contract_addr, "Desconhecido")
                                    logger.warning(f"🚨 📉 TRADE POLYMARKET DETECTADO!")
                                    logger.warning(f"� Baleia: {sender}")
                                    logger.info(f"� Contrato: {contract_name}")
                                    logger.info(f"🔗 TX: https://polygonscan.com/tx/{tx_hash}")
                                    
                                    if callback:
                                        asyncio.create_task(callback(tx_hash, sender))
                        except Exception as log_err:
                            pass # Ignora erros de log individual
                    
                    last_block = current_block
                
                await asyncio.sleep(3)
                
            except Exception as e:
                # Ignora erros de PoA silenciosamente, continua tentando
                await asyncio.sleep(5)

if __name__ == "__main__":
    radar = WhaleRadar()
    if radar.check_connection():
        asyncio.run(radar.watch_loop())
