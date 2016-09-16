from ..utility import *

def handle(data, theme):
    if data['state'] == 'pending' and not configValue("showPendingStatuses"):
        return

    theme.status(
        status = data['state'],
        description = data['description'],
        url = getShortURL(data['target_url'])
    )
