from ..utility import *

def handle(data, theme):
    milestone = ''
    if data['issue']['milestone'] and configValue("showMilestone"):
        milestone = data['issue']['milestone']['title']

    assignee = ''
    if 'assignee' in data['issue'] and data['issue']['assignee']:
        assignee = data['issue']['assignee']['login']

    theme.issue(
        repo = data['repository']['name'],
        actor = data['sender']['login'],
        action = data['action'],
        issueNo = data['issue']['number'],
        issueTitle = data['issue']['title'],
        creator = data['issue']['user']['login'],
        milestone = milestone,
        url = getShortURL(data['issue']['url']),
        assignee = assignee
    )
