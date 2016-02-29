from lib.mode import *
from lib.cmd import *
from lib import mem
from lib.listb import *
from lib.game import *

#DEBUG
DEBUG=False

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
NAME = 'DARK SOULS'
PNAME = 'DARKSOULS.exe'
GAME = Game(PNAME)

#DEMOCRACY
ENABLE_DEMO = False
DEMO = False
DEMOI = 0
VOTESIZE = [6,20]
VOTEGUI = [[4,0],[5,5]]
PAUSE = False

#LIST BOXES
LB_CHAT=Lb(10,30,[3,0])
LB_CMDS=Lb(10,20,[2,0])

#MODES
MODES = [
    #name,loname,hiname,posswitch,negswitch,max,min,init,width,grid=[0,0],pad=[5,5]
    Mode('Democracy','Demo','Chaos'     ,10,-10,100,-100,0,200,[0,0])
]

#COMMANDS
COMMANDS = {
    'f'    :    Command(Combo([KeyAction('W',Pause())])),
    'b'    :    Command(Combo([KeyAction('S',Pause())])),
    'r'    :    Command(Combo([KeyAction('D',Pause())])),
    'l'    :    Command(Combo([KeyAction('L',Pause())]))
}

#STATS
STATS = [
    mem.Stat('Health',0x7FF77A570000,[0x0,0x8,0x3b8,0x18,0x28,0x30,0x20,0x28,0x0,0x490,0x104])
]

#GUI
GUI_SIZE="230x380"
GUI_BG="black"