# Creates a "montage" (single image containing grid of subimages) which is more
# efficient than having an application load 52 separate images. Top left to
# bottom right we have A,2,3,...Q,K with spades, clubs, hearts, then diamonds
# per row.  This requires ImageMagick and make (duh).

card_image_size=36x54

deck_path=../../../../images/deck.png

card_images=sA.png s2.png s3.png s4.png s5.png s6.png s7.png s8.png s9.png \
sT.png sJ.png sQ.png sK.png cA.png c2.png c3.png c4.png c5.png c6.png c7.png \
c8.png c9.png cT.png cJ.png cQ.png cK.png hA.png h2.png h3.png h4.png h5.png \
h6.png h7.png h8.png h9.png hT.png hJ.png hQ.png hK.png dA.png d2.png d3.png \
d4.png d5.png d6.png d7.png d8.png d9.png dT.png dJ.png dQ.png dK.png 

$(deck_path): $(card_images)
	@montage -background \#ff00ff -geometry $(card_image_size) $(card_images) -tile 13x4 $(deck_path)
	@echo created $(deck_path)

clean:
	rm -f $(deck_path)
