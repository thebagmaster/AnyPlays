from time import sleep

import globals
import key
import pyautogui

class CmdProc(object) :
    def __init__(self):
        self.KBINDS = {
        'm':      KeyBind('TAB'),
        'aru':    KeyBind('UP'),
        'arr':    KeyBind('RIGHT'),
        'ard':    KeyBind('DOWN'),
        'arl':    KeyBind('LEFT'),
        'bs':     KeyBind('BACK'),
        
        'f':      KeyBind('W',0.6,0,True),
        'l':      KeyBind('A',0.6),
        'r':      KeyBind('D',0.6),
        'b':      KeyBind('S',0.6),
        'j':      KeyBind('SPACE'),
        
        'fr':     KeyCombo([KeyBind('W',0),KeyBind('D',0.6)]),
        'fl':     KeyCombo([KeyBind('W',0),KeyBind('A',0.6)]),
        'br':     KeyCombo([KeyBind('S',0),KeyBind('D',0.6)]),
        'bl':     KeyCombo([KeyBind('S',0),KeyBind('A',0.6)]),
        
        'wait':   KeyBind('T'),
        'hold':   KeyBind('',0.8),
        'linger': KeyBind('',2),
        
        'e':      KeyBind('E'),
        'enter':  KeyBind('RETURN'),
        'v':      KeyBind('V'),
        'grab':   KeyBind('Z'),
        
        #'save':   KeyBind('F5'),
        #'load':   KeyBind('F9'),
        
        'stats':  KeyBind('F1'),
        'items':  KeyBind('F2'),
        'data':   KeyBind('F3'),
        'lite':   KeyBind('TAB',2),
        
        'fire':   KeyBind('NUMPAD1'),
        'reload': KeyBind('R'),
        'block':  KeyBind('LMENU',0.05,0,True),
        
        'sneak':  KeyBind('LCONTROL',0.05,0,True),
        'run':    KeyCombo([KeyBind('W',0),KeyBind('LSHIFT',1.6)]),
        
        'll': MouseBind(-0.5,0),
        'lr': MouseBind(0.5,0),
        'lu': MouseBind(0,-0.5),
        'ld': MouseBind(0,0.5),
        
        'lll': MouseBind(-8,0),
        'lrl': MouseBind(8,0),
        'lul': MouseBind(0,-8),
        'ldl': MouseBind(0,8),
        
        'click': MouseBind(0,0,True)
        }
    def process(self,nick,cmd,multiplier=False) :
        target = True
        if len(cmd) > 1: 
            #MULTI#
            if len(cmd) >= 3 and not multiplier:
                num = cmd[-2:][1]
                if (cmd[-2:][0] == 'x') and num.isdigit():
                    n = int(num)
                    if n <= globals.MAXMULT:
                        cmd = cmd.replace('x'+num,'')
                        for x in range(1,n+1):
                            globals.CMD.process(nick,cmd,True)
                            sleep(.2)
                            #globals.TP.submit(self.process,nick,cmd,True)
                        return
                        
            #TARGET OR NAWW PREFIX#
            if cmd[:1][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in self.KBINDS:
                    sleep(0.05)
                    KeyBind('C').execute()
                    target=False
            if cmd[:1][0] == 'n' :
                cmd = cmd.replace('n','',1)
                if cmd in self.KBINDS:
                    target=False
                 
        #FINALLY EXECUTING COMMAND#
        if cmd in self.KBINDS and not (cmd == 'm' and globals.M_MENU.active):
            self.KBINDS[cmd].execute()
            if target :
                sleep(0.05)
                KeyBind('Z').execute()
            globals.LB_CMDS.add(nick,cmd)
        elif not multiplier:
            globals.LB_CHAT.add(nick,cmd)
            
    def isCmd(self, cmd):
        if len(cmd) > 1: 
            #MULTI#
            if len(cmd) >= 3 :
                num = cmd[-2:][1]
                if (cmd[-2:][0] == 'x') and num.isdigit():
                    n = int(num)
                    if n <= globals.MAXMULT:
                        cmd = cmd.replace('x'+num,'')
                        return self.isCmd(cmd)
                        
            #TARGET OR NAWW PREFIX#
            if cmd[:1][0] == 't' :
                cmd = cmd.replace('t','')
                if cmd in self.KBINDS:
                    return True
            if cmd[:1][0] == 'n' :
                cmd = cmd.replace('n','',1)
                if cmd in self.KBINDS:
                    return True

        if cmd in self.KBINDS :
            return True

class MouseBind() :
    def __init__(self, x, y, click=False):
        self.x = x
        self.y = y
        self.click = click
    def execute(self):
        key.MoveMouse(self.x,self.y,self.click)
                
class KeyBind() :
    def __init__(self, code, press=0.1, release=0.1, toggleable=False):
        self.code = code.lower()
        self.press=press
        self.release=release
        self.toggleable=toggleable
        self.down = False
        
    def execute(self, toggle=False):
        if self.toggleable and toggle and not self.down :
            key.PressKey(self.code)
            #pyautogui.keyDown(self.code)
            sleep(self.press)
            self.down = True
        elif self.toggleable and toggle and self.down :
            key.ReleaseKey(self.code)
            #pyautogui.keyUp(self.code)
            sleep(self.release)
            self.down = False
        else :
            key.PressKey(self.code)
            #pyautogui.keyDown(self.code)
            sleep(self.press)
            key.ReleaseKey(self.code)
            #pyautogui.keyUp(self.code)
            sleep(self.release)

class KeyCombo() :
    def __init__(self, actions, concurrent=True):
        self.actions = actions
        self.concurrent = concurrent
    def execute(self):
        if self.concurrent :
            for a in self.actions :
                a.toggleable = True
                a.execute(True)
            for a in actions :
                a.execute(True)
        else :
            for a in actions :
                a.execute()
        
