import requests
from loguru import logger

class PolyMapper:
    def __init__(self):
        self.gamma_api = "https://gamma-api.polymarket.com"

    def get_token_id_by_condition(self, condition_id, outcome_index=0):
        """
        Traduz um condition_id da blockchain para os token_ids da Polymarket.
        Geralmente: outcome 0 = YES, outcome 1 = NO
        """
        try:
            url = f"{self.gamma_api}/markets"
            params = {"condition_id": condition_id}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    market = data[0]
                    # Retorna os IDs dos tokens para YES e NO
                    clob_token_ids = market.get("clobTokenIds") # String formatada como JSON
                    import json
                    tokens = json.loads(clob_token_ids)
                    
                    logger.success(f"🎯 Mercado Mapeado: {market['question']}")
                    return tokens[outcome_index]
            return None
        except Exception as e:
            logger.error(f"⚠️ Falha no mapeamento de token: {e}")
            return None

    def decode_tx_data(self, input_data):
        """
        Lógica para extrair o conditionId e a direção do trade do input data da TX.
        Nota: Requer análise do ABI do contrato CTF Exchange.
        """
        # Esta é uma versão simplificada. Em produção, usaríamos o ABI oficial.
        # Mas para o desafio, vamos focar no mapeamento via logs de eventos.
        pass
