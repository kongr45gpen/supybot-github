from ..utility import *

def handle(data, theme):
    theme.ping(
        message = data['zen'],
        zen = not configValue('allowArbitraryMessages')
    )
