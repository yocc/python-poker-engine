#!/usr/bin/env python

import os, sys, random
from pyglet import media, clock

PWD = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PWD, '..', '..'))
sys.path.insert(0, os.path.join(PWD, '..'))

import pokerclient
win, fps, text = pokerclient.init_window()

from pokercore.handeval import *
from pokerclient.cardrenderer import *

deck_of_cards = range(52)
random.shuffle(deck_of_cards)
h = None

#def next_random_hand(dt):
#    global deck_of_cards, text, h
#    if len(deck_of_cards) < 7:
#        deck_of_cards = range(52)
#        random.shuffle(deck_of_cards)
#    h.reset()
#    for i in range(7):
#        h.add_card(Card(deck_of_cards.pop()))
#        text.text = h.get_desc()
#clock.schedule_interval(next_random_hand, 5) 
#next_random_hand(0)

test_hands = [
    ('Ac Qd Jh 4c 2c', 'ace-high'),
    ('Ac Ad 8h 7c Tc', 'pair of aces'),
    ('Ac Ad 8h 7c 7s', 'two pair (aces and sevens)'),
    ('8c 8d 8h 7c Tc', 'three of a kind (eights)'),
    ('8c 7d 6h 5c 4c', 'eight-high straight'),
    ('Ac 2d 3h 4c 5c', 'five-high straight'),         # test aces as low in straight
    ('Ac Jd Kh Tc Qc', 'ace-high straight'),          # test aces as high in straight
    ('8c 6c 5c Qc Jc', 'queen-high flush'),
    ('8c 8d 8h 6d 6h', 'full house (eights over sixes)'),
    ('Qc Qd Qh Qs 6h', 'four of a kind (queens)'),
    ('Ah 4h 2h 3h 5h', 'five-high straight flush'),   # test aces as low in straight flush
    ('Ac Jc Kc Tc Qc', 'royal flush'),                # test aces as high in straight flush (royal)
]

TEST_DELAY=0.1

test_hand_no=0
def go_next_test_hand(dt):
    global h, test_hand_no
    hand_str, expected_desc = test_hands[test_hand_no]
    h = Hand.from_str(hand_str)
    actual_desc = h.get_desc()
    result = "PASS!"
    if actual_desc != expected_desc: 
        result = "FAIL!!"
    text.text = "hand:%s\nactual:%s\nexpected:%s\n%s" % (hand_str, actual_desc, expected_desc, result)
    if test_hand_no + 1 == len(test_hands): 
        text.text = "ALL YOUR TESTS ARE BELONG TO US!"
    else: 
        test_hand_no = test_hand_no + 1
        clock.schedule_once(go_next_test_hand, TEST_DELAY) 
clock.schedule_once(go_next_test_hand, TEST_DELAY) 

FIRST,SECOND,SPLIT=range(3)

def compare_hands(s1,s2,expected):
    h1,h2=Hand.from_str(s1),Hand.from_str(s2)
    if   expected == FIRST  and h1>h2:  result='OK'
    elif expected == SPLIT  and h1==h2: result='OK'
    elif expected == SECOND and h1<h2:  result='OK'
    else: result='FAILED'
    line = str(h1)+' vs '+str(h2)
    line = '%-60s%s' % (line,result)
    print line

compare_hands('Ac Qd Jh 4c 2c', 'Qd Tc 4h 6s 9d', FIRST)
compare_hands('Ac Qd Jh 4c 2c', 'Ad Tc 4h 6s 9d', FIRST)   # test kickers
compare_hands('Ac Qd Jh 4c 2c', 'Ad 8c Qh Js 9d', SECOND)  # test kickers
compare_hands('Ac Qd Jh 4c 2c', 'Ad Tc 4h As 9d', SECOND)
compare_hands('2c 2d 4h 4c 8c', '2c 2d 4h 4c 8c', SPLIT)
compare_hands('2c 2d 4h 4c 9c', '2c 2d 4h 4c 8c', FIRST)   # test kickers
compare_hands('Ac Jc Kc Tc Qc', 'Ac Qd Jh 4c 2c', FIRST)   # royal flush beats everything
compare_hands('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c Tc', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Ac Ad 8h 7c 7s', FIRST)
compare_hands('Ac Jc Kc Tc Qc', '8c 8d 8h 7c Tc', FIRST)
compare_hands('Ac Jc Kc Tc Qc', '8c 7d 6h 5c 4c', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Ac 2d 3h 4c 5c', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Ac Jd Kh Tc Qc', FIRST)
compare_hands('Ac Jc Kc Tc Qc', '8c 6c 5c Qc Jc', FIRST)
compare_hands('Ac Jc Kc Tc Qc', '8c 8d 8h 6d 6h', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Qc Qd Qh Qs 6h', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Ah 4h 2h 3h 5h', FIRST)
compare_hands('Ac Jc Kc Tc Qc', 'Ac Jc Kc Tc Qc', SPLIT)
compare_hands('9c 8d 7h 6c 5c', '8c 7d 6h 5c 4c', FIRST)   # high card in straights win
compare_hands('9c 8c 7c 6c 5c', '8c 7c 6c 5c 4c', FIRST)   # high card in straight flushes win
compare_hands('Jc Js Td Th Tc', 'Qc Qd Qh Qs 6h', SECOND)  # 4-kind beats full house
compare_hands('Jc Js Jd Jh Tc', 'Qc Qd Qh Qs 6h', SECOND)  # higher rank in 4 of a kind wins
compare_hands('Ac As Ad 6h 6c', 'Qc Qd Qh Ts Th', FIRST)   # higher rank in Fh wins
compare_hands('Ac As Ad 6h 6c', 'Ac Ad Ah Ts Th', SECOND)  # higher rank in Fh wins
compare_hands('Ac As Ad 6h 6c', 'Ac Ad Ah 6s 6h', SPLIT)
compare_hands('6c Tc Qc 2c 9c', 'Kh 4h 9h Jh 8h', SECOND)  # high card in flush wins

while not win.has_exit:
    win.dispatch_events()
    media.dispatch_events()
    clock.tick()
    win.clear()
    render_hand(h)
    text.draw()
    fps.draw()
    win.flip()
