#!/usr/bin/env python3
"""Turn 512x512 portrait PNGs into round token webps.

usage: make_tokens.py SRC_DIR OUT_DIR
SRC_DIR holds token-<key>.png (square portraits); OUT_DIR gets token-<key>.webp:
circle-masked, a thin dark ring, transparent corners, 512px.
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFilter

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
S = 512
for p in sorted(src.glob("token-*.png")):
    im = Image.open(p).convert("RGBA")
    w, h = im.size
    m = min(w, h)
    im = im.crop(((w - m) // 2, (h - m) // 2, (w - m) // 2 + m, (h - m) // 2 + m)).resize((S, S), Image.LANCZOS)
    mask = Image.new("L", (S * 4, S * 4), 0)
    ImageDraw.Draw(mask).ellipse((8, 8, S * 4 - 8, S * 4 - 8), fill=255)
    mask = mask.resize((S, S), Image.LANCZOS)
    im.putalpha(mask)
    ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(ring)
    d.ellipse((2, 2, S - 3, S - 3), outline=(28, 20, 14, 255), width=10)
    d.ellipse((10, 10, S - 11, S - 11), outline=(196, 160, 96, 255), width=3)
    im = Image.alpha_composite(im, ring)
    im.save(out / (p.stem + ".webp"), "WEBP", quality=88, method=6)
    print("wrote", p.stem + ".webp")
