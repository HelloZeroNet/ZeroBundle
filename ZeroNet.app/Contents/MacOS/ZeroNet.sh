#!/bin/bash
cd "$(dirname "$0")/../../../"
if [ -d "ZeroNet" ]; then
    cd ZeroNet
    bash ../Python/python start.py
else
    osascript -e 'display notification "Downloading and starting latest version..." with title "ZeroNet"'
    ./Python/python -m zerobundle.run "https://github.com/HelloZeroNet/ZeroNet;https://gitlab.com/HelloZeroNet/ZeroNet;https://try.gogs.io/ZeroNet/ZeroNet" "start.py" "$@"
fi
exit 0