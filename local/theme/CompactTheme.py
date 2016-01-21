from DefaultTheme import DefaultTheme

from ..utility import *

class CompactTheme(DefaultTheme):
    def commit(self, branch, repo, author, message, id, url):
        self.msgs.append("%s @ %s: %s %s: %s %s" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(repo),
            ircutils.mircColor(author, "green"),
            ircutils.mircColor(id[0:6], "dark grey"),
            maxLen(message.splitlines()[0], 300),
            self.enclose(url)
        ))
