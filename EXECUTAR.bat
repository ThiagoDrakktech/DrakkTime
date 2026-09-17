@echo off
REM DrakkTime - Executável Portável
REM Não precisa de instalação, só clicar 2x

cd /d "%~dp0"

REM Detectar Python (seu próprio ou do sistema)
set PYTHON=

REM Tentar encontrar Python
if exist "C:\Users\tigui\AppData\Local\Programs\Python\Python314\python.exe" (
    set PYTHON=C:\Users\tigui\AppData\Local\Programs\Python\Python314\python.exe
) else (
    where python >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON=python
    )
)

if "%PYTHON%"=="" (
    echo.
    echo ERRO: Python nao encontrado!
    echo.
    echo Instale Python em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Iniciando DrakkTime...
echo.

REM Instalar Streamlit se necessario (primeira vez)
%PYTHON% -m pip install streamlit pandas -q 2>nul

REM RODAR COM LIMITE DE RECURSOS
REM Isso evita consumo excessivo de memoria
%PYTHON% -m streamlit run drakktime/ui/streamlit_app.py --logger.level=error --server.maxUploadSize=200 --client.showErrorDetails=false

pause
