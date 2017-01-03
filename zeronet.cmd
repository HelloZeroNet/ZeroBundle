@echo off
cd /d "%~dp0"
if not exist ZeroNet (
	if "%1" == "" (
		Python\python.exe -m zerobundle.run_win https://github.com/HelloZeroNet/ZeroNet;https://gitlab.com/HelloZeroNet/ZeroNet;https://try.gogs.io/ZeroNet/ZeroNet start.py
	) else (
		Python\python.exe -m zerobundle.run_win https://github.com/HelloZeroNet/ZeroNet;https://gitlab.com/HelloZeroNet/ZeroNet;https://try.gogs.io/ZeroNet/ZeroNet zeronet.py %*
	)
) else (
	cd ZeroNet
	if "%1" == "" (
		..\Python\python.exe start.py
	) else (
		..\Python\python.exe zeronet.py %*
	)
	cd ..
)
