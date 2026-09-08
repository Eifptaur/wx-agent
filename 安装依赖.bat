@echo off
rem wx-agent 依赖安装器（自动保障 Python：系统 Python 或自动解压/下载绿色版；依赖从 PyPI 或 offline\wheels 安装）
title wx-agent - 安装依赖
set "ROOT=%~dp0"
echo wx-agent：正在检查 Python 环境...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%ROOT%scripts\setup_python.ps1"
set /p PYPATH=<"%ROOT%logs\python_path.txt"
if not defined PYPATH (
  echo [错误] 没有可用的 Python，自动配置也失败了。请检查网络或离线包（offline\python）。
  pause
  exit /b 1
)
echo 使用 Python：%PYPATH%
%PYPATH% -X utf8 "%ROOT%scripts\setup_deps.py"
echo.
echo 依赖完成。下一步：运行自检（scripts\自检.bat），或直接双击「一键启动.vbs」。
pause
