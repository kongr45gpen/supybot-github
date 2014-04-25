import urllib2

import supybot.conf as conf
import supybot.ircutils as ircutils
import supybot.registry as registry

def registryValue(plugin, name, channel=None, value=True):
    group = conf.supybot.plugins.get(plugin)
    names = registry.split(name)
    for name in names:
        group = group.get(name)
    if channel is not None:
        if ircutils.isChannel(channel):
            group = group.get(channel)
        else:
            self.log.debug('registryValue got channel=%r', channel)
    if value:
        return group()
    else:
        return group


def configValue(name, channel=None, repo=None, type=None, module=None):
    return registryValue("Github", name, channel)

def plural(number, s, p):
    if number != 1:
        return p
    return s

def maxLen(msg, maxn=400):
    """Cut down a string if its longer than `maxn` chars"""
    if len(msg) > maxn:
        ret = "%s..." % (msg[0:(maxn-3)])
    else:
        ret = msg
    return ret

def colorAction(action):
    """Give an action string (e.g. created, edited) and get a nice IRC colouring"""
    if action == "created" or action == "opened" or action == "tagged":
        return ircutils.bold(ircutils.mircColor(action, "green"))
    if action == "deleted" or action == "closed" or action == "re-tagged" or \
       action == "deleted tag" or action == "failed" or action == "still failing":
        return ircutils.bold(ircutils.mircColor(action, "red"))
    if action == "merged":
        return ircutils.bold(ircutils.mircColor(action, "light blue"))
    if action == "reopened":
        return ircutils.bold(ircutils.mircColor(action, "blue"))
    if action == "forced the creation of" or action == "forced the deletion of":
        return ircutils.bold(ircutils.mircColor(action,"brown"))
    return action

def getShortURL(longurl):
    if configValue("shortURL") is False:
        url = longurl
    else:
        data = 'url=%s' % (longurl)
        req = urllib2.Request("http://git.io", data)
        response = urllib2.urlopen(req)
        url = response.info().getheader('Location')
    return ircutils.mircColor(url, "purple")
