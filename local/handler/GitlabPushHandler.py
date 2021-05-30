from ..utility import *

def handle(data, theme):
    commitno = len(data['commits'])
    ref = data['ref'].split('/', 2)
    branch = ref[2]

    pushVisible = configValue("hidePush") == False
    pushUrl = "{}/-/compare/{}...{}".format(
        data['repository']['homepage'],
        data['before'],
        data['after']
    )
    if pushVisible:
        theme.push(
            branch = branch,
            actor = data['user_username'],
            url = getShortURL(pushUrl),
            count = commitno,
            forced = False
        )

    for commit in data['commits']:
        theme.commit(
            branch = branch,
            author = commit['author']['name'],
            id = commit['id'],
            message = commit['message'],
            url = getShortURL(commit['url'])
        )

    return True

