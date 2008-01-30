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
    ( 'Ac Jc Kc Tc Qc', STRAIGHTFLUSH, 'royal flush'                    ) 

    # TODO please add a LOT more...
    # One idea would be to generate random hands along with what the hand 
    # evaluator thinks the hand is, verify that the type is correct manually
    # by looking at it yourself, then add the verified hands and their 
    # descriptions here...  see test-randomness.py for a start.
]

FIRST, SECOND, SPLIT = range(3)

class HandTestCase(unittest.TestCase):
    """Tests the hand module"""

    def test_hands(self):
        for entry in test_hands:
            card_str, type, desc = entry
            h = Hand.from_str(card_str)
            #print card_str, ' vs ', str(h)
            #print h._analysis_to_str()
            self.assertEquals(str(h), card_str)
            self.assertEquals(h.get_type(), type)
            self.assertEquals(h.describe(), desc)

    def test_invalid_hand_string_rep(self):
        self.assertRaises(CardFormatException, Hand.from_str, 'hi there')
        self.assertRaises(HandFormatException, Hand.from_str, 'As Qd')     # not enough cards

    def test_random_hand(self):
        h = Hand.random()
        self.assertTrue(len(h.cards) == 7)

    def _hand_wins(self, s1, s2, expected_winner):
        h1, h2 = Hand.from_str(s1), Hand.from_str(s2)
        if   expected_winner == FIRST  and h1>h2:  return True
        elif expected_winner == SPLIT  and h1==h2: return True
        elif expected_winner == SECOND and h1<h2:  return True
        return False

    def test_hand_comparisons(self):
        self.assertTrue(self._hand_wins('Ac Qd Jh 4c 2c', 'Qd Tc 4h 6s 9d', FIRST))
        self.assertTrue(self._hand_wins('Ac Qd Jh 4c 2c', 'Ad Tc 4h 6s 9d', FIRST))  # test kickers
        self.assertTrue(self._hand_wins('Ac Qd Jh 4c 2c', 'Ad 8c Qh Js 9d', SECOND)) # test kickers
        self.assertTrue(self._hand_wins('Ac Qd Jh 4c 2c', 'Ad Tc 4h As 9d', SECOND))
        self.assertTrue(self._hand_wins('2c 2d 4h 4c 8c', '2c 2d 4h 4c 8c', SPLIT))
        self.assertTrue(self._hand_wins('2c 2d 4h 4c 9c', '2c 2d 4h 4c 8c', FIRST))  # test kickers
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac Qd Jh 4c 2c', FIRST))  # royal flush beats everything
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c Tc', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c 7s', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', '8c 8d 8h 7c Tc', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', '8c 7d 6h 5c 4c', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac 2d 3h 4c 5c', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac Jd Kh Tc Qc', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', '8c 6c 5c Qc Jc', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', '8c 8d 8h 6d 6h', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Qc Qd Qh Qs 6h', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ah 4h 2h 3h 5h', FIRST))
        self.assertTrue(self._hand_wins('Ac Jc Kc Tc Qc', 'Ac Jc Kc Tc Qc', SPLIT))
        self.assertTrue(self._hand_wins('9c 8d 7h 6c 5c', '8c 7d 6h 5c 4c', FIRST))  # high card in straights win
        self.assertTrue(self._hand_wins('9c 8c 7c 6c 5c', '8c 7c 6c 5c 4c', FIRST))  # high card in straight flushes win
        self.assertTrue(self._hand_wins('Jc Js Td Th Tc', 'Qc Qd Qh Qs 6h', SECOND)) # 4-kind beats full house
        self.assertTrue(self._hand_wins('Jc Js Jd Jh Tc', 'Qc Qd Qh Qs 6h', SECOND)) # higher rank in 4 of a kind wins
        self.assertTrue(self._hand_wins('Ac As Ad 6h 6c', 'Qc Qd Qh Ts Th', FIRST))  # higher rank in Fh wins
        self.assertTrue(self._hand_wins('Ac As Ad 6h 6c', 'Ac Ad Ah Ts Th', SECOND)) # higher rank in Fh wins
        self.assertTrue(self._hand_wins('Ac As Ad 6h 6c', 'Ac Ad Ah 6s 6h', SPLIT))
        self.assertTrue(self._hand_wins('6c Tc Qc 2c 9c', 'Kh 4h 9h Jh 8h', SECOND)) # high card in flush wins

    def test_internal_analysis_string(self):
        h = Hand.random()
        s = h._analysis_to_str()
        self.assertTrue(s != None)   # bah

if __name__ == '__main__':
    unittest.main()

