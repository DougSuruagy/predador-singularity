import json
from web3 import Web3
from loguru import logger

class PolyDecoder:
    def __init__(self, w3_instance):
        self.w3 = w3_instance
        # ABI mÃnima para decodificar o evento 'Trade' do CTF Exchange
        # Evento Trade(bytes32 indexed conditionId, ...)
        self.TRADE_EVENT_ABI = {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "bytes32", "name": "conditionId", "type": "bytes32"},
                {"indexed": False, "internalType": "uint256", "name": "outcomeIndex", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "price", "type": "uint256"},
                {"indexed": True, "internalType": "address", "name": "maker", "type": "address"},
                {"indexed": True, "internalType": "address", "name": "taker", "type": "address"}
            ],
            "name": "Trade",
            "type": "event"
        }
        # TÃ³pico 0 do evento 'Trade' (keccak256("Trade(bytes32,uint256,uint256,uint256,address,address)"))
        self.TRADE_TOPIC = "0x011b95383f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f" # Simplificado para o exemplo
        # O tÃ³pico real Ã©: Web3.keccak(text="Trade(bytes32,uint256,uint256,uint256,address,address)").hex()
        self.CTF_EXCHANGE = "0xC5d7332C0C17173ED6682fc399D36B5d79069F74"

    def decode_trade_log(self, receipt):
        """
        Varre os logs de um recibo de transaÃ§Ã£o em busca de eventos de Trade da Polymarket.
        """
        trades = []
        for log in receipt['logs']:
            # Verifica se o log vem do contrato da CTF Exchange
            if log['address'].lower() == self.CTF_EXCHANGE.lower():
                try:
                    # Decodifica o log usando a ABI do evento Trade
                    # Nota: Em implementaÃ§Ã£o real, usarÃamos contract.events.Trade().processLog(log)
                    # Aqui simulamos a extraÃ§Ã£o de dados brutos para o desafio
                    condition_id = log['topics'][1].hex()
                    logger.success(f"🔓 Evento de Trade decodificado! ConditionID: {condition_id}")
                    trades.append({
                        "conditionId": condition_id,
                        "tx_hash": log['transactionHash'].hex()
                    })
                except Exception as e:
                    logger.error(f"⚠️ Erro ao decodificar log: {e}")
        return trades
