from ..utility import *

def handle(data, theme):
    if isStatusVisible(data['eventData']['projectId'], data['eventData']['status'].lower()):
        theme.travis(
            branch = data['eventData']['branch'],
            repo = data['eventData']['repositoryName'].split('/')[1],
            status = data['eventData']['status'],
            commitId = data['eventData']['commitId'],
            commitMessage = data['eventData']['commitMessage'],
            commitAuthor = data['eventData']['commitAuthor'],
            buildUrl = getShortURL(data['eventData']['buildUrl'])
        )
