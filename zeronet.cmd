@echo off
if "%1" == "" (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
) else (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
)
