from Theme import Theme

from ..utility import *

class DefaultTheme(Theme):
    def push(self, branch, actor, count, url):
        self.msgs.append( "%s: %s pushed %s %s %s%s" % (
            self.repo(branch),
            ircutils.mircColor(actor, "green"),
            ircutils.bold(str(count)),
            plural(count, "commit", "commits"),
            self.enclose(url),
            ':' if count else ''
        ))

    def commit(self, branch, author, message, id, url):
        self.msgs.append("%s: %s * %s %s" % (
            self.repo(branch),
            ircutils.mircColor(author, "green"),
            ircutils.bold(id[0:6]),
            self.enclose(url)
        ))

        commitlines = message.splitlines()
        for line in commitlines:
            self.msgs.append( "%s: %s" % (
                self.repo(branch),
                maxLen(line, 400)
            ))

    def merge(self, actor, action, mergeCount, regularCount, base, to, url):
        distinctMessage = ""
        if configValue("hidePush",None) == False and regularCount > 0:
            distinctMessage = " and %s %s %s" % ( colorAction("pushed"), regularCount, plural(regularCount, 'commit', 'commits'))

        self.msgs.append( "%s: %s %s %s %s from %s%s into %s%s" % (
            self.repo(),
            ircutils.mircColor(actor, "green"),
            colorAction(action),
            mergeCount,
            plural(mergeCount, 'commit', 'commits'),
            ircutils.bold(ircutils.mircColor(base, "blue")),
            distinctMessage,
            ircutils.bold(ircutils.mircColor(to, "blue")),
            ' %s' % self.enclose(url) if url else ''
        ))

    def branch(self, actor, action, count, to, url, base = None):
        self.msgs.append( "%s: %s %s branch %s%s%s%s" % (
            self.repo(),
            ircutils.mircColor(actor, "green"),
            colorAction(action),
            ircutils.bold(ircutils.mircColor(to, "blue")),
            ' from %s' % ircutils.bold(ircutils.mircColor(base, "blue")) if base else '',
            ' %s' % self.enclose(url) if url else '',
            ':' if count else ''
        ))

    def tag(self, actor, action, to, onlyDeleted, base = None, headMsg = None, headId = None, url = None):
        if onlyDeleted:
            commitInfo = ""
        else:
            commitMsg = ""
            if configValue("tagShowCommitMsg"):
                commitMsg = ircutils.mircColor(" (%s)" % (maxLen(headMsg.splitlines()[0],75)),"brown")
            commitInfo = " %s %s %s%s as" % (base, ircutils.bold('*'), ircutils.bold(headId[0:6]), commitMsg)

        self.msgs.append("%s: %s %s%s %s%s" % (
            self.repo(),
            ircutils.mircColor(actor, "green"),
            colorAction(action),
            commitInfo,
            ircutils.bold(ircutils.mircColor(to, "blue")),
            ' %s' % self.enclose(url) if url else ''
        ))

    def issue(self, actor, action, issueNo, issueTitle, creator, milestone, url, assignee = None, comment = None, labelName = None, labelColor = None):
        formattedActor = ircutils.mircColor(actor, "green")

        if actor == assignee:
            formattedActor = ircutils.bold(formattedActor)

        extra = ''
        if action == 'assigned':
            extra = " to %s" % ircutils.bold(ircutils.mircColor(assignee, "green"))
        elif action == 'unassigned':
            extra = " from %s" % ircutils.mircColor(assignee, "green")
        elif action == 'labeled' or action == 'unlabeled':
            extra = " as %s" % ircutils.mircColor(labelName, hexToMirc(labelColor))

        self.msgs.append( "%s: %s %s issue #%s \"%s\"%s%s %s %s" % (
            self.repo(),
            formattedActor,
            colorAction(action),
            issueNo,
            ircutils.bold(issueTitle),
            " by %s" % ircutils.mircColor(creator,"green") if creator != actor else '',
            extra,
            self.enclose("%s%s" % (
                ircutils.mircColor(milestone, "brown") + '- ' if milestone else '',
                url
            )),
            ": %s" % maxLen(comment, 70) if comment else ''
        ))

    def wikiPush(self, actor, count, url):
        self.msgs.append( "%s: %s modified %s wiki %s %s:" % (
            self.repo(),
            ircutils.mircColor(actor, "green"),
            ircutils.bold(str(count)),
            plural(count, "page", "pages"),
            self.enclose(url)
        ))

    def wikiPages(self, actor, pages, url):
        urlShown = False;

        for page in pages:
            if configValue("hidePush") and urlShown is False:
                pageurl = self.enclose(url)
                urlShown = True
            elif configValue("hidePush"):
                pageurl = ""
            else:
                pageurl = self.enclose(page['url'])

            self.msgs.append( "%s: %s %s %s * %s %s" % (
                self.repo(),
                ircutils.mircColor(actor, "green"),
                colorAction(page['action']),
                ircutils.bold(ircutils.mircColor(page['name'], "blue")),
                ircutils.bold(page['hash'][0:6]),
                pageurl,
            ))

    def travis(self, branch, repo, status, commitId, commitMessage, commitAuthor, buildUrl):
        self.msgs.append( "%s @ %s: Build status: %s * %s by %s %s" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(repo),
            colorAction(status.lower()),
            ircutils.bold(commitId[0:6]),
            ircutils.mircColor(commitAuthor, "green"),
            self.enclose("%s - %s" % (
                ircutils.mircColor(maxLen(commitMessage, 50), "dark gray"),
                buildUrl
            ))
        ))

    def status(self, status, description, url):
        self.msgs.append( "%s: %s - %s %s" % (
            self.repo(),
            colorAction(status),
            description,
            self.enclose(url)
        ))

    def repo(self, branch = None):
        name = ircutils.bold(self.repoInfo['name'])

        if self.repoInfo['fork'] and self.repoInfo['owner']:
            repo = "%s/%s" % (self.repoInfo['owner'], name)
        else:
            repo = name

        if branch is not None:
            return "%s @ %s" % (
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                repo
            )
        else:
            return repo
