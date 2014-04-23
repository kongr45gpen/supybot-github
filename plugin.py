#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

import re
import json
import time
import random
import urllib
import urllib2
import urlparse
import threading
import BaseHTTPServer

import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.registry as registry
import supybot.callbacks as callbacks

def plural(number, s, p):
    if number != 1:
        return p
    return s

def maxLen(msg, maxn=400):
    """Cut down a string if its longer than `maxn` chars"""
    if len(msg) > maxn:
        ret = "%s..." % (msg[0:(maxn-3)])
    else:
        ret = msg
    return ret

def colorAction(action):
    """Give an action string (e.g. created, edited) and get a nice IRC colouring"""
    if action == "created" or action == "opened" or action == "tagged":
        return ircutils.bold(ircutils.mircColor(action, "green"))
    if action == "deleted" or action == "closed" or action == "re-tagged" or \
       action == "deleted tag" or action == "failed" or action == "still failing":
        return ircutils.bold(ircutils.mircColor(action, "red"))
    if action == "merged":
        return ircutils.bold(ircutils.mircColor(action, "light blue"))
    if action == "reopened":
        return ircutils.bold(ircutils.mircColor(action, "blue"))
    if action == "forced the creation of" or action == "forced the deletion of":
        return ircutils.bold(ircutils.mircColor(action,"brown"))
    return action

def registryValue(plugin, name, channel=None, value=True):
    group = conf.supybot.plugins.get(plugin)
    names = registry.split(name)
    for name in names:
        group = group.get(name)
    if channel is not None:
        if ircutils.isChannel(channel):
            group = group.get(channel)
        else:
            self.log.debug('registryValue got channel=%r', channel)
    if value:
        return group()
    else:
        return group

def configValue(name, channel=None, repo=None, type=None, module=None):
    return registryValue("Github", name, channel)

def getShortURL(longurl):
    if configValue("shortURL") is False:
        url = longurl
    else:
        data = 'url=%s' % (longurl)
        req = urllib2.Request("http://git.io", data)
        response = urllib2.urlopen(req)
        url = response.info().getheader('Location')
    return ircutils.mircColor(url, "purple")

# Possible colours:
# white, black, (light/dark) blue, (light) green, red, brown, purple,
# orange, yellow, teal, pink, light/dark gray/grey

class GithubHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(s):
        """Respond to a POST request."""

        length = int(s.headers['Content-Length'])
        post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
        data = json.loads(post_data['payload'][0])

        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write('<!DOCTYPE html><html><head><title>Hello</title></head>')
        s.wfile.write("<body><p>Thanks, you're awesome.</p>")

        s.wfile.write('</body></html>\n')
        s.wfile.write(s.path.split('/'))
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

        path = s.path.split('/')
        channel = configValue('channel')
        receivedcode = ''
        requireCode = configValue('passcode').strip() \
            and configValue('passcode').strip().lower() != 'false' \
            and configValue('passcode').strip().lower() != 'null' \
            and configValue('passcode').strip().lower() != 'no'

        # Analyse the URL
        i = 0
        for part in path:
            part = urllib.unquote(part)
            if i == 1 and requireCode:
                receivedcode = part

            part = part.replace('+','#');
            part = part.replace('~','#');
            part = part.replace('-','#');
            part = part.replace('&','#');
            part = part.replace('^','#');

            if part.startswith("#") and not configValue('disallowChannelOverride'):
                channel = part

            i+=1




        if requireCode and receivedcode != configValue('passcode'):
            # The password is wrong
            s.wfile.write("The password is wrong")
            return

        for irc in world.ircs:
            # Handle different event types

            msgs = []

            if 'pages' in data:
                msgs = s.handle_wiki(irc, data, channel)
            elif 'commits' in data:
                msgs = s.handle_push(irc, data, channel)
            elif 'issue' in data:
                if 'comment' in data:
                    msgs = s.handle_issue_comment(irc, data, channel)
                else:
                    msgs = s.handle_issue(irc, data, channel)
            else:
                msgs.append( ircmsgs.privmsg(channel, "Something happened"))

            #msgs.append( ircmsgs.privmsg("#main", "%s" % ()) )
            for msg in msgs:
                    irc.queueMsg(msg)

    def handle_push(s, irc, data, channel):
        msgs = []

        commitno = len(data['commits'])
        ref = data['ref'].split('/',2)
        branch = ref[2]

        colon = ''
        if data['commits']:
            colon = ':'

        isTag = False

        branched = data['created'] or data['deleted'] or ref[1] == "tags"
        branchFrom = ''
        tagFrom = ''

        onlyDeleted = data['deleted'] and not data['created']

        if branched:
            print branch
            if ref[1] == 'tags':
                isTag = True

            urls = ' (%s)' % (getShortURL(data['compare']),)
            if 'base_ref' in data:
                base_ref = data['base_ref'].split('/',2)
                if isTag:
                    branchFrom = '%s %s ' % (base_ref[2], ircutils.bold('*'))
                else:
                    branchFrom = ' from %s' % (base_ref[2],)

            if data['created'] and data['deleted'] or (not data['created'] and not data['deleted'] and data['forced']):
                if isTag:
                    action = "re-tagged"
                else:
                    action = "re-created"
            elif data['created'] and not data['forced']:
                if isTag:
                    action = "tagged"
                else:
                    action = "created"
            elif data['deleted'] and not data['forced']:
                if isTag:
                    action = "deleted tag"
                else:
                    action = "deleted"
                urls = ''
            elif data['created']:
                if isTag:
                    action = "tagged"
                else:
                    action = "created"
            elif data['deleted']:
                if isTag:
                    action = "deleted tag"
                else:
                    action = "deleted"
                urls = ''
            else:
                action = "did something with"


        if configValue("hidePush",None) == False and not branched:
            msgs.append( ircmsgs.privmsg(channel, "%s @ %s: %s pushed %s %s (%s)%s" % (
            ircutils.bold(ircutils.mircColor(branch, "blue")),
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(data['pusher']['name'], "green"),
            ircutils.bold(str(commitno)),
            plural(commitno, "commit", "commits"),
            getShortURL(data['compare']),
            colon
            )) )
        elif branched:
            if isTag:
                if onlyDeleted:
                    commitInfo = ""
                else:
                    commitMsg = ""
                    if configValue("tagShowCommitMsg"):
                        commitMsg = ircutils.mircColor(" (%s)" % (maxLen(data['head_commit']['message'].splitlines()[0],75)),"brown")
                    commitInfo = " %s %s%s as" % (branchFrom, ircutils.bold(data['head_commit']['id'][0:6]), commitMsg)
                msgs.append( ircmsgs.privmsg(channel, "%s: %s %s%s %s%s" % (
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(data['pusher']['name'], "green"),
                colorAction(action),
                commitInfo,
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                urls,
                )) )
            else:
                msgs.append( ircmsgs.privmsg(channel, "%s: %s %s branch %s%s%s%s" % (
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(data['pusher']['name'], "green"),
                colorAction(action),
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                branchFrom,
                urls,
                colon
                )) )

        for commit in data['commits']:
            if 'username' in commit['author']:
                author = commit['author']['username']
            else:
                author = commit['author']['name']

            msgs.append( ircmsgs.privmsg(channel, "%s @ %s: %s * %s (%s)" % (
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(author, "green"),
                ircutils.bold(commit['id'][0:6]),
                getShortURL(commit['url']),
            )) )

            commitlines = commit['message'].splitlines()
            for rawline in commitlines:
                maxLen(rawline, 400)
                msgs.append(ircmsgs.privmsg(channel, "%s @ %s: %s" % (
                    ircutils.bold(ircutils.mircColor(branch, "blue")),
                    ircutils.bold(data['repository']['name']),
                    line,
                )) )

        return msgs

    def handle_wiki(s, irc, data, channel):
        msgs = []

        pageno = len(data['pages'])

        url = getShortURL("%s/wiki/_compare/%s" % ( data['repository']['html_url'], data['pages'][0]['sha'] ))

        if configValue("hidePush",None) is False:
            msgs.append( ircmsgs.privmsg(channel, "%s: %s modified %s wiki %s (%s):" % (
            ircutils.bold(data['repository']['name']),
            ircutils.mircColor(data['sender']['login'], "green"),
            ircutils.bold(str(pageno)),
            plural(pageno, "page", "pages"),
            url
            )) )

        urlShown = False;

        for page in data['pages']:
            if configValue("hidePush") and urlShown is False:
                pageurl = "(%s)" % (url,)
                urlShown = True
            elif configValue("hidePush"):
                pageurl = ""
            else:
                pageurl = "(%s)" % (page['html_url'],)

            # Unfortunately github doesn't support edit summaries :(
            msgs.append( ircmsgs.privmsg(channel, "%s: %s %s %s * %s %s" % (
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(data['sender']['login'], "green"),
                colorAction(page['action']),
                ircutils.bold(ircutils.mircColor(page['page_name'], "blue")),
                ircutils.bold(page['sha'][0:6]),
                pageurl,
            )) )

        return msgs

    def handle_issue(s, irc, data, channel):
        msgs = []

        url = data['issue']['url']

        if data['issue']['assignee'] and data['sender']['login'] == data['issue']['assignee']['login']:
            senderColor = "green"
        else:
            senderColor = "dark grey"

        creator = ''
        if data['sender']['login'] != data['issue']['user']['login']:
            creator = " by %s" % (ircutils.mircColor(data['issue']['user']['login'],"green"),)

        milestone = ''
        if data['issue']['milestone'] and configValue("showMilestone"):
            milestone = ircutils.mircColor(" (%s" % (data['issue']['milestone']['title']),"brown")

        if milestone:
            oparen = '- '
        else:
            oparen = '('

        msgs.append( ircmsgs.privmsg(channel, "%s: %s %s issue %s \"%s\"%s%s %s%s)" % (
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['sender']['login'], senderColor),
        colorAction(data['action']),
        ''.join(["#",str(data['issue']['number'])]),
        ircutils.bold(data['issue']['title']),
        creator,
        milestone,
        oparen, url
        )) )

        return msgs

    def handle_issue_comment(s, irc, data, channel):
        msgs = []

        url = getShortURL(data['comment']['url'])


        creator = ''
        if data['sender']['login'] != data['issue']['user']['login']:
            creator = " by %s" % (ircutils.mircColor(data['issue']['user']['login'],"green"),)

        milestone = ''
        if data['issue']['milestone'] and configValue("showMilestone"):
            milestone = ircutils.mircColor(" (%s" % (data['issue']['milestone']['title']),"brown")

        if milestone:
            oparen = '- '
        else:
            oparen = '('

        lines = data['comment']['body'].splitlines()
        line = lines[0]
        if len(line) > 70:
                line = "%s..." % (line[0:67])
        elif len(lines) > 1:
                line += "..."

        msgs.append( ircmsgs.privmsg(channel, "%s: %s commented on issue %s \"%s\"%s%s %s%s): %s" % (
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['comment']['user']['login'], "green"),
        ''.join(["#",str(data['issue']['number'])]),
        ircutils.bold(data['issue']['title']),
        creator,
        milestone,
        oparen, url,
        line
        )) )

        return msgs

