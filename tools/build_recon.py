#!/usr/bin/env python3
"""Build the plates for /reconstruction.html.

Five exposures, each carrying its own failure:
  1 bedroom  - warm, whole. the lie as she told it.
  2 cake     - the record, misregistered. three channels that do not agree.
  3 corridor - the machine's emptiness, printed in halftone.
  4 street   - the night the message lands, sodium and cyan.
  5 print    - the team photo, as a physical object. she is not in it.
"""
import os
from PIL import Image, ImageChops, ImageFilter, ImageEnhance, ImageDraw
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, '.impeccable', 'raw', 'recon')
IMG = os.path.join(ROOT, 'assets', 'img')
OUT = os.path.join(ROOT, 'assets', 'recon')
os.makedirs(OUT, exist_ok=True)

W, H = 2400, 1004          # 2.39:1
MW, MH = 1100, 460         # mobile


def cover(im, w, h, fx=0.5, fy=0.5):
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * fx)
    y = int((nh - h) * fy)
    return im.crop((x, y, x + w, y + h))


def grade(im, lift=(0, 0, 0), gain=(1, 1, 1), sat=1.0, contrast=1.0, gamma=None):
    r, g, b = im.split()
    lut_gain = lambda c, k: c.point(lambda v, k=k: min(255, int(v * k)))
    r, g, b = lut_gain(r, gain[0]), lut_gain(g, gain[1]), lut_gain(b, gain[2])
    im = Image.merge('RGB', (r, g, b))
    if lift != (0, 0, 0):
        im = ImageChops.add(im, Image.new('RGB', im.size, lift))
    if sat != 1.0:
        im = ImageEnhance.Color(im).enhance(sat)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    return im


def halation(im, radius=26, strength=0.30, tint=(255, 176, 128)):
    """Light bleeds through the emulsion: bloom the highlights warm."""
    l = im.convert('L')
    hi = l.point(lambda v: max(0, v - 168) * 3 if v > 168 else 0)
    bloom = hi.filter(ImageFilter.GaussianBlur(radius)).convert('RGB')
    bloom = ImageChops.multiply(bloom, Image.new('RGB', im.size, tint))
    return ImageChops.screen(im, ImageEnhance.Brightness(bloom).enhance(strength * 2.2))


def grain(im, sigma=22, opacity=0.16):
    n = Image.effect_noise(im.size, sigma).convert('RGB')
    return Image.blend(im, ImageChops.overlay(im, n), opacity)


def vignette(im, amount=0.55):
    w, h = im.size
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.30, -h * 0.42, w * 1.30, h * 1.42), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.16))
    dark = ImageEnhance.Brightness(im).enhance(1 - amount)
    return Image.composite(im, dark, mask)


def misregister(im, dx=7, dy=3, ghost=0.42):
    """Three channels, three slightly different exposures of the same moment."""
    r, g, b = im.split()
    r = ImageChops.offset(r, dx, dy)
    b = ImageChops.offset(b, -dx, -dy)
    out = Image.merge('RGB', (r, g, b))
    # a second impression, translucent, a hair to the left
    dup = ImageChops.offset(im, int(-dx * 3.4), int(dy * 2.2))
    out = Image.blend(out, dup, ghost * 0.42)
    return out


