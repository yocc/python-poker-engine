from pyglet import window, clock, font
from pyglet.gl import * 

def init_window(w=800, h=600):
    # initially invisible so we can load fonts which require the window to be created beforehand.

    win = window.Window(visible=False)
    fps = clock.ClockDisplay() 

    # Now we can load fonts

    ft = font.load('Tahoma', 24, bold=True) 
    text = font.Text(ft, 'Testing..', halign=font.Text.CENTER)

    win.set_size(w,h)
    win.set_visible(True)
    clock.set_fps_limit(30)

    text.y = win.height - text.height
    text.width = win.width

    # enable alpha-blending since some of our images are semi-transparent.

    glEnable(GL_BLEND) 
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 

    return win, fps, text

