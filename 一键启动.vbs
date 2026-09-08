Option Explicit
' wx-agent one-click start (no window): deps check -> auto install ->
' self test -> launch bot. Progress goes to logs\onestart.log (visible in
' Web console log page). Launchers: start.vbs / stop.vbs as backup switches.
Dim fso, sh, root, script
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)
script = root & "\scripts\onestart.py"
On Error Resume Next
sh.Run "pyw.exe -3 """ & script & """", 0, False
If Err.Number <> 0 Then
    Err.Clear
    sh.Run "pythonw.exe """ & script & """", 0, False
    If Err.Number <> 0 Then
        Err.Clear
        sh.Run "python.exe """ & script & """", 0, False
    End If
End If
