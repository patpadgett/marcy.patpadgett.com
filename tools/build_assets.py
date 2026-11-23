#!/usr/bin/env python3
"""Build every shipping raster for the Marcy site.

Sources: .impeccable/raw/*.png (generated, see assets/img/PROVENANCE.json)
Outputs: assets/img/*
Run: python3 tools/build_assets.py
"""
import io
import math
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, ".impeccable", "raw")
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)

VERDANA_B = "/mnt/c/Windows/Fonts/verdanab.ttf"
VERDANA = "/mnt/c/Windows/Fonts/verdana.ttf"

random.seed(1999)


# ---------------------------------------------------------------- helpers

def jpeg_crush(im, path, quality=42, passes=2, final=72):
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, subsampling=2, optimize=False)
    for _ in range(passes - 1):
        buf.seek(0)
        im2 = Image.open(buf).convert("RGB")
        buf = io.BytesIO()
        im2.save(buf, "JPEG", quality=min(92, quality + 22), subsampling=2)
    buf.seek(0)
    Image.open(buf).convert("RGB").save(path, "JPEG", quality=final, subsampling=2,
                                        optimize=True, progressive=False)
    return os.path.getsize(path)


def grain(im, sigma=7, opacity=0.10):
    n = Image.effect_noise(im.size, sigma).convert("L")
    n = n.convert("RGB")
    return Image.blend(im, n, opacity)


def vignette(im, strength=0.30):
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.25, -h * 0.30, w * 1.25, h * 1.30), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) // 8))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(im, Image.blend(im, dark, strength), mask)


def photo(src, name, w=360, h=270, warm=(1.03, 0.985, 0.94), sat=0.92, bright=1.0):
    im = Image.open(os.path.join(RAW, src)).convert("RGB")
    sw, sh = im.size
    target = w / h
    if sw / sh > target:
        nw = int(sh * target)
        im = im.crop(((sw - nw) // 2, 0, (sw + nw) // 2, sh))
    else:
        nh = int(sw / target)
        im = im.crop((0, (sh - nh) // 2, sw, (sh + nh) // 2))
    im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * warm[0])))
    g = g.point(lambda v: min(255, int(v * warm[1])))
    b = b.point(lambda v: min(255, int(v * warm[2])))
    im = Image.merge("RGB", (r, g, b))
    im = grain(im, 8, 0.13)
    im = vignette(im, 0.22)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=2))
    r, g, b = im.split()
    r = r.transform(r.size, Image.AFFINE, (1, 0, -0.9, 0, 1, 0))
    b = b.transform(b.size, Image.AFFINE, (1, 0, 0.9, 0, 1, 0))
    im = Image.merge("RGB", (r, g, b))
    kb = jpeg_crush(im, os.path.join(OUT, name + ".jpg"), quality=32, passes=3, final=66)
    sm = im.resize((96, 72), Image.LANCZOS)
    ks = jpeg_crush(sm, os.path.join(OUT, name + "_sm.jpg"), quality=24, passes=3, final=54)
    print(f"  {name}.jpg {w}x{h} {kb//1024}KB  sm {ks//1024}KB")


