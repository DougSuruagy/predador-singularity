@echo off
TITLE PREDADOR HFT - LOCALHOST (Master Node)
COLOR 0A

echo ========================================================
echo    PREDADOR v370.0 - INICIANDO SISTEMA LOCAL
echo ========================================================
echo.
echo [1/3] Carregando Variaveis de Ambiente...
echo Node Role: PRIMARY
echo.

echo [2/3] Iniciando Servidor API (Uvicorn)...
echo       Acesse: http://127.0.0.1:8000/docs
echo.

:: Define environment variables for local run if not in .env
set NODE_ROLE=PRIMARY
set PYTHON_VERSION=3.11

:: Run the server
uvicorn cloud_api:app --host 127.0.0.1 --port 8000 --reload

pause
