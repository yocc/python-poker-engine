#!/usr/bin/env python

import os, sys, random

from pyglet import media, clock
from pyglet.window import key
from pyglet.gl import glClearColor

PWD = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PWD, '..', '..'))
sys.path.insert(0, os.path.join(PWD, '..'))

import pokerclient

win, fps, text = pokerclient.init_window(w=800,h=200)
text.color = (0,0,0,1)

from pokercore.handeval import *
from pokerclient.cardrenderer import *

def update_ui(h):
    text.text = h.get_desc()
    win.clear()
    render_hand(win, h)
    text.draw()
    win.flip()

def step_events():
    win.dispatch_events()
    media.dispatch_events()
    clock.tick()

def save_hand_to_test_file(h, valid):
    if valid: path = os.path.join(PWD, '..', 'logs', 'hands-classified-pass.log')
    else:     path = os.path.join(PWD, '..', 'logs', 'hands-classified-fail.log')
    f = file(path, 'a')
    if valid: f.write('%s = %s\n' % (h.abbrev_desc(), h.get_desc()))
    else: f.write("%s = %s\n%s\n" % (h.abbrev_desc(), h.get_desc(), h._analysis_to_str()))
    f.close()

def on_key_press(symbol, modifiers): 
    global h
    if symbol == key.ESCAPE: return False
    valid = symbol == key.RETURN
    save_hand_to_test_file(h, valid)
    h = Hand.random()
    update_ui(h)
    return False

clock.set_fps_limit(3)
glClearColor(1,1,1,1)
step_events()
h = advance_hand()
win.push_handlers(on_key_press)

while not win.has_exit:
    step_events()
