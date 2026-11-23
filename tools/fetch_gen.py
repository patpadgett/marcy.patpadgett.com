#!/usr/bin/env python3
"""Fetch generated images through wsrv.nl (the vultr object host is blocked by the
local router). Usage: fetch_gen.py name=url [name=url ...]
"""
import sys, os, subprocess, urllib.parse

OUT = os.path.join(os.path.dirname(__file__), "..", ".impeccable", "raw")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)


def fetch(url, dest):
    proxied = "https://wsrv.nl/?url=" + urllib.parse.quote(url, safe="")
    r = subprocess.run(
        ["curl", "-4", "-sS", "-L", "--max-time", "90", "-o", dest,
         "-w", "%{http_code} %{size_download}", proxied],
        capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        name, _, url = arg.partition("=")
        dest = os.path.join(OUT, name + ".png")
        code, info = fetch(url, dest)
        print(name, code, info)
