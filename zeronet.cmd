@echo off
if "%1" == "" (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
) else (
	if not exist ZeroNet (
		Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
	) else (
		cd ZeroNet
		..\Python\python.exe zeronet.py %*
		cd ..
	)
)
