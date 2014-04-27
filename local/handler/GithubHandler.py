import re
import json
import time
import random
import urllib
import urllib2
import urlparse
import threading
import BaseHTTPServer
from time import strftime

import supybot.log as log
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.registry as registry
import supybot.callbacks as callbacks

from ..utility import *

import PushHandler
import WikiHandler
import IssueHandler
import StatusHandler
import IssueCommentHandler

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

        if 'X-GitHub-Event' in s.headers:
            eventType = s.headers['X-GitHub-Event']
        else:
            eventType = ''

        f = open('requests/' + eventType + strftime("%Y-%m-%d %H:%M:%S") + '.json', 'w')
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
        f.close()

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
                msgs = WikiHandler.handle(irc, data, channel)
            elif 'state' in data:
                msgs = StatusHandler.handle(irc, data, channel)
            elif 'commits' in data:
                msgs = PushHandler.handle(irc, data, channel)
            elif 'issue' in data:
                if 'comment' in data:
                    msgs = IssueCommentHandler.handle(irc, data, channel)
                else:
                    msgs = IssueHandler.handle(irc, data, channel)
            else:
                msgs.append( ircmsgs.privmsg(channel, "Something happened"))

            #msgs.append( ircmsgs.privmsg("#main", "%s" % ()) )
            for msg in msgs:
                irc.queueMsg(msg)

    def log_message(self, format, *args):
        log.info(format % args)
