from pyglet import image
from pokerclient.res import image_resource
import pokercore.handeval

ROWS, COLS = 4, 13
deck_grid = image.ImageGrid(image_resource('deck.png'), ROWS, COLS).texture_sequence

def get_card_image(card):
    col = card.rank + 1
    if card.rank == pokercore.handeval.ACE: 
        col = 0
    return deck_grid[(card.suit, col)]

def render_hand(win, h):
    card_images = [get_card_image(c) for c in h.cards]
    padding = 20
    full_width = (card_images[0].width + padding) * len(h.cards)
    x = win.width/2 - full_width/2
    y = win.height/2 - card_images[0].height/2
    for img in card_images:
        img.blit(x,y)
        x = x + img.width + padding

