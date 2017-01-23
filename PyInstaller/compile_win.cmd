rmdir /S /Q build
rmdir /S /Q dist
C:\Python27\scripts\pyinstaller.exe zeronet_win.spec -y
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
rmdir /S /Q dist\ZeroNet\core\src\Test\testdata
rem powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist/ZeroNet', '../dist/ZeroNet-win.zip'); }"
echo Adding info to ZeroNet.exe...
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /va /s desc "ZeroNet"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s name "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s product "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s copyright "2017 ZeroNet.io"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s productver "0.5.1.0"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe /s company "Open Source Developer, Tamas Kocsis"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet.exe 0.5.1.0
..\..\tools\ResourceHacker.exe -addoverwrite dist\ZeroNet\ZeroNet.exe, dist\ZeroNet\ZeroNet.exe, dist\ZeroNet\ZeroNet.exe.manifest,24,1,1033
del dist\ZeroNet\ZeroNet.exe.manifest
del ZeroNet.pkg
echo Adding info to ZeroNet-cli.exe...
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /va /s desc "ZeroNet"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /s name "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /s product "ZeroNet client"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /s copyright "2017 ZeroNet.io"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /s productver "0.5.1.0"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe /s company "Open Source Developer, Tamas Kocsis"
..\..\tools\verpatch.exe dist\ZeroNet\ZeroNet-cli.exe 0.5.1.0
..\..\tools\ResourceHacker.exe -addoverwrite dist\ZeroNet\ZeroNet-cli.exe, dist\ZeroNet\ZeroNet-cli.exe, dist\ZeroNet\ZeroNet-cli.exe.manifest,24,1,1033
del dist\ZeroNet\ZeroNet-cli.exe.manifest
del ZeroNet-cli.pkg
del dist\ZeroNet\ZeroNet-cli.pkg
copy tools\ZeroNet.cmd dist\ZeroNet\lib\ZeroNet.cmd
move dist\ZeroNet\ZeroNet-cli.exe dist\ZeroNet\lib\ZeroNet-cli.dat
echo Signing
set INPUT=
set /P INPUT=PVK password: %=%
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /t http://timestamp.verisign.com/scripts/timstamp.dll /v dist\ZeroNet\ZeroNet.exe
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /tr http://timestamp.digicert.com /fd sha256 /as /v dist\ZeroNet\ZeroNet.exe
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /t http://timestamp.verisign.com/scripts/timstamp.dll /v dist\ZeroNet\lib\ZeroNet-cli.dat
..\..\tools\signtool sign /f ..\..\cert.pfx /p %INPUT% /tr http://timestamp.digicert.com /fd sha256 /as /v dist\ZeroNet\lib\ZeroNet-cli.dat
pause