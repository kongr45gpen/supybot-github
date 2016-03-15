import os
import re
import hmac
import json
import time
import random
import urllib
import urllib2
import hashlib
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
        payload = s.rfile.read(length).decode('utf-8')
        if 'content-type' not in s.headers or s.headers['content-type'] == 'application/x-www-form-urlencoded':
            post_data = urlparse.parse_qs(payload)
            data = json.loads(post_data['payload'][0])
        else:
            data = json.loads(payload)

        if 'X-GitHub-Event' in s.headers:
            eventType = s.headers['X-GitHub-Event']
        else:
            eventType = ''

        if not world.testing:
            if not os.path.exists('requests/'):
                os.makedirs('requests')

            f = open('requests/' + eventType.replace('/','_') + strftime("%Y-%m-%d %H:%M:%S") + '.json', 'w')
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            f.close()

        path = s.path.split('/')
        channel = configValue('channel')
        receivedcode = ''
        requireCode = configValue('passcode').strip() \
            and configValue('passcode').strip().lower() != 'false' \
            and configValue('passcode').strip().lower() != 'null' \
            and configValue('passcode').strip().lower() != 'no'

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

        s.send_response(200)
        s.send_header('Content-type', 'text/html')
        s.end_headers()
        s.wfile.write("Thanks, you're awesome.\n")
        s.wfile.write(s.path.split('/'))

        if requireCode and receivedcode != configValue('passcode'):
            # The password is wrong
            s.wfile.write("The password is wrong")
            return

        secret = getChannelSecret(channel)
        if secret is not None:
            if not 'X-Hub-Signature' in s.headers:
                s.wfile.write("This channel requires a secret")
                return

            digest = "sha1=%s" % (hmac.new(secret, payload, hashlib.sha1).hexdigest(),)
            log.debug("expected digest: %s", digest)

            provided = s.headers['X-Hub-Signature']
            log.debug("provided digest: %s", provided)

            if not secureCompare(digest, provided):
                s.wfile.write("Invalid secret key")
                return

        brackets = parseBrackets(configValue('brackets'))
        themeName = configValue('theme')

        alphanumericPattern = re.compile('[\W_]+')
        themeClass = ''.join([alphanumericPattern.sub('', themeName).title(), 'Theme'])

        # Find the theme's class
        try:
            mod   = getattr(themes, themeClass)
            klass = getattr(mod, themeClass)
        except AttributeError:
            # The theme was not found
            log.error("The '%s' theme was not found" % themeName)
            klass = themes.DefaultTheme.DefaultTheme

        repo = {}

        repo['name']  = data.get('repository',{}).get('name')
        repo['owner'] = data.get('repository',{}).get('owner',{}).get('login')
        repo['fork']  = data.get('repository',{}).get('fork', False)
        theme = klass(repo, brackets)

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
            theme.unknown(eventType)

        theme.finalize()

        saveMessages(msgs)

        if not world.testing:
            for msg in msgs:
                for irc in world.ircs:
                    irc.queueMsg(ircmsgs.privmsg(channel, msg))

    def log_message(self, format, *args):
        log.info(format % args)
