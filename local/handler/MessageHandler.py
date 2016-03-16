from ..utility import *

def handle(data, theme):
    if configValue('allowArbitraryMessages'):
        theme.message(data['message'])
