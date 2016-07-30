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

conf.registerGlobalValue(Github, 'passcode',
        registry.String('', """Password which should be included into the URL (DEPRECATED AND DANGEROUS!)"""))

conf.registerGlobalValue(Github, 'disallowChannelOverride',
        registry.Boolean(False,
        """Don't let the user select the channel where the messages will be sent to on the URL"""))

conf.registerGlobalValue(Github, 'disallowConfigOverride',
        registry.Boolean(True,
        """Don't let the user change config values from the URL"""))

conf.registerGlobalValue(Github, 'showMilestone',
        registry.Boolean(True,
        """Show the name of the milestone when reporting issues or issue comments"""))

conf.registerGlobalValue(Github, 'tagShowCommitMsg',
        registry.Boolean(True,
        """Show the commit message of the commit a new tag points to"""))

conf.registerGlobalValue(Github, 'showMergedCommits',
        registry.Boolean(False,
        """Show merged commits when a branch is merged into another"""))

conf.registerGlobalValue(Github, 'showSuccessfulBuildMessages',
        registry.String('change',
        """Whether to show successful build messages - can be never, change or always"""))

conf.registerGlobalValue(Github, 'port',
        registry.Integer(8093,
        """The port where Github will send HTTP requests"""))

conf.registerGlobalValue(Github, 'theme',
        registry.String('default', """The name of the theme that will be used to style messages"""))

conf.registerGlobalValue(Github, 'brackets',
        registry.String('( )', """The brackets to use to enclose URLs (space-separated)"""))

conf.registerGlobalValue(Github, 'allowArbitraryMessages',
        registry.Boolean(False,
        """Whether to allow parsing and showing arbitrary messages sent by a client"""))

conf.registerGlobalValue(Github, 'hideURL',
        registry.Boolean(False,
        """Whether to not display the URLs of actions"""))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
