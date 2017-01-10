import zipfile
import os
import re
import sys
import cStringIO as StringIO
import ctypes
import ctypes.wintypes
import thread

# Windows API
WNDPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.LONG, ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)

DefWindowProc = ctypes.windll.user32.DefWindowProcW
DefWindowProc.restype = ctypes.wintypes.LONG
DefWindowProc.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]

GetMessage = ctypes.windll.user32.GetMessageW
GetMessage.restype = ctypes.wintypes.BOOL
GetMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG), ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.UINT]

GetWindowLong = ctypes.windll.user32.GetWindowLongW
GetWindowLong.restype = ctypes.wintypes.LONG
GetWindowLong.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]

TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.restype = ctypes.wintypes.BOOL
TranslateMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

DispatchMessage = ctypes.windll.user32.DispatchMessageW
DispatchMessage.restype = ctypes.wintypes.LONG
DispatchMessage.argtypes = [ctypes.POINTER(ctypes.wintypes.MSG)]

PostMessage = ctypes.windll.user32.PostMessageW
PostMessage.restype = ctypes.wintypes.BOOL
PostMessage.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]

SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.restype = ctypes.wintypes.LONG
SendMessage.argtypes = [ctypes.wintypes.HWND, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM]

SetWindowLong = ctypes.windll.user32.SetWindowLongW
SetWindowLong.restype = ctypes.wintypes.LONG
SetWindowLong.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.wintypes.LONG]

SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
SystemParametersInfo.restype = ctypes.wintypes.BOOL
SystemParametersInfo.argtypes = [ctypes.wintypes.UINT, ctypes.wintypes.UINT, ctypes.wintypes.LPVOID, ctypes.wintypes.UINT]

LF_FACESIZE = 32
class LOGFONT(ctypes.Structure):
    _fields_ = [("lfHeight", ctypes.wintypes.LONG),
                ("lfWidth", ctypes.wintypes.LONG),
                ("lfEscapement", ctypes.wintypes.LONG),
                ("lfOrientation", ctypes.wintypes.LONG),
                ("lfWeight", ctypes.wintypes.LONG),
                ("lfItalic", ctypes.wintypes.BYTE),
                ("lfUnderline", ctypes.wintypes.BYTE),
                ("lfStrikeOut", ctypes.wintypes.BYTE),
                ("lfCharSet", ctypes.wintypes.BYTE),
                ("lfOutPrecision", ctypes.wintypes.BYTE),
                ("lfClipPrecision", ctypes.wintypes.BYTE),
                ("lfQuality", ctypes.wintypes.BYTE),
                ("lfPitchAndFamily", ctypes.wintypes.BYTE),
                ("lfFaceName", ctypes.wintypes.WCHAR * LF_FACESIZE),]

CreateFontIndirect = ctypes.windll.gdi32.CreateFontIndirectW
CreateFontIndirect.restype = ctypes.wintypes.HFONT
CreateFontIndirect.argtypes = [ctypes.POINTER(LOGFONT)]

SPI_GETNONCLIENTMETRICS = 0x0029
class NONCLIENTMETRICS(ctypes.Structure):
    def __init__(self, *args, **kwargs):
        super(NONCLIENTMETRICS, self).__init__(*args, **kwargs)
        self.cbSize = ctypes.sizeof(self)
    _fields_ = [("cbSize", ctypes.wintypes.UINT),
                ("iBorderWidth", ctypes.c_int),
                ("iScrollWidth", ctypes.c_int),
                ("iScrollHeight", ctypes.c_int),
                ("iCaptionWidth", ctypes.c_int),
                ("iCaptionHeight", ctypes.c_int),
                ("lfCaptionFont", LOGFONT),
                ("iSmCaptionWidth", ctypes.c_int),
                ("iSmCaptionHeight", ctypes.c_int),
                ("lfSmCaptionFont", LOGFONT),
                ("iMenuWidth", ctypes.c_int),
                ("iMenuHeight", ctypes.c_int),
                ("lfMenuFont", LOGFONT),
                ("lfStatusFont", LOGFONT),
                ("lfMessageFont", LOGFONT)]

WM_CREATE = 0x0001
WM_DESTROY = 0x0002
WM_SETFONT = 0x0030
WM_CTLCOLORSTATIC = 0x0138
WM_USER = 0x0400

WS_POPUP        = 0x80000000L
WS_CHILD        = 0x40000000L
WS_VISIBLE      = 0x10000000L
WS_CAPTION      = 0x00C00000L
WS_SYSMENU      = 0x00080000L
WS_MINIMIZEBOX  = 0x00020000L

GWL_STYLE = -16

PBS_MARQUEE = 0x08

PBM_SETPOS = WM_USER+2
PBM_SETRANGE32 = WM_USER+6
PBM_SETMARQUEE = WM_USER+10

