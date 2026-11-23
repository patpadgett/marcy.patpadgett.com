#!/usr/bin/env python3
"""Embed the provenance of every shipping raster. Reads the same prompts the
generator used, so the record cannot drift from the asset."""
import json
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLI = "/home/pat/.hermes/skills/impeccable/scripts/impeccable"

GEN = {
    "photo_team": "z-image-turbo text-to-image: 1999 high school yearbook photograph of a girls junior varsity volleyball team, eight girls in matching navy blue jerseys kneeling and standing in a school gymnasium, arms around each other, smiling, slightly soft focus, direct on-camera flash, warm film color cast, 35mm grain, scanned from a print, wide shot, wholesome.",
    "photo_piano": "z-image-turbo text-to-image: close amateur photograph of a teenage girl's hands on an upright piano keyboard in a carpeted suburban living room, 1999, open sheet music on the stand, warm lamp light, slightly out of focus, film grain, scanned print, no face visible, no text.",
    "photo_desk": "z-image-turbo text-to-image: 1999 teenager bedroom desk, beige CRT monitor showing a purple webpage, beige keyboard, a volleyball trophy, a lava lamp, band posters on the wall, string lights, amateur flash photograph, cluttered and cozy, film grain, scanned print, wide shot, no people.",
    "photo_family": "z-image-turbo text-to-image: 1999 backyard barbecue family snapshot, a family of four seen from behind and from the side sitting at a wooden picnic table, paper plates and a jug of iced tea, dappled shade, faces not visible, slightly overexposed, 35mm film grain, scanned from a print.",
    "photo_hallway": "z-image-turbo text-to-image: 1999 high school hallway, a teenage girl with a backpack walking away from the camera toward a row of lockers, motion blur, fluorescent light, other students small in the distance, film grain, amateur snapshot.",
    "sub_wall": "z-image-turbo text-to-image: dark biomechanical interior, ribbed vertebral architecture of bone and brushed steel, cables like tendons, wet specular highlights, airbrushed 1970s science fiction illustration, black and bone palette, ominous, symmetrical, no text.",
    "sub_eye": "z-image-turbo text-to-image: a vast biomechanical aperture like an eye set into ribbed bone and cable, airbrushed 1970s dark science fiction illustration, bone white and black, wet highlights, symmetrical, no text.",
}

POST_PHOTO = " Post-processed in tools/build_assets.py: 4:3 crop, 400x300 (thumb 96x72), saturation -8%, warm channel curves, +-0.9px chromatic offset, film grain, vignette, unsharp mask, triple JPEG at q32/q54/q66. All people depicted are synthetic; no photograph resolves a face."
POST_SUB = " Post-processed in tools/build_assets.py: crop, resize, saturation -45%, contrast lift, grain, double JPEG."

PROC = {
    "sub_ribs": "Procedural, no image model: tools/make_ribs.py (PIL). Seamless 512x512 periodic rib field with vertebral modulation and specular crests.",
    "tile_stars": "Procedural, no image model: tools/build_assets.py, 96x96 seamless star tile, PIL.",
    "tile_stars_dark": "Procedural, no image model: tools/build_assets.py, degenerate star tile with rib bleed, PIL.",
    "broken": "Procedural, no image model: tools/build_assets.py, broken-image icon drawn with PIL (torn page, red cross, filename bar).",
    "favicon": "Procedural, no image model: 32x32 star tile favicon drawn with PIL.",
}
for g in ("gif_construct", "gif_new", "gif_star", "gif_flame", "gif_email", "gif_divider", "gif_heart"):
    PROC[g] = "Procedural, no image model: animated GIF drawn frame-by-frame with PIL in tools/build_assets.py."

manifest = {}


def embed(path, prompt):
    r = subprocess.run([CLI, "embed-prompt", path, "--prompt", prompt],
                       capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


for name, prompt in list(GEN.items()):
    for suf, post in (("", POST_PHOTO if name.startswith("photo") else POST_SUB),
                      ("_sm", " Derived from the full-size same-named file: 96x72 lanczos downscale, triple JPEG q24/q46/q54. No new generation.")):
        f = os.path.join(ROOT, "assets", "img", name + suf + ".jpg")
        if os.path.exists(f):
            full = prompt + post
            print(embed(f, full))
            manifest["assets/img/" + name + suf + ".jpg"] = full

for name, prompt in PROC.items():
    for ext in (".png", ".gif", ".jpg"):
        f = os.path.join(ROOT, "assets", "img", name + ext)
        if os.path.exists(f):
            print(embed(f, prompt))
            manifest["assets/img/" + name + ext] = prompt

with open(os.path.join(ROOT, "assets", "img", "PROVENANCE.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
print("wrote PROVENANCE.json", len(manifest))