def halftone(im, cell=7, angleless=True):
    """A printed dot screen, at full resolution."""
    w, h = im.size
    small = im.convert('L').resize((w // cell, h // cell), Image.LANCZOS)
    small = ImageEnhance.Contrast(small).enhance(1.25)
    out = Image.new('L', (w, h), 255)
    d = ImageDraw.Draw(out)
    px = small.load()
    step = cell
    for y in range(small.size[1]):
        for x in range(small.size[0]):
            v = px[x, y]
            radius = (1 - v / 255.0) ** 0.72 * (step * 0.62)
            if radius < 0.35:
                continue
            cx, cy = x * step + step / 2, y * step + step / 2
            d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=int(v * 0.35))
    return out.convert('RGB')


def dropout(im, rows=9, seed=7):
    rnd = random.Random(seed)
    w, h = im.size
    out = im.copy()
    d = ImageDraw.Draw(out)
    for _ in range(rows):
        y = rnd.uniform(0, h)
        band = rnd.uniform(2, 14)
        mode = rnd.random()
        if mode < 0.55:
            d.rectangle((0, y, w, y + band), fill=(6, 6, 7))
        elif mode < 0.8:
            d.rectangle((0, y, w, y + band * 0.4), fill=(232, 226, 214))
        else:
            d.rectangle((0, y, rnd.uniform(w * 0.3, w), y + band * 0.5), fill=(6, 6, 7))
    return out


def scan(im, every=4, opacity=0.16):
    w, h = im.size
    band = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(band)
    for y in range(0, h, every):
        d.line((0, y, w, y), fill=255)
    dark = ImageEnhance.Brightness(im).enhance(1 - opacity)
    return Image.composite(dark, im, band)


def save(im, name, quality=84):
    im.save(os.path.join(OUT, name), 'JPEG', quality=quality, optimize=True, progressive=True)
    m = im.resize((MW, int(im.size[1] * MW / im.size[0])), Image.LANCZOS)
    m.save(os.path.join(OUT, name.replace('.jpg', '-sm.jpg')), 'JPEG', quality=82, optimize=True)
    print(name, im.size, os.path.getsize(os.path.join(OUT, name)) // 1024, 'KB')


# ---------------------------------------------------------------- 1 the lie
b = Image.open(os.path.join(RAW, 'r-bedroom.png')).convert('RGB')
im = cover(b, W, H, fx=0.52, fy=0.50)
im = grade(im, lift=(4, 2, 0), gain=(1.06, 1.00, 0.94), sat=1.04, contrast=1.05)
im = halation(im, 30, 0.34, (255, 170, 118))
im = grain(im, 20, 0.15)
im = vignette(im, 0.50)
save(im, 'plate1.jpg')

# ------------------------------------------------------------ 2 the record
c = Image.open(os.path.join(RAW, 'r-cake.png')).convert('RGB')
im = cover(c, W, H, fx=0.5, fy=0.55)
im = grade(im, lift=(0, 2, 1), gain=(1.10, 1.02, 0.96), sat=1.10, contrast=1.08)
im = misregister(im, 7, 3, 0.42)
im = halation(im, 22, 0.26, (255, 150, 120))
im = grain(im, 26, 0.18)
im = vignette(im, 0.56)
save(im, 'plate2.jpg')

# ----------------------------------------------------------- 3 the machine
k = Image.open(os.path.join(RAW, 'r-corridor.png')).convert('RGB')
im = cover(k, W, H, fx=0.5, fy=0.5)
im = grade(im, lift=(0, 0, 2), gain=(0.94, 0.97, 1.02), sat=0.30, contrast=1.16)
im = Image.blend(im, halftone(im, 7), 0.52)
im = grade(im, gain=(1.0, 1.02, 1.06), contrast=1.05)
im = dropout(im, 11, 11)
im = grain(im, 16, 0.20)
im = vignette(im, 0.60)
save(im, 'plate3.jpg', 80)

# ------------------------------------------------------------- 4 the night
s = Image.open(os.path.join(RAW, 'r-street.png')).convert('RGB')
im = cover(s, W, H, fx=0.5, fy=0.62)
im = grade(im, lift=(10, 6, 0), gain=(1.10, 1.00, 0.86), sat=1.06, contrast=1.06)
im = halation(im, 46, 0.62, (255, 148, 78))
im = halation(im, 14, 0.30, (255, 190, 130))
# a light leak: the film was not wound on properly
leak = Image.new('RGB', im.size, (0, 0, 0))
d = ImageDraw.Draw(leak)
d.ellipse((-W * 0.35, -H * 0.9, W * 0.30, H * 0.55), fill=(120, 52, 12))
leak = leak.filter(ImageFilter.GaussianBlur(180))
im = ImageChops.add(im, leak)
im = grain(im, 26, 0.19)
im = vignette(im, 0.58)
save(im, 'plate4.jpg')

# ------------------------------------------------------------ 5 the object
t = Image.open(os.path.join(IMG, 'photo_team.jpg')).convert('RGB')
im = grade(t, lift=(6, 6, 4), gain=(0.96, 0.98, 1.02), sat=0.52, contrast=1.02)
im = grain(im, 18, 0.14)
im = im.resize((1500, int(im.size[1] * 1500 / im.size[0])), Image.LANCZOS)
im.save(os.path.join(OUT, 'print.jpg'), 'JPEG', quality=86, optimize=True, progressive=True)
print('print.jpg', im.size, os.path.getsize(os.path.join(OUT, 'print.jpg')) // 1024, 'KB')
