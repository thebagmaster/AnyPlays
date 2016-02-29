import irc.bot					#IRC
import irc.strings				#
import tkinter					#GUI imports
from tkinter import *			#
from tkinter import ttk			#
from concurrent.futures 
	import ThreadPoolExecutor	#Threaded Input
import config					#Read In Config
import re 						#Regex for sanity
import demo						#demo functionality

#init Thread Pool
TP = ThreadPoolExecutor(max_workers=64)

#init GUI
clear = lambda: os.system('cls')
clear()
root = Tk()
root.title("GUI")
root.configure(bg='black')

for m in config.MODES:
	m.createGui(root).grid(row=m.grid[0],
							column=m.grid[1], 
							padx=m.pad[0], 
							pady=m.pad[1])

if config.ENABLE_DEMO:
	config.DEMO = demo.Demo(config.MODES[config.DEMOI],config.VOTESIZE)
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
		
TP.submit(StartBot)
TP.submit(root.mainloop)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
#Bot Start Func
def StartBot():
    bot = Bot(config.IRC_CHANNEL, config.IRC_NICK, config.IRC_SERVER, config.IRC_PORT)
    bot.start()

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, config.IRC_OAUTH)], nickname, nickname, reconnection_interval=config.IRC_RECON)
        self.channel = channel

    def on_welcome(self, c, e):
        config.CON = self.connection
        c.join(self.channel)

    def on_pubmsg(self, c, e) :
        nick = self.Sanitize(e.source.nick)
        cmd = self.Sanitize(e.arguments[0])
        cmds = cmd.split()
        
        if len(cmds) > 1 :
            config.LB_CHAT.addChat(nick,cmd)
        elif cmds[0] and nick :
			if cmds[0] in config.COMMANDS
				if config.ENABLE_DEMO and config.DEMO.mode.switch:
					config.DEMO.votesraw.append(cmds[0])
                    config.DEMO.updateVotes()
				else:
					config.CMDS[cmds[0]].execute()
			else:
				config.LB_CHAT.addChat(nick,cmd)
	def Sanitize(cmd):
		tmp = re.search(u'[\u0000-\uFFFF]+',cmd)
		if tmp :
			return tmp.group(0)
		else :
			return False