class Github(callbacks.Plugin):

    """Add the help for \"@plugin help Github\" here
    This should describe how to use this plugin."""

    travisCount = 0
    travisShown = False

    threaded = True
    pass

    def ServerStart(self, httpd):
        try:
            print time.asctime(), 'Server Starts - %s:%s' % ('', 8093)
            httpd.serve_forever()
        except:
            return

    def __init__(self, irc):
        self.__parent = super(Github, self)
        self.__parent.__init__(irc)
        self.rng = random.Random()  # create our rng
        self.rng.seed()  # automatically seeds with current time
        server_class = BaseHTTPServer.HTTPServer
        self.httpd = server_class(('', 8093), GithubHandler)
        t = threading.Thread(target=self.ServerStart, args=(self.httpd,))
        t.daemon = False
        t.start()

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)

    def die(self):
        self.httpd.server_close()
        self.httpd.shutdown()
        self.__parent.die()

    def create_dummy_request(self):
        server = xmlrpclib.Server('http://localhost:%s' % (8093))
        server.ping()

    def toast(self, irc, msg, args, seed, items):
        """<seed> <item1> [<item2> ...]

        Returns the next random number from the random number generator.
        """
        if seed < len(items):
            irc.error('<number of items> must be less than the number of arguments.')
            return
        irc.reply('%s %s %s' % (str(seed), str(self.rng.random()), utils.str.commaAndify(items)))

    toast = wrap(toast, ['float', many('anything')])


Class = Github

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
