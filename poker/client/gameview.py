from pyglet import window, clock, font
from pyglet.gl import * 

from resources import font_resource

FONT_NAME = 'Tahoma'

class GameView(window.Window):
    """A view of a single poker game/table. Each such view is enclosed in 
       a distinct OS window."""

    def __init__(self, w=800, h=600):
        # leave initially invisible, load fonts, etc. then make visible.

        window.Window.__init__(self, visible=False)
        
        self.fps = clock.ClockDisplay() 

        self.big_font   = font_resource(FONT_NAME, size=24)
        self.small_font = font_resource(FONT_NAME, size=12)

        self.set_size(w, h)
        self.set_visible(True)
        clock.set_fps_limit(30)

        self.status_text = font.Text(self.small_font, '')
        self.status_text.y = self.height - self.status_text.height
        self.status_text.width = self.width

        # enable alpha-blending since some of our images are semi-transparent.
        # this must be done after creating the window (and really only once but
        # it doesn't matter if we have >1 window/view).

        glEnable(GL_BLEND) 
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
