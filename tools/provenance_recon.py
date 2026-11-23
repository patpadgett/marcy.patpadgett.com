#!/usr/bin/env python3
"""Embed provenance for the reconstruction plates (a second, separate pipeline
from tools/provenance.py, which covers the Angelfire artifact)."""
import json
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLI = "/home/pat/.hermes/skills/impeccable/scripts/impeccable"
OUT = os.path.join(ROOT, "assets", "recon")

SRC = {
    "plate1.jpg": "z-image-turbo text-to-image: 1999 photograph of a teenage girl's bedroom at night, seen from the doorway with the light off: fairy lights along the headboard, band posters taped to the wall, a beige CRT computer switched off, a volleyball on the floor, a made bed, a window with blinds half open, warm lamp glow from the hall, film grain, amateur flash-free snapshot, no people.",
    "plate2.jpg": "z-image-turbo text-to-image: 1999 photograph of a kitchen table after a birthday: a half-eaten sheet cake with pink frosting and sixteen candles, paper plates, plastic cups, a crumpled napkin, warm tungsten light, tile floor, nobody in frame, film grain, amateur snapshot flash.",
    "plate3.jpg": "z-image-turbo text-to-image: 1999 photograph of an empty American high school corridor in daylight, blue lockers along both walls, polished floor, fluorescent lights, flyers taped to the walls, long perspective, nobody in frame, 35mm film grain, slightly overexposed.",
    "plate4.jpg": "z-image-turbo text-to-image: 1999 photograph of a quiet suburban Florida street at dusk, one sodium streetlight on, live oak trees with spanish moss, a mailbox, wet asphalt after rain, low warm horizon, no cars, no people, 35mm film grain, slightly underexposed.",
    "print.jpg": "z-image-turbo text-to-image: 1999 high school yearbook photograph of a girls junior varsity volleyball team, eight girls in matching navy blue jerseys kneeling and standing in a school gymnasium, arms around each other, smiling, slightly soft focus, direct on-camera flash, warm film color cast, 35mm grain, scanned from a print, wide shot, wholesome.",
}

POST = (" Post-processed in tools/build_recon.py (PIL): 2.39:1 crop at 2400x1004, "
        "per-act colour grade, halation, misregistration, halftone dot screen, dropout, "
        "film grain, vignette, JPEG q84. All people depicted are synthetic; no photograph "
        "resolves a face.")

PROC = {
    "plate5.jpg": ("Derived, no new image model: assets/recon/plate1.jpg (itself synthetic) "
                   "blurred, darkened and desaturated in tools/build_recon.py to serve as the "
                   "ghost plate behind the closing text."),
    "plate1-sm.jpg": "Downscale of plate1.jpg for narrow viewports (within its provenance).",
    "plate2-sm.jpg": "Downscale of plate2.jpg for narrow viewports (within its provenance).",
    "plate3-sm.jpg": "Downscale of plate3.jpg for narrow viewports (within its provenance).",
    "plate4-sm.jpg": "Downscale of plate4.jpg for narrow viewports (within its provenance).",
    "plate5-sm.jpg": "Downscale of plate5.jpg for narrow viewports (within its provenance).",
}

manifest = {}


def embed(path, prompt):
    r = subprocess.run([CLI, "embed-prompt", path, "--prompt", prompt],
                       capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


for name, prompt in SRC.items():
    path = os.path.join(OUT, name)
    if not os.path.exists(path):
        print("missing", name)
        continue
    manifest[name] = embed(path, prompt + POST)

for name, note in PROC.items():
    path = os.path.join(OUT, name)
    if not os.path.exists(path):
        continue
    manifest[name] = embed(path, note)

with open(os.path.join(OUT, "PROVENANCE.json"), "w") as f:
    json.dump(manifest, f, indent=2, sort_keys=True)
    f.write("\n")

for k, v in manifest.items():
    print(k, "->", (v or "")[:90])
