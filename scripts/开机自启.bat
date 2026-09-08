@echo off
rem Register wx-agent auto-start (one-click flow: Python auto-provision -> deps -> selftest -> launch)
set "VBS=%~dp0..\一键启动.vbs"
schtasks /create /tn "wx-agent" /tr "\"wscript.exe\" \"%VBS%\"" /sc onlogon /rl limited /f
if errorlevel 1 (
  echo Register failed. Try run as Administrator.
  echo Zhu ce shi bai, qing yi guan li yuan quan xian yun xing.
) else (
  echo Registered auto-start task wx-agent (logon).
  echo Yi zhu ce kai ji zi dong qi dong.
)
pause
