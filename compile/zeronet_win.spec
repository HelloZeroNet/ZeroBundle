# -*- mode: python -*-
import sys

block_cipher = None

sys.modules['FixTk'] = None

a = Analysis(
    ['boot.py'],
    pathex=[],
    binaries=None,
    datas=None,
    hiddenimports=["win32file", "resource", "gevent", "msgpack", "sqlite3", 'queue', 'aifc', 'antigravity', 'argparse', 'asynchat', 'asyncore', 'audiodev', 'BaseHTTPServer', 'Bastion', 'binhex', 'cgi', 'CGIHTTPServer', 'cgitb', 'chunk', 'code', 'codeop', 'colorsys', 'commands', 'compileall', 'ConfigParser', 'Cookie', 'cProfile', 'csv', 'dircache', 'DocXMLRPCServer', 'filecmp', 'fileinput', 'formatter', 'fpformat', 'fractions', 'glob', 'hmac', 'htmlentitydefs', 'htmllib', 'HTMLParser', 'ihooks', 'imaplib', 'imghdr', 'imputil', 'macpath', 'macurl2path', 'mailbox', 'mailcap', 'markupbase', 'md5', 'mhlib', 'MimeWriter', 'mimify', 'modulefinder', 'multifile', 'mutex', 'netrc', 'new', 'nntplib', 'pickletools', 'pipes', 'pkgutil', 'popen2', 'poplib', 'posixfile', 'profile', 'pstats', 'pty', 'pyclbr', 'pydoc', 'rexec', 'rlcompleter', 'robotparser', 'runpy', 'sched', 'sets', 'sgmllib', 'sha', 'shelve', 'SimpleHTTPServer', 'SimpleXMLRPCServer', 'site', 'smtpd', 'smtplib', 'sndhdr', 'SocketServer', 'statvfs', 'stringold', 'struct', 'sunau', 'sunaudio', 'symbol', 'symtable', 'tabnanny', 'telnetlib', 'this', 'timeit', 'toaiff', 'trace', 'tty', 'user', 'UserList', 'UserString', 'uuid', 'wave', 'webbrowser', 'xdrlib', 'xmllib', 'xmlrpclib', '_pyio', '__phello__.foo', 'bsddb.dbobj', 'bsddb.dbrecio', 'bsddb.dbshelve', 'bsddb.dbtables', 'compiler.ast', 'compiler.consts', 'compiler.future', 'compiler.misc', 'compiler.pyassem', 'compiler.pycodegen', 'compiler.symbols', 'compiler.syntax', 'compiler.transformer', 'compiler.visitor', 'curses.ascii', 'curses.has_key', 'curses.panel', 'curses.textpad', 'curses.wrapper', 'email.mime.application', 'email.mime.audio', 'email.mime.base', 'email.mime.image', 'email.mime.message', 'email.mime.multipart', 'email.mime.nonmultipart', 'email.mime.text', 'gevent.aresd', 'gevent.backdoor', 'gevent.baseserver', 'gevent.corecextd', 'gevent.coros', 'gevent.pywsgi', 'gevent.server', 'gevent.util', 'gevent.wsgi', 'gevent._semaphore', 'gevent._semaphored', 'gevent._socket3', 'hotshot.log', 'hotshot.stats', 'hotshot.stones', 'json.decoder', 'json.encoder', 'json.scanner', 'json.tool', 'logging.config', 'logging.handlers', 'msgpack._packerd', 'msgpack._unpackerd', 'msilib.schema', 'msilib.sequence', 'msilib.text', 'multiprocessing.connection', 'multiprocessing.forking', 'multiprocessing.heap', 'multiprocessing.managers', 'multiprocessing.pool', 'multiprocessing.process', 'multiprocessing.queues', 'multiprocessing.reduction', 'multiprocessing.sharedctypes', 'multiprocessing.synchronize', 'multiprocessing.util', 'multiprocessing.dummy.connection', 'unittest.__main__', 'wsgiref.handlers', 'wsgiref.headers', 'wsgiref.simple_server', 'wsgiref.util', 'wsgiref.validate', 'xml.dom.domreg', 'xml.dom.expatbuilder', 'xml.dom.minicompat', 'xml.dom.minidom', 'xml.dom.NodeFilter', 'xml.dom.pulldom', 'xml.dom.xmlbuilder', 'xml.etree.cElementTree', 'xml.etree.ElementInclude', 'xml.etree.ElementPath', 'xml.etree.ElementTree', 'Queue'],
    hookspath=[],
    excludes=['sys', 'zeronet', 'FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
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
    icon="zeronet.ico",
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
    icon="zeronet.ico",
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
