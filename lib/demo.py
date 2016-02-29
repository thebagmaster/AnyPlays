# -*- coding: utf-8 -*-
import Tkinter
from Tkinter import *
import ttk
from collections import defaultdict
from collections import Counter

from time import sleep

from listb import *

class Demo(object):
    quit=False
    def __init__(self, mode, voteboxsize, TP, channel, CON, COMMANDS, paused=[False],pause=[0],resume=[0]):
        self.mode = mode
        self.listb = Lb(voteboxsize[0],voteboxsize[1])
        self.current = 0
        self.votesraw = []
        self.topcmd = 'linger'
        self.max = 30
        self.guivar = 0
        self.TP=TP
        self.CON=CON
        self.COMMANDS=COMMANDS
        self.channel=channel
        self.paused=paused
        self.pause=pause
        self.resume=resume
        
    def createGui(self,root,bg='black',ft="LucidaConsole 10 bold",fg='#FF6600'):
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor =bg)
        self.s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', troughcolor =bg)
        self.s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow', troughcolor =bg)
        self.s.configure("orange.Horizontal.TProgressbar", foreground='#FF6600', background='#FF6600', troughcolor =bg)
        self.s.configure("ltgreen.Horizontal.TProgressbar", foreground='#7FFF00', background='#7FFF00', troughcolor =bg)
        
        self.frame = Tkinter.Frame(root, bg=bg)
        
        self.mode.createGui(self.frame).pack()
        
        self.guivar = IntVar()
        self.guivar.set(self.current)
        
        self.innerframe = Tkinter.Frame(self.frame, bg=bg)
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
            if self.paused[0] :
                self.resume[0]()
        else :
            self.current = 0
            self.votesraw = []
            self.listb.lb.delete(0, END)
            
        self.updateGui()
        self.checkIfTimed()
        if not self.quit:
            self.TP.submit(self.count)
        
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
            if self.paused[0] :
                self.resume[0]()
            self.current = 0
            sleep(0.05)
            self.COMMANDS[self.topcmd].execute()
            sleep(0.05)
            if self.paused[0] :
                self.pause[0]()
            self.CON[0].privmsg(self.channel,"╚═ Too late to vote Kappa ═╝")
            self.current = 0
            self.guivar.set(self.current)
            self.votesraw = []
            self.topcmd = 'linger'
        
        