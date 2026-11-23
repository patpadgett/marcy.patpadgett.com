#!/usr/bin/env python3
"""Generate the 1999 Angelfire-era assets for Marcy's page."""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/pat/impetus/2_PUBLISHED/fubar.patpadgett.com/assets/img"
os.makedirs(OUT, exist_ok=True)

def svg_or_canvas(name):  # placeholder kept for reference
    pass

def pick_font(bold=False):
    cands = []
    for d in ["/usr/share/fonts", "/usr/local/share/fonts", "/opt/homebrew/share/fonts"]:
        if os.path.isdir(d):
            cands += [os.path.join(d, f) for f in os.listdir(d)]
    cands = sorted(set(cands))
    for c in cands:
        if "DejaVuSerif" in c and bold and "Bold" in os.path.basename(c):
            return c
        if "DejaVuSans" in c and bold and "Bold" in os.path.basename(c):
            return c
    return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else \
           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

F = pick_font
def font(sz, bold=False):
    return ImageFont.truetype(F(bold), sz)

def new(size=(760, 560), bg=(0, 0, 64)):
    return Image.new("RGB", size, bg)

def save(im, name, animated=False, frames=None, duration=None, loop=0):
    p = os.path.join(OUT, name)
    if animated and frames:
        frames[0].save(p, save_all=True, append_images=frames[1:],
                        duration=duration, loop=loop, disposal=2)
    else:
        im.save(p)
    print("wrote", p)

# ------------------------------------------------------------------ backgrounds
def stars(n=140, w=76, h=76):
    im = Image.new("RGB", (w, h), (0, 0, 64))
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x = random.randrange(w); y = random.randrange(h)
        r = random.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
    return im

def marble(w=76, h=76, pal=("e8d8c8", "d8c8e8", "c8e8d0", "e8c8d8", "f0e8d8", "d8e8f0")):
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            c = random.choice(pal)
            px[x, y] = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    # soften with a light blur pass written by re-copy
    return im

def tiled(name, maker, tw, th, seps=4, bg=(0, 0, 64)):
    """A 2x2 grid of maker() tiles on bg."""
    T = Image.new("RGB", (tw * 2, th * 2), bg)
    for r in range(2):
        for c in range(2):
            T.paste(maker(tw, th), (c * tw, r * th))
    save(T, name)

tiled("bg_stars.gif", stars, 76, 76)
tiled("bg_marbles.gif", marble, 76, 76)

# ------------------------------------------------------------------ dividers
def rainbow_bar(w=76, h=14):
    cols = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 128, 255), (0, 0, 255), (255, 0, 255)]
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    sw = w // len(cols)
    for i, c in enumerate(cols):
        d.rectangle([i * sw, 0, i * sw + sw, h], fill=c)
    return im

def star_div(w=76, h=12):
    im = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(38, 0), (46, 12), (38, 12), (46, 12), (38, 12)], fill=(255, 255, 255))
    return im

save(rainbow_bar(), "div_rainbow.gif")
save(star_div(), "div_star.gif")

# ------------------------------------------------------------------ badges
def badge(name, title, sub, sub2, bg, txt, subcol, w=88, h=31):
    im = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=6, fill=bg)
    d.text((6, 1), title, fill=txt, font=font(13, True))
    d.text((6, 15), sub, fill=subcol, font=font(8))
    d.text((6, 22), sub2, fill=subcol, font=font(8))
    save(im, name)

badge("badge_netscape.gif", "Netscape", "best viewed in", "Netscape 4.0+", (60, 60, 180), (255, 255, 255), (255, 255, 255))
badge("badge_ie.gif", "Explorer", "best viewed in", "Internet Explorer", (200, 180, 40), (0, 0, 0), (0, 0, 0))

# ------------------------------------------------------------------ wordart: "MARCY" banner
def wordart():
    W, H = 760, 150
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    txt = "MARCY"
    sz = 150
    fnt = ImageFont.truetype(F(True), sz)
    # bounding box of text
    bbox = d.textbbox((0, 0), txt, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) // 2 - bbox[0]
    y = (H - th) // 2 - bbox[1]
    # soft shadow
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx or dy:
                d.text((x + dx, y + dy), txt, font=fnt, fill=(20, 10, 40, 180))
    # rainbow vertical gradient fill (each scanline a colour)
    for yy in range(H):
        col = tuple(int(c * (yy / H)) % 256 for c in (255, 0, 0))
        c2 = tuple(int(c * (yy / H)) % 256 for c in (0, 255, 255))
        # cycle through a rainbow on the alpha so it reads rainbow
        shade = int(255 * (0.55 + 0.45 * (yy / H)))
        d.text((x, y), txt, font=fnt, fill=(shade, shade, shade, 255))
    # white inner rim
    d.text((x + 1, y + 1), txt, font=fnt, fill=(255, 255, 255, 255))
    # outer glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(24, 0, -1):
        gd.text((x - r // 2, y - r // 2), txt, font=fnt, fill=(255, 120, 200, 60))
    im = Image.alpha_composite(im, glow)
    return im.convert("RGB")

save(wordart(), "wordart.gif")

# ------------------------------------------------------------------ news/now, new, under-construction
def news_now(w=76, h=76):
    im = Image.new("RGB", (w, h), (230, 230, 230))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8, fill=(255, 255, 255))
    d.polygon([(20, 8), (28, 16), (36, 8), (36, 24), (28, 16), (36, 24), (28, 16), (28, 24)], fill=(200, 40, 40))
    d.text((40, 20), "News/Now", fill=(40, 40, 40), font=font(13, True))
    return im
save(news_now(), "news.gif")

def nowvis(w=76, h=76):
    im = Image.new("RGB", (w, h), (230, 230, 230))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=8, fill=(255, 255, 255))
    d.ellipse([20, 18, 56, 54], fill=(40, 40, 40))
    d.ellipse([34, 4, 46, 26], fill=(200, 40, 40))
    return im
