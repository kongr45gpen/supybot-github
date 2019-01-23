from .DefaultTheme import DefaultTheme

from ..utility import *

class CompactTheme(DefaultTheme):
    def commit(self, branch, author, message, id, url):
        self.msgs.append("%s: %s %s: %s %s" % (
            self.repo(branch),
            ircutils.mircColor(author, "green"),
            ircutils.mircColor(id[0:6], "dark grey"),
            maxLen(message.splitlines()[0], 300),
            self.enclose(url)
        ))

    def travis(self, branch, repo, status, commitId, commitMessage, commitAuthor, buildUrl):
        self.msgs.append( "%s @ %s: %s %s: build %s %s" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(repo),
            ircutils.mircColor(commitAuthor, "green"),
            ircutils.mircColor(commitId[0:6], "dark grey"),
            colorAction(status.lower()),
            self.enclose("%s - %s" % (
                ircutils.mircColor(maxLen(commitMessage, 50), "dark gray"),
                buildUrl
            ))
        ))

    def deployment(self, branch, repo, status, commitId, commitMessage, commitAuthor, url):
        self.msgs.append( "%s @ %s: %s %s: deploy %s %s" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(repo),
            ircutils.mircColor(commitAuthor, "green"),
            ircutils.mircColor(commitId[0:6], "dark grey"),
            colorAction(status.lower()),
            self.enclose("%s - %s" % (
                ircutils.mircColor(maxLen(commitMessage, 50), "dark gray"),
                url
            ))
        ))
