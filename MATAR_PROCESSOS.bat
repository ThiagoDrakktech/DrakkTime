@echo off
echo.
echo Encerrando processos DrakkTime...
echo.

taskkill /F /IM python.exe /T
taskkill /F /IM DrakkTime.exe /T

echo.
echo OK - Processos encerrados
echo.
pause
