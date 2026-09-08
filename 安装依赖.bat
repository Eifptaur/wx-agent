@echo off
rem wx-agent dependency installer (auto Python provisioning + pip install from PyPI or offline\wheels)
title wx-agent - install deps
set "ROOT=%~dp0"
echo wx-agent: checking Python environment...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%scripts\setup_python.ps1"
set /p PYPATH=<"%ROOT%logs\python_path.txt"
if not defined PYPATH (
  echo [ERROR] No Python available and auto setup failed. Check network / offline package.
  pause
  exit /b 1
)
echo Using Python: %PYPATH%
%PYPATH% -X utf8 "%ROOT%scripts\setup_deps.py"
echo.
echo Done. Now run self-test: scripts\selftest or just double-click 一键启动.vbs
pause
