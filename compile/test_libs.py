import os, sys

sys.path.insert(0, "Lib")

import gevent
import gevent.monkey
import sqlite3
from errno import EAGAIN
from gevent.socket import wait_write
from gevent.server import DatagramServer
import os
import sys
import stat
import time
import logging
import ssl
import webbrowser
import msgpack
import ctypes as _ctypes
from ctypes.wintypes import HWND as _HWND, HANDLE as _HANDLE,DWORD as _DWORD,LPCWSTR as _LPCWSTR,MAX_PATH as _MAX_PATH, create_unicode_buffer as _cub
_SHGetFolderPath = _ctypes.windll.shell32.SHGetFolderPathW
import ctypes
import ctypes.wintypes
import os
import uuid
import time
import gevent
from gevent import sleep
from gevent.pool import Pool
from gevent.coros import BoundedSemaphore

while 1:
	print eval(raw_input("?"))