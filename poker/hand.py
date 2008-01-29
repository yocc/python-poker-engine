import random
from card import Card

def _plural(r_str):
    """make a rank name _plural"""
    if r_str == 'six': return r_str + 'es'
    return r_str + 's'

class Hand:
    """holds a set of cards and can determine if they comprise various poker hands"""

    def __init__(self):
        self.cards = []
        self.dirty = False
        self.type = UNKNOWN
        self.ranks = []             # desc. order
        self.desc = ''

    @classmethod
    def random(cls,n=7):
        """creates a random hand of N cards"""
        deck = range(52)
        random.shuffle(deck)
        h = Hand()
        for i in range(7): h.add_card(Card(deck.pop()))
        return h

    @classmethod
    def from_abbrev_str(cls, str):
        """Creates a hand from a string like 'Ad Th 3s 5c 7d 8d Qc'"""
        h = Hand()
        for c in [Card.from_abbrev_str(part) for part in str.split()]:
            h.add_card(c)
        return h

    def abbrev_desc(self):
        """returns a abbreviated string representation of the hand's cards as in 
           'Ad Th 3s 5c 7d 8d Qc'"""
        return ' '.join([c.abbrev_desc() for c in self.cards])

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
        type = self.get_type()
        other_type = other.get_type()
        n = cmp(type, other_type)
        if n != 0: return n
        if self.ranks == other.ranks: return 0
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
        return r2c, s2c

    def _analysis_to_str(self):
        r2c, s2c = self._analyze()
        str = "r2c:\n"
        for r in r2c:
            str += '> %s: %s' % (RANK_ABBR[r], ' '.join([c.abbrev_desc() for c in r2c[r]]))
            str += '\n'
        str += "s2c:\n"
        for s in s2c:
            str += '> %s: %s' % (SUIT_ABBR[s], ' '.join([c.abbrev_desc() for c in s2c[s]]))
            str += '\n'
        return str

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
        self.desc = 'four of a kind (%s)' % _plural(RANK_NAME[r])
        return True

    def _find_fullhouse(self,r2c,s2c): 
        trip_rank = self._largest_rank_with_n(r2c, 3)
        if not trip_rank: return False
        pair_rank = self._largest_rank_with_n(r2c, 2, trip_rank)
        if not pair_rank: return False
        self.type = FULLHOUSE
        self.ranks = [trip_rank, trip_rank, trip_rank, pair_rank, pair_rank]
        self.desc = 'full house (%s over %s)' % (_plural(RANK_NAME[max(trip_rank, pair_rank)]), 
                                                 _plural(RANK_NAME[min(trip_rank, pair_rank)]))
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
        self.desc = 'three of a kind (%s)' % _plural(RANK_NAME[r])
        return True

    def _find_twopair(self,r2c,s2c): 
        r0 = self._largest_rank_with_n(r2c, 2)
        if not r0: return False
        r1 = self._largest_rank_with_n(r2c, 2, r0)
        if not r1: return False
        self.type = TWOPAIR
        min_r, max_r = (min(r0,r1), max(r0,r1))
        self.ranks = [max_r, max_r, min_r, min_r] + self._find_kickers(1, r0, r1)
        self.desc = 'two pair (%s and %s)' % (_plural(RANK_NAME[max_r]), _plural(RANK_NAME[min_r]))
        return True

    def _find_pair(self,r2c,s2c): 
        r = self._largest_rank_with_n(r2c, 2)
        if not r: return False
        self.type = PAIR
        self.ranks = [r,r] + self._find_kickers(3, r)
        self.desc = 'pair of %s' % _plural(RANK_NAME[r])
        return True

    def _find_highcard(self,r2c,s2c):
        self.type = HIGHCARD
        self.ranks = self._find_kickers(5)
        self.desc = '%s-high' % RANK_NAME[self.ranks[0]]
        return True
