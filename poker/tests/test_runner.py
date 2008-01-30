#!/usr/bin/env python

from unittest import *

import test_card
import test_hand
import test_randomness

import os

if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(test_card.CardTestCase())
    suite.addTest(test_hand.HandTestCase())
    suite.addTest(test_randomness.RandomnessTestCase())
    TextTestRunner(verbosity=2).run(suite)
