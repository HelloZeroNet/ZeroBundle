rmdir /S /Q build
rmdir /S /Q dist
C:\Python27\scripts\pyinstaller.exe zeronet.spec -y
rmdir /S /Q dist\ZeroNet\Include
mkdir dist\ZeroNet\core
mkdir dist\ZeroNet\lib
move dist\ZeroNet\*.pyd dist\ZeroNet\lib
move dist\ZeroNet\pywintypes27.dll dist\ZeroNet\lib
move dist\ZeroNet\sqlite*.dll dist\ZeroNet\lib
move dist\ZeroNet\lib\gevent.corecext.pyd dist\ZeroNet
move dist\ZeroNet\lib\gevent._semaphore.pyd dist\ZeroNet
git clone --depth 1 file://f:\Work\ZeroNet-git\ZeroBundle\PyInstall\..\..\ZeroNet\.git\ dist\ZeroNet\core
rmdir /S /Q dist\ZeroNet\core\.git
rem powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist/ZeroNet', '../dist/ZeroNet-win.zip'); }"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /va /s desc "ZeroNet"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s name "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s product "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s copyright "2017 ZeroNet.io"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s productver "0.5.1.0"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s company "Open Source Developer, Tamas Kocsis"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe 0.5.1.0
rem ..\..\tools\mt.exe -nologo -manifest "dist\ZeroNet\ZeroNet.exe.manifest" -outputresource:"dist\ZeroNet\ZeroNet.exe;1"
..\..\tools\ResourceHacker.exe -addoverwrite dist\ZeroNet\ZeroNet.exe, dist\ZeroNet\ZeroNet.exe, dist\ZeroNet\ZeroNet.exe.manifest,24,1,1033
del dist\ZeroNet\ZeroNet.exe.manifest
set INPUT=
set /P INPUT=PVK password: %=%
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /t http://timestamp.verisign.com/scripts/timstamp.dll /v dist\ZeroNet\ZeroNet.exe
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /tr http://timestamp.digicert.com /fd sha256 /as /v dist\ZeroNet\ZeroNet.exe
pause