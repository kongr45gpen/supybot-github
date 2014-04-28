from ..utility import *

def handle(data):
    msgs = []

    commitno = len(data['commits'])
    ref = data['ref'].split('/',2)
    branch = ref[2]

    colon = ''
    if data['commits']:
        colon = ':'

    isTag = False
    isMerge = False

    branched = data['created'] or data['deleted'] or ref[1] == "tags" or 'base_ref' in data
    branchFrom = ''
    tagFrom = ''

    onlyDeleted = data['deleted'] and not data['created']

    if branched:
        if ref[1] == 'tags':
            isTag = True

        urls = ' (%s)' % (getShortURL(data['compare']),)
        if 'base_ref' in data:
            base_ref = data['base_ref'].split('/',2)
            baseBranch = base_ref[2]
            if isTag:
                branchFrom = '%s %s ' % (baseBranch, ircutils.bold('*'))
            else:
                branchFrom = ' from %s' % (ircutils.bold(ircutils.mircColor(baseBranch, "blue")), )

        if (data['created'] and data['deleted']) or (not data['created'] and not data['deleted'] and data['forced']):
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
            action = "merged"
            mergedCommitCount = sum(not commit['distinct'] for commit in data['commits'])
            regularCommitCount = len(data['commits']) - mergedCommitCount
            isMerge = True

    if configValue("hidePush",None) == False and not branched:
        msgs.append( "%s @ %s: %s pushed %s %s (%s)%s" % (
        ircutils.bold(ircutils.mircColor(branch, "blue")),
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['pusher']['name'], "green"),
        ircutils.bold(str(commitno)),
        plural(commitno, "commit", "commits"),
        getShortURL(data['compare']),
        colon
        ))
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
        elif isMerge:
            distinctMessage = ""
            if configValue("hidePush",None) == False and regularCommitCount > 0:
                distinctMessage = " and %s %s %s" % ( colorAction("pushed"), regularCommitCount, plural(regularCommitCount, 'commit', 'commits'))

            msgs.append( "%s: %s %s %s %s%s%s into %s%s" % (
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(data['pusher']['name'], "green"),
                colorAction(action),
                mergedCommitCount,
                plural(mergedCommitCount, 'commit', 'commits'),
                branchFrom,
                distinctMessage,
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                urls
            ))
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

        commitBranch = branch

        if not commit['distinct'] and not configValue('showMergedCommits'):
            continue

        if isMerge and not commit['distinct']:
            commitBranch = "%s -> %s" % ( baseBranch, branch )

        msgs.append("%s @ %s: %s * %s (%s)" % (
            ircutils.bold(ircutils.mircColor(commitBranch, "blue")),
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(author, "green"),
            ircutils.bold(commit['id'][0:6]),
            getShortURL(commit['url']),
        ))

        commitlines = commit['message'].splitlines()
        for rawline in commitlines:
            line = maxLen(rawline, 400)
            msgs.append( "%s @ %s: %s" % (
                ircutils.bold(ircutils.mircColor(commitBranch, "blue")),
                ircutils.bold(data['repository']['name']),
                line,
            ))

    return msgs
