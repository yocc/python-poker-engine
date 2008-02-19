# Create a "montage" (single image containing grid of subimages)
# which is more efficient than having an application load 52 separate
# images.
#
# All images should be named like <rank><suit>.gif with 
# <rank> = { a,2,3...9,t,j,q,k },
# <suit> = { s,c,h,d }
#
# We want a specific layout in the final deck image hence the 
# enumeration of the files (cf. *.gif).
#
# This requires ImageMagick and make (duh).

card_image_size=73x97

deck_path=../../../../images/deck.png

card_images=as.gif 2s.gif 3s.gif 4s.gif 5s.gif 6s.gif 7s.gif 8s.gif 9s.gif \
ts.gif js.gif qs.gif ks.gif ac.gif 2c.gif 3c.gif 4c.gif 5c.gif 6c.gif 7c.gif \
8c.gif 9c.gif tc.gif jc.gif qc.gif kc.gif ah.gif 2h.gif 3h.gif 4h.gif 5h.gif \
6h.gif 7h.gif 8h.gif 9h.gif th.gif jh.gif qh.gif kh.gif ad.gif 2d.gif 3d.gif \
4d.gif 5d.gif 6d.gif 7d.gif 8d.gif 9d.gif td.gif jd.gif qd.gif kd.gif 

$(deck_path): $(card_images)
	@montage -background \#ff00ff -geometry $(card_image_size) $(card_images) -tile 13x4 $(deck_path)
	@echo created $(deck_path)

clean:
	rm -f $(deck_path)
