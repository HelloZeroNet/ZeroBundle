#!/usr/bin/env python2.7


# Included modules
import sys
import os

# Add Windows exe source directories
start_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(start_dir, "lib"))
sys.path.insert(0, os.path.join(start_dir, "core"))

# For best compatibility copy required dlls to lib dir
if os.path.isfile(start_dir + "\\msvcr90.dll") and not os.path.isfile(start_dir + "\\lib\\msvcr90.dll"):
    import shutil
    for file_name in ("msvcm90.dll", "msvcp90.dll", "msvcr90.dll", "Microsoft.VC90.CRT.manifest"):
        try:
            shutil.copyfile(start_dir + "\\" + file_name, start_dir + "\\lib\\" + file_name)
        except Exception, err:
            print "Error copy", file_name, err


# ZeroNet Modules
import zeronet


def main():
    sys.argv = [sys.argv[0]]+["--open_browser", "default_browser"]+sys.argv[1:]
    zeronet.main()

if __name__ == '__main__':
    main()
