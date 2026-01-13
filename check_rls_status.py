
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Hardcoded fallbacks to match cloud_api.py logic for local checks
url = os.environ.get("SUPABASE_URL", "https://xayaogxbjudpmwylaiuf.supabase.co")
# Note: This is a publishable key, so it's safe to be here for read operations.
# For RLS checks that need write, we might need the service role key, but let's try with this first.
key = os.environ.get("SUPABASE_KEY", "sb_publishable_wNuQ-HzDYPoD3YEPB-v5VA_zi21tBxs")

if not url or not key:
    print("Erro: SUPABASE_URL ou SUPABASE_KEY não encontradas.")
    exit(1)

supabase = create_client(url, key)

def check_policies():
    print("🔍 Inspecionando Conexão e RLS no Supabase (Teste Real)...")
    print("=" * 60)
    
    try:
        # 1. Teste de Leitura (READ)
        print("1️⃣  Testando LEITURA (Public/Anon)...")
        response = supabase.table("system_status").select("*").limit(1).execute()
        print(f"   ✅ Leitura Permitida! Registros encontrados: {len(response.data)}")
        if response.data:
            print(f"   ℹ️  Exemplo de dado: {response.data[0].get('version', 'N/A')}")
        else:
            print("   ℹ️  Tabela vazia, mas acesso permitido.")

        # 2. Teste de Escrita (WRITE) - Tentativa de Log
        print("\n2️⃣  Testando ESCRITA (Insert Log)...")
        try:
            log_entry = {
                "event_type": "SECURITY_CHECK",
                "message": "Verificacao manual de RLS via script local",
                "time": "now()"
            }
            # Se a tabela 'system_logs' exigir autenticação, isso pode falhar com a chave pública
            # Se falhar, significa que o RLS está protegendo (o que pode ser bom ou ruim dependendo da config desejada)
            # Como o cloud_api usa essa chave, DEVE funcionar se a config for 'public insert'.
            supabase.table("system_logs").insert(log_entry).execute()
            print("   ✅ Escrita Permitida! Log inserido com sucesso em 'system_logs'.")
        except Exception as e_write:
            print(f"   ⚠️ Escrita Bloqueada ou Falha: {e_write}")
            print("   (Isso é NORMAL se o RLS estiver configurado para permitir insert apenas via Service Role ou Auth User,")
            print("    mas se o cloud_api usa a mesma chave, ele também falhará.)")

        print("\n✅ Conclusão:")
        print("   O banco de dados está acessível e as políticas RLS estão respondendo.")
        print("   Se o passo 2 falhou mas o cloud_api funciona, verifique se o cloud_api usa uma chave diferente (Service Role).")
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO DE CONEXÃO: {e}")
        print("   Verifique URL e KEY no arquivo ou variáveis de ambiente.")

    print("=" * 60)

if __name__ == "__main__":
    check_policies()
