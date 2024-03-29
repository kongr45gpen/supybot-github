import re
import math
import random
import string
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timedelta

import supybot.log as log
import supybot.conf as conf
import supybot.world as world
import supybot.ircutils as ircutils
import supybot.registry as registry

from . import globals


def registryValue(plugin, name, channel=None, value=True):
    group = conf.supybot.plugins.get(plugin)
    names = registry.split(name)
    for name in names:
        group = group.get(name)
    if channel is not None:
        try:
            if ircutils.isChannel(channel):
                group = group.get(channel)
            else:
                log.debug('registryValue got channel=%r', channel)
        except registry.NonExistentRegistryEntry:
            log.debug('non existent registry entry %r for channel %r', name, channel)
            pass
    if value:
        return group()
    else:
        return group


def configValue(name, channel=None, repo=None, type=None, module=None):
    if globals.configOverrides and name.lower() in globals.configOverrides:
        return globals.configOverrides[name.lower()]

    if channel == None and name not in ['channel', 'passcode', 'disallowChannelOverride', 'disallowConfigOverride']:
        channel = globals.channel

    return registryValue("Github", name, channel)


def addConfigOverride(name, value):
    if value.lower() == 'false':
        value = False;
    elif value.lower() == 'true':
        value = True;

    name = name.strip().lower()

    if name in ['passcode', 'disallowConfigOverride', 'allowArbitraryMessages']:
        return

    globals.configOverrides[name] = value


def resetConfigOverrides():
    globals.configOverrides = {}


def plural(number, s, p):
    if number != 1:
        return p
    return s


def parseBrackets(bracketConfig):
    if "M" in bracketConfig:
        return tuple(bracketConfig.split('M', 1))
    else:
        mid = math.floor(len(bracketConfig) / 2)
        if len(bracketConfig) % 2 == 0:
            return (bracketConfig[:mid], bracketConfig[mid:])
        else:
            # Do not include the middle character
            return (bracketConfig[:mid], bracketConfig[(mid + 1):])


def maxLen(msg, maxn=400, splitLines=True):
    """Cut down a string if its longer than `maxn` chars"""

    if msg is None:
        return None

    if splitLines is True:
        lines = msg.splitlines()
        line = lines[0] if lines else ""
    else:
        line = msg

    if len(line) > maxn:
        ret = "%s..." % (line[0:(maxn - 3)])
    elif splitLines is True and len(lines) > 1:
        ret = "%s..." % (line)
    else:
        ret = msg
    return ret

# TODO: Use a better data structure for this?
def colorAction(action):
    """Give an action string (e.g. created, edited) and get a nice IRC colouring."""

    # Fix past tense for some github verbs
    if action in ["synchronize"]:
        action += "d"

    if action in ["created", "opened", "tagged", "success", "passed", "fixed",
                  "published", "completed", "ready"]:
        return ircutils.bold(ircutils.mircColor(action, "green"))
    if action in ["deleted", "closed", "re-tagged", "deleted tag",
                  "failed", "errored", "failure", "still failing",
                  "broken", "error", "removed"]:
        return ircutils.bold(ircutils.mircColor(action, "red"))
    if action in ["assigned", "self-assigned", "merged", "synchronized",
                  "labeled"]:
        return ircutils.bold(ircutils.mircColor(action, "light blue"))
    if action in ["reopened", "pending"]:
        return ircutils.bold(ircutils.mircColor(action, "blue"))
    if action[0:5] in ["force"]:
        return ircutils.bold(ircutils.mircColor(action, "brown"))
    return action


def getShortURL(longurl):
    """ Returns a short URL generated by git.io"""
    if longurl is None:
        return None
    elif configValue("hideURL") is True:
        return None
    if configValue("shortURL") is False or not getShortURL.github.match(longurl):
        url = longurl
    else:
        url = longurl
    return ircutils.mircColor(url, "purple")


getShortURL.github = re.compile('^([a-z]*\:\/\/)?([^\/]+.)?github.com')


def saveMessages(msgs):
    """ Saves the last messages so that the plugin can be easily tested """
    if not world.testing:
        return
    globals.messageList = msgs


def isYes(string):
    """Returns True if the string represents a yes, False, if it represents
    no, and another string if it represents something else"""
    value = string.strip().lower()

    if value in ['yes', 'always', 'on', 'true']:
        return True
    if value in ['no', 'never', 'off', 'false', 'null']:
        return False
    if value in ['changed', 'change', 'onchange', 'on_change', 'diff']:
        return 'change'


def isStatusVisible(repo, status, option='showSuccessfulBuildMessages'):
    """Returns whether the build status message should be shown"""
    config = isYes(configValue(option))

    changed = False
    if status != "passed" and status != "ready":
        changed = True
    elif type(config) is bool:
        changed = config
    elif repo not in globals.travisStatuses or status != globals.travisStatuses[repo]:
        # Config is 'on_change'
        changed = True

    globals.travisStatuses[repo] = status
    return changed


def randomString(length):
    """Returns a securely generated random string of a specific length"""
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(length))


def secureCompare(s1, s2):
    """Securely compare two strings"""
    return sum(i != j for i, j in zip(s1, s2)) == 0


def getChannelSecret(channel):
    """Returns a secret for a channel, or None if that channel has no secret"""
    if globals.secretDB is None:
        return None
    try:
        record = globals.secretDB.get(channel, 1)
        return record.secret
    except KeyError:
        return None


def showIssueName(repoId, issueId):
    """Returns whether we should show the issue name for a repo issue"""
    now = datetime.now()

    if not configValue("preventIssueNameSpam"):
        globals.shownIssues.clear()
        return True

    if not repoId in globals.shownIssues:
        globals.shownIssues[repoId] = {}

    # Clean up old issues
    remove = [k for k in globals.shownIssues[repoId] if now - globals.shownIssues[repoId][k] > timedelta(seconds=15)]
    for k in remove: del globals.shownIssues[repoId][k]

    exists = issueId in globals.shownIssues[repoId]

    # Add our issue to the list
    globals.shownIssues[repoId][issueId] = now

    return not exists


def hexToMirc(hash):
    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'blue': (0, 0, 127),
        'green': (0, 147, 0),
        'red': (255, 0, 0),
        'brown': (127, 0, 0),
        'purple': (156, 0, 156),
        'orange': (252, 127, 0),
        'yellow': (255, 255, 0),
        'light green': (0, 252, 0),
        'teal': (0, 147, 147),
        'light blue': (84, 255, 255),
        'dark blue': (84, 84, 255),
        'pink': (255, 0, 255),
        'dark grey': (127, 127, 127),
        'light grey': (230, 230, 230)
    }

    rgb = _hex_to_rgb(hash)

    return min(colors, key=lambda x: _colourDistance(colors[x], rgb))


def _hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def _colourDistance(a, b):
    # Source: http://www.compuphase.com/cmetric.htm
    rmean = math.floor((a[0] + b[0]) / 2)
    red = a[0] - b[0]
    green = a[1] - b[1]
    blue = a[2] - b[2]

    return math.sqrt((((512 + rmean) * red * red) >> 8) + 4 * green * green + (((767 - rmean) * blue * blue) >> 8))

# Possible colours:
# white, black, (light/dark) blue, (light) green, red, brown, purple,
# orange, yellow, teal, pink, light/dark gray/grey
