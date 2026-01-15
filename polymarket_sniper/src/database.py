import os
from supabase import create_client, Client
from loguru import logger
from dotenv import load_dotenv

# Carrega ambiente da RAIZ (onde estão as chaves do Supabase) e local
load_dotenv("..\\.env") # Tenta carregar do pai
load_dotenv() # Carrega local (sobrepõe se houver duplicata)

class PolyDatabase:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
                logger.success("🗄️ Conectado ao Supabase (Polymarket Module)")
            except Exception as e:
                logger.error(f"❌ Erro ao conectar Supabase: {e}")
        else:
            logger.warning("⚠️ Credenciais do Supabase não encontradas. Logs apenas no console.")

    def log_trade(self, trade_data: dict):
        """Salva um trade copiado na tabela polymarket_trades"""
        if not self.client:
            return

        try:
            # Prepara dados para o formato do banco
            db_data = {
                "token_id": trade_data.get("token_id", "UNKNOWN"),
                "market_question": trade_data.get("question", "Unknown Market"),
                "side": trade_data.get("side", "BUY"),
                "outcome": trade_data.get("outcome", "YES"),
                "amount_usdc": float(trade_data.get("size_usdc", 0)),
                "price": float(trade_data.get("price", 0)),
                "tx_hash": trade_data.get("tx_hash", ""),
                "whale_address": trade_data.get("whale", ""),
                "status": "EXECUTED"
            }
            
            self.client.table("polymarket_trades").insert(db_data).execute()
            logger.info(f"💾 Trade salvo no Supabase: {db_data['tx_hash'][:10]}...")
            
        except Exception as e:
            logger.error(f"❌ Falha ao salvar trade no banco: {e}")

    def update_whale_stats(self, whale_address: str, pnl_change: float = 0):
        """Atualiza estatísticas da baleia"""
        if not self.client:
            return
            
        try:
            # Verifica se baleia existe, senão cria
            res = self.client.table("whales").select("*").eq("address", whale_address).execute()
            
            if not res.data:
                self.client.table("whales").insert({
                    "address": whale_address,
                    "nickname": f"Whale {whale_address[:6]}"
                }).execute()
            
            # Atualiza last_trade_at (simples, sem cálculo complexo de PnL por enquanto)
            self.client.table("whales").update({
                "last_trade_at": "now()",
                # "total_trades": res.data[0]['total_trades'] + 1 (Ideal seria incrementar)
            }).eq("address", whale_address).execute()
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar baleia: {e}")

# Instância global
db = PolyDatabase()
