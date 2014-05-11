from ..utility import *

def handle(data):
    msgs = []

    msgs.append( "%s: The build %s * %s by %s (%s - %s)" % (
        ircutils.bold(data['repository']['name']),
        colorAction(data['status_message'].lower()),
        ircutils.bold(data['commit'][0:6]),
        ircutils.mircColor(data['author_name'], "green"),
        ircutils.mircColor(maxLen(data['message'].splitlines()[0], 50), "dark gray"),
        getShortURL(data['build_url'])
    ))

    return msgs