class WNDCLASSEX(ctypes.Structure):
    def __init__(self, *args, **kwargs):
        super(WNDCLASSEX, self).__init__(*args, **kwargs)
        self.cbSize = ctypes.sizeof(self)
    _fields_ = [("cbSize", ctypes.wintypes.UINT),
                ("style", ctypes.wintypes.UINT),
                ("lpfnWndProc", WNDPROC),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", ctypes.wintypes.HINSTANCE),
                ("hIcon", ctypes.wintypes.HICON),
                ("hCursor", ctypes.wintypes.HICON),
                ("hbrBackground", ctypes.wintypes.HBRUSH),
                ("lpszMenuName", ctypes.wintypes.LPCWSTR),
                ("lpszClassName", ctypes.wintypes.LPCWSTR),
                ("hIconSm", ctypes.wintypes.HICON)]

# Request https SSL error workaround
def httpRequest(url, as_file=False):
    if url.startswith("http://"):
        import urllib
        response = urllib.urlopen(url)
    else:  # Hack to avoid Python gevent ssl errors
        import socket
        import httplib
        import ssl

        host, request = re.match("https://(.*?)(/.*?)$", url).groups()

        conn = httplib.HTTPSConnection(host, timeout=15)
        sock = socket.create_connection((conn.host, conn.port), conn.timeout, conn.source_address)
        conn.sock = ssl.wrap_socket(sock, conn.key_file, conn.cert_file)
        conn.request("GET", request)
        response = conn.getresponse()
        if response.status in [301, 302, 303, 307, 308]:
            response = httpRequest(response.getheader('Location'))
    return response


def download(url, target_dir):
    global done, cancelled

    print "Downloading %s to %s directory." % (url, target_dir)
    ctypes.windll.user32.SetDlgItemTextW(hWnd, 1, u"Downloading %s to %s directory." % (url, target_dir))

    hWndProgress = ctypes.windll.user32.GetDlgItem(hWnd, 2)
    winLong = GetWindowLong(hWndProgress, GWL_STYLE)
    SetWindowLong(hWndProgress, GWL_STYLE, winLong | PBS_MARQUEE)
    PostMessage(hWndProgress, PBM_SETMARQUEE, 1, 0)

    file = httpRequest(url)

    total_size = file.getheader('Content-Length').strip()
    total_size = int(total_size)

    if total_size != 0:
        PostMessage(hWndProgress, PBM_SETMARQUEE, 0, 0)
        SetWindowLong(hWndProgress, GWL_STYLE, winLong)
        PostMessage(hWndProgress, PBM_SETRANGE32, 0, total_size)

    downloaded_size = 0
    data = StringIO.StringIO()
    while True:
        if cancelled:
            print "User cancelled."
            thread.exit()
        buff = file.read(1024 * 16)
        if not buff:
            print "not buff"
            break
        data.write(buff)
        downloaded_size += len(buff)
        PostMessage(hWndProgress, PBM_SETPOS, downloaded_size, 0)
        print ".",
    print "Downloaded."
    ctypes.windll.user32.SetDlgItemTextW(hWnd, 1, u"Downloaded. Extracting...")

    print "Extracting...",
    zip = zipfile.ZipFile(data)
    for inner_path in zip.namelist():
        inner_path = inner_path.replace("\\", "/")  # Make sure we have unix path
        print ".",
        dest_path = re.sub("^[^/]*-master.*?/", target_dir + "/", inner_path)  # Change -master dir with target_dir
        if target_dir not in dest_path:
            dest_path = target_dir+"/"+dest_path

        if ".." in dest_path:
            continue
        if not dest_path:
            continue

        dest_dir = os.path.dirname(dest_path)

        if dest_dir and not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        if dest_dir != dest_path.strip("/"):
            data = zip.read(inner_path)
            open(dest_path, 'wb').write(data)

    done = True
    print "Done."
    ctypes.windll.user32.SetDlgItemTextW(hWnd, 1, u"Done!")
    PostMessage(hWnd, 16, 0, 0)

def getDir(url):
    return re.match(".*/(.+?)$", url).group(1)

