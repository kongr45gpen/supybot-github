from ..utility import *

def handle(data, theme):
    theme.release(
        action = data['action'],
        author = data['release']['author']['login'],
        commit = data['release']['target_commitish'],
        description = data['release']['body'],
        name = data['release']['name'],
        prerelease = data['release']['prerelease'],
        tag = data['release']['tag_name'],
        url = getShortURL(data['release']['html_url'])
    )
