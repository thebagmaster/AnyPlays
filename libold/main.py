#! /usr/bin/env python

import os

import tkinter
from tkinter import *
from tkinter import ttk

import globals


def main(): 
    globals.init()
    
    clear = lambda: os.system('cls')
    clear()
    root = Tk()
    root.title("GUI")
    root.configure(bg='black')
    
    padx = 5
    pady = 5
    globals.M_DEMO.createGui(root).grid(row=0,column=0, padx=padx, pady=pady)
    globals.M_MENU.createGui(root).grid(row=1,column=0, padx=padx, pady=pady)
    globals.M_PAUSES.createGui(root).grid(row=2,column=0, padx=padx, pady=pady)
    
    globals.DEMO.createGui(root).grid(row=3,column=0, padx=padx, pady=pady)
    
    globals.LB_CHAT.createGui(root).grid(row=5,column=0, padx=padx, pady=pady)
    globals.LB_CMDS.createGui(root).grid(row=4,column=0, padx=padx, pady=pady)
    
    #globals.ST_HP.createGui(root).grid(row=6,column=0, padx=padx, pady=pady)
    #globals.ST_LVL.createGui(root).grid(row=7,column=0, padx=padx, pady=pady)
    #globals.ST_DEATHS.createGui(root).grid(row=8,column=0, padx=padx, pady=pady)
    
    globals.TP.submit(globals.bot.StartBot)
    globals.TP.submit(globals.DEMO.count)
    #globals.TP.submit(globals.STATS.update)
    
    root.mainloop()
    
    globals.TP.shutdown(wait=True)

if __name__ == "__main__":
    main() 