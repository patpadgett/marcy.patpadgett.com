from PIL import Image, ImageDraw
OUT = "/home/pat/impetus/2_PUBLISHED/fubar.patpadgett.com/assets/img"
im = Image.new("RGBA", (152, 12), (255, 251, 230, 0))
d = ImageDraw.Draw(im)
cols = [(220, 40, 40), (40, 90, 190), (220, 160, 40), (40, 150, 90), (150, 60, 180)]
for i, x in enumerate(range(8, 150, 18)):
    c = cols[i % len(cols)]
    d.polygon([(x, 2), (x + 3, 5), (x, 8), (x - 3, 5)], fill=c + (255,))
im.save(OUT + "/div_star.gif", transparency=(255, 251, 230))
print("wrote", OUT + "/div_star.gif")
