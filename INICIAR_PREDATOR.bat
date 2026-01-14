@echo off
title PREDATOR HFT - LIGANDO MOTORES...
cls
echo ============================================================
echo         PREDATOR v375.0 - ATIVACAO AUTOMATICA (WSL)
echo ============================================================
echo.
echo [1/3] Acessando Nucleo Linux (Ubuntu)...
echo [2/3] Sincronizando Saldo e Inteligencia...
echo [3/3] Iniciando Cacada...
echo.
echo Pressione qualquer tecla para dar a partida!
pause > nul

wsl -d Ubuntu -e bash -c "cd /mnt/c/Users/Douglas/tryd && source venv_linux/bin/activate && python3 cloud_api.py"

pause
