#!/usr/bin/env python3
"""A seamless ribbed-bone wall. Tiles in both axes; the substrate must have
structure everywhere, because a hole can open anywhere."""
import math
from PIL import Image

S = 512
im = Image.new("RGB", (S, S))
px = im.load()

for y in range(S):
    for x in range(S):
        u = (x % 64) / 64.0
        rib = math.sin(math.pi * u) ** 1.7
        # vertebral segmentation, periodic in y
        v = 0.74 + 0.26 * math.sin(2 * math.pi * y / 128 + 0.7 * math.sin(2 * math.pi * x / 256))
        base = rib * v
        # a fine second rib tucked behind
        base += 0.30 * (math.sin(2 * math.pi * (x % 128) / 128 + 1.1) ** 2) * 0.22
        # deep crevice between ribs
        if u < 0.035 or u > 0.965:
            base *= 0.28
        val = 14 + 168 * (base ** 1.34)
        # a soft sheen, never a hot spot
        val += 10 * rib
        if val > 255:
            val = 255
        # bone: warm ivory, cooler in the shadow
        shade = val / 255.0
        r = int(val * (0.86 + 0.20 * shade))
        g = int(val * (0.82 + 0.17 * shade))
        b = int(val * (0.72 + 0.14 * shade))
        px[x, y] = (min(255, r), min(255, g), min(255, b))

im.save("assets/img/sub_ribs.png")
print("sub_ribs.png", im.size)
