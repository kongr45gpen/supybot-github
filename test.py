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

    def testV3Push(self):
        self.sendRequest('push-v3')

        self.describe('first message',
            it().should.contain('gh-pages'),
            it().should.contain('baxterthehacker'),
            it().should.contain('pushed 1 commit'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/compare/4d2ab4e76d0d...7700ca29dd05')
        )

        self.describe('second message',
            it().should.contain('7700ca'),
            it().should.contain('kdaigle'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/commit/7700ca29dd050d9adacc0803f866d9b539513535')
        )

        self.describe('third message',
            it().should.contain('Trigger pages build')
        )

    def testNewWikiPage(self):
        self.sendRequest('wiki-new-page')

        self.describe('first message',
            it().should.contain('kongr45gpen/supybot-github'),
            it().should.contain('kongr45gpen modified 1 wiki page'),
            it().should.contain('https://github.com/kongr45gpen/supybot-github/wiki/_compare/9941c1a1bb1b2db99ad9aabf10c8f946d808e634')
        )

        self.describe('second message',
            it().should.contain('created Home'),
            it().should.contain('https://github.com/kongr45gpen/supybot-github/wiki/Home')
        )

    def testTravisNotification(self):
        self.sendRequest('travis-notification')

        self.describe('first message',
            it().should.contain('master @ minimal'),
            it().should.contain('passed'),
            it().should.contain('62aae'),
            it().should.contain('Sven Fuchs'),
            it().should.contain('this is a long commit message'),
            it().should_not.contain('this is a long commit message, because we must learn how to lead ever-present lives in the face of turbulence. It is a sign of things to come. The vector of aspiration is now happening'),
            it().should.contain('https://travis-ci.org/svenfuchs/minimal/builds/1')
        )

        self.assertError('get second message')

    def testCreateTag(self):
        self.sendRequest('create-tag')

        self.describe('first message',
            it().should.contain('public-repo'),
            it().should.contain('baxterthehacker'),
            it().should.contain('tagged'),
            it().should.contain('0.0.1'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/releases/tag/0.0.1')
        )

    def testDeleteTag(self):
        self.sendRequest('delete-tag')

        self.describe('first message',
            it().should.contain('public-repo'),
            it().should.contain('baxterthehacker'),
            it().should.contain('deleted tag'),
            it().should.contain('simple-tag'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/tags')
        )

    def testCreateBranch(self):
        self.sendRequest('create-branch')

        self.describe('first message',
            it().should.contain('public-repo'),
            it().should.contain('baxterthehacker'),
            it().should.contain('created branch'),
            it().should.contain('develop'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/tree/develop')
        )

    def testDeleteBranch(self):
        self.sendRequest('delete-branch')

        self.describe('first message',
            it().should.contain('public-repo'),
            it().should.contain('baxterthehacker'),
            it().should.contain('deleted branch'),
            it().should.contain('blue-lights'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/branches')
        )

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
