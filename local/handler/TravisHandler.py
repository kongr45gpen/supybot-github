from ..utility import *

def handle(data, theme):
    if isStatusVisible(data['repository']['url'], data['status_message'].lower()):
        theme.travis(
            branch = data['branch'],
            repo = data['repository']['name'],
            status = data['status_message'],
            commitId = data['commit'],
            commitMessage = data['message'],
            commitAuthor = data['author_name'],
            buildUrl = getShortURL(data['build_url'])
        )
