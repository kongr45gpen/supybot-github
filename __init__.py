###

"""
Add a description of the plugin (to be presented to the user inside the wizard)
here.  This should describe *what* the plugin does.
"""

import supybot
import supybot.world as world

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = ""

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.Author('kongr45gpen', 'alezakos', 'kongr45gpen@helit.org')

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = 'https://github.com/kongr45gpen/supybot-github'


from . import config
from . import plugin
from imp import reload
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!
from .local import globals
from .local import utility
from .local.handler import GithubHandler as RequestHandler
from .local.handler import PingHandler
from .local.handler import PushHandler
from .local.handler import WikiHandler
from .local.handler import IssueHandler
from .local.handler import StatusHandler
from .local.handler import TravisHandler
from .local.handler import MessageHandler
from .local.handler import NetlifyHandler
from .local.handler import ReleaseHandler
from .local.handler import UnknownHandler
from .local.handler import AppVeyorHandler
from .local.handler import CreateDeleteHandler
from .local.handler import IssueCommentHandler
from .local.theme import Theme
from .local.theme import DefaultTheme
from .local.theme import CompactTheme
reload(globals)
reload(utility)
reload(RequestHandler)
reload(PingHandler)
reload(PushHandler)
reload(WikiHandler)
reload(IssueHandler)
reload(StatusHandler)
reload(TravisHandler)
reload(MessageHandler)
reload(NetlifyHandler)
reload(ReleaseHandler)
reload(UnknownHandler)
reload(AppVeyorHandler)
reload(CreateDeleteHandler)
reload(IssueCommentHandler)
reload(Theme)
reload(DefaultTheme)
reload(CompactTheme)

globals.init()

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
