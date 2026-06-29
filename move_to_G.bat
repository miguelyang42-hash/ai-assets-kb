@echo off
set "sourceDir=%cd%"
set "targetDir=G:\XPES_Customer_Assets"

echo Moving XPES Lead Generation Assets to %targetDir%...

if not exist "%targetDir%" mkdir "%targetDir%"

move "%sourceDir%\XPES_Leads_2026-06-16.csv" "%targetDir%\"
move "%sourceDir%\XPES_Email_Drafts_2026-06-16.md" "%targetDir%\"

echo.
echo Assets moved successfully!
pause
