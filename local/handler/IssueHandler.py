from ..utility import *

def handle(data, theme):
    milestone = ''
    if data['issue']['milestone'] and configValue("showMilestone"):
        milestone = data['issue']['milestone']['title']

    assignee = ''
    if 'assignee' in data and data['assignee']:
        assignee = data['assignee']['login']
    elif 'assignee' in data['issue'] and data['issue']['assignee']:
        assignee = data['issue']['assignee']['login']

    labelName = None
    labelColor = None
    if 'label' in data and data['label']:
        labelName = data['label']['name']
        labelColor = data['label']['color']

    theme.issue(
        actor = data['sender']['login'],
        action = data['action'],
        issueNo = data['issue']['number'],
        issueTitle = data['issue']['title'],
        creator = data['issue']['user']['login'],
        milestone = milestone,
        url = getShortURL(data['issue']['html_url']),
        assignee = assignee,
        labelName = labelName,
        labelColor = labelColor
    )
