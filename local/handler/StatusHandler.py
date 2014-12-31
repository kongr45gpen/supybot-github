from ..utility import *

def handle(data, theme):
    theme.status(
        repo = data['repository']['name'],
        status = data['state'],
        description = data['description'],
        url = data['target_url']
    )
