#! /usr/bin/env python

import irc.bot
import irc.strings
import ctypes
import win32process
from ctypes import *
from ctypes.wintypes import *
from collections import defaultdict
from collections import Counter
from time import sleep
import tkinter
from tkinter import *
from tkinter import ttk
import win32api
import win32gui
import win32ui
import win32con
import win32com.client
import threading
import os
import sys
import psutil
import struct
import pythoncom 
from concurrent.futures import ThreadPoolExecutor

TP = ThreadPoolExecutor(max_workers=10)

#REBOOT________
ELAPSED=0

#IRC HANDLE____________________________________________________________________________________________
CON = 0

#PAUSE FUNCTIONALITY___________________________________________________________________________________
DS = 0
PROCNAME = "DARKSOULS.exe"
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        DS = proc
PAUSED = True

#READ MEM FUNCTIONALITY________________________________________________________________________________
OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

SYNCHRONIZE = 0x00100000;
STANDARD_RIGHTS_REQUIRED = 0x000F0000;
PROCESS_ALL_ACCESS        = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF);

HWND = win32ui.FindWindow(None,u'DARK SOULS').GetSafeHwnd()
TID,PID = win32process.GetWindowThreadProcessId(HWND)
processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, PID)
buffer = c_char_p(b"The data goes here")
bufferSize = len(buffer.value)

#DEMOCRACY VOTE FUNCTIONALITY__________________________________________________________________________
dvotes = defaultdict(int)
draw = []
dcntr = 0
dvotes_s = defaultdict(int)
dcmd = 'f'

#GUI ELEMENTS__________________________________________________________________________________________

listChat = 0
listCmds = 0
listVotes = 0
progTime = 0
deaths = 0
level = 0

#CONTROL MODES_________________________________________________________________________________________
CTRL = {
    #type:[mode,min,max,current,gui]
    1:[True,0,1000,950,0,'CHAOS                                ORDER'],
    2:[True,0,1000,520,0,'UNBANM                               BANM'],
    3:[True,0,60,40,0,'DELAYDN                         DELAYUP']
}    

CTRLS = {
    #cmd : [type,inc/dec]
    'demo':     [1,1],
    'democracy':[1,1],
    'order':    [1,1],
    'chaos':    [1,-1],
    'anarchy':  [1,-1],
    
    'banm':     [2,1],
    'banmenu':  [2,1],
    'unbanm':   [2,-1],
    'unbanmenu':[2,-1],
    
    'delayup':  [3,1],
    'delaydn':  [3,-1]
}

