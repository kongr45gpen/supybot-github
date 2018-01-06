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
#
# Global values should also be added to configValue() in utility.py
conf.registerGlobalValue(Github, 'channel',
        registry.String('#commits', """Determines the channel where commit
					notifications will go by default."""))

conf.registerChannelValue(Github, 'shortURL',
        registry.Boolean(True, """Use git.io to produce shorter URLs"""))

conf.registerChannelValue(Github, 'hidePush',
        registry.Boolean(False, """Whether to hide 'user pushed ... commits' message"""))

conf.registerGlobalValue(Github, 'passcode',
        registry.String('', """Password which should be included into the URL (DEPRECATED AND DANGEROUS!)"""))

conf.registerGlobalValue(Github, 'disallowChannelOverride',
        registry.Boolean(False,
        """Don't let the user select the channel where the messages will be sent to on the URL"""))

conf.registerGlobalValue(Github, 'disallowConfigOverride',
        registry.Boolean(True,
        """Don't let the user change config values from the URL"""))

conf.registerChannelValue(Github, 'showMilestone',
        registry.Boolean(True,
        """Show the name of the milestone when reporting issues or issue comments"""))

conf.registerChannelValue(Github, 'tagShowCommitMsg',
        registry.Boolean(True,
        """Show the commit message of the commit a new tag points to"""))

conf.registerChannelValue(Github, 'showMergedCommits',
        registry.Boolean(False,
        """Show merged commits when a branch is merged into another"""))

conf.registerChannelValue(Github, 'showSuccessfulBuildMessages',
        registry.String('change',
        """Whether to show successful build messages - can be never, change or always"""))

conf.registerChannelValue(Github, 'showSuccessfulDeployMessages',
        registry.String('always',
        """Whether to show successful deployment messages - can be never, change or always"""))

conf.registerGlobalValue(Github, 'address',
        registry.String('',
        """The IP address or hostname to which the HTTP server will bind. The default empty value ('') should work for most cases."""))

conf.registerGlobalValue(Github, 'port',
        registry.Integer(8093,
        """The port where Github will send HTTP requests"""))

conf.registerChannelValue(Github, 'theme',
        registry.String('default', """The name of the theme that will be used to style messages"""))

conf.registerChannelValue(Github, 'brackets',
        registry.String('( )', """The brackets to use to enclose URLs (space-separated)"""))

conf.registerChannelValue(Github, 'allowArbitraryMessages',
        registry.Boolean(False,
        """Whether to allow parsing and showing arbitrary messages sent by a client"""))

conf.registerChannelValue(Github, 'hideURL',
        registry.Boolean(False,
        """Whether to not display the URLs of actions"""))

conf.registerChannelValue(Github, 'preventIssueNameSpam',
        registry.Boolean(True,
        """Whether to prevent the same issue name from showing up too often"""))

conf.registerChannelValue(Github, 'showIssueEdits',
        registry.Boolean(True,
        """Whether to show a message when an issue is edited"""))

conf.registerChannelValue(Github, 'showPendingStatuses',
        registry.Boolean(False,
        """Whether to show a message for a pending status (e.g. a build in progress)"""))

conf.registerChannelValue(Github, 'alwaysShowForcedPushes',
        registry.Boolean(True,
        """Whether to always show force-pushes, even if hidePush is set to True"""))

conf.registerChannelValue(Github, 'maxCommitCount',
        registry.Integer(7,
        """The maximum number of commits to show (0 to disable)"""))
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
