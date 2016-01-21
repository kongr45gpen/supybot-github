from ..utility import *

def handle(data, theme):
    created = 'master_branch' in data

    if data['ref_type'] == 'tag':
        theme.tag(
            actor = data['sender']['login'],
            action = "tagged" if created else "deleted tag",
            to = data['ref'],
            onlyDeleted = True,
            url = getShortURL("%s/releases/tag/%s" % (data['repository']['html_url'], data['ref'])) if created else getShortURL("%s/tags" % data['repository']['html_url'])
        )
    else:
        theme.branch(
            actor = data['sender']['login'],
            action = "created" if created else "deleted",
            count = 0,
            to = data['ref'],
            url = getShortURL("%s/tree/%s" % (data['repository']['html_url'], data['ref'])) if created else getShortURL("%s/branches" % data['repository']['html_url'])
        )
