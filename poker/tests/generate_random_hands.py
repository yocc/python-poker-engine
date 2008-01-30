#!/usr/bin/env python

from poker.hand import *

import sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 100

if n < 0: n = 100

for i in range(n):
    h = Hand.random()
    print '( "%s", %20s, "%s" )' % (str(h), TYPE_NAMES[h.get_type()], h.describe())
