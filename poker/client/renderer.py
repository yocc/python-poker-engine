from pyglet import image
from poker.client.resources import image_resource
import poker.card

"""
the image grid is an image composed of 52 subimages (one per playing card
in a deck), arranged in a 4x13 grid.  by convention, the order of the ranks per
row is A,2,3,...,T,J,Q,K and the order of the suits from bottom to top is
diamonds, hearts, clubs, spades.
"""

ROWS, COLS = 4, 13
deck_grid = image.ImageGrid(image_path('deck.png'), ROWS, COLS).texture_sequence

def get_card_image(card):
    """returns a pyglet image for the given card"""

    col = card.rank + 1
    if card.rank == poker.card.ACE: col = 0
    return deck_grid[(card.suit, col)]

def render_hand(win, h):
    """simply renders the given hand in the center of the given window.
       really just for testing."""

    card_images = [get_card_image(c) for c in h.cards]
    padding = 20
    full_width = (card_images[0].width + padding) * len(h.cards)
    x = win.width/2 - full_width/2
    y = win.height/2 - card_images[0].height/2
    for img in card_images:
        img.blit(x,y)
        x = x + img.width + padding

