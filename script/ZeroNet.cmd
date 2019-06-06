@echo off
cd /d "%~dp0"
copy /Y ZeroNet-cli.dat ..\ZeroNet-cli.exe >NUL
copy /Y ..\ZeroNet.pkg ..\ZeroNet-cli.pkg >NUL
..\ZeroNet-cli.exe  --open_browser False %*
