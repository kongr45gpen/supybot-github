from ..utility import *

def handle(data, theme):
    if isStatusVisible(data['site_id'], data['state'].lower(), 'showSuccessfulDeployMessages'):
        theme.deployment(
            branch = data['branch'],
            repo = data['name'],
            status = data['state'],
            commitId = data['commit_ref'],
            commitMessage = data['title'],
            commitAuthor = data['commit_url'].split('/')[3], #TODO: Make this show the proper author
            url = getShortURL(data['deploy_url'])
        )
