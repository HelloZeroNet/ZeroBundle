@echo off
if "%1" == "" (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet;https://gitlab.com/HelloZeroNet/ZeroNet;https://try.gogs.io/ZeroNet/ZeroNet start.py
) else (
	if not exist ZeroNet (
		Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet;https://gitlab.com/HelloZeroNet/ZeroNet;https://try.gogs.io/ZeroNet/ZeroNet zeronet.py %*
	) else (
		cd ZeroNet
		..\Python\python.exe zeronet.py %*
		cd ..
	)
)
