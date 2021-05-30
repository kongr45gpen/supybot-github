import supybot.conf as conf
import supybot.log as log
import supybot.registry as registry
import supybot.world as world
import supybot.test as test
import supybot.callbacks as callbacks
from local.handler.GithubHandler import GithubHandler
import time
import re
import sys
import json

# ANSI colour codes from https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32
    ColourAssignment = {
        "02": BLUE,
        "03": GREEN,
        "04": LIGHT_RED,
        "05": RED,
        "06": PURPLE,
        "07": BROWN,
        "08": YELLOW,
        "09": GREEN,
        "10": CYAN,
        "11": LIGHT_CYAN,
        "12": LIGHT_BLUE,
        "13": LIGHT_PURPLE,
        "14": DARK_GRAY,
        "15": LIGHT_GRAY
    }

# Configure plugin
from config import configure
configure(False)

log.testing = False
world.testing = False

conf.registerNetwork("test")
# conf.supybot.log.stdout.level.setValue(0)
# log._stdoutHandler.setLevel(0)

irc = test.getTestIrc()

# Import all relevant and required modules
import __init__

# Initialise and run the plugin object
from plugin import Github
object = Github(irc)
irc.addCallback(object)

def printmsgs():
    ircmsg = irc.takeMsg()

    if ircmsg:
        msg = ircmsg.args[1]

        # Convert mIRC colour codes to ANSI colour codes for terminal viewing
        msg = re.sub(r"\u0002(.*?)\u0002", Colors.BOLD + r"\1" + Colors.END, msg)
        for ircColour, ansiColour in Colors.ColourAssignment.items():
            msg = re.sub(r"\u0003(" + ircColour + ")(.*?)\u0003", ansiColour + r"\2" + Colors.END, msg)

        print(msg)

if len(sys.argv) > 1:
    # Argument provided. Run it and bail
    string = open(sys.argv[1], 'r').read()
    data = json.loads(string)
    log._stdoutHandler.setLevel(0)
    GithubHandler.process_data(data, "##none")
    printmsgs()
    log.setLevel("WARNING")
    object.die()
else:
    while True:
        time.sleep(0.05) # polling
        printmsgs()
