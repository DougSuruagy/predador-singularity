@echo off
echo ========================================================
echo   PREDATOR v13.0 - UPLOAD PARA GITHUB
echo ========================================================
echo.
echo [1/3] Adicionando arquivos...
git add .

echo [2/3] Criando commit...
git commit -m "Upgrade: Cloud API, Supabase, MQL5 Bridge e Dashboard Real-time"

echo [3/3] Enviando para GitHub...
git push origin main

echo.
if %errorlevel% neq 0 (
    echo ERRO: Nao foi possivel enviar para o GitHub.
    echo Verifique se voce esta logado ou se ha conflitos.
) else (
    echo SUCESSO! Codigo na nuvem.
    echo Verifique o Render/Vercel para acompanhar o deploy.
)
pause
