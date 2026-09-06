@echo off
cd /d "%~dp0"
py -3 -X utf8 scripts\setup_deps.py
echo.
pause