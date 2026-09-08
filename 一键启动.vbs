Option Explicit
' wx-agent one-click start (no window):
'  1) setup_python.ps1 : ensure Python (system or auto-downloaded portable) -> logs\python_path.txt (ASCII)
'  2) onestart.py      : deps check -> auto install -> selftest -> launch watchdog (+open console)
' Progress goes to logs\onestart.log (visible in Web console log page).
' If no Python and auto-download fails, a message box explains what to do.
Dim fso, sh, root, code, pyCmd, pyPath, runCmd, onestart, code2
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
pyPath = root & "\logs\python_path.txt"

' 1) Python environment (auto-download portable if missing; ASCII file)
code = sh.Run("powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & root & "\scripts\setup_python.ps1""", 0, True)
pyCmd = ""
If fso.FileExists(pyPath) Then
  pyCmd = Trim(fso.OpenTextFile(pyPath, 1, 0).ReadAll())   ' tristate 0 = ASCII
End If
If pyCmd = "" Then
  Dim FAIL_PY
  FAIL_PY = "wx-agent: no Python found and auto-download failed." & vbCrLf & vbCrLf & _
            "Check your network and retry, or copy offline\python folder (from the offline package) into the program folder — " & _
            "the launcher will unpack the portable Python by itself." & _
            ChrW(10) & ChrW(65292) & ChrW(25110) & ChrW(26597) & ChrW(30475) & ChrW(32) & ChrW(108) & ChrW(111) & ChrW(103) & ChrW(115) & ChrW(92) & ChrW(111) & ChrW(110) & ChrW(101) & ChrW(115) & ChrW(116) & ChrW(97) & ChrW(114) & ChrW(116) & ChrW(46) & ChrW(108) & ChrW(111) & ChrW(103) & ChrW(12290)
  MsgBox FAIL_PY, 48, "wx-agent"
  WScript.Quit 1
End If

' pyCmd may be "py -3" (launcher) or an exe path
If InStr(pyCmd, " ") > 0 Then
  runCmd = pyCmd
Else
  runCmd = """" & pyCmd & """"
End If

' 2) one-click start body (deps -> selftest -> launch)
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
  FAIL_START = "wx-agent: one-click start failed (deps or selftest)." & vbCrLf & _
               "Open the Web console [running log], or read " & root & "\logs\onestart.log" & _
               ChrW(20877) & ChrW(36182) & ChrW(29256) & ChrW(38646) & ChrW(65306) & ChrW(10) & ChrW(32) & ChrW(32) & ChrW(19968) & ChrW(38190) & ChrW(21551) & ChrW(21160) & ChrW(22833) & ChrW(36133) & ChrW(65308) & ChrW(65281)
  MsgBox FAIL_START, 48, "wx-agent"
End If
