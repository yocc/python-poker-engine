GAME_START        = 0
GAME_END          = 1
GAME_HAND_START   = 2
GAME_HAND_END     = 3
DEALT_FLOP        = 4 
DEALT_TURN        = 5 
DEALT_RIVER       = 6 
PLAYER_DEALT_HOLE = 7
PLAYER_WIN        = 8
PLAYER_LOSE       = 9
PLAYER_SITS       = 10
PLAYER_CHATS      = 11

# TODO use pyglet.event.EventDispatcher

class Event:
    def __init__(self, type, game):
        self.type = type
        self.game = game