def substrate(src, name, w, h, crop_bias=0.5):
    im = Image.open(os.path.join(RAW, src)).convert("RGB")
    sw, sh = im.size
    target = w / h
    if sw / sh > target:
        nw = int(sh * target)
        left = int((sw - nw) * crop_bias)
        im = im.crop((left, 0, left + nw, sh))
    else:
        nh = int(sw / target)
        top = int((sh - nh) * crop_bias)
        im = im.crop((0, top, sw, top + nh))
    im = im.resize((w, h), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(0.55)
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Brightness(im).enhance(0.62)
    im = grain(im, 5, 0.10)
    k = jpeg_crush(im, os.path.join(OUT, name + ".jpg"), quality=52, passes=2, final=78)
    print(f"  {name}.jpg {w}x{h} {k//1024}KB")


# ---------------------------------------------------------------- tiles

def tiles():
    for variant, name in ((0, "tile_stars"), (1, "tile_stars_dark")):
        size = 96
        im = Image.new("RGB", (size, size), (18, 8, 34) if variant == 0 else (9, 5, 15))
        d = ImageDraw.Draw(im)
        for _ in range(26):
            x, y = random.randrange(size), random.randrange(size)
            c = random.choice([(60, 36, 96), (80, 54, 120), (44, 26, 72)])
            d.point((x, y), fill=c)
        for _ in range(7):
            x, y = random.randrange(size), random.randrange(size)
            d.point((x, y), fill=(210, 190, 255))
            d.point(((x + 1) % size, y), fill=(120, 96, 160))
            d.point((x, (y + 1) % size), fill=(120, 96, 160))
        if variant == 1:
            # bone ribs bleeding into the tile
            for i in range(3):
                x = random.randrange(size)
                for y in range(size):
                    if random.random() > 0.25:
                        d.point((x, y), fill=(58, 54, 46) if i else (40, 37, 31))
        im.save(os.path.join(OUT, name + ".png"))
    print("  tiles 96x96")


# ---------------------------------------------------------------- gifs

def save_gif(frames, path, duration=110, colors=64):
    pal = [f.convert("RGBA").convert("P", palette=Image.ADAPTIVE, colors=colors) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=duration,
                loop=0, disposal=2, optimize=False)
    print(f"  {os.path.basename(path)} {len(frames)}f {os.path.getsize(path)//1024}KB")


def gif_construct():
    w, h = 132, 44
    frames = []
    font = ImageFont.truetype(VERDANA_B, 9)
    for f in range(4):
        im = Image.new("RGB", (w, h), (0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, w, 5), fill=(255, 204, 0))
        d.rectangle((0, h - 6, w, h), fill=(255, 204, 0))
        for x in range(-8, w, 12):
            d.polygon([(x, 0), (x + 5, 0), (x - 1, 5), (x - 6, 5)], fill=(30, 30, 30))
            d.polygon([(x, h - 6), (x + 5, h - 6), (x - 1, h - 1), (x - 6, h - 1)], fill=(30, 30, 30))
        on = (f % 2 == 0)
        d.text((6, 13), "UNDER", font=font, fill=(255, 230, 60) if on else (190, 150, 30))
        d.text((6, 24), "CONSTRUCTION", font=font, fill=(255, 255, 255) if on else (150, 150, 150))
        # little hard hat
        bx = 106 + (0 if f < 2 else 2)
        d.ellipse((bx, 16, bx + 20, 28), fill=(255, 200, 0))
        d.rectangle((bx, 22, bx + 20, 26), fill=(255, 200, 0))
    # frames must be rebuilt per loop
    frames = []
    for f in range(4):
        im = Image.new("RGB", (w, h), (0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, w, 5), fill=(255, 204, 0))
        d.rectangle((0, h - 6, w, h), fill=(255, 204, 0))
        for x in range(-8, w, 12):
            d.polygon([(x, 0), (x + 5, 0), (x - 1, 5), (x - 6, 5)], fill=(30, 30, 30))
            d.polygon([(x, h - 6), (x + 5, h - 6), (x - 1, h - 1), (x - 6, h - 1)], fill=(30, 30, 30))
        on = (f % 2 == 0)
        d.text((6, 13), "UNDER", font=font, fill=(255, 230, 60) if on else (170, 130, 20))
        d.text((6, 24), "CONSTRUCTION", font=font, fill=(255, 255, 255) if on else (140, 140, 140))
        bx = 106 + (0 if f < 2 else 2)
        d.ellipse((bx, 15, bx + 20, 29), fill=(255, 200, 0))
        d.rectangle((bx - 2, 22, bx + 22, 25), fill=(230, 170, 0))
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_construct.gif"), 220)


def gif_new():
    w, h = 46, 20
    font = ImageFont.truetype(VERDANA_B, 11)
    frames = []
    for f in range(4):
        im = Image.new("RGB", (w, h), (172, 0, 0))
        d = ImageDraw.Draw(im)
        for i in range(0, w, 4):
            d.line((i, 0, i - 6, h), fill=(210, 10, 10))
        d.rectangle((0, 0, w - 1, h - 1), outline=(255, 210, 60))
        col = (255, 255, 120) if f % 2 == 0 else (255, 255, 255)
        d.text((7, 3), "NEW!", font=font, fill=col)
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_new.gif"), 300)


def gif_star():
    w = h = 22
    frames = []
    for f in range(8):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        a = f * math.pi / 8
        cx = cy = w / 2
        pts = []
        for i in range(8):
            r = 10 if i % 2 == 0 else 3.2
            th = a + i * math.pi / 4
            pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
        d.polygon(pts, fill=(255, 246, 160, 255))
        d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=1)
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_star.gif"), 110)


def gif_flame():
    w, h = 14, 22
    frames = []
    for f in range(6):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        wob = math.sin(f / 6 * math.tau)
        d.polygon([(7, 0 + 2 * wob), (12, 10), (11, 19), (7, 22), (3, 19), (2, 11)],
                  fill=(255, 120, 0, 235))
        d.polygon([(7, 5 + wob), (10, 12), (9, 19), (7, 21), (5, 19), (4, 12)],
                  fill=(255, 216, 60, 255))
        d.polygon([(7, 11), (8.6, 15), (7, 19), (5.6, 15)], fill=(255, 255, 210, 255))
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_flame.gif"), 90)


