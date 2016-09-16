def init():
    global messageList
    global configOverrides
    global travisStatuses
    global secretDB
    global shownIssues
    global channel

    messageList = []
    configOverrides = {}
    travisStatuses = {}
    secretDB = None
    shownIssues = {}
    channel = None
