@echo off
echo ========================================================
echo   PREDATOR v13.0 - AMBIENTE LOCAL
echo ========================================================
echo.

echo [1/3] Verificando dependencias...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias. Verifique seu Python.
    pause
    exit /b
)

echo.
echo [2/3] Verificando arquivo .env...
if not exist .env (
    echo AVISO: Arquivo .env nao encontrado!
    echo "O sistema rodara em modo RAM Volatil (sem Supabase)."
    echo Para conectar o DB, crie o arquivo .env com suas chaves.
) else (
    echo Arquivo .env encontrado. Carregando variaveis...
)

echo.
echo [3/3] Iniciando API Local...
echo Acesse: http://127.0.0.1:8000/docs
echo.
python -m uvicorn cloud_api:app --reload

pause
