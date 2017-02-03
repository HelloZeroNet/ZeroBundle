#!/usr/bin/env python2.7
import sys
import os
import time


def getWorkDir():
    if getattr(sys, 'frozen', False):
        work_dir = os.path.dirname(os.path.abspath(sys.executable))  # Normally next to .exe

        if work_dir.startswith("/Application") or work_dir.startswith("/private") or work_dir.startswith(os.path.expanduser("~/Library")):
            # In Applcation Support
            work_dir = os.path.expanduser("~/Library/Application Support/ZeroNet")
            if not os.path.isdir(work_dir):
                os.mkdir(work_dir)
        elif ".app" in work_dir:
            # Outside of .app
            import re
            work_dir = re.sub("/[^/]+\.app/.*$", "", work_dir)
    elif __file__:
        # Right next to .py
        work_dir = os.path.dirname(os.path.abspath(__file__))

    return work_dir


# Get revision from Config.py file
def getRev(file_path):
    import re
    try:
        config_data = open(file_path).read(1024)
        rev = re.search("rev = ([0-9]+)", config_data).group(1)
        return int(rev)
    except Exception:
        return -1


# ZeroNet source paths
def addSourcePaths(work_dir):
    if sys.platform == "darwin":
        source_packed_dir = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable)) + "/../Resources/core")
        source_update_dir = work_dir + "/core"

        if getRev(source_update_dir + "/src/Config.py") > getRev(source_packed_dir + "/src/Config.py"):
            sys.path.append(source_update_dir)  # Updated source

        sys.path.append(source_packed_dir)  # Packed-in source
        sys.source_update_dir = source_update_dir  # Updated source code should be put here
    else:
        sys.path.insert(0, os.path.join(work_dir, "lib"))  # External modules
        sys.path.insert(0, os.path.join(work_dir, "core"))  # ZeroNet source code


# On Windows for best compatibility copy required dlls to lib dir
def copyDlls(work_dir):
    if os.path.isfile(work_dir + "\\msvcr90.dll") and not os.path.isfile(work_dir + "\\lib\\msvcr90.dll"):
        import shutil
        for file_name in ("msvcm90.dll", "msvcp90.dll", "msvcr90.dll", "Microsoft.VC90.CRT.manifest"):
            try:
                shutil.copyfile(work_dir + "\\" + file_name, work_dir + "\\lib\\" + file_name)
            except Exception, err:
                print "Error copy dll", file_name, err


def setup():
    work_dir = getWorkDir()

    # Redirect stdout to file if running as .app
    if sys.platform == "darwin" and not sys.stdout.isatty() and os.path.isdir(work_dir + "/log"):
        print "Running as .app", sys.argv
        try:
            sys.stdout = open(work_dir + "/log/stdout.log", "w")
            sys.stderr = sys.stdout
        except Exception, err:
            print "Error redirecting stdout:", err

    # Remove weird -psn_ argument
    if len(sys.argv) > 1 and sys.argv[1].startswith('-psn_'):
        del sys.argv[1]

    # Replace boot.py with the real executable
    if sys.argv[0].endswith("Resources/boot.py"):
        sys.argv[0] = sys.argv[0].replace("Resources/boot.py", "MacOS/ZeroNet")
        sys.executable = sys.argv[0]

    addSourcePaths(work_dir)
    if sys.platform.startswith("win"):
        copyDlls(work_dir)


setup()


import zeronet


gui_root = None

def gui():
    global gui_root
    sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk")
    sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/")

    # Wait for ui_server startup
    while not (sys.modules.get("main") and "ui_server" in dir(sys.modules["main"]) and getattr(sys.modules["main"].ui_server, "server", None)):
        time.sleep(0.1)

    def click():
        import webbrowser
        webbrowser.open("http://127.0.0.1:43110")

    def quit():
        sys.exit(0)

    try:
        from Tkinter import Tk
        gui_root = Tk()
        gui_root.iconify()
        gui_root.createcommand('tk::mac::ReopenApplication', click)
        gui_root.createcommand('tk::mac::Quit', quit)
        if not os.environ.get("SECURITYSESSIONID"):  # Not started by auto-run
            click()
        gui_root.mainloop()
    except ExitCommand:
        print "Stopping..."
    except Exception, err:
        print "Gui error: %s" % err
        while 1:
            time.sleep(1000)


class ExitCommand(Exception):
    pass


def signalHandler(signal, frame):
    raise ExitCommand()



def main(mode="main", open_browser=True):
    if open_browser:
        sys.argv = [sys.argv[0]] + ["--open_browser", "default_browser"] + sys.argv[1:]  # Open browser window

    if mode == "thread":
        # Manipulate sys.exit to send exit signal before killing the thread
        sys_exit = sys.exit

        def threadedExit(*args):
            if gui_root:
                gui_root.destroy()
            os.kill(os.getpid(), signal.SIGUSR1)
            sys_exit(*args)
        sys.exit = threadedExit

    # Start ZeroNet itself
    zeronet.main()

    # Stop gui
    if gui_root:
        gui_root.destroy()

    if mode == "thread":
        # Send exit signal
        os.kill(os.getpid(), signal.SIGUSR1)


if __name__ == '__main__':
    if sys.platform == "darwin":
        import signal
        signal.signal(signal.SIGUSR1, signalHandler)
        from threading import Thread
        t = Thread(target=main, kwargs={"mode": "thread", "open_browser": False})
        t.daemon = True
        t.start()

        try:
            # Start dock icon click watcher on macOS
            gui()
        except ExitCommand:
            pass
    else:
        main()
