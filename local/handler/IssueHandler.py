from ..utility import *

def handle(data, theme):
    if 'issue' in data:
        issue = data['issue']
        type = 'issue'
    elif 'pull_request' in data:
        issue = data['pull_request']
        type = 'pull request'
    else:
        type = 'something'

    if data['action'] == 'edited' and not configValue("showIssueEdits"):
        return

    milestone = ''
    if issue['milestone'] and configValue("showMilestone"):
        milestone = issue['milestone']['title']

    assignee = ''
    if 'assignee' in data and data['assignee']:
        assignee = data['assignee']['login']
    elif 'assignee' in issue and issue['assignee']:
        assignee = issue['assignee']['login']

    labelName = None
    labelColor = None
    if 'label' in data and data['label']:
        labelName = data['label']['name']
        labelColor = data['label']['color']

    theme.issue(
        actor = data['sender']['login'],
        action = data['action'],
        issueNo = issue['number'],
        issueTitle = issue['title'],
        creator = issue['user']['login'],
        milestone = milestone,
        url = getShortURL(issue['html_url']),
        assignee = assignee,
        labelName = labelName,
        labelColor = labelColor,
        type = type
    )
