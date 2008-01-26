from pyglet import font, window

win = window.Window()

ft = font.load('Arial', 36)
text = font.Text(ft, 'Hey dude')

@win.event
def on_resize(w,h):
    print 'window resized to %d x %d' % (w,h)

while not win.has_exit:
    win.dispatch_events()
    win.clear()
    text.draw()
    win.flip()
