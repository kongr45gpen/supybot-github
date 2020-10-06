###
from supybot.ircutils import stripFormatting
from supybot.log import info
from supybot.test import *

from copy import deepcopy

from sys import stdout
from time import sleep

import re
import urllib.request, urllib.parse, urllib.error

class ExpectationPluginTestCase(PluginTestCase):
    plugins       = {}

    def describe(self, query, *args):
        m = self._feedMsg('get ' + query)
        manyEs = tcolors.FAIL + 'E' * len(args) + tcolors.ENDC
        if m is None:
            print(manyEs)
            raise TimeoutError(query)
        if m.args[1].startswith('Error:'):
            print(manyEs)
            self.fail('%r errored: %s' % (query, m.args[1]))

        errors = []
        for expectation in args:
            expectation.reply = m.args[1]
            if expectation.evaluate():
                stdout.write(tcolors.OKGREEN + '.' + tcolors.ENDC)
            else:
                stdout.write(tcolors.FAIL + 'F' + tcolors.ENDC)
                errors.append(expectation.getSummary())
            stdout.flush()
        stdout.write('')
        stdout.flush()

        if errors:
            print("\n%sWhile describing %s" % (tcolors.FAIL, query))
            for error in errors:
                print("- Failed to assert that %s" % (error,))
            print(tcolors.ENDC)
            self.fail("%i assertions failed while describing %s" % (len(errors), query))

    def sendRequest(self, file):
        """ Opens the `samples` folder and sends a file as a request
            to the plugin's server """
        if file in self.files:
            content = self.files[file]
        else:
            with open('samples/' + file + '.json', 'r') as content_file:
                content = content_file.read()
            self.files[file] = content
        content = bytes('payload=' + content, 'utf-8')
        urllib.request.urlopen('http://localhost:' + str(self.port), content)
        # Tests on Travis fail randomly, so let's slow things down...
        sleep(1)

    def conf(self, name, value):
        """Sets one of the plugin's configuration values"""
        conf.supybot.plugins.get("Github").get(name).setValue(value)

    def testDocumentation(self):
        if self.__class__ == ExpectationPluginTestCase:
            return
        else:
            PluginTestCase.testDocumentation(self)

    def setUp(self):
        # Prevent supybot's testDocumentation from going mad
        PluginTestCase.setUp(self)

    def tearDown(self):
        # Add a space between our LEDs and python's OK message
        PluginTestCase.tearDown(self)
        stdout.write(' ')
        stdout.flush()

class tcolors:
    HEADER  = '\033[95m'
    OKBLUE  = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL    = '\033[91m'
    ENDC    = '\033[0m'

def expect(query):
    m = GithubTestCase._feedMsg('get' + query)
    return Expectation(m.args[1])

def it():
    return Expectation()

class Expectation(object):
    def __init__(self):
        self.error = ''
        self.negation = False

        self.should = self
        self.to     = self
        self.should_not = self.negate()

    def evaluate(self):
        if self.negation is True:
            return not self.assertion()
        else:
            return self.assertion()

    def negate(self):
        other = deepcopy(self)
        other.negation = not other.negation
        return other

    def cleanReply(self):
        return ircutils.stripFormatting(self.reply)

    def getSummary(self):
        if self.assertionParameter:
            return self.summary % (self.cleanReply(), self.assertionParameter)
        else:
            return self.summary % (self.cleanReply())

    def contain(self, what):
        self.assertion = self.contains
        self.assertionParameter = what
        if self.negation:
            verb = "does not contain"
        else:
            verb = "contains"
        self.summary = "'%s' " +verb+ " '%s'"
        return self

    def contains(self, flags=re.I):
        return re.search(self.assertionParameter, self.cleanReply(), flags)

class Object(object):
    pass
