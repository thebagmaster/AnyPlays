import tkinter
from tkinter import *
from tkinter import ttk
from collections import defaultdict
from collections import Counter

from time import sleep

from listb import *

class Demo(object):
    def __init__(self, mode, voteboxsize):
        self.mode = mode
        self.listb = Lb(voteboxsize[0],voteboxsize[1])
        self.current = 0
        self.votesraw = []
        self.topcmd = 'linger'
        self.max = 30
		self.guivar = 0
        
    def createGui(self,root,bg='black',ft="LucidaConsole 10 bold",fg='#FF6600'):
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor =bg)
        self.s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', troughcolor =bg)
        self.s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow', troughcolor =bg)
        self.s.configure("orange.Horizontal.TProgressbar", foreground='#FF6600', background='#FF6600', troughcolor =bg)
        self.s.configure("ltgreen.Horizontal.TProgressbar", foreground='#7FFF00', background='#7FFF00', troughcolor =bg)
        
        self.frame = tkinter.Frame(root, bg=bg)
        
        self.mode.createGui(self.frame).pack()
        
        self.guivar = IntVar()
        self.guivar.set(self.current)
        
        self.innerframe = tkinter.Frame(self.frame, bg=bg)
        self.bar = ttk.Progressbar(self.innerframe, style="green.Horizontal.TProgressbar", orient='vertical', \
        mode='determinate',length=105,variable=self.guivar,maximum=self.max)
        self.bar.pack(side=LEFT)
        
        self.listb.createGui(self.innerframe).pack(side=LEFT)
        self.innerframe.pack(pady=10)
        
        self.updateGui()
        
        return self.frame
        
    def updateGui(self):
        self.bar["maximum"] = self.max
        self.guivar.set(self.current)
        if (self.current) >= 0.85 * self.max : 
            self.bar["style"] = "red.Horizontal.TProgressbar"
        elif (self.current) >= 0.65 * self.max : 
            self.bar["style"] = "orange.Horizontal.TProgressbar"
        elif (self.current) >= 0.5 * self.max : 
            self.bar["style"] = "yellow.Horizontal.TProgressbar"
        elif (self.current) >= 0.35 * self.max : 
            self.bar["style"] = "ltgreen.Horizontal.TProgressbar"
        else :
            self.bar["style"] = "green.Horizontal.TProgressbar"
        
    def count(self) :
        sleep(.99)
        if mode.switch :
            self.current += 1
            if globals.M_PAUSES.active :
                globals.GAME.resume()
        else :
            self.current = 0
            self.votesraw = []
            self.listb.lb.delete(0, END)
            
        self.updateGui()
        self.checkIfTimed()
        globals.TP.submit(globals.DEMO.count)
        
    def updateVotes(self) :
        self.talliedvotes = Counter(self.votesraw).most_common()
        for key,v in self.talliedvotes:
            self.topcmd = key
            break
        
        self.listb.lb.delete(0, END)
        top10 = 0
        for key,v in self.talliedvotes:
            top10+=1
            if top10 <= self.listb.rows :
                self.listb.lb.insert(END,'%2s' %  str(v) + ": " + key)
                self.checkIfTimed()
            else:
                break
    
    def checkIfTimed(self) :
        if self.current >= self.max :
            if globals.M_PAUSES.active :
                globals.GAME.resume()
            self.current = 0
            sleep(0.05)
            globals.CMD.process('Demo',self.topcmd)
            sleep(0.05)
            if globals.M_PAUSES.active :
                globals.GAME.pause()
            globals.CON.privmsg("#twitchplaysfallouts","____________")
            globals.CON.privmsg("#twitchplaysfallouts","____________")
            globals.CON.privmsg("#twitchplaysfallouts","Too late to vote Kappa")
            self.current = 0
            self.guivar.set(self.current)
            self.votesraw = []
            self.topcmd = 'linger'
        
        