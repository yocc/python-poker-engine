# Create a "montage" (single image containing grid of subimages)
# which is more efficient than having an application load 52 separate
# images.
#
# All images should be named like <rank><suit>.gif with 
# <rank> = { a,2,3...9,t,j,q,k },
# <suit> = { s,c,h,d }
#
# We want a specific layout in the final deck image hence the 
# enumeration of the files (cf. $(card_dir)/*.gif).
#
# This requires ImageMagick and make (duh).

card_dir=cards/gpl-cards
card_image_size=73x97
deck_path=../../images/deck.png
card_images=$(card_dir)/as.gif $(card_dir)/2s.gif $(card_dir)/3s.gif \
$(card_dir)/4s.gif $(card_dir)/5s.gif $(card_dir)/6s.gif $(card_dir)/7s.gif \
$(card_dir)/8s.gif $(card_dir)/9s.gif $(card_dir)/ts.gif $(card_dir)/js.gif \
$(card_dir)/qs.gif $(card_dir)/ks.gif $(card_dir)/ac.gif $(card_dir)/2c.gif \
$(card_dir)/3c.gif $(card_dir)/4c.gif $(card_dir)/5c.gif $(card_dir)/6c.gif \
$(card_dir)/7c.gif $(card_dir)/8c.gif $(card_dir)/9c.gif $(card_dir)/tc.gif \
$(card_dir)/jc.gif $(card_dir)/qc.gif $(card_dir)/kc.gif $(card_dir)/ah.gif \
$(card_dir)/2h.gif $(card_dir)/3h.gif $(card_dir)/4h.gif $(card_dir)/5h.gif \
$(card_dir)/6h.gif $(card_dir)/7h.gif $(card_dir)/8h.gif $(card_dir)/9h.gif \
$(card_dir)/th.gif $(card_dir)/jh.gif $(card_dir)/qh.gif $(card_dir)/kh.gif \
$(card_dir)/ad.gif $(card_dir)/2d.gif $(card_dir)/3d.gif $(card_dir)/4d.gif \
$(card_dir)/5d.gif $(card_dir)/6d.gif $(card_dir)/7d.gif $(card_dir)/8d.gif \
$(card_dir)/9d.gif $(card_dir)/td.gif $(card_dir)/jd.gif $(card_dir)/qd.gif \
$(card_dir)/kd.gif 

$(deck_path): $(card_images)
	@montage -geometry $(card_image_size) $(card_images) -tile 13x4 $(deck_path)
	@echo created $(deck_path) from $(card_dir).

clean:
	rm -f $(deck_path)
