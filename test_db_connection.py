import os
from dotenv import load_dotenv
from supabase import create_client

def test_connection():
    # Carrega variáveis
    load_dotenv()
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    print("="*50)
    print("TESTE DE CONEXÃO SUPABASE")
    print("="*50)
    
    if not url or not key:
        print("❌ ERRO: Variáveis SUPABASE_URL ou SUPABASE_KEY não encontradas.")
        print("Certifique-se de criar o arquivo .env baseado no .env.example")
        return

    print(f"URL: {url}")
    print("Tentando conectar...")
    
    try:
        supabase = create_client(url, key)
        
        # Tenta uma leitura simples (mesmo que vazia)
        response = supabase.table("trades").select("*").limit(1).execute()
        
        print("✅ CONEXÃO BEM SUCEDIDA!")
        print(f"Resposta do DB: {response}")
        print("\nSua tabela 'trades' está acessível.")
        
    except Exception as e:
        print("\n❌ FALHA NA CONEXÃO:")
        print(e)
        print("\nVerifique se:")
        print("1. As chaves no .env estão corretas")
        print("2. Você rodou o script SQL no Supabase para criar a tabela")
    
    print("="*50)
    input("Pressione ENTER para sair...")

if __name__ == "__main__":
    test_connection()
