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

import random
import json
import time
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

def colorAction(action):
    """Get an action string (e.g. created, edited) and get a nice IRC colouring"""
    if action == "created":
        return ircutils.bold(ircutils.mircColor(action, "green"))
    if action == "deleted":
        return ircutils.bold(ircutils.mircColor(action, "red"))
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
        return longurl
    data = 'url=%s' % (longurl)
    req = urllib2.Request("http://git.io", data)
    response = urllib2.urlopen(req)
    return response.info().getheader('Location')

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
        s.wfile.write('<html><head><title>Hello</title></head>')
        s.wfile.write("<body><p>Thanks, you're great.</p>")

        s.wfile.write('</body></html>')
        s.wfile.write(vars(s))
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        for irc in world.ircs:
            # Handle different event types

            msgs = []

            if 'pages' in data:
                msgs = s.handle_wiki(irc, data)
            elif 'commits' in data:
                msgs = s.handle_push(irc, data)
            else:
                msgs.append( ircmsgs.privmsg(configValue('channel'), "Something happened"))

            #msgs.append( ircmsgs.privmsg("#main", "%s" % ()) )
            for msg in msgs:
                    irc.queueMsg(msg)

    def handle_push(s, irc, data):
        msgs = []

        commitno = len(data['commits'])
        branch = data['ref'].split('/',2)[2]

        msgs.append( ircmsgs.privmsg(configValue('channel'), "%s @ %s: %s pushed %s %s (%s):" % (
        ircutils.bold(ircutils.mircColor(branch, "blue")),
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['pusher']['name'], "green"),
        ircutils.bold(str(commitno)),
        plural(commitno, "commit", "commits"),
        getShortURL(data['compare'])
        )) )

        for commit in data['commits']:
            if 'username' in commit['author']:
                author = commit['author']['username']
            else:
                author = commit['author']['name']

            msgs.append( ircmsgs.privmsg(configValue('channel'), "%s @ %s: %s * %s (%s)" % (
                ircutils.bold(ircutils.mircColor(branch, "blue")),
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(author, "green"),
                ircutils.bold(commit['id'][0:6]),
                getShortURL(commit['url']),
            )) )
            commitlines = commit['message'].splitlines()
            for rawline in commitlines:
                if len(rawline) > 400:
                    line = "%s..." % (rawline[0:397])
                else :
                    line = rawline
                    msgs.append(ircmsgs.privmsg(configValue('channel'), "%s @ %s: %s" % (
                        ircutils.bold(ircutils.mircColor(branch, "blue")),
                        ircutils.bold(data['repository']['name']),
                        line,
                    )) )

        return msgs

    def handle_wiki(s, irc, data):
        msgs = []

        pageno = len(data['pages'])

        url = getShortURL("%s/wiki/_compare/%s" % ( data['repository']['html_url'], data['pages'][0]['sha'] ))

        msgs.append( ircmsgs.privmsg(configValue('channel'), "%s: %s modified %s wiki %s (%s):" % (
        ircutils.bold(data['repository']['name']),
        ircutils.mircColor(data['sender']['login'], "green"),
        ircutils.bold(str(pageno)),
        plural(pageno, "page", "pages"),
        url
        )) )

        for page in data['pages']:
            # Unfortunately github doesn't support edit summaries :(
            msgs.append( ircmsgs.privmsg(configValue('channel'), "%s: %s %s %s * %s (%s)" % (
                ircutils.bold(data['repository']['name']),
                ircutils.mircColor(data['sender']['login'], "green"),
                colorAction(page['action']),
                ircutils.bold(ircutils.mircColor(page['page_name'], "blue")),
                ircutils.bold(page['sha'][0:6]),
                page['html_url'],
            )) )

        return msgs


class Github(callbacks.Plugin):

    """Add the help for \"@plugin help Github\" here
    This should describe how to use this plugin."""

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
        self.__parent.die()

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
