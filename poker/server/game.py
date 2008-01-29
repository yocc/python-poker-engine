import random

class Game:
    def __init__(self):
        self.deck = range(52)
        self.players = {}
        self.seats = {}
        self.min_players = 2
        self.max_players = 10
        self.ante = 0
        self.small_blind = 5
        self.big_blind = 10
        self.dealer = 0
        self.community = []

    def add_observer(self, obs):
        self.observers[obs] = 1

    def set_callbacks(self, action_cb, event_cb):
        self.action_cb = action_cb
        self.event_cb = event_cb

    def join(self, player):
        pass # TODO fail if no seats avail

    def start(self):
        pass # TODO fail if not enough players

    def standings(self):
        pass # TODO return players sorted by chips desc.

    def _newhand(self):
        self.deck = range(52)
        random.shuffle(self.deck)
