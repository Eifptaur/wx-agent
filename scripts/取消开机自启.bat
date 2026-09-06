@echo off
schtasks /delete /tn "wx-agent" /f
echo 已取消开机自启。
pause
