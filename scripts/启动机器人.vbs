Option Explicit
' wx-agent launcher used by autostart (no window): delegates to the full one-click
' flow (ensure Python -> deps -> selftest -> launch). Runs hidden.
Dim fso, sh, root, root2
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh  = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)     ' scripts\
root2 = fso.GetParentFolderName(root)                       ' program root
sh.Run "wscript.exe """ & root2 & "\一键启动.vbs""", 0, False
