import threading
import webbrowser
import sys
import time
import os
from waitress import serve
from video_converter.backend.main import app
import socket

HOST = '127.0.0.1'
PORT = 5000

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def open_browser():
    time.sleep(1.5)  # Give server time to start
    webbrowser.open_new("http://127.0.0.1:5000")

def hide_console():
    if sys.platform == "win32":
        # Method 1: Use kernel32 directly
        try:
            kernel32 = ctypes.WinDLL('kernel32')
            user32 = ctypes.WinDLL('user32')
            hwnd = kernel32.GetConsoleWindow()
            if hwnd:
                user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE
        except:
            # Method 2: Alternative approach if first fails
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            os.environ['PYTHONWARNINGS'] = "ignore"  # Suppress warnings

if __name__ == '__main__':

    if is_port_in_use(5000):
        print("Server is already running on port 5000.")
        webbrowser.open_new(f"http://127.0.0.1:{PORT}")
        sys.exit(0)  # Prevent double-run

    # Hide console immediately
    if sys.platform == "win32":
        import ctypes
        hide_console()
    
    # Start browser in appropriate mode
    if getattr(sys, 'frozen', False):
        # Compiled executable mode
        import subprocess
        subprocess.Popen(['start', 'http://127.0.0.1:5000'], 
                        shell=True,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    else:
        # Script mode
        threading.Thread(target=open_browser, daemon=True).start()
    
    # Start server with proper hidden flags
    serve(
        app, 
        host='127.0.0.1', 
        port=5000,
        threads=4,
        ident=None,  # Remove server identification
        _quiet=True  # Suppress waitress output
    )