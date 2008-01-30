import unittest
import math
import sys

from poker.hand import *

class RandomnessTestCase(unittest.TestCase):
    """Test that over many hands the expected percentages of
       poker hands are seen for randomly created hands from a
       shuffled deck of cards.  We are testing 7-card hands here
       since we are initially focused on Texas Hold'em (2-hole,
       3-flop, 1-turn, 1-river).  Source of probabilities:
       http://en.wikipedia.org/wiki/Poker_probability#Frequency_of_7-card_poker_hands
    """

    def runTest(self):
        hand_count = 1000

        stats = { HIGHCARD:0.0, 
                  PAIR:0.0, 
                  TWOPAIR:0.0, 
                  SET:0.0, 
                  STRAIGHT:0.0, 
                  FLUSH:0.0, 
                  FULLHOUSE:0.0, 
                  QUADS:0.0, 
                  STRAIGHTFLUSH:0.0 }

        probs = { HIGHCARD:17.4, 
                  PAIR:43.8, 
                  TWOPAIR:23.5, 
                  SET:4.83, 
                  STRAIGHT:4.62, 
                  FLUSH:3.03, 
                  FULLHOUSE:2.60, 
                  QUADS:0.168, 
                  STRAIGHTFLUSH:0.0311 }

        fudge = 5.0      # +/- fudge percentage points is OK ... TODO how to tune?

        print 'generating stats on %d hands... please wait...' % hand_count

        for i in range(hand_count):
            h = Hand.random()
            stats[h.get_type()] += 1
            if i % 10000 == 0: 
                print '.',
                sys.stdout.flush()

        print
        print 'probabilities of hand occurrences:'

        for x in stats:
            stats[x] = (stats[x] / hand_count) * 100.0
            print '%-20s expected %5.2f actual %5.2f delta %3.2f' % \
                (TYPE_NAMES[x], probs[x], stats[x], math.fabs(probs[x] - stats[x]))

        for x in stats:
            delta = math.fabs(probs[x] - stats[x])
            self.assertTrue(delta < fudge)
