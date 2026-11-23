from PIL import Image, ImageDraw, ImageFont
import os
OUT = "/home/pat/impetus/2_PUBLISHED/fubar.patpadgett.com/assets/img"
f = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
if not os.path.exists(f):
    f = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def counter(digits, name):
    im = Image.new("RGB", (152, 22), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 151, 21], radius=3, fill=(20, 10, 40), outline=(120, 100, 160))
    for i, ch in enumerate(digits):
        x = 8 + i * 23
        d.rounded_rectangle([x, 3, x + 19, 18], radius=2, fill=(4, 20, 12))
        d.text((x + 4, 2), ch, font=ImageFont.truetype(f, 13), fill=(90, 255, 170))
    im.save(OUT + "/" + name)
    print("wrote", OUT + "/" + name)

counter("001999", "counter_1999.gif")
counter("020471", "counter_2041.gif")
