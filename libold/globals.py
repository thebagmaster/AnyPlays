import key
import mem  
import bot
import mode
import listb
import game
import cmds
import demo

from concurrent.futures import ThreadPoolExecutor
def init():
    global TP
    TP = ThreadPoolExecutor(max_workers=10)
    
    global NAME, PNAME, GAME, PAUSE
    NAME = 'Fallout3'
    PNAME = 'Fallout3.exe'
    GAME = game.Game(PNAME)
    PAUSE = True
    
    global CMD,MAXMULT
    CMD = cmds.CmdProc()
    MAXMULT = 5
    
    global M_DEMO,M_MENU,M_DELAY,M_PAUSES
    M_DEMO = mode.Mode(True,0,100,65,1,-1,['order','demo','democracy'],['chaos','anarchy'])
    M_MENU = mode.Mode(False,0,100,45,1,-1,['banm','banmenu','bm','bmnu'],['unbanm','unbanmenu','unbm','unbmnu'])
    M_DELAY = mode.Mode(True,30,60,30,0.5,-0.5,['delayup','dlyup','dup'],['delaydn','dlydn','dlydown','delaydown','ddn','ddown'])
    M_PAUSES = mode.Mode(False,0,100,25,1,-1,['pause'],['nopause'])
    
    global MODES
    MODES = mode.Modes([M_DEMO,M_MENU,M_DELAY,M_PAUSES])
    
    global LB_CHAT,LB_CMDS,LB_VOTE
    LB_CHAT=listb.Lb(10,30)
    LB_CMDS=listb.Lb(10,20)
    LB_VOTE=listb.Lb(6,10)
    
    global DEMO
    DEMO = demo.Demo(M_DELAY,LB_VOTE)

    global ST_HP,ST_LVL,ST_DEATHS
    ST_HP=mem.Stat('Health',0x137D8B8,0x2cc)
    ST_LVL=mem.Stat('Level',0x137D8B8,0x208)
    ST_DEATHS=mem.Stat('Deaths',0x1378700,0x5c)
    
    global STATS
    STATS = mem.Stats([ST_HP,ST_LVL,ST_DEATHS])
    
    global CON
    CON=0
    
    global IRC_SERVER,IRC_PORT,IRC_CHANNEL,IRC_NICK,IRC_OAUTH,IRC_RECON
    IRC_SERVER = "irc.twitch.tv"
    IRC_PORT = 6667
    IRC_CHANNEL = "#twitchplaysfallouts"
    IRC_NICK = "TP_Fallout_Mod"
    IRC_OAUTH = "oauth:v505nbpf3ntf4451o5h0le1qqmrbmy"
    IRC_RECON = 1
    
