TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE = range(13)

DIAMONDS, HEARTS, CLUBS, SPADES = range(4)

RANK_ABBR = '23456789TJQKA'
SUIT_ABBR = 'dhcs'

RANK_NAME = ['two','three','four','five','six','seven',\
             'eight','nine','ten','jack','queen','king','ace']

SUIT_NAME = ['diamonds','hearts','clubs','spades']

class CardFormatException(Exception):
    """Invalid string representation; cannot convert to Card"""
    pass

class Card(object):
    """A playing card; e.g. ace of hearts, queen of spades, etc."""

    def __init__(self, val): 
        """val is a value in [0,52) where [0,12] represents the 2-A ranks
           in the diamonds suit, [13,25] hearts, [26-38] clubs, and [39,51]
           spades.  Generally one would just create a deck of cards like so:

           deck = range(52)
           random.shuffle(deck)
           top_card = Card(deck.pop())
        """
        self.suit = val / 13
        self.rank = val % 13

    def __cmp__(self, other): 
        """Cards are compared by their rank alone"""
        return cmp(self.rank, other.rank)

    def __str__(self): 
        """Essentially describe(long_fmt=False)"""
        return self.describe(long_fmt=False)

    def describe(self, long_fmt=False):
        """return description of card. If long_fmt is True then this returns
           something like 'ace of clubs' (cf. 'As')."""
        if long_fmt:
            return '%s of %s' % (RANK_NAME[self.rank], SUIT_NAME[self.suit])
        return RANK_ABBR[self.rank] + SUIT_ABBR[self.suit]

    @classmethod
    def from_str(cls, s):
        """return Card instance from a short format string representation 
           of the card such as 'Ac' or '3d'"""

        s = s.strip()

        if len(s) < 2:
            raise CardFormatException("need string with two characters")

        rank, suit = s[0], s[1]

        if   rank >= '2' and rank <= '9': rank = int(rank)-2
        elif rank == 'A': rank = ACE
        elif rank == 'T': rank = TEN
        elif rank == 'J': rank = JACK
        elif rank == 'Q': rank = QUEEN
        elif rank == 'K': rank = KING
        else: raise CardFormatException("unknown card rank '%s'" % rank)

        if   suit == 's': suit = SPADES
        elif suit == 'c': suit = CLUBS
        elif suit == 'd': suit = DIAMONDS
        elif suit == 'h': suit = HEARTS
        else: raise CardFormatException("unknown card suit '%s'" % suit)

        return Card(suit * 13 + rank)
