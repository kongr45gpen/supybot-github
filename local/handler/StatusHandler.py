from ..utility import *

def handle(data, theme):
    theme.status(
        status = data['state'],
        description = data['description'],
        url = data['target_url']
    )
