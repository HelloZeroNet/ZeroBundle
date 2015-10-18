@echo off
IF "%1" == "" (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
) ELSE (
	Python\python.exe -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet zeronet.py %*
)
