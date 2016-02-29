from lib.mode import *
from lib.cmd import *
from lib import mem
from lib.listb import *
from lib.game import *

#CON connection object (for sending chat messages)
#RECON reconnection delay (seconds)
#IRC
IRC_CON = 0
IRC_SERVER = "irc.twitch.tv"
IRC_PORT = 6667
IRC_CHANNEL = "#thebagmaster"
IRC_NICK = "TP_Fallout_Mod"
IRC_OAUTH = "oauth:v505nbpf3ntf4451o5h0le1qqmrbmy"
IRC_RECON = 1

#PROCESS INFO
NAME = 'Fallout3'
PNAME = 'Fallout3.exe'
GAME = Game(PNAME)

#DEMOCRACY
ENABLE_DEMO = True
DEMO = False
DEMOI = 0
VOTESIZE = [6,20]
VOTEGUI = [[0,4],[5,5]]
PAUSE = False

#LIST BOXES
LB_CHAT=Lb(10,30,[0,2])
LB_CHAT.setChatParams(6,22)
LB_CMDS=Lb(10,20,[0,3])

#MODES
MODES = [
	Mode('Democracy'	,10,-10,100,-100,0,0,False,200,[0,0]),
	Mode('Pause'		,10,-10,100,-100,0,0,False,200,[0,1])
]

#COMMANDS
CMDS = {
	'forward'	:	Command('f',Combo([KeyAction('W',Pause())]))
}

#STATS
STATS = [
	mem.Stat('Health',0x7FF77A570000,[0x0,0x8,0x3b8,0x18,0x28,0x30,0x20,0x28,0x0,0x490,0x104]),
]