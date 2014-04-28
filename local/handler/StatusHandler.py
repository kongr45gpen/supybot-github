from ..utility import *

def handle(data):
    msgs = []

    msgs.append( "%s: %s - %s (%s)" % (
        ircutils.bold(data['repository']['name']),
        colorAction(data['state']),
        data['description'],
        data['target_url']
    ))

    return msgs
