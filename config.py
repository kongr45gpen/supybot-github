###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Github', True)


Github = conf.registerPlugin('Github')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Github, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))
conf.registerGlobalValue(Github, 'channel',
        registry.String('#commits', """Determines the channel where commit
					notifications will go by default."""))

conf.registerGlobalValue(Github, 'shortURL',
        registry.Boolean(True, """Use git.io to produce shorter URLs"""))

conf.registerGlobalValue(Github, 'hidePush',
        registry.Boolean(False, """Whether to hide 'user pushed ... commits' message"""))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
