Option Explicit
' wx-agent 一键启动（无窗口）：
'  1) setup_python.ps1：确保有 Python（系统已有则直接用；没有则自动解压/下载绿色版）→ 写入 logs\python_path.txt
'  2) onestart.py：依赖检查 → 自动安装缺失依赖 → 55 项自检 → 拉起机器人（并打开 Web 控制台）
' 进度记录在 logs\onestart.log（Web 控制台「运行日志」可见）。
' 若没找到 Python 且自动下载失败，弹窗说明处理办法。
Dim fso, sh, root, code, pyCmd, pyPath, runCmd, onestart, code2
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
pyPath = root & "\logs\python_path.txt"

' 1) Python 环境（无则自动配置，等待完成）
code = sh.Run("powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & root & "\scripts\setup_python.ps1""", 0, True)
pyCmd = ""
If fso.FileExists(pyPath) Then
  pyCmd = Trim(fso.OpenTextFile(pyPath, 1, 0).ReadAll())   ' tristate 0 = ASCII
End If
If pyCmd = "" Then
  Dim FAIL_PY
  FAIL_PY = "没有找到可用的 Python，自动下载也失败了。" & vbCrLf & vbCrLf & _
            "请检查网络后重试；或把离线包里的 offline\python 文件夹放进程序目录，" & _
            "它会自动解压绿色版 Python，不用自己安装。" & vbCrLf & _
            "查看日志：\logs\onestart.log"
  MsgBox FAIL_PY, 48, "wx-agent"
  WScript.Quit 1
End If

' pyCmd 可能是 "py -3"（启动器）或完整 exe 路径
If InStr(pyCmd, " ") > 0 Then
  runCmd = pyCmd
Else
  runCmd = """" & pyCmd & """"
End If

' 2) 一键启动主体（依赖 → 自检 → 启动）
onestart = root & "\scripts\onestart.py"
On Error Resume Next
code2 = sh.Run(runCmd & " -X utf8 """ & onestart & """", 0, True)
If Err.Number <> 0 Then
  Err.Clear
  code2 = sh.Run("cmd /c " & runCmd & " -X utf8 """ & onestart & """", 0, True)
End If
On Error GoTo 0
If code2 <> 0 Then
  Dim FAIL_START
  FAIL_START = "一键启动失败（依赖或自检未通过）。" & vbCrLf & _
               "请打开 Web 控制台「运行日志」，或查看：" & root & "\logs\onestart.log"
  MsgBox FAIL_START, 48, "wx-agent"
End If
