import emu
from time import sleep

class ModeAction:
    def __init__(self,index,step):
        self.index = index
        self.step = step
    def execute(self):
        config.MODES[index].update(self.step)

class JoyAction:
    def __init__(self,index,button,pause,isbutton=True,axis=0,apos=0,hat=0,hpos=0):
        self.button = button
        self.isbutton = isbutton
        self.index = index
        if apos == 0 :
            self.amove=False
        else:
            self.amove=True
            self.axis = axis
            self.apos = apos
        if hpos == 0 :
            self.hmove=False
        else:
            self.hmove=True
            self.hat = hat
            self.hpos = hpos
        self.pause = pause
    def execute(self,press=True,release=True):
        if self.isbutton:
            if press:
                self.pause.sleepbefore()                #down
                emu.JoystickPress(self.index,self.button,1)
                self.pause.sleepduring()
            if release:                                    #up
                emu.JoystickPress(self.index,self.button,0)
                self.pause.sleepafter()
        else:
            if press:
                self.pause.sleepbefore()
                if self.amove:
                    emu.JoystickAxis(self.index,self.axis,self.apos)
                if self.hmove:
                    emu.JoystickPOV(self.index,self.hat,self.hpos)
                self.pause.sleepduring()
            if release:
                self.pause.sleepafter()

class MouseAction:
    def __init__(self,dx,dy,button,pause):
        self.button = button
        self.pause = pause
        if dx == 0 and dy == 0:
            self.move=False
        else:
            self.move=True
            self.dx = dx
            self.dy = dy
    def execute(self,press=True,release=True):
        if press:
            self.pause.sleepbefore()
            if self.move:
                emu.MoveMouseDelay(self.dx,self.dy,self.pause.delay)
            else:
                emu.ClickMouse(self.button + 'BUTTOND')
                self.pause.sleepduring()
        if release:
            if not self.move:
                emu.ClickMouse(self.button + 'BUTTONU')
            self.pause.sleepafter()

class KeyAction:
    def __init__(self,key,pause):
        self.key = key
        self.pause = pause
    def execute(self,press=True,release=True):
        if press:
            self.pause.sleepbefore()
            emu.KeyStroke(self.key)
            self.pause.sleepduring()
        if release:
            emu.KeyStroke(self.key,False)
            self.pause.sleepafter()

class Combo:
    def __init__(self,actions,serial=True):
        self.actions = actions
        self.serial = serial
    def execute(self):
        if self.serial :
            for action in self.actions:
                action.execute()
        else:
            for action in self.actions:
                action.execute(True,False)
            for action in self.actions:
                action.execute(False,True)

class Axis:
    X, Y, Z, Rx, Ry, Rz, Sl1, Sl2 = range(8)

class Pause:
    def __init__(self,before=10,during=50,after=10):
        self.before = before/1000
        self.during = during/1000
        self.after = after/1000
    def sleepbefore(self):
        sleep(self.before)
    def sleepduring(self):
        sleep(self.during)
    def sleepafter(self):
        sleep(self.after)

class Command:
    def __init__(self,combo,banned=False,admin=False):
        self.combo = combo
        self.banned = banned
        self.admin = admin
    def execute(self):
        self.combo.execute()