#type:[mode,min,max,current,gui]
import tkinter
from tkinter import *
from tkinter import ttk

import globals

class Modes(object) :
    def __init__(self, modes):
        self.modes = modes
    def process(self, nick, cmd):
        for m in self.modes :
            if m.process(nick,cmd) :
                return True
        return False

class Mode(object) :
    def __init__(self, active, min, max, current, stepup, stepdn, ups, downs):
        self.active = active
        self.min = min
        self.max = max
        self.current = current
        self.guivar = 0
        self.stepup = stepup
        self.stepdn = stepdn
        self.ups = ups
        self.downs = downs
        self.bar = 0
        self.s = 0
    def updateGui(self) :
        self.guivar.set(self.current)
        if (self.current) >= 0.85 * self.max : 
            self.bar["style"] = "green.Horizontal.TProgressbar"
        elif (self.current) >= 0.65 * self.max : 
            self.bar["style"] = "ltgreen.Horizontal.TProgressbar"
        elif (self.current) >= 0.5 * self.max : 
            self.bar["style"] = "yellow.Horizontal.TProgressbar"
        elif (self.current) >= 0.35 * self.max : 
            self.bar["style"] = "orange.Horizontal.TProgressbar"
        else :
            self.bar["style"] = "red.Horizontal.TProgressbar"
    def process(self, nick, cmd) :
        wascmd = False
        if cmd in self.ups :
            globals.LB_CMDS.add(nick,cmd)
            wascmd = True
            if (self.current + self.stepup) <= self.max :
                self.current += self.stepup
                self.updateGui()
        elif cmd in self.downs :
            globals.LB_CMDS.add(nick,cmd)
            wascmd = True
            if (self.current + self.stepdn) >= self.min :
                self.current += self.stepdn
                self.updateGui()
        if wascmd :
            self.active = (self.current >= 0.5 * self.max)
            return True
        else :
            return False

    def createGui(self, root, bg='black',ft="LucidaConsole 10 bold",fg='#FF6600') :
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor =bg)
        self.s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', troughcolor =bg)
        self.s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow', troughcolor =bg)
        self.s.configure("orange.Horizontal.TProgressbar", foreground='#FF6600', background='#FF6600', troughcolor =bg)
        self.s.configure("ltgreen.Horizontal.TProgressbar", foreground='#7FFF00', background='#7FFF00', troughcolor =bg)
        
        self.guivar = IntVar()
        self.guivar.set(self.current)
        
        self.frame = tkinter.Frame(root, bg=bg)
        
        self.innerframe = tkinter.Frame(self.frame, bg=bg)
        Label(self.innerframe,anchor=W, text=self.downs[0].upper(), font=ft, bg=bg,fg=fg, width=13).pack(side=LEFT)
        Label(self.innerframe,anchor=E, text=self.ups[0].upper(), font=ft, bg=bg,fg=fg, width=13).pack(side=LEFT)
        self.innerframe.pack()
        
        self.bar = ttk.Progressbar(self.frame, style="green.Horizontal.TProgressbar", orient='horizontal', \
        mode='determinate',length=218,variable=self.guivar,maximum=self.max)
        
        self.bar.pack(side=TOP)
        
        self.updateGui()
        
        return self.frame