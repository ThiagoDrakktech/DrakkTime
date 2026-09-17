@echo off
cd /d "%~dp0"
set PYTHON=C:\Users\tigui\AppData\Local\Programs\Python\Python314\python.exe

cls
echo.
echo ===============================================
echo    DrakkTime - Compilador
echo ===============================================
echo.

echo [1/3] Limpando compilacoes anteriores...
if exist "dist" rmdir /s /q dist >nul 2>&1
if exist "build" rmdir /s /q build >nul 2>&1
del *.spec >nul 2>&1

echo OK - Limpeza concluida
echo.

echo [2/3] Compilando executavel...
echo Aguarde...
echo.

%PYTHON% -m PyInstaller --onefile --windowed --name "DrakkTime" drakktime/__main__.py

echo.
echo [3/3] Verificando resultado...
echo.

if exist "dist\DrakkTime.exe" (
    echo.
    echo ===============================================
    echo    SUCESSO!
    echo ===============================================
    echo.
    echo Arquivo: dist\DrakkTime.exe
    echo.
    timeout /t 3
    start explorer dist
) else (
    echo.
    echo ===============================================
    echo    ERRO na compilacao!
    echo ===============================================
    echo.
)

pause



