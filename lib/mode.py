import Tkinter
from Tkinter import *
import ttk

class Mode:
    def __init__(self,name,loname,hiname,posswitch,negswitch,max,min,init,width,grid=[0,0],pad=[5,5]):
        self.switch = True
        self.name = name
        self.loname = loname
        self.hiname = hiname
        self.pos = posswitch
        self.neg = negswitch
        self.max = max
        self.min = min
        self.value = init
        self.grid = grid
        self.pad = pad
        self.width = width
        self.mid = ((abs(max)+abs(min))//2)+min
        self.guivar = 0
        
    def update(self,change=0):
        if change != 0:
            self.value += change
        if self.value >= self.pos:
            self.switch = True
        if self.value < self.neg:
            self.switch = False
        if self.value > max:
            self.value = max
        if self.value < min:
            self.value = min
        self.updateGui()
            
    def updateGui(self) :
        self.guivar.set(self.value)
        if (self.value) >= self.pos : 
            self.bar["style"] = "green.Horizontal.TProgressbar"
        elif (self.value) >= self.mid : 
            self.bar["style"] = "ltgreen.Horizontal.TProgressbar"
        elif (self.value) >= self.neg : 
            self.bar["style"] = "orange.Horizontal.TProgressbar"
        else :
            self.bar["style"] = "red.Horizontal.TProgressbar"

    def createGui(self, root, bg='black',ft="LucidaConsole 10 bold",fg='#FF6600') :
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure("red.Horizontal.TProgressbar", foreground='red', background='red', troughcolor =bg)
        self.s.configure("green.Horizontal.TProgressbar", foreground='green', background='green', troughcolor =bg)
        self.s.configure("orange.Horizontal.TProgressbar", foreground='#FF6600', background='#FF6600', troughcolor =bg)
        self.s.configure("ltgreen.Horizontal.TProgressbar", foreground='#7FFF00', background='#7FFF00', troughcolor =bg)
        
        self.guivar = IntVar()
        self.guivar.set(self.value)
        
        self.frame = Tkinter.Frame(root, bg=bg)
        
        self.innerframe = Tkinter.Frame(self.frame, bg=bg)
        Label(self.innerframe,anchor=W, text=self.loname.upper(), font=ft, bg=bg,fg=fg, width=13).pack(side=LEFT)
        Label(self.innerframe,anchor=E, text=self.hiname.upper(), font=ft, bg=bg,fg=fg, width=13).pack(side=LEFT)
        self.innerframe.pack()
        
        self.bar = ttk.Progressbar(self.frame, style="green.Horizontal.TProgressbar", orient='horizontal', \
        mode='determinate',length=self.width,variable=self.guivar,maximum=self.max)
        
        self.bar.pack(side=TOP)
        
        self.updateGui()
        
        return self.frame