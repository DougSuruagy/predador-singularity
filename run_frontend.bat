@echo off
echo ========================================================
echo   PREDATOR v13.0 - FRONTEND SERVER
echo ========================================================
echo.
echo Iniciando servidor web local para contornar bloqueios de seguranca do navegador...
echo.
echo Dashboard disponivel em: http://localhost:5500
echo.
echo Mantenha esta janela aberta!
echo.
python -m http.server 5500
