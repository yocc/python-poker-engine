import unittest
import random

from poker.card import *

class CardTestCase(unittest.TestCase):
    """Tests the card module"""
    def test_deck_init(self):
        deck = range(52)
        for i in range(52):
            c = Card(i)
            self.assertEquals(c.rank, i % 13)
            self.assertEquals(c.suit, i / 13)

    def test_from_str(self):
        ace_spades = Card.from_str('As')
        ten_clubs = Card.from_str('Tc')
        three_hearts = Card.from_str('3h')
        four_spades = Card.from_str('4s')
        two_diamonds = Card.from_str('2d')

        self.assertEquals(ace_spades.suit, SPADES)
        self.assertEquals(ace_spades.rank, ACE)
        self.assertEquals(ten_clubs.suit, CLUBS)
        self.assertEquals(ten_clubs.rank, TEN)
        self.assertEquals(three_hearts.suit, HEARTS)
        self.assertEquals(three_hearts.rank, THREE)
        self.assertEquals(four_spades.suit, SPADES)
        self.assertEquals(four_spades.rank, FOUR)
        self.assertEquals(two_diamonds.suit, DIAMONDS)
        self.assertEquals(two_diamonds.rank, TWO)

    def test_invalid_from_str(self):
        self.assertRaises(CardFormatException, Card.from_str, '#$')
        self.assertRaises(CardFormatException, Card.from_str, 'A')    # not enough chars

    def test_cmp(self):
        ace_spades = Card.from_str('As')
        ten_clubs = Card.from_str('Tc')
        three_hearts = Card.from_str('3h')
        four_spades = Card.from_str('4s')
        two_diamonds = Card.from_str('2d')
        two_clubs = Card.from_str('2c')

        self.assertTrue(ace_spades > two_diamonds)
        self.assertTrue(ace_spades > ten_clubs)
        self.assertTrue(ace_spades > three_hearts)
        self.assertTrue(ace_spades > four_spades)
        self.assertTrue(three_hearts < ace_spades)
        self.assertTrue(three_hearts < four_spades)
        self.assertEquals(two_diamonds, two_clubs)

    def test_to_str(self):
        for i in range(52):
            c = Card(i)
            self.assertEquals(str(c), RANK_ABBR[c.rank]+SUIT_ABBR[c.suit])

if __name__ == '__main__':
    unittest.main()

