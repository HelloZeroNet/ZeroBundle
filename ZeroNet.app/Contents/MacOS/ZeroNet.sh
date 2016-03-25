#!/bin/bash
if [ -d "ZeroNet" ]; then
    cd "$(dirname "$0")/../../../ZeroNet"
    bash ../Python/python start.py "$@"
else
    cd "$(dirname "$0")/../../../"
    bash Python/python -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet start.py
fi
