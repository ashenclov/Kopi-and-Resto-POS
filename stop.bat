@echo off
title Hentikan Kopi & Resto POS
echo Menghentikan layanan kasir pada port 8000...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Layanan kasir berhasil dihentikan.
pause
