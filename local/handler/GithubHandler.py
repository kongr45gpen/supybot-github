import os
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
import TravisHandler
import CreateDeleteHandler
import IssueCommentHandler

from .. import theme as themes

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

        if not world.testing:
	    if not os.path.exists('requests/'):
		os.makedirs('requests')

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
        brackets = parseBrackets(configValue('brackets'))

        resetConfigOverrides()

        # Analyse the URL
        i = 0
        for part in path:
            part = urllib.unquote(part)
            if i == 1 and requireCode:
                receivedcode = part

            part = part.replace('+','#');
            part = part.replace('~','#');
            part = part.replace('&','#');
            part = part.replace('^','#');

            if part.startswith("#") and not configValue('disallowChannelOverride'):
                channel = part
            elif '=' in part and not configValue('disallowConfigOverride'):
                explosion = part.split('=', 1)
                addConfigOverride(explosion[0], explosion[1])

            i+=1

        if requireCode and receivedcode != configValue('passcode'):
            # The password is wrong
            s.wfile.write("The password is wrong")
            return

        themeName = configValue('theme')

        alphanumericPattern = re.compile('[\W_]+')
        themeClass = ''.join([alphanumericPattern.sub('', themeName).title(), 'Theme'])

        try:
            mod   = getattr(themes, themeClass)
            klass = getattr(mod, themeClass)
        except AttributeError:
            # The theme was not found
            log.error("The '%s' theme was not found" % themeName)
            klass = themes.DefaultTheme.DefaultTheme

        theme = klass(brackets)

        #
        # Handle different event types
        #
        msgs = []
        theme.msgs = msgs

        if 'matrix' in data:
            TravisHandler.handle(data, theme)
        elif 'pages' in data:
            WikiHandler.handle(data, theme)
        elif 'state' in data:
            StatusHandler.handle(data, theme)
        elif 'commits' in data:
            PushHandler.handle(data, theme)
        elif 'issue' in data:
            if 'comment' in data:
                IssueCommentHandler.handle(data, theme)
            else:
                IssueHandler.handle(data, theme)
        elif 'ref_type' in data:
            CreateDeleteHandler.handle(data, theme)
        else:
            msgs.append("Something happened")

        theme.finalize()

        saveMessages(msgs)

        if not world.testing:
            for msg in msgs:
                for irc in world.ircs:
                    irc.queueMsg(ircmsgs.privmsg(channel, msg))

    def log_message(self, format, *args):
        log.info(format % args)