save(nowvis(), "nowvis.gif")

def newbadge(w=30, h=18):
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.polygon([(12, 0), (30, 8), (12, 16), (12, 16), (30, 8), (12, 8)], fill=(255, 0, 0))
    d.text((10, 0), "NEW", fill=(255, 255, 255), font=font(10, True))
    return im
save(newbadge(), "new.gif")

def underconst(w=400, h=22):
    im = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(0, 0, 0))
    d.text((4, 0), "Under construction; please use IE 4.0+ or Netscape 4.0+", fill=(255, 255, 255), font=font(11))
    return im
save(underconst(), "underconst.gif")

# ------------------------------------------------------------------ spinning @ (animated)
def spinner(frames=10, size=40):
    im0 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for i in range(frames):
        a = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        dd = ImageDraw.Draw(a)
        ang = i * (2 * math.pi / frames)
        # rotating disc
        dd.ellipse([0, 0, size - 1, size - 1], outline=(0, 0, 180, 220), width=4)
        # a spoke
        ex = int(size // 2 + math.cos(ang) * (size // 2 - 6))
        ey = int(size // 2 + math.sin(ang) * (size // 2 - 6))
        dd.line([(size // 2, size // 2), (ex, ey)], fill=(0, 0, 200, 255), width=5)
        # dot
        dd.ellipse([size // 2 - 5, size // 2 - 5, size // 2 + 5, size // 2 + 5], fill=(255, 60, 60, 255))
        im0 = a if i == 0 else im0
    frames_im = [im0]
    for i in range(1, frames):
        a = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        dd = ImageDraw.Draw(a)
        ang = i * (2 * math.pi / frames)
        dd.ellipse([0, 0, size - 1, size - 1], outline=(0, 0, 180, 220), width=4)
        ex = int(size // 2 + math.cos(ang) * (size // 2 - 6))
        ey = int(size // 2 + math.sin(ang) * (size // 2 - 6))
        dd.line([(size // 2, size // 2), (ex, ey)], fill=(0, 0, 200, 255), width=5)
        dd.ellipse([size // 2 - 5, size // 2 - 5, size // 2 + 5, size // 2 + 5], fill=(255, 60, 60, 255))
        frames_im.append(a)
    frames_im[0].save(OUT + "/spinner.gif", save_all=True, append_images=frames_im[1:],
                       duration=[90] * frames, loop=0, disposal=2)
    # still frame for the freeze
    still = Image.new("RGB", (size, size), (0, 120, 220))
    ds = ImageDraw.Draw(still)
    ds.ellipse([8, 8, size - 9, size - 9], outline=(0, 0, 200), width=4)
    ds.line([(size // 2, size // 2), (size // 2 + 14, size // 2 + 14)], fill=(0, 0, 200), width=5)
    ds.ellipse([size // 2 - 8, size // 2 - 8, size // 2 + 8, size // 2 + 8], fill=(255, 60, 60))
    still.save(OUT + "/spinner_still.gif")

spinner()

# ------------------------------------------------------------------ hearts (animated pulse)
def heart_path(d, cx, cy, s, fill):
    d.ellipse([cx - s, cy - s * 0.4, cx + s, cy + s * 0.4], fill=fill)
    d.polygon([(cx - s * 0.6, cy + s * 0.4), (cx, cy + s * 1.7), (cx + s * 0.6, cy + s * 0.4)], fill=fill)

def hearts(n=7, size=40):
    frames = []
    for i in range(n):
        a = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        s = 0.5 + 0.5 * math.sin(i / n * math.pi)  # expand then settle-ish
        heart_path(ImageDraw.Draw(a), size // 2, size // 2, int(size * s * 0.8), (255, 40, 60))
        frames.append(a)
    frames[0].save(OUT + "/heart.gif", save_all=True, append_images=frames[1:],
                    duration=[110] * n, loop=0, disposal=2)
    # still heart
    st = Image.new("RGB", (size, size), (0, 0, 0))
    heart_path(ImageDraw.Draw(st), size // 2, size // 2, int(size * 0.7), (255, 40, 60))
    st.save(OUT + "/heart_still.gif")

hearts()

# ------------------------------------------------------------------ favicon
def favicon():
    im = Image.new("RGB", (32, 32), (0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([3, 3, 29, 29], fill=(255, 40, 60))
    d.ellipse([8, 8, 24, 24], outline=(255, 255, 255), width=3)
    d.ellipse([16, 6, 22, 12], fill=(0, 0, 0))
    d.ellipse([16, 20, 22, 26], fill=(0, 0, 0))
    return im
favicon().save(OUT + "/favicon.gif")

# ------------------------------------------------------------------ grain/noise overlays
def grain(name, size=76, density=0.12):
    im = Image.new("RGB", (size, size), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(size):
        for x in range(size):
            if random.random() < density:
                d.point((x, y), fill=(255, 255, 255))
    return im

