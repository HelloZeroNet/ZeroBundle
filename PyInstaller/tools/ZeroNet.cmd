@echo off
copy ZeroNet-cli.dat ..\ZeroNet.com >NUL
..\ZeroNet.com %*
del ..\ZeroNet.com