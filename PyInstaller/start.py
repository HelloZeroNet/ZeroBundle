#!/usr/bin/env python2.7


# Included modules
import sys
import os

if getattr(sys, 'frozen', False):
    start_dir = os.path.dirname(sys.executable)
elif __file__:
    start_dir = os.path.dirname(__file__)

os.chdir(start_dir)  # Change the working dir

sys.path.insert(0, os.path.join(start_dir, "lib"))  # External modules
sys.path.insert(0, os.path.join(start_dir, "core"))  # ZeroNet source code

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
