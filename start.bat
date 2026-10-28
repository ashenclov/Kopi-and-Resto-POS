@echo off
title Kopi & Resto POS
cd /d "%~dp0"

echo ===================================================
echo Memulai Aplikasi Kasir (POS) Kopi & Resto...
echo ===================================================

set "PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" main.py
) else (
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Terjadi kendala saat menjalankan aplikasi.
    pause
)
