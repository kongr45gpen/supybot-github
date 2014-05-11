from ..utility import *

def handle(data):
    msgs = []

    status = data['status_message'].lower()

    if isStatusVisible(data['repository']['url'], status):
        msgs.append( "%s: The build %s * %s by %s (%s - %s)" % (
            ircutils.bold(data['repository']['name']),
            colorAction(status),
            ircutils.bold(data['commit'][0:6]),
            ircutils.mircColor(data['author_name'], "green"),
            ircutils.mircColor(maxLen(data['message'].splitlines()[0], 50), "dark gray"),
            getShortURL(data['build_url'])
        ))

    return msgs
