###

from supybot.log import info
from supybot.test import *

import re
import urllib

class GithubTestCase(ChannelPluginTestCase):
    plugins = ('Github',)
    port    = 27230
    files   = {}
    config  = { 'plugins.github.shortUrl': False,
                'plugins.github.hidePush': False
              }

    def assertContains(self, query, expectedNeedle, flags=re.I, **kwargs):
        regex = re.compile("((\x02)|(\x03))(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)

        m = self._feedMsg(query, **kwargs)
        messageString = regex.sub('', m.args[1])
        if m is None:
            raise TimeoutError, query
        self.failUnless(re.search(expectedNeedle, messageString, flags),
                        '%r does not match %r' % (messageString, expectedNeedle))
        return m

    def setUp(self):
        # Set a different port from the default one to make testing while a
        # supybot-github instance is running possible - we don't use the config
        # variable because supybot's test framework sets the value after the
        # plugin has been loaded
        conf.supybot.plugins.get("Github").get('port').setValue(self.port)
        ChannelPluginTestCase.setUp(self)

    def sendRequest(self, file):
        if file in self.files:
            content = self.files[file]
        else:
            with open('samples/' + file + '.json', 'r') as content_file:
                content = content_file.read()
            self.files[file] = content

        res = urllib.urlopen('http://localhost:' + str(self.port), 'payload=' + content)



    def testMerge(self):
        self.sendRequest('push-merge')

        # By default, merged commits should not be shown
        self.assertError('get 5th message')

        self.assertContains('get first message', 'merged 4 commits')
        self.assertContains('get first message', 'from newTestBranch')
        self.assertContains('get first message', 'pushed 1 commit')
        self.assertContains('get first message', 'to master')

        self.assertContains('get first message', 'https://github.com/username/test/compare/cb12c8e51c8e...f386345fa3c5')

    def testHeaders(self):
          #  self.assertError('headers ftp://ftp.cdrom.com/pub/linux')
         #   self.assertNotError('headers http://www.slashdot.org/')
         return


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
