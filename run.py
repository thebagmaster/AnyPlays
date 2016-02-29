import irc.bot                    #IRC
import irc.strings
import Tkinter                    #GUI imports
from Tkinter import *
import ttk
import atexit
from concurrent.futures import ThreadPoolExecutor    #Threaded Input
import config                    #Read In Config
import re                        #Regex for sanity
import lib.demo as demo          #demo functionality
import os
import sys

def main():
    #init irc bot
    global bot
    bot=0
    
    #init Thread Pool
    TP = ThreadPoolExecutor(max_workers=64)

    #init GUI
    clear = lambda: os.system('cls')
    clear()
    root = Tk()
    root.title("GUI")
    root.geometry(config.GUI_SIZE)
    root.configure(bg=config.GUI_BG)
    atexit.register(StopBot)

    for i,m in enumerate(config.MODES):
        if i!=config.DEMOI:
            m.createGui(root).grid(row=m.grid[0],
                                    column=m.grid[1], 
                                    padx=m.pad[0], 
                                    pady=m.pad[1])

    if config.ENABLE_DEMO:
        config.DEMO = demo.Demo(config.MODES[config.DEMOI],config.VOTESIZE,TP,config.IRC_CHANNEL,config.IRC_CON, config.COMMANDS)
        config.DEMO.createGui(root).grid(row=config.VOTEGUI[0][0],
                                        column=config.VOTEGUI[0][1], 
                                        padx=config.VOTEGUI[1][0], 
                                        pady=config.VOTEGUI[1][1])
        TP.submit(config.DEMO.count)

    config.LB_CHAT.createGui(root).grid(row=config.LB_CHAT.grid[0],
                                        column=config.LB_CHAT.grid[1], 
                                        padx=config.LB_CHAT.pad[0], 
                                        pady=config.LB_CHAT.pad[1])
    config.LB_CMDS.createGui(root).grid(row=config.LB_CMDS.grid[0],
                                        column=config.LB_CMDS.grid[1], 
                                        padx=config.LB_CMDS.pad[0], 
                                        pady=config.LB_CMDS.pad[1])
    # if having issues debugging 
    # make bot main thread for error messages
    # StartBot()
    TP.submit(StartBot)
    root.mainloop()
    
#================================Begin Bot Code===================
                                    
def StartBot():
    global bot
    bot = Bot(config.IRC_CHANNEL, config.IRC_NICK, config.IRC_SERVER, config.IRC_PORT)
    bot.start()
    
def StopBot():
    global bot
    if config.ENABLE_DEMO:
        config.DEMO.quit=True
    bot.die("Gui Closed, BRB")
    sys.exit(0)
    

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, config.IRC_OAUTH)], nickname, nickname, reconnection_interval=config.IRC_RECON)
        self.channel = channel
        
    def on_welcome(self, c, e):
        print("Bot Connected")
        config.IRC_CON = [self.connection]
        c.join(self.channel)
        
    def Sanitize(self, cmd):
        tmp = re.search(u'[\u0000-\uFFFF]+',cmd)
        if tmp :
            return tmp.group(0)
        else :
            return " "
        
    def on_pubmsg(self, c, e) :
        if config.DEBUG:
            print("Message Recieved From "+e.source.nick+": "+e.arguments[0])
        nick = self.Sanitize(e.source.nick)
        cmd = self.Sanitize(e.arguments[0])
        cmds = cmd.split()
        if len(cmds) > 1 :
            config.LB_CHAT.addChat(nick,cmd)
        elif cmds[0] and nick :
            if cmds[0] in config.COMMANDS:
                if config.ENABLE_DEMO and config.DEMO.mode.switch:
                    config.DEMO.votesraw.append(cmds[0])
                    config.DEMO.updateVotes()
                else:
                    config.COMMANDS[cmds[0]].execute()
                    config.LB_CMDS.addChat(nick,cmd)
            else:
                config.LB_CHAT.addChat(nick,cmd)

if __name__ == "__main__":
    main()  