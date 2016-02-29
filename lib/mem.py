import tkinter
from tkinter import *
from tkinter import ttk

import win32ui
import win32process
import ctypes
from ctypes import *
from ctypes.wintypes import *

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

SYNCHRONIZE = 0x00100000;
STANDARD_RIGHTS_REQUIRED = 0x000F0000;
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF);

HWND = 0
TID = 0
PID = 0
processHandle = 0
buffer = 0
bufferSize = 0

#add unicode 'u' before sending string
def init(name) :
    HWND = win32ui.FindWindow(None,name).GetSafeHwnd()
    TID,PID = win32process.GetWindowThreadProcessId(HWND)
    processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, PID)
    buffer = c_char_p(b"The data goes here")
    bufferSize = len(buffer.value)

def readStat(address, offset):     
    val = c_ulonglong (0) 
    bytesRead = ctypes.c_size_t(0)
    if ReadProcessMemory(processHandle, address+offset, buffer, bufferSize, byref(bytesRead)):
        memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))        
        return val.value
    else:
        return -1


class Stat(object):
    def __init__(self, name, address, offsets, updaterate=0.2):
        self.name = name
        self.address = address
        self.offsets = offsets
        self.guivar = 0
        self.val = 0
		self.updaterate = updaterate
    def update(self):
		try:
			v = self.address
			for a in offsets:
				v = readStat(v,a)
			self.val = ctypes.c_ulong(v).value
		
			#if self.name == "Health" and self.val == 0 and globals.PAUSE:
			#    globals.GAME.resume()
			self.guivar.set(self.val)    
		except:
			pass
    def createGui(self, root, bg='black',ft="LucidaConsole 20 bold",fg='#FF6600') :
        self.guivar=StringVar()
        self.frame = tkinter.Frame(root, bg=bg)
        Label(self.frame, text=self.name+":",font=ft, bg=bg,fg=fg).pack(side="left")
        self.label = Label(self.frame, textvariable=self.guivar,font=ft, bg=bg,fg=fg).pack(side="left")
        return self.frame
	def updateCycle(self):
		while True:
			sleep(self.updaterate)
			self.update()
        
class Stats(object):
    def __init__(self, stats):
        self.stats = stats
    def process(self):
        for s in self.stats :
            s.update()