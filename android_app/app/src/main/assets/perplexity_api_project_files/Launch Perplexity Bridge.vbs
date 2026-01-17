Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = strScriptPath

' Run the start script in a minimized window
objShell.Run "cmd /c start.bat", 0, False

' Exit
WScript.Quit
