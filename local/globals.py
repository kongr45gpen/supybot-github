def init():
    global messageList
    global configOverrides
    global travisStatuses
    global secretDB
    global shownIssues

    messageList = []
    configOverrides = {}
    travisStatuses = {}
    secretDB = None
    shownIssues = {}
