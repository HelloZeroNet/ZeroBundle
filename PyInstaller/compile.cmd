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
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist/ZeroNet', '../dist/ZeroNet-win.zip'); }"
