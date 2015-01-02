from ..utility import *

def handle(data, theme):
    commitno = len(data['commits'])
    ref = data['ref'].split('/',2)
    branch = ref[2]

    isTag = False
    isMerge = False

    branched = data['created'] or data['deleted'] or ref[1] == "tags" or ('base_ref' in data and data['base_ref'])
    branchFrom = ''
    tagFrom = ''

    onlyDeleted = data['deleted'] and not data['created']

    if branched:
        if ref[1] == 'tags':
            isTag = True

        urls = getShortURL(data['compare'])
        if 'base_ref' in data:
            base_ref = data['base_ref'].split('/',2)
            baseBranch = base_ref[2]
            branchFrom = baseBranch

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
        theme.push(
            repo = data['repository']['name'],
            branch = branch,
            actor = data['pusher']['name'],
            url = getShortURL(data['compare']),
            count = commitno
        )
    elif branched:
        if isTag:
            theme.tag(
                repo = data['repository']['name'],
                actor = data['pusher']['name'],
                action = action,
                base = branchFrom,
                to = branch,
                onlyDeleted = onlyDeleted,
                headMsg = data['head_commit']['message'],
                headId = data['head_commit']['id'],
                url = urls
            )
        elif isMerge:
            theme.merge(
                repo = data['repository']['name'],
                actor = data['pusher']['name'],
                action = action,
                mergeCount = mergedCommitCount,
                regularCount = regularCommitCount,
                base = branchFrom,
                to = branch,
                url = urls
            )
        else:
            theme.branch(
                repo = data['repository']['name'],
                actor = data['pusher']['name'],
                action = action,
                count = commitno,
                base = branchFrom,
                to = branch,
                url = urls
            )

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

        theme.commit(
            branch = commitBranch,
            repo = data['repository']['name'],
            author = author,
            id = commit['id'],
            message = commit['message'],
            url = getShortURL(commit['url'])
        )