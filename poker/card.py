class Card(object):
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

    @classmethod
    def from_abbrev_str(cls, str):
        """return Card instance from an abbreviated string representation of the card
           such as 'Ac' or '3d'"""
        r, s = str[0], str[1]

        if r >= '2' and r <= '9': r = int(r)-2
        elif r == 'A': r = ACE
        elif r == 'T': r = TEN
        elif r == 'J': r = JACK
        elif r == 'Q': r = QUEEN
        elif r == 'K': r = KING

        if   s == 's': s = SPADES
        elif s == 'c': s = CLUBS
        elif s == 'd': s = DIAMONDS
        elif s == 'h': s = HEARTS

        return Card(s * 13 + r)

    def abbrev_desc(self):
        """returns a string containing an abbreviated version of the card such as 'Ac' or '3d'"""
        return '%c%c' % (RANK_ABBR[self.rank], SUIT_ABBR[self.suit])
