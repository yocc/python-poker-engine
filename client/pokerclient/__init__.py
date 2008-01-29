from pyglet import window, clock, font
from pyglet.gl import * 

def init_window():
    # initially invisible so we can load fonts which require the window to be created beforehand.

    win = window.Window(visible=False)
    fps = clock.ClockDisplay() 

    # Now we can load fonts

    ft = font.load('Tahoma', 24) 
    text = font.Text(ft, '', x=0, y=220)

    win.set_size(800, 600)
    win.set_visible(True)
    clock.set_fps_limit(30)

    # enable alpha-blending since some of our images are semi-transparent.

    glEnable(GL_BLEND) 
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

    return win, fps, text