#COMMANDS LIST_____________________________________________________
STDLY = 40    
BINDS = {
    'm':      [1,STDLY,0xCF,STDLY],
    'aru':    [1,STDLY,0xC8,STDLY],
    'arr':    [1,STDLY,0xCD,STDLY],
    'ard':    [1,STDLY,0xD0,STDLY],
    'arl':    [1,STDLY,0xCB,STDLY],
    'bs':     [1,STDLY,0x0E,STDLY],
    
    'fr':     [2,STDLY,0x11,0,0x20,300],
    'fl':     [2,STDLY,0x11,0,0x1E,300],
    'br':     [2,STDLY,0x1F,0,0x20,300],
    'bl':     [2,STDLY,0x1F,0,0x1E,300],
    'run':    [2,STDLY,0x11,0,0x39,800],
    'flong':  [1,0,0x11,800],
    'fwdlong':[1,0,0x11,800],
    'f':      [1,STDLY,0x11,300],
    'fwd':    [1,STDLY,0x11,300],
    'l':      [1,STDLY,0x1E,300],
    'left':   [1,STDLY,0x1E,300],
    'r':      [1,STDLY,0x20,300],
    'right':  [1,STDLY,0x20,300],
    'b':      [1,STDLY,0x1F,300],
    'back':   [1,STDLY,0x1F,300],
    'd':      [1,STDLY,0x39,300],
    'back':   [1,STDLY,0x1F,300],
    
    'hold':   [1,400,0x0,STDLY],
    'linger': [1,1000,0x0,STDLY],
    'a':      [1,200,0x10,STDLY],
    'e':      [1,STDLY,0x1C,STDLY],
    'u':      [1,1200,0x12,STDLY],
    'x':      [1,STDLY,0x12,STDLY],
    'du':     [1,STDLY,0x13,STDLY],
    'dd':     [1,STDLY,0x21,STDLY],
    'dr':     [1,STDLY,0x2F,STDLY],
    'dl':     [1,STDLY,0x2E,STDLY],
    
    'cu':     [1,STDLY,0x25,100],
    'cd':     [1,STDLY,0x17,100],
    'cl':     [1,STDLY,0x24,100],
    'cr':     [1,STDLY,0x26,100],
    'cur':    [2,STDLY,0x25,0,0x26,100],
    'cul':    [2,STDLY,0x25,0,0x24,100],
    'cdr':    [2,STDLY,0x17,0,0x26,100],
    'cdl':    [2,STDLY,0x17,0,0x24,200],
    'ges':    [1,STDLY,0x22,STDLY],
    
    'r1':     [1,1100,0x23,STDLY],
    'kick':   [2,300,0x11,0,0x23,STDLY],
    'k':      [2,300,0x11,0,0x23,STDLY],
    'jumpattack':[3,1500,0x11,0,0x39,0,0x16,STDLY],
    'ja':     [3,1500,0x11,0,0x39,0,0x16,STDLY],
    'r2':     [1,1500,0x16,STDLY],
    'l1':     [1,400,0x2A,STDLY],
    'l2':     [1,100,0x0F,STDLY],
    'g':      [1,100,0x38,STDLY],
    
    'rf':     [2,900,0x11,STDLY,0x39,100],
    'roll':   [2,900,0x11,STDLY,0x39,100],
    'rb':     [2,900,0x1F,STDLY,0x39,100],
    'rl':     [2,900,0x1E,STDLY,0x39,100],
    'rr':     [2,900,0x20,STDLY,0x39,100]
}
    
#TOGGLES_______________________________________________________________________________________________
TOGG = defaultdict(bool)
TOGG['f'] = False
TOGG['fwd'] = False
TOGG['l1'] = False
TOGG['run'] = False

def Sanitize(message):
    tmp = re.search(u'[\u0000-\uFFFF]+',message)
    if tmp :
        return tmp.group(0)
    else :
        return False

def StartBot():
    server = "irc.twitch.tv"
    port = 6667
    channel = "#twitchplaysdark"
    nickname = "thebagmaster"
    # thebagmaster oauth:fe20g2udsuh4fj3lo939a4531ggg1y
    # TPD_BanHammer oauth:mfnv3lmqg0fii1iuivp4s1o8x5woaj
    bot = Bot(channel, nickname, server, port)
    bot.start()

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, "oauth:fe20g2udsuh4fj3lo939a4531ggg1y")], nickname, nickname, reconnection_interval=1)
        self.channel = channel

    def on_welcome(self, c, e):
        global CON
        CON = self.connection
        c.join(self.channel)

    def on_pubmsg(self, c, e) :
        global CTRL,PAUSED,DS
        sender = e.source.nick
        cmds = e.arguments[0].split()
        if len(cmds) > 1 :
            SendChat(sender,e.arguments[0])
                                #democracy
        elif isCmd(cmds[0]) and CTRL[1][0]:
            global draw
            draw.append(cmds[0])
            updateVote()
        else:
            if not CTRL[1][0] : 
                if PAUSED :
                    DS.resume()
                    PAUSED = False
            global TP
            TP.submit(ProcessCmd,sender,cmds[0],True)
    