def gif_email():
    w, h = 40, 26
    frames = []
    for f in range(6):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle((1, 4, w - 2, h - 2), fill=(250, 250, 255, 255), outline=(90, 90, 120, 255))
        flap = 4 + (f if f < 3 else 5 - f)
        d.polygon([(1, 4), (w / 2, 4 + flap * 2.2), (w - 2, 4)], fill=(215, 220, 240, 255),
                  outline=(90, 90, 120, 255))
        d.polygon([(1, h - 2), (w / 2, 10), (w - 2, h - 2)], outline=(150, 150, 190, 255))
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_email.gif"), 160)


def gif_divider():
    w, h = 96, 18
    frames = []
    for f in range(8):
        im = Image.new("RGB", (w, h), (28, 12, 48))
        d = ImageDraw.Draw(im)
        for x in range(w):
            v = int(90 + 60 * math.sin((x + f * 4) / 9.0))
            d.line((x, 8, x, 9), fill=(min(255, v + 60), min(255, v), 255))
        for i in range(6):
            x = (i * 17 + f * 5) % w
            d.point((x, 7), fill=(255, 255, 255))
            d.point((x + 1, 8), fill=(200, 160, 255))
            d.point((x - 1, 9), fill=(200, 160, 255))
        d.line((0, 0, w, 0), fill=(70, 40, 110))
        d.line((0, h - 1, w, h - 1), fill=(70, 40, 110))
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_divider.gif"), 120)


def gif_heart():
    w, h = 18, 16
    frames = []
    for f in range(4):
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        s = 1 + (0.06 if f in (1, 2) else 0)
        cx, cy = w / 2, h / 2
        d.ellipse((cx - 7 * s, cy - 6 * s, cx, cy + 1 * s), fill=(255, 40, 110, 255))
        d.ellipse((cx, cy - 6 * s, cx + 7 * s, cy + 1 * s), fill=(255, 40, 110, 255))
        d.polygon([(cx - 7 * s, cy - 1 * s), (cx + 7 * s, cy - 1 * s), (cx, cy + 7 * s)],
                  fill=(255, 40, 110, 255))
        d.ellipse((cx - 5 * s, cy - 4 * s, cx - 2 * s, cy - 1 * s), fill=(255, 170, 200, 255))
        frames.append(im)
    save_gif(frames, os.path.join(OUT, "gif_heart.gif"), 220)


def broken_icon():
    w, h = 120, 92
    im = Image.new("RGB", (w, h), (238, 238, 238))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), outline=(160, 160, 160))
    d.rectangle((0, 0, w - 1, 12), fill=(200, 200, 200))
    d.text((3, 2), "marcy_hs.jpg", font=ImageFont.truetype(VERDANA, 8), fill=(70, 70, 70))
    # torn page
    d.polygon([(40, 26), (78, 24), (84, 30), (80, 68), (44, 70), (38, 62)],
              fill=(252, 252, 246), outline=(120, 120, 120))
    for i in range(5):
        d.line((47, 36 + i * 7, 72 - (i % 2) * 6, 35 + i * 7), fill=(150, 150, 150))
    d.line((34, 20, 90, 76), fill=(190, 30, 30), width=3)
    d.line((90, 20, 34, 76), fill=(190, 30, 30), width=3)
    jpeg_crush(im.resize((w, h)), os.path.join(OUT, "broken.jpg"), quality=55, passes=1, final=80)
    print("  broken.jpg")


if __name__ == "__main__":
    print("photos")
    photo("team.png", "photo_team", 400, 300, warm=(1.04, 0.99, 0.93))
    photo("piano.png", "photo_piano", 400, 300, warm=(1.08, 0.96, 0.88))
    photo("desk.png", "photo_desk", 400, 300, warm=(1.0, 0.97, 1.03))
    photo("family.png", "photo_family", 400, 300, warm=(1.06, 1.0, 0.9))
    photo("hallway.png", "photo_hallway", 400, 300, warm=(0.98, 1.0, 1.05))
    print("substrate")
    substrate("wall.png", "sub_wall", 1600, 900, 0.5)
    substrate("eye.png", "sub_eye", 760, 1140, 0.42)
    print("tiles")
    tiles()
    print("gifs")
    gif_construct()
    gif_new()
    gif_star()
    gif_flame()
    gif_email()
    gif_divider()
    gif_heart()
    broken_icon()
    print("done")
