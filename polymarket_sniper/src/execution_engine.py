import os
import asyncio
from loguru import logger
from dotenv import load_dotenv
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON
from py_clob_client.clob_types import MarketOrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY, SELL

load_dotenv()

class PolyExecutionEngine:
    def __init__(self):
        self.host = "https://clob.polymarket.com"
        self.key = os.getenv("PRIVATE_KEY")
        self.funder = os.getenv("WALLET_ADDRESS")
        self.chain_id = int(os.getenv("CHAIN_ID", 137))
        self.sig_type = int(os.getenv("SIGNATURE_TYPE", 0))
        
        # API Creds (Opcionais se você já tiver, mas o SDK pode derivar)
        self.api_key = os.getenv("POLY_API_KEY")
        self.api_secret = os.getenv("POLY_API_SECRET")
        self.api_passphrase = os.getenv("POLY_API_PASSPHRASE")

        # Inicializa o Cliente conforme a documentação oficial
        self.client = ClobClient(
            self.host,
            key=self.key,
            chain_id=self.chain_id,
            signature_type=self.sig_type,
            funder=self.funder
        )

        # Autenticação: Define as credenciais se existirem no .env
        if self.api_key:
            self.client.set_api_creds({
                "key": self.api_key,
                "secret": self.api_secret,
                "passphrase": self.api_passphrase
            })
        else:
            logger.warning("⚠️ API Keys não encontradas. O robô funcionará apenas em modo READ-ONLY.")

    async def execute_market_trade(self, token_id, amount_usdc, side=BUY):
        """
        Executa uma ordem a mercado (FOK - Fill or Kill) 
        Ideal para Copy Trading agressivo.
        """
        try:
            logger.info(f"🚀 Enviando Ordem a Mercado: {side} ${amount_usdc} no Token {token_id}")
            
            # Constrói a ordem conforme Quickstart
            mo = MarketOrderArgs(
                token_id=token_id, 
                amount=float(amount_usdc), 
                side=side, 
                order_type=OrderType.FOK
            )
            
            # Assina e envia
            signed_order = self.client.create_market_order(mo)
            resp = self.client.post_order(signed_order, OrderType.FOK)
            
            if resp.get("success"):
                logger.success(f"✅ Trade executado! Order ID: {resp.get('orderID')}")
                return True
            else:
                logger.error(f"❌ Erro na execução: {resp}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Falha fatal no motor de execução: {e}")
            return False

    async def get_market_price(self, token_id):
        """Busca o preço atual de compra e venda"""
        try:
            price_buy = self.client.get_price(token_id, side=BUY)
            price_sell = self.client.get_price(token_id, side=SELL)
            return {"buy": price_buy, "sell": price_sell}
        except Exception as e:
            logger.error(f"⚠️ Erro ao buscar preços para {token_id}: {e}")
            return None

if __name__ == "__main__":
    # Teste de conexão básica (Read-Only)
    engine = PolyExecutionEngine()
    print(f"Server OK: {engine.client.get_ok()}")
    print(f"Server Time: {engine.client.get_server_time()}")
