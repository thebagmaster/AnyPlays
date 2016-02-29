import ctypes
import win32process
import vjoy
from ctypes import *
from ctypes.wintypes import *
from time import sleep

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
        
def KeyStroke(hexKeyCode,press=True):
    #    scan and press        scan and release
    #    (0x0|0x8)            (0x2|0x8)
    code = 0x8 if press else 0xa 
    if hexKeyCode == '' :
        return
    if hexKeyCode.isalpha() :
        hexKeyCode = lookup[hexKeyCode.upper()]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, code, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def MoveMouse(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    #x = int(x*(65536/ctypes.windll.user32.GetSystemMetrics(0))+1)
    #y = int(y*(65536/ctypes.windll.user32.GetSystemMetrics(1))+1)
    ii_.mi = MouseInput(x, y, 0, 0x0001, 1, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
def MoveMouseDelay(x,y,delay):
    movements = max([abs(x),abs(y)])
    pauselength = float(movements)/delay
    stepx = 0
    stepy = 0

    if self.dx > 0:
        stepx = -1
    elif self.dx < 0:
        stepx = 1
        
    if self.dy > 0:
        stepy = -1
    elif self.dy < 0:
        stepy = 1
        
    for i in range(movements):
        MoveMouse(stepx,stepy)
        x += stepx
        y += stepy
        if x == 0:
            stepx = 0
        if y == 0:
            stepy = 0
        sleep(pauselength)

def ClickMouse(evt):
    evt = lookup[evt.upper()]
    ctypes.windll.user32.mouse_event(evt, 0, 0, 0,0)
        
def JoystickPress(index,button,state):
    if not init:
        JoyInit()
    joyState = [vjoy.JoystickState(), vjoy.JoystickState()]
    joy.SetButton(joyState[0],button,state)
    vjoy.UpdateJoyState(index, joyState[0])
    
def JoystickAxis(index,axis,value):
    if not init:
        JoyInit()    
    joyState = [vjoy.JoystickState(), vjoy.JoystickState()]
    joy.SetAxis(joyState[0],axis,value)
    vjoy.UpdateJoyState(index, joyState[0])    
    
def JoystickPOV(index,pov,value):
    if not init:
        JoyInit()
    joyState = [vjoy.JoystickState(), vjoy.JoystickState()]
    joy.SetPOV(joyState[0],pov,value)
    vjoy.UpdateJoyState(index, joyState[0])    

def JoyInit():
    init = True
    try :
        vjoy.Shutdown()
    except :
        pass
    vjoy.Initialize()

init = False   
lookup = {
    #mouse
    'LBUTTOND':           0x02,
    'LBUTTONU':           0x04,
    'RBUTTOND':           0x08,
    'RBUTTONU':           0x10,
    'MBUTTOND':           0x20,
    'MBUTTONU':           0x40,
    #keybd
    'ESCAPE':          0x01,
    '1':               0x02,
    '2':               0x03,
    '3':               0x04,
    '4':               0x05,
    '5':               0x06,
    '6':               0x07,
    '7':               0x08,
    '8':               0x09,
    '9':               0x0A,
    '0':               0x0B,
    'MINUS':           0x0C,    # - on main keyboard     
    'EQUALS':          0x0D,
    'BACK':            0x0E,    # backspace     
    'TAB':             0x0F,
    'Q':               0x10,
    'W':               0x11,
    'E':               0x12,
    'R':               0x13,
    'T':               0x14,
    'Y':               0x15,
    'U':               0x16,
    'I':               0x17,
    'O':               0x18,
    'P':               0x19,
    'LBRACKET':        0x1A,
    'RBRACKET':        0x1B,
    'RETURN':          0x1C,    # Enter on main keyboard     
    'LCONTROL':        0x1D,
    'A':               0x1E,
    'S':               0x1F,
    'D':               0x20,
    'F':               0x21,
    'G':               0x22,
    'H':               0x23,
    'J':               0x24,
    'K':               0x25,
    'L':               0x26,
    'SEMICOLON':       0x27,
    'APOSTROPHE':      0x28,
    'GRAVE':           0x29,    # accent grave     
    'LSHIFT':          0x2A,
    'BACKSLASH':       0x2B,
    'Z':               0x2C,
    'X':               0x2D,
    'C':               0x2E,
    'V':               0x2F,
    'B':               0x30,
    'N':               0x31,
    'M':               0x32,
    'COMMA':           0x33,
    'PERIOD':          0x34,    # . on main keyboard     
    'SLASH':           0x35,    # / on main keyboard     
    'RSHIFT':          0x36,
    'MULTIPLY':        0x37,    # * on numeric keypad     
    'LMENU':           0x38,    # left Alt     
    'SPACE':           0x39,
    'CAPITAL':         0x3A,
    'F1':              0x3B,
    'F2':              0x3C,
    'F3':              0x3D,
    'F4':              0x3E,
    'F5':              0x3F,
    'F6':              0x40,
    'F7':              0x41,
    'F8':              0x42,
    'F9':              0x43,
    'F10':             0x44,
    'NUMLOCK':         0x45,
    'SCROLL':          0x46,    # Scroll Lock     
    'NUMPAD7':         0x47,
    'NUMPAD8':         0x48,
    'NUMPAD9':         0x49,
    'SUBTRACT':        0x4A,    # - on numeric keypad     
    'NUMPAD4':         0x4B,
    'NUMPAD5':         0x4C,
    'NUMPAD6':         0x4D,
    'ADD':             0x4E,    # + on numeric keypad     
    'NUMPAD1':         0x4F,
    'NUMPAD2':         0x50,
    'NUMPAD3':         0x51,
    'NUMPAD0':         0x52,
    'DECIMAL':         0x53,    # . on numeric keypad     
    'F11':             0x57,
    'F12':             0x58,
    'F13':             0x64,    #                     (NEC PC98)     
    'F14':             0x65,    #                     (NEC PC98)     
    'F15':             0x66,    #                     (NEC PC98)    
    'KANA':            0x70,    # (Japanese keyboard)                
    'CONVERT':         0x79,    # (Japanese keyboard)                
    'NOCONVERT':       0x7B,    # (Japanese keyboard)                
    'YEN':             0x7D,    # (Japanese keyboard)                
    'NUMPADEQUALS':    0x8D,    # = on numeric keypad (NEC PC98)     
    'CIRCUMFLEX':      0x90,    # (Japanese keyboard)                
    'AT':              0x91,    #                     (NEC PC98)     
    'COLON':           0x92,    #                     (NEC PC98)     
    'UNDERLINE':       0x93,    #                     (NEC PC98)     
    'KANJI':           0x94,    # (Japanese keyboard)                
    'STOP':            0x95,    #                     (NEC PC98)     
    'AX':              0x96,    #                     (Japan AX)     
    'UNLABELED':       0x97,    #                        (J3100)     
    'NUMPADENTER':     0x9C,    # Enter on numeric keypad     
    'RCONTROL':        0x9D,
    'NUMPADCOMMA':     0xB3,    # , on numeric keypad (NEC PC98)     
    'DIVIDE':          0xB5,    # / on numeric keypad     
    'SYSRQ':           0xB7,
    'RMENU':           0xB8,    # right Alt     
    'HOME':            0xC7,    # Home on arrow keypad     
    'UP':              0xC8,    # UpArrow on arrow keypad     
    'PRIOR':           0xC9,    # PgUp on arrow keypad     
    'LEFT':            0xCB,    # LeftArrow on arrow keypad     
    'RIGHT':           0xCD,    # RightArrow on arrow keypad     
    'END':             0xCF,    # End on arrow keypad     
    'DOWN':            0xD0,    # DownArrow on arrow keypad     
    'NEXT':            0xD1,    # PgDn on arrow keypad     
    'INSERT':          0xD2,    # Insert on arrow keypad     
    'DELETE':          0xD3,    # Delete on arrow keypad     
    'LWIN':            0xDB,    # Left Windows key     
    'RWIN':            0xDC,    # Right Windows key     
    'APPS':            0xDD     # AppMenu key     
}
  