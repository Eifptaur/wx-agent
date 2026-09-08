Option Explicit
' wx-agent stopper (no window): ensures Python (auto-provision if needed), then stops bot + watchdog.
Dim fso, sh, root, pyCmd, pyPath, script, cmd, code
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
pyPath = root & "\logs\python_path.txt"

' 1) Python environment (same auto-provision as launcher; fast when Python exists)
sh.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & root & "\scripts\setup_python.ps1""", 0, True
pyCmd = ""
If fso.FileExists(pyPath) Then
  pyCmd = Trim(fso.OpenTextFile(pyPath, 1, 0).ReadAll())
End If
script = root & "\scripts\stop_bot.py"
If pyCmd = "" Then
  ' 极端情况：无 Python 且下载失败 —— 尝试直接杀 PID 兜底
  On Error Resume Next
  Dim pidFile
  pidFile = root & "\data\bot.pid"
  If fso.FileExists(pidFile) Then
    Dim pid
    pid = Trim(fso.OpenTextFile(pidFile, 1, 0).ReadAll())
    If pid <> "" Then sh.Run("taskkill /F /PID " & pid & " /T", 0, True)
  End If
  fso.DeleteFile pidFile, True
  MsgBox "wx-agent: Python not available; fallback kill done. Please install Python or retry with network." & ChrW(32) & ChrW(65292) & ChrW(26080) & ChrW(38656) & ChrW(23433) & ChrW(35013) & ChrW(32) & ChrW(80) & ChrW(121) & ChrW(116) & ChrW(104) & ChrW(111) & ChrW(110) & ChrW(65292) & ChrW(25110) & ChrW(19979) & ChrW(36733) & ChrW(22833) & ChrW(36133) & ChrW(65292) & ChrW(19981) & ChrW(20250) & ChrW(20877) & ChrW(33258) & ChrW(21160) & ChrW(21355) & ChrW(35299) & ChrW(21160) & ChrW(21387) & ChrW(32511) & ChrW(33394) & ChrW(29256), 48, "wx-agent"
  WScript.Quit 1
End If
If InStr(pyCmd, " ") > 0 Then
  cmd = pyCmd & " """ & script & """"
Else
  cmd = """" & pyCmd & """ """ & script & """"
End If
On Error Resume Next
code = sh.Run(cmd, 0, True)
If Err.Number <> 0 Then
  Err.Clear
  code = sh.Run("cmd /c " & cmd, 0, True)
End If
On Error GoTo 0
Dim OK_MSG, FAIL_MSG
OK_MSG = ChrW(119) & ChrW(120) & ChrW(45) & ChrW(97) & ChrW(103) & ChrW(101) & ChrW(110) & ChrW(116) & ChrW(32) & ChrW(24050) & ChrW(20572) & ChrW(27490) & ChrW(10) & ChrW(10) & ChrW(24050) & ChrW(25104) & ChrW(21151) & ChrW(32467) & ChrW(26463) & ChrW(20840) & ChrW(37096) & ChrW(36827) & ChrW(31243) & ChrW(65306) & ChrW(10) & ChrW(65288) & ChrW(26426) & ChrW(22120) & ChrW(20154) & ChrW(19982) & ChrW(30475) & ChrW(38376) & ChrW(29399) & ChrW(37117) & ChrW(24050) & ChrW(34987) & ChrW(20572) & ChrW(27490) & ChrW(65292) & ChrW(19981) & ChrW(20250) & ChrW(20877) & ChrW(33258) & ChrW(21160) & ChrW(25289) & ChrW(36215) & ChrW(65289) & ChrW(10) & ChrW(10) & ChrW(20572) & ChrW(27490) & ChrW(21518) & ChrW(22914) & ChrW(38656) & ChrW(20877) & ChrW(36816) & ChrW(34892) & ChrW(65292) & ChrW(35831) & ChrW(21452) & ChrW(20987) & ChrW(39033) & ChrW(30446) & ChrW(26681) & ChrW(30446) & ChrW(24405) & ChrW(30340) & ChrW(65306) & ChrW(10) & ChrW(32) & ChrW(32) & ChrW(21551) & ChrW(21160) & ChrW(26426) & ChrW(22120) & ChrW(20154) & ChrW(46) & ChrW(118) & ChrW(98) & ChrW(115) & ChrW(32) & ChrW(32) & ChrW(65288) & ChrW(20165) & ChrW(21551) & ChrW(21160) & ChrW(65289) & ChrW(10) & ChrW(32) & ChrW(32) & ChrW(25110) & ChrW(32) & ChrW(19968) & ChrW(38190) & ChrW(21551) & ChrW(21160) & ChrW(46) & ChrW(98) & ChrW(97) & ChrW(116) & ChrW(32) & ChrW(32) & ChrW(65288) & ChrW(20381) & ChrW(36182) & ChrW(26816) & ChrW(26597) & ChrW(32) & ChrW(43) & ChrW(32) & ChrW(33258) & ChrW(26816) & ChrW(32) & ChrW(43) & ChrW(32) & ChrW(21551) & ChrW(21160) & ChrW(65292) & ChrW(25512) & ChrW(33616) & ChrW(65289) & ChrW(10) & ChrW(10) & ChrW(32676) & ChrW(32842) & ChrW(19982) & ChrW(23384) & ChrW(26723) & ChrW(25968) & ChrW(25454) & ChrW(19981) & ChrW(20250) & ChrW(20002) & ChrW(22833) & ChrW(65292) & ChrW(19979) & ChrW(27425) & ChrW(21551) & ChrW(21160) & ChrW(33258) & ChrW(21160) & ChrW(24674) & ChrW(22797) & ChrW(12290)
FAIL_MSG = ChrW(26410) & ChrW(21457) & ChrW(29616) & ChrW(27491) & ChrW(22312) & ChrW(36816) & ChrW(34892) & ChrW(30340) & ChrW(32) & ChrW(119) & ChrW(120) & ChrW(45) & ChrW(97) & ChrW(103) & ChrW(101) & ChrW(110) & ChrW(116) & ChrW(32) & ChrW(36827) & ChrW(31243) & ChrW(65288) & ChrW(21487) & ChrW(33021) & ChrW(24050) & ChrW(22312) & ChrW(36816) & ChrW(34892) & ChrW(20013) & ChrW(27809) & ChrW(26377) & ChrW(21551) & ChrW(21160) & ChrW(65289) & ChrW(12290) & ChrW(10) & ChrW(22914) & ChrW(30830) & ChrW(35748) & ChrW(38656) & ChrW(35201) & ChrW(20572) & ChrW(27490) & ChrW(65292) & ChrW(35831) & ChrW(20808) & ChrW(22312) & ChrW(25511) & ChrW(21046) & ChrW(21488) & ChrW(39030) & ChrW(37096) & ChrW(30830) & ChrW(35748) & ChrW(29366) & ChrW(24577) & ChrW(65292) & ChrW(25110) & ChrW(37325) & ChrW(35797) & ChrW(20572) & ChrW(27490) & ChrW(25805) & ChrW(20316) & ChrW(12290)
If code = 0 Then
  MsgBox OK_MSG, 64, "wx-agent"
Else
  MsgBox FAIL_MSG, 48, "wx-agent"
End If
