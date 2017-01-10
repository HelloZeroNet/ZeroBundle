#!/usr/bin/env python2.7


# Included modules
import sys
import os

# Add Windows exe source directories
start_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(start_dir, "lib"))
sys.path.insert(0, os.path.join(start_dir, "core"))

# ZeroNet Modules
import zeronet


def main():
    sys.argv = [sys.argv[0]]+["--open_browser", "default_browser"]+sys.argv[1:]
    zeronet.main()

if __name__ == '__main__':
    main()
