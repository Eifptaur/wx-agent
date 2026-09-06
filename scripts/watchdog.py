# -*- coding: utf-8 -*-
"""wx-agent 看门狗（无窗口）：机器人崩溃/退出后自动重启。

用 pythonw 运行、零 PowerShell 依赖（无 cmd、无 powershell 窗口）。
启动时把自己的 PID 写到 data/watchdog.pid，供 停止机器人 读取。
"""
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PID_FILE = os.path.join(DATA, "watchdog.pid")
CRASH_LOG = os.path.join(DATA, "bot_crash.log")
os.makedirs(DATA, exist_ok=True)


def find_pythonw():
    if shutil.which("pythonw"):
        return shutil.which("pythonw")
    if sys.executable and os.path.basename(sys.executable).lower() == "python.exe":
        pyw = sys.executable[:-10] + "pythonw.exe"
        if os.path.exists(pyw):
            return pyw
    return sys.executable or "pythonw"


def main():
    try:
        with open(PID_FILE, "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass
    exe = find_pythonw()
    flags = 0x08000000 | 0x00000008 if os.name == "nt" else 0
    while True:
        try:
            # stderr 重定向到崩溃日志：下次机器人无声挂掉时能查到原因
            # （wx_agent 若 import 失败/启动即崩溃，之前 stderr=DEVNULL 会静默重启，无从排查）
            crash = open(CRASH_LOG, "a", encoding="utf-8")
            crash.write("\n[watchdog] %s 拉起 wx_agent…\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
            crash.flush()
            p = subprocess.Popen([exe, os.path.join(ROOT, "wx_agent.py")],
                                 cwd=ROOT, creationflags=flags,
                                 stdin=subprocess.DEVNULL, stdout=crash, stderr=crash)
            crash.close()
            p.wait()
        except Exception as e:
            try:
                with open(CRASH_LOG, "a", encoding="utf-8") as crash:
                    crash.write("[watchdog] 异常：%s\n" % e)
            except Exception:
                pass
        time.sleep(5)


if __name__ == "__main__":
    main()
