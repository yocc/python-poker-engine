from pyglet import image
from pokerclient.res import image_res
import pokercore.handeval

deck_rows, deck_cols = 4, 13
deck_grid = image.ImageGrid(image_res('deck.png'), deck_rows, deck_cols).texture_sequence

def get_card_image(card):
    col = card.rank + 1
    if card.rank == pokercore.handeval.ACE: col = 0
    return deck_grid[(card.suit, col)]

print 'ok'
