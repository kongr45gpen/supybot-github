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
        if 'base_ref' in data and data['base_ref'] is not None:
            base_ref = data['base_ref'].split('/',2)
            baseBranch = base_ref[2]
            branchFrom = baseBranch

        if (data['created'] and data['deleted']) or (not data['created'] and not data['deleted'] and data['forced']):
            if isTag:
                action = "re-tagged"
            else:
                action = "re-created"
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

    visible = configValue("hidePush") == False or (configValue("alwaysShowForcedPushes") == True and data['forced'])

    if visible and not branched:
        theme.push(
            branch = branch,
            actor = data['pusher']['name'],
            url = getShortURL(data['compare']),
            count = commitno,
            forced = data['forced']
        )
    elif branched:
        if data['forced']:
            action = "force %s" % (action,)

        if isTag:
            theme.tag(
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
                actor = data['pusher']['name'],
                action = action,
                count = commitno,
                base = branchFrom,
                to = branch,
                url = urls
            )

    def __commit(commit):
        if 'username' in commit['author']:
            author = commit['author']['username']
        else:
            author = commit['author']['name']

        commitBranch = branch

        if not commit['distinct'] and not configValue('showMergedCommits'):
            return False

        if isMerge and not commit['distinct']:
            commitBranch = "%s -> %s" % (baseBranch, branch)

        theme.commit(
            branch=commitBranch,
            author=author,
            id=commit['id'],
            message=commit['message'],
            url=getShortURL(commit['url'])
        )

        return True

    i = 0
    for commit in data['commits']:
        max = configValue('maxCommitCount')
        if max != 0 and len(data['commits']) != max + 1 and i >= max:
            theme.more(
                branch = branch,
                number = len(data['commits']) - i,
                type = "commits"
            )
            break

        if __commit(commit):
            i += 1


