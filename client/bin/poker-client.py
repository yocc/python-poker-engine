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

def render_hand(h):
    x, y = 20, win.height/2
    for img in [get_card_image(c) for c in h.cards[0:7]]:
        img.blit(x,y)
        x += img.width

test_hand_no=0
def go_next_test_hand(dt):
    global h, test_hand_no
    hand_str, expected_desc = test_hands[test_hand_no]
    h = Hand.from_str(hand_str)
    actual_desc = h.get_desc()
    result = "PASS!"
    if actual_desc != expected_desc: 
        result = "FAIL!!"
        clock.unschedule(go_next_test_hand) 
    text.text = "hand:%s\nactual:%s\nexpected:%s\n%s" % (hand_str, actual_desc, expected_desc, result)
    if test_hand_no + 1 == len(test_hands): 
        text.text = "ALL YOUR TESTS ARE BELONG TO US!"
        clock.unschedule(go_next_test_hand) 
    else: 
        test_hand_no = test_hand_no + 1
clock.schedule_interval(go_next_test_hand, 0.25) 
go_next_test_hand(0)

while not win.has_exit:
    win.dispatch_events()
    media.dispatch_events()
    clock.tick()
    win.clear()
    render_hand(h)
    text.draw()
    fps.draw()
    win.flip()
