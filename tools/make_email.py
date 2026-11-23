from PIL import Image, ImageDraw, ImageFont
import os
OUT = "/home/pat/impetus/2_PUBLISHED/fubar.patpadgett.com/assets/img"
f = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
im = Image.new("RGB", (40, 26), (255, 255, 255))
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 39, 25], outline=(60, 60, 120))
d.text((15, 0), "@", font=ImageFont.truetype(f, 24), fill=(0, 0, 180))
im.save(OUT + "/gif_email.gif")
print("wrote", OUT + "/gif_email.gif")