def SendChat(sender,message):
    global listChat
    nick = Sanitize(sender)
    msg = Sanitize(message)
    if nick and msg :
        listChat.delete(0)
        listChat.insert(END, nick[:6] + ': ' + msg[:22])

def SendCmds(sender,message):
    global listCmds
    nick = Sanitize(sender)
    msg = Sanitize(message)
    if nick and msg :
        listCmds.delete(0)
        listCmds.insert(END, nick[:6] + ': ' + msg[:22])

def ProcessCmd(sender,cmd,release):
    try:
        target=True
        global CTRLS,BINDS,TOGG,CTRL   
        cmd = Sanitize(cmd)
        if cmd and len(cmd) > 1:   
            #MULTI COMMANDS _______________________________________________________________________________
            if len(cmd) >= 3:
                num = cmd[-2:][1]
                if (cmd[-2:][0] == 'x') and num.isdigit():
                    n = int(num)
                    if n <= 5:
                        cmd = cmd.replace('x'+num,'')
                        for x in range(1,n+1):
                            if cmd not in CTRLS :
                                ProcessCmd("Multi",cmd,True)
                        return        
            #SINGLE COMMANDS_______________________________________________________________________________
            if cmd[:1][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in BINDS:
                    sleep(0.05)
                    PressKey(0x18)
                    sleep(0.05)
                    ReleaseKey(0x18)
                    target=False
            if cmd[:1][0] == 'n' :
                cmd = cmd.replace('n','',1)
                if cmd in BINDS:
                    target=False
            #TOGGLE COMMANDS_______________________________________________________________________________
            if cmd[-1:][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in TOGG :
                    if not TOGG[cmd] :
                        ProcessCmd("TogOn",cmd,False)
                        TOGG[cmd] = True
                        return
                    else :
                        ProcessCmd("TogOff",cmd,True)
                        TOGG[cmd] = False
                        return
                                                    #ban menu
        if cmd in BINDS and (not cmd == 'm' or not CTRL[2][0]):
            SendCmds(sender,cmd)
            for x in range(0,BINDS[cmd][0]):
                PressKey(BINDS[cmd][2+2*x])
                #print(' '+str(x)+' '+str(BINDS[cmd][1+2*x])+' ' + str(BINDS[cmd][2+2*x]))
                sleep(0.002*BINDS[cmd][3+2*x])

            if release :
                for x in range(0,BINDS[cmd][0]):
                    ReleaseKey(BINDS[cmd][2+2*x])
                    #sleep(0.002*BINDS[cmd][3+2*x])
            sleep(BINDS[cmd][1]*0.001)
            #fixcam
            if target :
                sleep(0.02)
                PressKey(0x18)
                sleep(0.02)
                ReleaseKey(0x18)
                sleep(0.4)
            
        elif cmd in CTRLS:
            SendCmds(sender,cmd)
            type = CTRLS[cmd][0]
            ad = CTRLS[cmd][1]
            cur = CTRL[type][3]
            prog = CTRL[type][4]
            max = CTRL[type][2]
            if (cur+ad) >= CTRL[type][1] and (cur+ad) <= CTRL[type][2] and not (type==3 and (cur+ad) < 20):
                #styles
                if (cur+ad) >= 0.65 * max : 
                    prog["style"] = "green.Horizontal.TProgressbar"
                elif (cur+ad) <= 0.5 * max : 
                    prog["style"] = "red.Horizontal.TProgressbar"
                else :
                    prog["style"] = "yellow.Horizontal.TProgressbar"
                CTRL[type][3] = cur+ad
                cur = CTRL[type][3]
                CTRL[type][4]["value"] = cur
                CTRL[type][0] = (cur >= .5*max)
                
        else :
            if not CTRL[1][0] :
                SendChat(sender,cmd)
    except:
        if not CTRL[1][0] :
                SendChat(sender,cmd)
 
#Junk for pressing keys
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

def PressKey(hexKeyCode):
    if hexKeyCode != 0x0 :
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    if hexKeyCode != 0x0 :
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def readStat(address, offset):     

    val = c_int()    
    bytesRead = c_ulong(0)
    
    if ReadProcessMemory(processHandle, address, buffer, bufferSize, byref(bytesRead)):
        memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
        if ReadProcessMemory(processHandle, val.value + offset, buffer, bufferSize, byref(bytesRead)):
            memmove(ctypes.byref(val), buffer, ctypes.sizeof(val))
            return val.value
        else:
            return -1
        
        return val.value
    else:
        return -1
    
def Focus(event):
    if threading.currentThread ().getName () != 'MainThread': 
        pythoncom.CoInitialize () 
    shell = win32com.client.Dispatch('WScript.Shell')
    shell.AppActivate('DARK SOULS')
 
def dCnt():
    sleep(0.99)
    global CTRL,ELAPSED
        #demo
    if CTRL[1][0] :
        global dcntr
        global progTime
        dcntr += 1
        #delayvalue
        max = CTRL[3][3]
        progTime["maximum"] = max
        progTime["value"] = dcntr
        #styles
        if dcntr >= 0.65 * max : 
            progTime["style"] = "red.Horizontal.TProgressbar"
        elif dcntr <= 0.35 * max : 
            progTime["style"] = "green.Horizontal.TProgressbar"
        else :
            progTime["style"] = "yellow.Horizontal.TProgressbar"
        updateVote()
    checkDemo()
    ELAPSED += 1
    #if ELAPSED >= 28800 :
    #    os.execv(__file__, sys.argv)
    #threading.Timer(1, dCnt).start()
    global TP
    TP.submit(dCnt)
    

def isCmd(cmd):
    cmd = Sanitize(cmd)
    try:
        if cmd in BINDS:
            return True
        if cmd and len(cmd) > 1:   
            #MULTI COMMANDS _______________________________________________________________________________
            if len(cmd) >= 3:
                num = cmd[-2:][1]
                if (cmd[-2:][0] == 'x') and num.isdigit():
                    n = int(num)
                    if n <= 5:
                        if cmd not in CTRLS :
                            cmd = cmd.replace('x'+num,'',1)
                            if cmd in BINDS :
                                return True
                        else :
                            return False        
            #SINGLE COMMANDS_______________________________________________________________________________
            if cmd[:1][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in BINDS:
                    return True
            if cmd[:1][0] == 'n' :
                cmd = cmd.replace('n','',1)
                if cmd in BINDS:
                    return True
            #TOGGLE COMMANDS_______________________________________________________________________________
            if cmd[-1:][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in TOGG :
                    return True
        else :
            return False
    except:
        return False
    
def updateVote():
    global draw,dvotes,listVotes,dcmd
    dvotes = Counter(draw).most_common()
    for key,v in dvotes:
        dcmd = key
        break
    listVotes.delete(0, END)
    top10 = 0
    for key,v in dvotes:
        top10+=1
        if top10 < 11 :
            listVotes.insert(END,'%2s' %  str(v) + ':' + key)
        else:
            break

def checkDemo():
    global CTRL
    global dcntr,dcmd,draw
    global DS,PAUSED
    global CON
    max = CTRL[3][3]
    if dcntr >= max :
        if PAUSED :
            DS.resume()
            sleep(0.1)
            PAUSED = False
        Focus(0)
        ProcessCmd("Demo",dcmd,True)
        if not PAUSED:
           DS.suspend()
           PAUSED = True 
        CON.privmsg("#twitchplaysdark","--------------------------")
        CON.privmsg("#twitchplaysdark","-----Too late to vote-----")
        CON.privmsg("#twitchplaysdark","--------------------------")
        dcntr = 0
        draw = []
        dcmd = 'linger'

def deathCnt():
    sleep(0.99)
    global PAUSED
    global deaths,level
    #tmp = str(hex(dc.GetPixel( 265,150)))
    hp = readStat(0x137D8B8, 0x2cc)
    if hp == 0 :
        if PAUSED :
            DS.resume()
    deaths.set(readStat(0x1378700, 0x5c))
    level.set(readStat(0x137D8B8, 0x208))
    #print(threading.activeCount())
    #threading.Timer(1, deathCnt).start()
    global TP
    TP.submit(deathCnt)

def main():   
    global CTRLS,BINDS,TOGG,CTRL
    global listChat,listCmds,listVotes,deaths,level
    global progTime
    clear = lambda: os.system('cls')
    clear()
    
    bk = '#000000'
    fg = '#FF6600'
    rd = '#FF0000'
    gn = '#00FF00'
    ft = "LucidaConsole 10 bold"
    ftb = "LucidaConsole 20 bold"
    window = Tk()
    window.title("GUI")
    window.geometry("350x750")
    window.configure(bg=bk)
    window.bind('`',Focus)
    
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor =bk)
    s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', troughcolor =bk)
    s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow', troughcolor =bk)
    
    Label(window, text="",font=ft, bg=bk,fg=fg).pack()
    
    fbars = Frame(window, bg=bk)
    fbars.pack()
    for x in range(1,4):
        tmp = CTRL[x]
        Label(fbars, text="",font=ft, bg=bk,fg=fg).pack()
        Label(fbars, text=tmp[5],font=ft, bg=bk,fg=fg).pack()
        tmp[4] = ttk.Progressbar(fbars, style="green.Horizontal.TProgressbar", orient='horizontal', mode='determinate',length=218,value=tmp[3],maximum=tmp[2])
        tmp[4].pack()
    Label(fbars, text="",font=ft, bg=bk,fg=fg).pack()
    
    fboxes = Frame(window, bg=bk)
    fboxes.pack()
    
    fcmdsvotes = Frame(fboxes, bg=bk)
    fcmdsvotes.pack()
    progTime = ttk.Progressbar(fcmdsvotes, style="red.Horizontal.TProgressbar", orient='vertical', mode='determinate',length=174,value=0,maximum=60)
    progTime.pack(side="left")
    listVotes = Listbox(fcmdsvotes,height=10, width=10, font=ft, bg=bk,fg=fg)
    for x in range(0,10):
        listVotes.insert(END,'')
    listVotes.pack(side="left")
    listCmds = Listbox(fcmdsvotes,height=10, width=20, font=ft, bg=bk,fg=fg)
    for x in range(0,10):
        listCmds.insert(END,'')
    listCmds.pack(side="left")
    
    Label(fboxes, text="",font=ft, bg=bk,fg=fg).pack()
    listChat = Listbox(fboxes,height=5, width=30, font=ft, bg=bk,fg=fg)
    for x in range(0,5):
        listChat.insert(END,'')
    listChat.pack()
    
    deaths = StringVar()
    fDeaths = Frame(window, bg=bk)
    fDeaths.pack()
    Label(fDeaths, text="",font=ft, bg=bk,fg=fg).pack()
    Label(fDeaths, text="Deaths:",font=ftb, bg=bk,fg=fg).pack(side="left")
    Label(fDeaths, textvariable=deaths,font=ftb, bg=bk,fg=fg).pack(side="left")
    
    level = StringVar()
    fLevel = Frame(window, bg=bk)
    fLevel.pack()
    Label(fLevel, text="",font=ft, bg=bk,fg=fg).pack()
    Label(fLevel, text="Level:",font=ftb, bg=bk,fg=fg).pack(side="left")
    Label(fLevel, textvariable=level,font=ftb, bg=bk,fg=fg).pack(side="left")
    
    #START THREADS______________________________________________________________________________________________
    global TP
    TP.submit(StartBot)
    TP.submit(deathCnt)
    TP.submit(dCnt)
    
    
    window.mainloop()
    
if __name__ == "__main__":
    main()  
