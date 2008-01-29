ACTION_FOLD, ACTION_BET, ACTION_CHECK = range(3)

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 0

    def __str__(self):
        return '%s (%d)' % (self.name, self.chips)
