@echo off
cd /d "%~dp0"
docker compose stop
echo ERPNext stopped. Data is kept.
pause
