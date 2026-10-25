@echo off
cd /d "%~dp0"
echo This deletes the test site and ALL its data.
set /p ans=Type YES to continue: 
if /I not "%ans%"=="YES" exit /b
docker compose down -v
echo Done. Run START-ERPNext-Armenian.bat for a fresh site.
pause
