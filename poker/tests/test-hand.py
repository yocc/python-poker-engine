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
]

class HandTestCase(unittest.TestCase):
    """Tests the hand module"""
    def test_hands(self):
        for entry in test_hands:
            try:
                card_str, type, desc = entry
                h = Hand.from_str(card_str)
                #print card_str, ' vs ', str(h)
                #print h._analysis_to_str()
                self.assertEquals(str(h), card_str)
                self.assertEquals(h.get_type(), type)
                self.assertEquals(h.describe(), desc)
            except CardFormatException, e:
                fail("internal testing error - invalid hand string: %s" % e.message)

    def test_invalid_hand_string_rep(self):
        self.assertRaises(CardFormatException, Hand.from_str, 'hi there')
        self.assertRaises(HandFormatException, Hand.from_str, 'As Qd')     # not enough cards

if __name__ == '__main__':
    unittest.main()

