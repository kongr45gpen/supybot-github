import os
import re
import hmac
import json
import time
import random
import socket
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import hashlib
import urllib.parse
import threading
import http.server
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

from ..globals import *
from ..utility import *

from . import PingHandler
from . import PushHandler
from . import WikiHandler
from . import IssueHandler
from . import StatusHandler
from . import TravisHandler
from . import MessageHandler
from . import NetlifyHandler
from . import ReleaseHandler
from . import UnknownHandler
from . import AppVeyorHandler
from . import CreateDeleteHandler
from . import IssueCommentHandler

from .. import theme as themes

#TODO: Use a better name and location for this
class GithubHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(s):
        """Respond to a POST request."""
        length = int(s.headers['Content-Length'])
        payload = s.rfile.read(length).decode('utf-8')
        if 'content-type' not in s.headers or s.headers['content-type'] == 'application/x-www-form-urlencoded':
            post_data = urllib.parse.parse_qs(payload)
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
            part = urllib.parse.unquote(part)
            if i == 1 and requireCode:
                receivedcode = part

            part = part.replace('+','#')
            part = part.replace('~','#')
            part = part.replace('&','#')
            part = part.replace('^','#')

            # TODO: Throw out a warning when a URL specifies a configuration
            # value but we don't allow that
            if part.startswith("#") and not configValue('disallowChannelOverride'):
                channel = part
            elif '=' in part and not configValue('disallowConfigOverride'):
                explosion = part.split('=', 1)
                addConfigOverride(explosion[0], explosion[1])

            i+=1
        globals.channel = channel

        try:
            s.send_response(200)
            s.send_header('Content-type', 'text/plain')
            s.end_headers()
            s.wfile.write("Thanks!\n".encode())
            s.wfile.write(repr(s.path.lstrip('/').split('/')).encode())
            s.wfile.write("\n".encode())
        except socket.error:
            pass

        if requireCode and receivedcode != configValue('passcode'):
            # The password is wrong
            s.wfile.write("The password is wrong\n".encode())
            return

        # Handle Github secrets
        secret = getChannelSecret(channel)
        if secret is not None:
            if not 'X-Hub-Signature' in s.headers:
                s.wfile.write("This channel requires a secret\n".encode())
                return

            digest = "sha1=%s" % (hmac.new(secret, payload, hashlib.sha1).hexdigest(),)
            log.debug("expected digest: %s", digest)

            provided = s.headers['X-Hub-Signature']
            log.debug("provided digest: %s", provided)

            if not secureCompare(digest, provided):
                s.wfile.write("Invalid secret key\n".encode())
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

        repo['unknown'] = 'repository' not in data
        repo['name']    = data.get('repository',{}).get('name')
        repo['owner']   = data.get('repository',{}).get('owner',{}).get('login')
        repo['fork']    = data.get('repository',{}).get('fork', False)
        repo['id']      = data.get('repository',{}).get('id', "%s/%s" % (repo['owner'], repo['name']))
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
        elif 'screenshot_url' in data:
            NetlifyHandler.handle(data, theme)
        elif 'state' in data:
            StatusHandler.handle(data, theme)
        elif 'commits' in data:
            PushHandler.handle(data, theme)
        elif 'issue' in data or 'pull_request' in data:
            if 'comment' in data:
                IssueCommentHandler.handle(data, theme)
            else:
                IssueHandler.handle(data, theme)
        elif 'ref_type' in data:
            CreateDeleteHandler.handle(data, theme)
        elif 'release' in data:
            ReleaseHandler.handle(data, theme)
        elif 'zen' in data:
            PingHandler.handle(data, theme)
        elif 'message' in data:
            MessageHandler.handle(data, theme)
        elif 'eventName' in data:
            AppVeyorHandler.handle(data, theme)
        else:
            data['eventType'] = eventType
            UnknownHandler.handle(data, theme)

        theme.finalize()

        saveMessages(msgs)

        if not world.testing:
            for msg in msgs:
                for irc in world.ircs:
                    irc.queueMsg(ircmsgs.privmsg(channel, msg))

    def finish(self):
        try:
            if not self.wfile.closed:
                self.wfile.flush()
            self.wfile.close()
            self.rfile.close()
        except socket.error:
            # An final socket error may have occurred here, such as a broken
            # pipe
            pass

    def log_message(self, format, *args):
        log.info(format % args)
