from ..utility import *

def handle(data, theme):
    if 'pull_request' in data['issue']:
        type = 'pull request'
    else:
        type = 'issue'

    milestone = ''
    if configValue("showMilestone") and 'milestone' in data['issue'] and data['issue']['milestone']:
        milestone = data['issue']['milestone']['title']

    assignee = ''
    if 'assignee' in data['issue'] and data['issue']['assignee']:
        assignee = data['issue']['assignee']['login']

    theme.issue(
        actor = data['comment']['user']['login'],
        action = 'commented on',
        comment = data['comment']['body'],
        issueNo = data['issue']['number'],
        issueTitle = data['issue']['title'],
        creator = data['issue']['user']['login'],
        milestone = milestone,
        url = getShortURL(data['comment']['html_url']),
        assignee = assignee,
        type = type
    )