def WndProc(hWnd, Msg, wParam, lParam):
    if Msg == WM_CREATE:
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetClientRect(hWnd, ctypes.pointer(rect))

        width = 480
        height = 60
        hWndStatic = ctypes.windll.user32.CreateWindowExW(0, u"Static", 0, WS_CHILD | WS_VISIBLE, (rect.right / 2) - (width / 2), 20, width, height, hWnd, 1, 0, 0)

        # GetStockObject does not get the "true" font, use SystemParametersInfo SPI_GETNONCLIENTMETRICS.
        hFont = 0
        ncm = NONCLIENTMETRICS()
        ret = SystemParametersInfo(SPI_GETNONCLIENTMETRICS, ctypes.sizeof(NONCLIENTMETRICS), ctypes.pointer(ncm), 0)
        if ret:
            hFont = CreateFontIndirect(ctypes.pointer(ncm.lfMessageFont))
        else:
            hFont = ctypes.windll.gdi32.GetStockObject(17) # DEFAULT_GUI_FONT

        SendMessage(hWndStatic, WM_SETFONT, hFont, False)

        width = 480
        ctypes.windll.user32.CreateWindowExW(0, u"msctls_progress32", 0, WS_CHILD | WS_VISIBLE, (rect.right / 2) - (width / 2), 70, width, 20, hWnd, 2, 0, 0)
    elif Msg == WM_DESTROY:
        cancelled = True
        ctypes.windll.user32.PostQuitMessage(0)
    elif Msg == WM_CTLCOLORSTATIC:
        return 6 # COLOR_WINDOW+1
    else:
        return DefWindowProc(hWnd, Msg, wParam, lParam)
    return 0

# http://stackoverflow.com/a/10444161

class ACTCTX(ctypes.Structure):
    def __init__(self, *args, **kwargs):
        super(ACTCTX, self).__init__(*args, **kwargs)
        self.cbSize = ctypes.sizeof(self)
    _fields_ = [("cbSize", ctypes.wintypes.ULONG),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("lpSource", ctypes.wintypes.LPCWSTR),
                ("wProcessorArchitecture", ctypes.wintypes.USHORT),
                ("wLangId", ctypes.wintypes.LANGID),
                ("lpAssemblyDirectory", ctypes.wintypes.LPCWSTR),
                ("lpResourceName", ctypes.c_int),
                ("lpApplicationName", ctypes.wintypes.LPCWSTR),
                ("hModule", ctypes.wintypes.HMODULE),]

ACTCTX_FLAG_RESOURCE_NAME_VALID = 0x00000008

def EnableVisualStyles():
    if hasattr(ctypes.windll.kernel32, 'CreateActCtxW'):
        dir = ctypes.create_unicode_buffer(256)
        ctypes.windll.kernel32.GetSystemDirectoryW(dir, 256)
        actCtx = ACTCTX()
        actCtx.dwFlags = ACTCTX_FLAG_RESOURCE_NAME_VALID
        actCtx.lpSource = dir.value + u"\\shell32.dll"
        actCtx.lpResourceName = 124

        ulpActivationCookie = ctypes.c_int()
        ctypes.windll.kernel32.ActivateActCtx(ctypes.windll.kernel32.CreateActCtxW(ctypes.pointer(actCtx)), ctypes.pointer(ulpActivationCookie))

def downloadThread():
    global target_dir
    for url in urls:
        if ".zip" not in url:
            target_dir = getDir(url)
            if "github.com" in url:
                url += "/archive/master.zip"
            elif "gitlab.com" in url:
                url += "/repository/archive.zip?ref=master"
            elif "gogs.io" in url:
                url += "/archive/master.zip"

        if not os.path.isdir(target_dir):
            try:
                download(url, target_dir)
                break
            except Exception, err:
                print "Error downloading from %s: %s" % (url, err)

if __name__ == "__main__":
    if ";" in sys.argv[1]:
        urls = sys.argv[1].split(";")
    else:
        urls = [sys.argv[1]]
    script = " ".join(['"%s"' % arg for arg in sys.argv[2:]])

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)  # Hide console

    EnableVisualStyles()

    IDC_ARROW = 32512
    wndClass = WNDCLASSEX()
    wndClass.lpfnWndProc = WNDPROC(WndProc)
    wndClass.hCursor = ctypes.windll.user32.LoadCursorW(0, IDC_ARROW)
    wndClass.hbrBackground = 6 # COLOR_WINDOW+1
    wndClass.lpszClassName = "ZeroNet"
    ctypes.windll.user32.RegisterClassExW(ctypes.byref(wndClass))

    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    screenWidth = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
    screenHeight = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
    width = 500
    height = 130

    hWnd = ctypes.windll.user32.CreateWindowExW(0, u"ZeroNet", u"ZeroNet", WS_POPUP | WS_VISIBLE | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX, (screenWidth / 2) - (width / 2), (screenHeight / 2) - (height / 2), width, height, 0, 0, 0, 0)
    if hWnd == 0:
        exit()

    global done, cancelled
    done = False
    cancelled = False
    thread.start_new_thread(downloadThread, ())

    message = ctypes.wintypes.MSG()
    while GetMessage(ctypes.pointer(message), 0, 0, 0):
        TranslateMessage(ctypes.pointer(message))
        DispatchMessage(ctypes.pointer(message))

    print done
    if done:
        global target_dir
        print "Starting %s/%s..." % (target_dir, script)
        os.chdir(target_dir)
        os.execv("../Python/python", ["../Python/python", '%s' % script.strip("\"'")])
