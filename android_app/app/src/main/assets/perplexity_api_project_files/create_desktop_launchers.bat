@echo off
REM Create Windows desktop launcher
REM This script creates a shortcut on the desktop

set SCRIPT_DIR=%~dp0
set DESKTOP_DIR=%USERPROFILE%\Desktop
set SHORTCUT_NAME=Perplexity Bridge.lnk

echo Creating desktop launcher...

REM Create VBScript to create shortcut
set VBS=%TEMP%\create_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS%"
echo sLinkFile = "%DESKTOP_DIR%\%SHORTCUT_NAME%" >> "%VBS%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS%"
echo oLink.TargetPath = "%SCRIPT_DIR%Launch Perplexity Bridge.vbs" >> "%VBS%"
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS%"
echo oLink.Description = "Perplexity AI Bridge with Web UI" >> "%VBS%"
echo oLink.WindowStyle = 7 >> "%VBS%"
echo oLink.Save >> "%VBS%"

REM Run VBScript
cscript //nologo "%VBS%"
del "%VBS%"

echo.
echo Desktop launcher created at: %DESKTOP_DIR%\%SHORTCUT_NAME%
echo.
echo You can now:
echo   1. Double-click "Perplexity Bridge" on your desktop
echo   2. Or run: start.bat
echo.
pause
