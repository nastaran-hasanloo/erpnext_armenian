@echo off
chcp 65001 >nul
echo Rebuilding the image with the current translations (erpnext_armenian\locale\hy.po)...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1" --rebuild
