###
from supybot.log import info
from supybot.test import *

from local.testing.ExpectationPluginTestCase import *

class GithubTestCase(ExpectationPluginTestCase):
    plugins = ('Github',)
    port    = 27230
    files   = {}
    config  = { 'plugins.github.shortUrl': False,
                'plugins.github.hidePush': False
              }

    def setUp(self):
        # Set a different port from the default one to make testing while a
        # supybot-github instance is running possible - we don't use the config
        # variable because supybot's test framework sets the value after the
        # plugin has been loaded
        conf.supybot.plugins.get("Github").get('port').setValue(self.port)
        PluginTestCase.setUp(self)


    def testMerge(self):
        self.sendRequest('push-merge')

        self.describe('first message',
            it().should.contain('merged 4 commits'),
            it().should.contain('from newTestBranch'),
            it().should.contain('pushed 1 commit'),
            it().should.contain('to master'),
            it().should.contain('https://github.com/username/test/compare/cb12c8e51c8e...f386345fa3c5')
        )

        # By default, merged commits should not be shown
        self.assertError('get 5th message')

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
