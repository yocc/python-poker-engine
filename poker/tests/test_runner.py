#!/usr/bin/env python

from unittest import *

import test_card
import test_hand
import test_randomness

import os

if __name__ == '__main__':
    skip_long_tests = len(sys.argv) > 1 and sys.argv[1] == '--skip-long'
    suite = TestSuite()
    suite.addTest(test_card.CardTestCase())
    suite.addTest(test_hand.HandTestCase())
    if not skip_long_tests:
        suite.addTest(test_randomness.RandomnessTestCase())
    else:
        print 'skipping RandomnessTestCase...'
    TextTestRunner(verbosity=2).run(suite)
