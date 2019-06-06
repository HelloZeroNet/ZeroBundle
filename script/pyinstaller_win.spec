# -*- mode: python -*-
import sys

block_cipher = None

sys.modules['FixTk'] = None

a = Analysis(
    ['boot.py'],
    pathex=[],
    binaries=None,
    datas=None,
    hiddenimports=[
        'asn1crypto', 'asn1crypto.keys', 'cffi', 'base58','pyelliptic', 'rsa', 'socks', 'sockshandler', 'pyasn1', 'websocket', 'geventwebsocket', 'bencode', 'bitcoin', 'bitcoin.signmessage', 'bitcoin.core', 'bitcoin.wallet', 'maxminddb', 'merkletools',
        'zipimport', 'marshal', 'nt', 'winreg', 'encodings', 'codecs', 'ctypes', 'ctypes.wintypes', 'abc', 'os', 'stat', 'ntpath', 'genericpath', 'os.path', 'time', 'logging', 'traceback', 'collections', 'operator', 'keyword', 'heapq', 'itertools', 'reprlib', 'linecache', 'functools', 'tokenize', 're', 'enum', 'types', 'sre_compile', 'sre_parse', 'sre_constants', 'copyreg', 'token', 'warnings', 'weakref', 'collections.abc', 'string', 'threading', 'atexit', 'socket', 'selectors', 'math', 'select', 'errno', 'importlib', 'textwrap', 'signal', 'tracemalloc', 'fnmatch', 'posixpath', 'pickle', 'struct', 'gc', 'inspect', 'dis', 'opcode', 'importlib.machinery', 'zipfile', 'importlib.util', 'importlib.abc', 'contextlib', 'shutil', 'zlib', 'bz2', 'lzma', 'binascii', 'pkgutil', 'platform', 'subprocess', 'msvcrt', 'plistlib', 'datetime', 'xml', 'xml.parsers', 'xml.parsers.expat', 'pyexpat', 'email', 'email.parser', 'email.feedparser', 'email.errors', 'email._policybase', 'email.header', 'email.quoprimime', 'email.base64mime', 'base64', 'email.charset', 'email.encoders', 'quopri', 'email.utils', 'random', 'hashlib', 'bisect', 'urllib', 'urllib.parse', 'email._parseaddr', 'calendar', 'locale', 'tempfile', 'copy', 'pprint', 'email.message', 'uu', 'email._encoded_words', 'email.iterators', 'ssl', 'queue', 'argparse', 'gettext', 'configparser', 'logging.handlers', 'encodings.cp1250', 'urllib.request', 'http', 'http.client', 'urllib.error', 'urllib.response', 'nturl2path', 'xml.dom', 'json', 'array', 'sqlite3', 'html', 'html.entities', 'hmac', 'encodings.idna', 'stringprep', 'unicodedata', 'pathlib', 'difflib', 'cgi', 'mimetypes', 'uuid', 'concurrent'
    ],
    runtime_hooks=["script/pyinstaller_lib_hook.py"],
    excludes=['lib2to3', 'sys', 'zeronet', 'FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', 'gevent'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe_gui = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    append_pkg=False,
    name='ZeroNet',
    debug=False,
    strip=False,
    upx=True,
    icon="script/zeronet.ico",
    console=False
)

exe_cli = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    append_pkg=False,
    name='ZeroNet-cli',
    debug=False,
    strip=False,
    upx=True,
    icon="script/zeronet.ico",
    console=True
)

coll = COLLECT(
    exe_gui,
    exe_cli,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ZeroNet'
)
