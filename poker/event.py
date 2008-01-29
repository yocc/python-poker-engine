EVENT_GAME_START        = 0
EVENT_GAME_END          = 1
EVENT_GAME_HAND_START   = 2
EVENT_GAME_HAND_END     = 3
EVENT_DEALT_FLOP        = 4 
EVENT_DEALT_TURN        = 5 
EVENT_DEALT_RIVER       = 6 
EVENT_PLAYER_DEALT_HOLE = 7
EVENT_PLAYER_WIN        = 8
EVENT_PLAYER_LOSE       = 9
EVENT_PLAYER_SITS       = 10
EVENT_PLAYER_CHATS      = 11

class Event:
    def __init__(self, type, game):
        self.type = type
        self.game = game
