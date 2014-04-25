import supybot.ircmsgs as ircmsgs

from ..utility import *

def handle(irc, data, channel):
    msgs = []

    commitno = len(data['commits'])
    ref = data['ref'].split('/',2)
    branch = ref[2]

    colon = ''
    if data['commits']:
        colon = ':'

    isTag = False

    branched = data['created'] or data['deleted'] or ref[1] == "tags"
    branchFrom = ''
    tagFrom = ''

    onlyDeleted = data['deleted'] and not data['created']

    if branched:
        print branch
        if ref[1] == 'tags':
            isTag = True

        urls = ' (%s)' % (getShortURL(data['compare']),)
        if 'base_ref' in data:
            base_ref = data['base_ref'].split('/',2)
            if isTag:
                branchFrom = '%s %s ' % (base_ref[2], ircutils.bold('*'))
            else:
                branchFrom = ' from %s' % (base_ref[2],)

        if data['created'] and data['deleted'] or (not data['created'] and not data['deleted'] and data['forced']):
            if isTag:
                action = "re-tagged"
            else:
                action = "re-created"
        elif data['created'] and not data['forced']:
            if isTag:
                action = "tagged"
            else:
                action = "created"
        elif data['deleted'] and not data['forced']:
            if isTag:
                action = "deleted tag"
            else:
                action = "deleted"
            urls = ''
        elif data['created']:
            if isTag:
                action = "tagged"
            else:
                action = "created"
        elif data['deleted']:
            if isTag:
                action = "deleted tag"
            else:
                action = "deleted"
            urls = ''
        else:
            action = "did something with"


    if configValue("hidePush",None) == False and not branched:
        msgs.append( ircmsgs.privmsg(channel, "%s @ %s: %s pushed %s %s (%s)%s" % (
        ircutils.bold(ircutils.mircColor(branch, "blue")),
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['pusher']['name'], "green"),
        ircutils.bold(str(commitno)),
        plural(commitno, "commit", "commits"),
        getShortURL(data['compare']),
        colon
        )) )
    elif branched:
        if isTag:
            if onlyDeleted:
                commitInfo = ""
            else:
                commitMsg = ""
                if configValue("tagShowCommitMsg"):
                    commitMsg = ircutils.mircColor(" (%s)" % (maxLen(data['head_commit']['message'].splitlines()[0],75)),"brown")
                commitInfo = " %s %s%s as" % (branchFrom, ircutils.bold(data['head_commit']['id'][0:6]), commitMsg)
            msgs.append( ircmsgs.privmsg(channel, "%s: %s %s%s %s%s" % (
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(data['pusher']['name'], "green"),
            colorAction(action),
            commitInfo,
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            urls,
            )) )
        else:
            msgs.append( ircmsgs.privmsg(channel, "%s: %s %s branch %s%s%s%s" % (
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(data['pusher']['name'], "green"),
            colorAction(action),
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            branchFrom,
            urls,
            colon
            )) )

    for commit in data['commits']:
        if 'username' in commit['author']:
            author = commit['author']['username']
        else:
            author = commit['author']['name']

        msgs.append( ircmsgs.privmsg(channel, "%s @ %s: %s * %s (%s)" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(author, "green"),
            ircutils.bold(commit['id'][0:6]),
            getShortURL(commit['url']),
        )) )

        commitlines = commit['message'].splitlines()
        for rawline in commitlines:
            line = maxLen(rawline, 400)
            msgs.append(ircmsgs.privmsg(channel, "%s @ %s: %s" % (
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                ircutils.bold(data['repository']['name']),
                line,
            )) )

    return msgs
