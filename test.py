###
from supybot.log import info
from supybot.test import *

from .local.testing.ExpectationPluginTestCase import *

class GithubTestCase(ExpectationPluginTestCase):
    plugins = ('Github',)
    port    = 27230
    address = '127.0.0.1'
    files   = {}
    config  = { 'plugins.github.shortUrl': False,
                'plugins.github.hidePush': False
              }

    def setUp(self):
        # Set a different port and address from the default one to make
        # testing while a supybot-github instance is running possible - we
        # don't use the config variable because supybot's test framework sets
        # the value after the plugin has been loaded
        conf.supybot.plugins.get("Github").get('port').setValue(self.port)
        conf.supybot.plugins.get("Github").get('address').setValue(self.address)
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

    def testForcePush(self):
        self.sendRequest('push-forced')

        self.describe('first message',
            it().should.contain('force pushed'),
            it().should.contain('2 commits'),
            it().should.contain('kongr45gpen'),
            it().should.contain('pullr1'),
            it().should.contain('test'),
            it().should.contain('https://github.com/kongr45gpen/test/compare/3be0d004b9d9...12121ad459e0')
        )

        self.describe('second message',
            it().should.contain('kongr45gpen'),
            it().should.contain('726'),
            it().should.contain('https://github.com/kongr45gpen/test/commit/726b044d600a19ce10eccf1014f7dd19b6efddf6')
        )

        self.describe('fourth message',
            it().should.contain('Padiaten'),
            it().should.contain('121'),
            it().should.contain('https://github.com/kongr45gpen/test/commit/12121ad459e0ae12ec91928949aab27a84a0478f')
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

    def testAppVeyor(self):
        self.sendRequest('appveyor')

        self.describe('first message',
            it().should.contain('pullr1 @ test'),
            it().should.contain('failed'),
            it().should.contain('3be0d'),
            it().should.contain('alezakos'),
            it().should.contain('Update README.md'),
            it().should.contain('https://ci.appveyor.com/project/kongr45gpen/test/build/1.0.2')
        )

        self.assertError('get second message')

    def testNetlify(self):
        self.sendRequest('netlify-ready')

        self.describe('first message',
            it().should.contain('master @ bzflag-plugin-starter'),
            it().should.contain('ready'),
            it().should.contain('19a67'),
            it().should.contain('iisgood')
        )

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

    def testIssueCreate(self):
        self.sendRequest('issue-create')

        self.describe('first message',
            it().should.contain('kongr45gpen'),
            it().should.contain('test'),
            it().should.contain('opened'),
            it().should.contain('Another issue'),
            it().should.contain('#6'),
            it().should_not.contain('pull request'),
            it().should.contain('https://github.com/kongr45gpen/test/issues/6')
        )

    def testIssueComment(self):
        self.sendRequest('issue-comment')

        self.describe('first message',
            it().should.contain('kongr45gpen'),
            it().should.contain('test'),
            it().should.contain('commented'),
            it().should.contain('Another issue'),
            it().should.contain('#6'),
            it().should_not.contain('pull request'),
            it().should.contain('https://github.com/kongr45gpen/test/issues/6#issuecomment-181134370')
        )

    def testIssueSelfAssign(self):
        self.sendRequest('issue-assign-self')

        self.describe('first message',
            it().should.contain('kongr45gpen'),
            it().should.contain('supybot-github'),
            it().should.contain('self-assigned'),
            it().should.contain('issue'),
            it().should.contain('#22'),
            it().should.contain('Handle duplicate notifications for branches and tags'),
            it().should.contain('https://github.com/kongr45gpen/supybot-github/issues/22')
        )

    def testPullRequestCreate(self):
        self.sendRequest('pr-create')

        self.describe('first message',
            it().should.contain('baxterthehacker'),
            it().should.contain('public-repo'),
            it().should.contain('opened'),
            it().should.contain('Update the README with new information'),
            it().should.contain('#1'),
            it().should.contain('pull request'),
            it().should_not.contain('issue'),
            it().should.contain('https://github.com/baxterthehacker/public-repo/pull/1')
        )

    def testPullRequestComment(self):
        self.sendRequest('pr-comment')

        self.describe('first message',
            it().should.contain('kongr45gpen'),
            it().should.contain('test'),
            it().should.contain('commented'),
            it().should.contain('Update README.md'),
            it().should.contain('#7'),
            it().should.contain('pull request'),
            it().should_not.contain('commented on issue'),
            it().should.contain('https://github.com/kongr45gpen/test/pull/7#issuecomment-247345280')
        )

    def testRelease(self):
        self.sendRequest('release')

        self.describe('first message',
            it().should.contain('myproject'),
            it().should.contain('kongr45gpen'),
            it().should.contain('prerelease'),
            it().should_not.contain('draft'),
            it().should.contain('Useless Release'),
            it().should.contain('v2.6.5'),
            it().should.contain('https://github.com/kongr45gpen/myproject/releases/tag/v2.6.5')
        )

    def testPing(self):
        self.conf('allowArbitraryMessages', False)
        self.sendRequest('ping')

        self.describe('first message',
            it().should.contain('Mind your words, they are important.'),
            it().should.contain('test'),
            it().should.contain('zen')
        )

        self.conf('allowArbitraryMessages', True)
        self.sendRequest('ping')

        self.describe('first message',
            it().should.contain('Mind your words, they are important.'),
            it().should.contain('test'),
            it().should_not.contain('zen')
        )



# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
