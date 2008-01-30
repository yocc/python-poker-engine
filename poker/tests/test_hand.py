import unittest

from poker.hand import *

test_hands = [
    ( 'Ac Qd Jh 4c 2c', HIGHCARD,      'ace-high'                       ),
    ( 'Ac Ad 8h 7c Tc', PAIR,          'pair of aces'                   ),
    ( 'Ac Ad 8h 7c 7s', TWOPAIR,       'two pair (aces and sevens)'     ),
    ( '8s 8d 8h 7c Tc', SET,           'three of a kind (eights)'       ),
    ( '8c 7d 6h 5c 4c', STRAIGHT,      'eight-high straight'            ),
    ( 'Ac 2d 3h 4c 5c', STRAIGHT,      'five-high straight'             ),
    ( 'Ac Jd Kh Tc Qc', STRAIGHT,      'ace-high straight'              ),
    ( '8c 6c 5c Qc Jc', FLUSH,         'queen-high flush'               ),
    ( '8c 8d 8h 6d 6h', FULLHOUSE,     'full house (eights over sixes)' ),
    ( 'Qc Qd Qh Qs 6h', QUADS,         'four of a kind (queens)'        ),
    ( 'Ah 4h 2h 3h 5h', STRAIGHTFLUSH, 'five-high straight flush'       ),
    ( 'Ac Jc Kc Tc Qc', STRAIGHTFLUSH, 'royal flush'                    ),
    ( "Ah 6d 4c 3s 2h 2s 2c",  SET, "three of a kind (twos)" ),
    ( "Qs Js Tc 9s 8d 7s 3s",  FLUSH, "queen-high flush" ),
    ( "Kc Qc 8c 7c 6s 5c 4s",  FLUSH, "king-high flush" ),

    # TODO please add a LOT more...
    # One idea would be to generate random hands along with what the hand 
    # evaluator thinks the hand is, verify that the type is correct manually
    # by looking at it yourself, then add the verified hands and their 
    # descriptions here...  see test-randomness.py for a start.
]

FIRST, SECOND, SPLIT = range(3)

class HandTestCase(unittest.TestCase):
    """Tests the hand module"""

    def runTest(self):
        self.test_hands()
        self.test_invalid_hand_string_rep()
        self.test_random_hand()
        self.test_hand_comparisons()
        self.test_internal_analysis_string()

    def test_hands(self):
        for entry in test_hands:
            card_str, type, desc = entry
            h = Hand.from_str(card_str)
            self.assertEquals(str(h), card_str,   msg = '%s: %s expected %s' % (card_str, str(h), card_str))
            self.assertEquals(h.get_type(), type, msg = '%s: %s expected %s' % (card_str, TYPE_NAMES[h.get_type()], TYPE_NAMES[type]))
            self.assertEquals(h.describe(), desc, msg = '%s: %s expected %s' % (card_str, h.describe(), desc))

    def test_invalid_hand_string_rep(self):
        self.assertRaises(CardFormatException, Hand.from_str, 'hi there')
        self.assertRaises(HandFormatException, Hand.from_str, 'As Qd')     # not enough cards

    def test_random_hand(self):
        h = Hand.random()
        self.assertTrue(len(h.cards) == 7)

    def _winner(self, s1, s2):
        h1, h2 = Hand.from_str(s1), Hand.from_str(s2)
        if h1 > h2: return FIRST
        if h1 < h2: return SECOND
        return SPLIT

    def test_hand_comparisons(self):
        self.assertEquals(self._winner('Ac Qd Jh 4c 2c', 'Qd Tc 4h 6s 9d'), FIRST)
        self.assertEquals(self._winner('Ac Qd Jh 4c 2c', 'Ad Tc 4h 6s 9d'), FIRST)  # test kickers
        self.assertEquals(self._winner('Ac Qd Jh 4c 2c', 'Ad 8c Qh Js 9d'), SECOND) # test kickers
        self.assertEquals(self._winner('Ac Qd Jh 4c 2c', 'Ad Tc 4h As 9d'), SECOND)
        self.assertEquals(self._winner('2c 2d 4h 4c 8c', '2c 2d 4h 4c 8c'), SPLIT)
        self.assertEquals(self._winner('2c 2d 4h 4c 9c', '2c 2d 4h 4c 8c'), FIRST)  # test kickers
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac Qd Jh 4c 2c'), FIRST)  # royal flush beats everything
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c Tc'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c 7s'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', '8c 8d 8h 7c Tc'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', '8c 7d 6h 5c 4c'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac 2d 3h 4c 5c'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac Jd Kh Tc Qc'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', '8c 6c 5c Qc Jc'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', '8c 8d 8h 6d 6h'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Qc Qd Qh Qs 6h'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ah 4h 2h 3h 5h'), FIRST)
        self.assertEquals(self._winner('Ac Jc Kc Tc Qc', 'Ac Jc Kc Tc Qc'), SPLIT)
        self.assertEquals(self._winner('9c 8d 7h 6c 5c', '8c 7d 6h 5c 4c'), FIRST)  # high card in straights win
        self.assertEquals(self._winner('9c 8c 7c 6c 5c', '8c 7c 6c 5c 4c'), FIRST)  # high card in straight flushes win
        self.assertEquals(self._winner('Jc Js Td Th Tc', 'Qc Qd Qh Qs 6h'), SECOND) # 4-kind beats full house
        self.assertEquals(self._winner('Jc Js Jd Jh Tc', 'Qc Qd Qh Qs 6h'), SECOND) # higher rank in 4 of a kind wins
        self.assertEquals(self._winner('Ac As Ad 6h 6c', 'Qc Qd Qh Ts Th'), FIRST)  # higher rank in Fh wins
        self.assertEquals(self._winner('Ac As Ad 6h 6c', 'Ac Ad Ah Ts Th'), SECOND) # higher rank in Fh wins
        self.assertEquals(self._winner('Ac As Ad 6h 6c', 'Ac Ad Ah 6s 6h'), SPLIT)
        self.assertEquals(self._winner('6c Tc Qc 2c 9c', 'Kh 4h 9h Jh 8h'), SECOND) # high card in flush wins

    def test_internal_analysis_string(self):
        h = Hand.random()
        s = h._analysis_to_str()
        self.assertTrue(s != None)   # bah
