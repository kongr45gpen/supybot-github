from ..utility import *

def handle(data, theme):
    actor = data['sender']['login'] \
        if 'sender' in data and 'login' in data['sender'] \
        else None
    action = data['action'] if 'action' in data else None

    url = None
    for key in data:
        if key not in ['repository', 'sender'] \
                and isinstance(data[key], dict)\
                and 'html_url' in data[key]:
            url = data[key]['html_url']
            break

    theme.unknown(
        eventType = data['eventType'],
        action = action,
        actor = actor,
        url = getShortURL(url)
    )
