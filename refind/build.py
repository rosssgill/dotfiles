#!/usr/bin/env python3
"""Build the rEFInd theme: wallpaper background and accent-coloured selection images from matugen's output."""
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

SIZE = (2560, 1440)
here = Path(__file__).resolve().parent
env_file = Path(sys.argv[1])
out = Path(sys.argv[2])

env = dict(line.split("=", 1) for line in env_file.read_text().splitlines() if "=" in line)
accent = tuple(int(env["PRIMARY"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

shutil.rmtree(out, ignore_errors=True)
shutil.copytree(here / "theme", out)

# Cover-crop to the screen size; darkened so nox's white icons stay readable
Image.MAX_IMAGE_PIXELS = None
wallpaper = Image.open(env["WALLPAPER"]).convert("RGB")
scale = max(SIZE[0] / wallpaper.width, SIZE[1] / wallpaper.height)
wallpaper = wallpaper.resize((round(wallpaper.width * scale), round(wallpaper.height * scale)), Image.LANCZOS)
left, top = (wallpaper.width - SIZE[0]) // 2, (wallpaper.height - SIZE[1]) // 2
wallpaper = wallpaper.crop((left, top, left + SIZE[0], top + SIZE[1]))
ImageEnhance.Brightness(wallpaper).enhance(0.5).save(out / "background.png", optimize=True)

# Keep each selection image's shape (alpha), replace its colour with the accent
for name in ("selection_big.png", "selection_small.png"):
    shape = Image.open(out / name).convert("RGBA")
    tinted = Image.new("RGBA", shape.size, accent + (0,))
    tinted.putalpha(shape.getchannel("A"))
    tinted.save(out / name)
