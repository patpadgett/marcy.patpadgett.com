#!/usr/bin/env python3
"""A torn-paper alpha mask for the fragment card. Real torn stock has a
fibrous, irregular edge and a few deep bites — a polygon cannot fake it."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

W, H = 720, 540
random.seed(7)

im = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(im)

def edge(n, a, b, wobble=5.0, step=3):
    """points from a to b with high-frequency jitter"""
    out = []
    for i in range(n + 1):
        t = i / n
        x = a[0] + (b[0] - a[0]) * t
        y = a[1] + (b[1] - a[1]) * t
        out.append((x + random.uniform(-wobble, wobble), y + random.uniform(-wobble, wobble)))
    return out

m = 10
pts = []
pts += edge(180, (m, m), (W - m, m), 15)
pts += edge(140, (W - m, m), (W - m, H - m), 15)
pts += edge(180, (W - m, H - m), (m, H - m), 15)
pts += edge(140, (m, H - m), (m, m), 15)
d.polygon(pts, fill=255)

# a few deep bites, so the silhouette is not a rounded rectangle
for _ in range(11):
    side = random.choice(["t", "b", "l", "r"])
    if side == "t":
        cx, cy = random.uniform(40, W - 40), m
    elif side == "b":
        cx, cy = random.uniform(40, W - 40), H - m
    elif side == "l":
        cx, cy = m, random.uniform(40, H - 40)
    else:
        cx, cy = W - m, random.uniform(40, H - 40)
    r = random.uniform(18, 54)
    bite = []
    for i in range(14):
        a = i / 14 * 6.283
        rr = r * random.uniform(0.55, 1.35)
        bite.append((cx + rr * 1.6 * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(bite, fill=0)

im = im.filter(ImageFilter.GaussianBlur(0.9))
# soften the very edge a touch more without losing the fibre
im = im.point(lambda v: 255 if v > 128 else (int(v * 1.6) if v > 60 else 0))
im.save("assets/img/torn.png")
print("torn.png", im.size)
