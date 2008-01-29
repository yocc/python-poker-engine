import random

UNKNOWN, HIGHCARD, PAIR, TWOPAIR, SET, STRAIGHT, FLUSH, FULLHOUSE, QUADS, STRAIGHTFLUSH = range(10)
TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(13)
RANK_ABBR = '23456789TJQKA'
SUIT_ABBR = 'dhcs'
RANK_NAME = ['two','three','four','five','six','seven','eight','nine','ten','jack','queen','king','ace']
SUIT_NAME = ['diamonds','hearts','clubs','spades']
DIAMONDS, HEARTS, CLUBS, SPADES = range(4)

from pprint import pprint

def plural(r_str):
    """make a rank name plural"""
    if r_str == 'six': return r_str + 'es'
    return r_str + 's'

class Card:
    """a playing card; e.g. ace of hearts, queen of spades, etc."""

    def __init__(self, val): 
        self.suit = val / 13
        self.rank = val % 13

    def __cmp__(self, other): 
        return cmp(self.rank, other.rank)

    def __str__(self): 
        return RANK_ABBR[self.rank] + SUIT_ABBR[self.suit]

    def get_desc(self):
        """return long description of card; e.g. 'ace of clubs'"""
        return '%s of %s' % (RANK_NAME[self.rank], SUIT_NAME[self.suit])

