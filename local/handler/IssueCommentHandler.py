from ..utility import *

def handle(irc, data):
    msgs = []

    url = getShortURL(data['comment']['html_url'])

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

    lines = data['comment']['body'].splitlines()
    line = lines[0]
    if len(line) > 70:
            line = "%s..." % (line[0:67])
    elif len(lines) > 1:
            line += "..."

    msgs.append( "%s: %s commented on issue %s \"%s\"%s%s %s%s): %s" % (
                 ircutils.bold(data['repository']['name']),
                 ircutils.mircColor(data['comment']['user']['login'], "green"),
                 ''.join(["#",str(data['issue']['number'])]),
                 ircutils.bold(data['issue']['title']),
                 creator,
                 milestone,
                 oparen, url,
                 line
    ))

    return msgs
