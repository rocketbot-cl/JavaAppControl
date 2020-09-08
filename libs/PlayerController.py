import pyautogui, sys
import ctypes
import time
import win32com.client as comclt

class MouseEventFlag:
    """MouseEventFlag from Win32."""
    Move = 0x0001
    LeftDown = 0x0002
    LeftUp = 0x0004
    RightDown = 0x0008
    RightUp = 0x0010
    MiddleDown = 0x0020
    MiddleUp = 0x0040
    XDown = 0x0080
    XUp = 0x0100
    Wheel = 0x0800
    HWheel = 0x1000
    MoveNoCoalesce = 0x2000
    VirtualDesk = 0x4000
    Absolute = 0x8000

class KeyboardEventFlag:
    """KeyboardEventFlag from Win32."""
    KeyDown = 0x0000
    ExtendedKey = 0x0001
    KeyUp = 0x0002
    KeyUnicode = 0x0004
    KeyScanCode = 0x0008

def do_click(bounds_component):
    x = bounds_component['x']
    y = bounds_component['y']
    width = bounds_component['width']
    height = bounds_component['heigth']
    x_center = (x * 2 + width) / 2
    y_center = (y * 2 + height) / 2
    Click(int(x_center),int (y_center))

def set_text(bounds_component, text):
    do_click(bounds_component)
    wsh= comclt.Dispatch("WScript.Shell")
    wsh.SendKeys(text) 

def mouse_event(dwFlags: int, dx: int, dy: int, dwData: int, dwExtraInfo: int) :
    """mouse_event from Win32."""
    ctypes.windll.user32.mouse_event(dwFlags, dx, dy, dwData, dwExtraInfo)

def Click(x: int, y: int):
    """
    Simulate mouse click at point x, y.
    x: int.
    y: int.
    waitTime: float.
    """
    #SetCursorPos(x, y)
    ctypes.windll.user32.SetCursorPos(x, y)
    screenWidth, screenHeight = GetScreenSize()
    time.sleep(0.05)
    mouse_event(MouseEventFlag.LeftDown | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(0.05)
    mouse_event(MouseEventFlag.LeftUp | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(0.5)

def GetScreenSize():
    """Return Tuple[int, int], two ints tuple (width, height)."""
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    w = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
    h = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
    return w, h

def SendKey(key: int, waitTime= 0.5) -> None:
    """
    Simulate typing a key.
    key: int, a value in class `Keys`.
    """
    keybd_event(key, 0, KeyboardEventFlag.KeyDown | KeyboardEventFlag.ExtendedKey, 0)
    keybd_event(key, 0, KeyboardEventFlag.KeyUp | KeyboardEventFlag.ExtendedKey, 0)
    time.sleep(waitTime)

def keybd_event(bVk: int, bScan: int, dwFlags: int, dwExtraInfo: int) -> None:
    """keybd_event from Win32."""
    ctypes.windll.user32.keybd_event(bVk, bScan, dwFlags, dwExtraInfo)