class Hand:
    """holds a set of cards and can determine if they comprise various poker hands"""

    def __init__(self):
        self.reset()

    @classmethod
    def from_str(cls, str):
        h = Hand()

        for c in str.split():
            r,s = c[0],c[1]

            if r >= '2' and r <= '9': r = int(r)-2
            elif r == 'A': r = ACE
            elif r == 'T': r = TEN
            elif r == 'J': r = JACK
            elif r == 'Q': r = QUEEN
            elif r == 'K': r = KING

            if s == 's': s = SPADES
            elif s == 'c': s = CLUBS
            elif s == 'd': s = DIAMONDS
            elif s == 'h': s = HEARTS

            h.add_card(Card(s*13+r))

        return h

    def reset(self):
        """remove cards from hand"""
        self.cards = []
        self.dirty = False
        self.type = UNKNOWN
        self.ranks = []             # desc. order
        self.desc = ''

    def add_card(self, card):
        """adds a card to the hand. avoid accessing the cards directly"""
        self.cards.append(card)
        self.dirty = True

    def get_type(self):
        """returns one of HIGHCARD, PAIR, etc. requires at least 5 cards in the hand"""
        if not self.dirty: return self.type
        self._analyze()
        return self.type

    def get_desc(self):
        """returns description of hand such as 'ace-high' or 'pair of tens'"""
        if self.dirty: self._analyze()
        return self.desc

    def __cmp__(self, other):
        """compare hands following standard poker hand rankings, including kickers."""
        if other == None: return 0
        type = self.get_type()
        other_type = other.get_type()
        n = cmp(type, other_type)
        if n != 0: return n
        if self.ranks < other.ranks: return -1
        return 1

    def __str__(self):
        """returns simple string representation of hand such as 'Ah 3d Tc 9s Ac'"""
        if self.dirty: self._analyze()
        return ' '.join([str(c) for c in self.cards])

    def _analyze(self):
        """determine the best hand possible given the current set of cards"""
        self.dirty = False
        if len(self.cards) < 5: return
        r2c = {}
        s2c = {}
        for c in self.cards: r2c.setdefault(c.rank, []).append(c)
        for c in self.cards: s2c.setdefault(c.suit, []).append(c)
        for r in r2c: 
            r2c[r].sort()
            r2c[r].reverse()
        for s in s2c: 
            s2c[s].sort()
            s2c[s].reverse()
        self._find_straightflush(r2c,s2c) or \
        self._find_quads(r2c,s2c) or \
        self._find_fullhouse(r2c,s2c) or \
        self._find_flush(r2c,s2c) or \
        self._find_straight(r2c,s2c) or \
        self._find_set(r2c,s2c) or \
        self._find_twopair(r2c,s2c) or \
        self._find_pair(r2c,s2c) or \
        self._find_highcard(r2c,s2c)

    def _largest_rank_with_n(self, r2c, n, ignore0 = -1, ignore1 = -1):
        """return the largest rank such that n cards have the rank"""
        for r in range(ACE,TWO-1,-1):
            if r != ignore0 and r != ignore1 and len(r2c.get(r, [])) == n: return r
            r = r - 1
        return False

    def _find_kickers(self, n, ignore0 = -1, ignore1 = -1):
        """find n 'kicker' cards that do not have rank ignore1 nor ignore2"""
        ranks = [c.rank for c in self.cards if c.rank != ignore0 and c.rank != ignore1]
        ranks.sort()
        ranks.reverse()
        return ranks[0:n]

    def _find_straightflush(self,r2c,s2c): 
        if not self._find_straight(r2c,s2c): return False
        for s in range(4):
            if len(s2c.get(s,[])) >= 5:
                self.type = STRAIGHTFLUSH
                if self.ranks[0] == ACE: self.desc = 'royal flush'
                else: self.desc = '%s-high straight flush' % RANK_NAME[self.ranks[0]]
                return True
        return False

    def _find_quads(self,r2c,s2c): 
        r = self._largest_rank_with_n(r2c, 4)
        if not r: return False
        self.type = QUADS
        self.ranks = [r,r,r,r] + self._find_kickers(1, r)
        self.desc = 'four of a kind (%s)' % plural(RANK_NAME[r])
        return True

    def _find_fullhouse(self,r2c,s2c): 
        trip_rank = self._largest_rank_with_n(r2c, 3)
        if not trip_rank: return False
        pair_rank = self._largest_rank_with_n(r2c, 2, trip_rank)
        if not pair_rank: return False
        self.type = FULLHOUSE
        self.ranks = [trip_rank, trip_rank, trip_rank, pair_rank, pair_rank]
        self.desc = 'full house (%s over %s)' % (plural(RANK_NAME[max(trip_rank, pair_rank)]), 
                                                 plural(RANK_NAME[min(trip_rank, pair_rank)]))
        return True

    def _find_flush(self,r2c,s2c): 
        for s in range(4):
            if len(s2c.get(s,[])) >= 5:
                self.type = FLUSH
                self.ranks = [c.rank for c in s2c[s][0:5]]
                self.desc = '%s-high flush' % RANK_NAME[self.ranks[0]]
                return True
        return False

    def _find_straight(self,r2c,s2c):
        r, n = ACE, 0
        while r >= TWO:
            if len(r2c.get(r, [])) > 0:
                n = n + 1
                if n == 5: break
            else:
                n = 0
            r = r - 1
        found = False
        if n == 5:
            found = True
            self.ranks = range(r + n - 1, r, -1)
        elif n == 4 and r < TWO and len(r2c.get(ACE, [])) > 0:
            self.ranks = [FIVE, FOUR, THREE, TWO, ACE]
            found = True
        if found:
            self.type = STRAIGHT
            self.desc = '%s-high straight' % RANK_NAME[self.ranks[0]]
        return found

    def _find_set(self,r2c,s2c): 
        r = self._largest_rank_with_n(r2c, 3)
        if not r: return False
        self.type = QUADS
        self.ranks = [r,r,r,r] + self._find_kickers(1, r)
        self.desc = 'three of a kind (%s)' % plural(RANK_NAME[r])
        return True

    def _find_twopair(self,r2c,s2c): 
        r0 = self._largest_rank_with_n(r2c, 2)
        if not r0: return False
        r1 = self._largest_rank_with_n(r2c, 2, r0)
        if not r1: return False
        self.type = TWOPAIR
        min_r, max_r = (min(r0,r1), max(r0,r1))
        self.ranks = [max_r, max_r, min_r, min_r] + self._find_kickers(1, r0, r1)
        self.desc = 'two pair (%s and %s)' % (plural(RANK_NAME[max_r]), plural(RANK_NAME[min_r]))
        return True

    def _find_pair(self,r2c,s2c): 
        r = self._largest_rank_with_n(r2c, 2)
        if not r: return False
        self.type = PAIR
        self.ranks = [r,r] + self._find_kickers(3, r)
        self.desc = 'pair of %s' % plural(RANK_NAME[r])
        return True

    def _find_highcard(self,r2c,s2c):
        self.type = HIGHCARD
        self.ranks = self._find_kickers(5)
        self.desc = '%s-high' % RANK_NAME[self.ranks[0]]
        return True

ACTION_FOLD, ACTION_BET, ACTION_CHECK = range(3)

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 0

    def __str__(self):
        return '%s (%d)' % (self.name, self.chips)

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

