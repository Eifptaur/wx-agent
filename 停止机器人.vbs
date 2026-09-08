' wx-agent stopper (no window): stops bot + watchdog by PID files (no PowerShell).
' ÏêÏ¸µ¯´°£¨chrW Öð×Ö·û±àÂë£¬GBK »·¾³ÏÂÒ²²»»áÂÒÂë£©
Option Explicit
Dim fso, sh, root, script, cmd, code, msg
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
script = root & "\scripts\stop_bot.py"
On Error Resume Next
cmd = "pyw.exe -3 \"" & script & "\""
sh.Run cmd, 0, True
If Err.Number <> 0 Then
    Err.Clear
    cmd = "pythonw.exe \"" & script & "\""
    sh.Run cmd, 0, True
    If Err.Number <> 0 Then
        Err.Clear
        cmd = "python.exe \"" & script & "\""
        sh.Run cmd, 0, True
    End If
End If
code = sh.Run(cmd, 0, True)
Dim OK_MSG, FAIL_MSG
OK_MSG = ChrW(119) & ChrW(120) & ChrW(45) & ChrW(97) & ChrW(103) & ChrW(101) & ChrW(110) & ChrW(116) & ChrW(32) & ChrW(24050) & ChrW(20572) & ChrW(27490) & ChrW(10) & ChrW(10) & ChrW(24050) & ChrW(25104) & ChrW(21151) & ChrW(32467) & ChrW(26463) & ChrW(20840) & ChrW(37096) & ChrW(36827) & ChrW(31243) & ChrW(65306) & ChrW(10) & ChrW(65288) & ChrW(26426) & ChrW(22120) & ChrW(20154) & ChrW(19982) & ChrW(30475) & ChrW(38376) & ChrW(29399) & ChrW(37117) & ChrW(24050) & ChrW(34987) & ChrW(20572) & ChrW(27490) & ChrW(65292) & ChrW(19981) & ChrW(20250) & ChrW(20877) & ChrW(33258) & ChrW(21160) & ChrW(25289) & ChrW(36215) & ChrW(65289) & ChrW(10) & ChrW(10) & ChrW(20572) & ChrW(27490) & ChrW(21518) & ChrW(22914) & ChrW(38656) & ChrW(20877) & ChrW(27425) & ChrW(36816) & ChrW(34892) & ChrW(65292) & ChrW(35831) & ChrW(21452) & ChrW(20987) & ChrW(39033) & ChrW(30446) & ChrW(26681) & ChrW(30446) & ChrW(24405) & ChrW(30340) & ChrW(65306) & ChrW(10) & ChrW(32) & ChrW(32) & ChrW(21551) & ChrW(21160) & ChrW(26426) & ChrW(22120) & ChrW(20154) & ChrW(46) & ChrW(118) & ChrW(98) & ChrW(115) & ChrW(32) & ChrW(32) & ChrW(65288) & ChrW(20165) & ChrW(21551) & ChrW(21160) & ChrW(65289) & ChrW(10) & ChrW(32) & ChrW(32) & ChrW(25110) & ChrW(32) & ChrW(19968) & ChrW(38190) & ChrW(21551) & ChrW(21160) & ChrW(46) & ChrW(98) & ChrW(97) & ChrW(116) & ChrW(32) & ChrW(32) & ChrW(65288) & ChrW(20381) & ChrW(36182) & ChrW(26816) & ChrW(26597) & ChrW(32) & ChrW(43) & ChrW(32) & ChrW(33258) & ChrW(26816) & ChrW(32) & ChrW(43) & ChrW(32) & ChrW(21551) & ChrW(21160) & ChrW(65292) & ChrW(25512) & ChrW(33616) & ChrW(65289) & ChrW(10) & ChrW(10) & ChrW(32676) & ChrW(32842) & ChrW(19982) & ChrW(23384) & ChrW(26723) & ChrW(25968) & ChrW(25454) & ChrW(19981) & ChrW(20250) & ChrW(20002) & ChrW(22833) & ChrW(65292) & ChrW(19979) & ChrW(27425) & ChrW(21551) & ChrW(21160) & ChrW(33258) & ChrW(21160) & ChrW(24674) & ChrW(22797) & ChrW(12290)
FAIL_MSG = ChrW(26410) & ChrW(21457) & ChrW(29616) & ChrW(27491) & ChrW(22312) & ChrW(36816) & ChrW(34892) & ChrW(30340) & ChrW(32) & ChrW(119) & ChrW(120) & ChrW(45) & ChrW(97) & ChrW(103) & ChrW(101) & ChrW(110) & ChrW(116) & ChrW(32) & ChrW(36827) & ChrW(31243) & ChrW(65288) & ChrW(21487) & ChrW(33021) & ChrW(24050) & ChrW(22312) & ChrW(36816) & ChrW(34892) & ChrW(20013) & ChrW(27809) & ChrW(26377) & ChrW(21551) & ChrW(21160) & ChrW(65289) & ChrW(12290) & ChrW(10) & ChrW(22914) & ChrW(30830) & ChrW(35748) & ChrW(38656) & ChrW(35201) & ChrW(20572) & ChrW(27490) & ChrW(65292) & ChrW(35831) & ChrW(20808) & ChrW(22312) & ChrW(25511) & ChrW(21046) & ChrW(21488) & ChrW(39030) & ChrW(37096) & ChrW(30830) & ChrW(35748) & ChrW(29366) & ChrW(24577) & ChrW(65292) & ChrW(25110) & ChrW(37325) & ChrW(35797) & ChrW(20572) & ChrW(27490) & ChrW(25805) & ChrW(20316) & ChrW(12290)
If code = 0 Then
  MsgBox OK_MSG, 64, "wx-agent"
Else
  MsgBox FAIL_MSG, 48, "wx-agent"
End If
