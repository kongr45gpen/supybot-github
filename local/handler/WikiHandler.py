from ..utility import *

def handle(data):
    msgs = []

    pageno = len(data['pages'])

    url = getShortURL("%s/wiki/_compare/%s" % ( data['repository']['html_url'], data['pages'][0]['sha'] ))

    if configValue("hidePush",None) is False:
        msgs.append( ircmsgs.privmsg(channel, "%s: %s modified %s wiki %s (%s):" % (
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['sender']['login'], "green"),
        ircutils.bold(str(pageno)),
        plural(pageno, "page", "pages"),
        url
        )) )

    urlShown = False;

    for page in data['pages']:
        if configValue("hidePush") and urlShown is False:
            pageurl = "(%s)" % (url,)
            urlShown = True
        elif configValue("hidePush"):
            pageurl = ""
        else:
            pageurl = "(%s)" % (page['html_url'],)

        # Unfortunately github doesn't support edit summaries :(
        msgs.append( "%s: %s %s %s * %s %s" % (
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(data['sender']['login'], "green"),
            colorAction(page['action']),
            ircutils.bold(ircutils.mircColor(page['page_name'], "blue")),
            ircutils.bold(page['sha'][0:6]),
            pageurl,
        ))

    return msgs
