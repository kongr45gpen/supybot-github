import supybot.ircmsgs as ircmsgs

from ..utility import *

def handle(irc, data, channel):
    msgs = []

    msgs.append( ircmsgs.privmsg(channel, "%s: %s - %s (%s)" % (
        ircutils.bold(data['repository']['name']),
        colorAction(data['state']),
        data['description'],
        data['target_url']
    )) )

    return msgs
