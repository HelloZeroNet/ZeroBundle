#!/bin/bash
cd "$(dirname "$0")/../../../"
if [ -d "ZeroNet" ]; then
    cd ZeroNet
    bash ../Python/python start.py
else
    bash Python/python -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
fi
exit 0
