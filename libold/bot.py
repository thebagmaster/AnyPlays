import irc.bot
import irc.strings

from time import sleep

import re

import globals

def StartBot():
    bot = Bot(globals.IRC_CHANNEL, globals.IRC_NICK, globals.IRC_SERVER, globals.IRC_PORT)
    bot.start()

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, globals.IRC_OAUTH)], nickname, nickname, reconnection_interval=globals.IRC_RECON)
        self.channel = channel

    def on_welcome(self, c, e):
        globals.CON = self.connection
        c.join(self.channel)

    def on_pubmsg(self, c, e) :
        nick = Sanitize(e.source.nick)
        cmd = Sanitize(e.arguments[0])
        cmds = cmd.split()
        
        if len(cmds) > 1 :
            globals.LB_CHAT.add(nick,cmd)
        elif cmds[0] and nick :
            if not globals.MODES.process(nick,cmds[0]) :
                if globals.M_DEMO.active and globals.CMD.isCmd(cmds[0]):
                    globals.DEMO.votesraw.append(cmds[0])
                    globals.DEMO.updateVotes()
                else :
                    globals.TP.submit(globals.CMD.process,nick,cmds[0])
def Sanitize(cmd):
    tmp = re.search(u'[\u0000-\uFFFF]+',cmd)
    if tmp :
        return tmp.group(0)
    else :
        return False