#!/usr/bin/env python3
"""Make six low-resolution, scanned-looking photos for Marcy's 1999 album.

Source files are the generated photos in .impeccable/raw/. The output is what a
point-and-shoot print or a flatbed scan would have looked like on a 1999 page:
320x240, soft, slightly noisy, JPEG-crushed, with a warm cast.
"""
import os
import random
from PIL import Image, ImageEnhance, ImageFilter

ROOT = "/home/pat/impetus/2_PUBLISHED/fubar.patpadgett.com"
RAW = os.path.join(ROOT, ".impeccable/raw")
OUT = os.path.join(ROOT, "assets/img")
random.seed(19990314)

SOURCES = [
    ("test-marcy.png", "photo_marcy.jpg"),
    ("team.png", "photo_team.jpg"),
    ("piano.png", "photo_piano.jpg"),
    ("family.png", "photo_family.jpg"),
    ("desk.png", "photo_desk.jpg"),
    ("hallway.png", "photo_hallway.jpg"),
]


def crop_4_3(im):
    w, h = im.size
    target = 4 / 3
    if w / h > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / target)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def scan(src_name, dst_name):
    im = Image.open(os.path.join(RAW, src_name)).convert("RGB")
    im = crop_4_3(im).resize((320, 240), Image.LANCZOS)

    # the soft focus of a cheap camera and a flatbed scan
    im = im.filter(ImageFilter.GaussianBlur(0.45))
    im = ImageEnhance.Sharpness(im).enhance(0.88)
    im = ImageEnhance.Color(im).enhance(0.86)
    im = ImageEnhance.Contrast(im).enhance(0.94)

    # a warm print cast
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.025)))
    b = b.point(lambda v: int(v * 0.965))
    im = Image.merge("RGB", (r, g, b))

    # fine grain: mostly dark specks, a few bright ones
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            n = random.random()
            if n < 0.055:
                d = random.randint(-26, -8)
            elif n > 0.975:
                d = random.randint(8, 22)
            else:
                continue
            p = px[x, y]
            px[x, y] = tuple(max(0, min(255, c + d)) for c in p)

    im.save(os.path.join(OUT, dst_name), "JPEG", quality=58, optimize=True)
    print("wrote", dst_name, os.path.getsize(os.path.join(OUT, dst_name)), "bytes")


for src, dst in SOURCES:
    scan(src, dst)
