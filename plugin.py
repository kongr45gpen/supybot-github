###

import random
import json
import time
import threading
import BaseHTTPServer

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

class GithubHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_POST(s):
		"""Respond to a POST request."""
		length = int(s.headers['Content-Length'])
		data = json.loads(s.rfile.read(length).decode('utf-8'))

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><head><title>Hello</title></head>")
		s.wfile.write("<body><p>Thanks, you're great.</p>")
		#s.wfile.write("<p>POST: You accessed path: %s</p>" % s.path)
		s.wfile.write("</body></html>")
		s.wfile.write(vars(s))
		print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

class Github(callbacks.Plugin):
    """Add the help for "@plugin help Github" here
    This should describe how to use this plugin."""
    threaded = True
    pass

    def ServerStart(meh):
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('', 8093), GithubHandler)
	print time.asctime(), "Server Starts - %s:%s" % ('', 8093)
        httpd.serve_forever()

    def __init__(self, irc):
	    self.__parent = super(Github, self)
	    self.__parent.__init__(irc)
	    self.rng = random.Random()   # create our rng
	    self.rng.seed()   # automatically seeds with current time
	    t = threading.Thread(target=self.ServerStart)
	    t.daemon = True
	    t.start()
	    
    
    def __call__(self, irc, msg):
	self.__parent.__call__(irc, msg)
	print "I have no idea what is happeninig"

    def toast(self, irc, msg, args, seed, items):
		"""<seed> <item1> [<item2> ...]

		Returns the next random number from the random number generator.
		"""
		if seed < len(items):
			irc.error('<number of items> must be less than the number of arguments.')
			return
		irc.reply(str(seed) + str(self.rng.random()) + utils.str.commaAndify(items))
    toast = wrap(toast,['float', many('anything')])


Class = Github


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
