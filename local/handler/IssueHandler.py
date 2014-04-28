from ..utility import *

def handle(data):
    msgs = []

    url = data['issue']['url']

    if data['issue']['assignee'] and data['sender']['login'] == data['issue']['assignee']['login']:
        senderColor = "green"
    else:
        senderColor = "dark grey"

    creator = ''
    if data['sender']['login'] != data['issue']['user']['login']:
        creator = " by %s" % (ircutils.mircColor(data['issue']['user']['login'],"green"),)

    milestone = ''
    if data['issue']['milestone'] and configValue("showMilestone"):
        milestone = ircutils.mircColor(" (%s" % (data['issue']['milestone']['title']),"brown")

    if milestone:
        oparen = '- '
    else:
        oparen = '('

    msgs.append( "%s: %s %s issue %s \"%s\"%s%s %s%s)" % (
    ircutils.bold(data['repository']['name']),
    ircutils.mircColor(data['sender']['login'], senderColor),
    colorAction(data['action']),
    ''.join(["#",str(data['issue']['number'])]),
    ircutils.bold(data['issue']['title']),
    creator,
    milestone,
    oparen, url
    ))

    return msgs
