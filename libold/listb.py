import tkinter
from tkinter import *
from tkinter import ttk

class Lb (object):
    def __init__(self, rows, length):
        self.rows = rows
        self.length  = length
        
    def createGui(self, root, bg='black',ft="LucidaConsole 10 bold",fg='#FF6600') :
        self.frame = tkinter.Frame(root, bg=bg)
        self.lb = Listbox(self.frame,height=self.rows, width=self.length, font=ft, bg=bg,fg=fg)
        for x in range(0,self.rows):
            self.lb.insert(END,'')
        self.lb.pack()
        return self.frame
        
    def addChat(self, nick, msg):
        self.lb.delete(0)
        self.lb.insert(END, nick[:6] + ': ' + msg[:22])
		
	def add(self, msg):
        self.lb.delete(0)
        self.lb.insert(END, msg)