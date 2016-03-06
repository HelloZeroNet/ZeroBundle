#!/bin/bash
cd "$(dirname "$0")"
if [ x$DISPLAY != x ] ; then
    # Has gui, open browser
    SCRIPT="start.py"
else
    # No gui
    SCRIPT="zeronet.py"
fi

if [ -d "ZeroNet" ]; then
    cd "$(dirname "$0")/ZeroNet"
    ../Python/python $SCRIPT "$@"
else
    ./Python/python -m zerobundle.run https://github.com/HelloZeroNet/ZeroNet $SCRIPT "$@"
fi