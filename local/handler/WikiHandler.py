from ..utility import *

def handle(data, theme):
    pageno = len(data['pages'])

    url = getShortURL("%s/wiki/_compare/%s" % ( data['repository']['html_url'], data['pages'][0]['sha'] ))

    if configValue("hidePush",None) is False:
        theme.wikiPush(
            actor = data['sender']['login'],
            count = pageno,
            url = url
        )

    pages = []
    for page in data['pages']:
        pages.append({
            'action': page['action'],
            'name'  : page['page_name'],
            'hash'  : page['sha'],
            'url'   : page['html_url']
        })

    # Unfortunately github doesn't support edit summaries :(
    theme.wikiPages(
        actor = data['sender']['login'],
        pages = pages,
        url = url
    )
