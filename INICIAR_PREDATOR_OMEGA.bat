@echo off
title PREDADOR-OMEGA [SOVEREIGN EDITION]
color 0E
echo.
echo    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo       PREDADOR-OMEGA : SER UNICO VIVO (v1.0)
echo    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
echo [1] Verificando DeepMachine (Hardware)...
python -c "import torch; print('GPU CUDA:', 'ATIVA' if torch.cuda.is_available() else 'OFFLINE')"
echo.
echo [2] Acordando o Organismo Digital...
python omega_core.py
pause
