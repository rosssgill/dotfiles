#!/usr/bin/env bash
# Copies the current wallpaper and matugen colours into the SDDM astronaut theme.
# SDDM can't read ~, so files are copied into the theme. One-time setup (README) makes these paths user-writable.
theme=/usr/share/sddm/themes/sddm-astronaut-theme
src=~/.config/matugen/generated/sddm-astronaut.conf
[ -w "$theme/Backgrounds/matugen" ] && [ -w "$theme/Themes/astronaut.conf.user" ] || exit 0

wallpaper=$(sed -n 's/^# wallpaper: //p' "$src")
# Scaled to screen size: Qt refuses images over 256MB decoded, which large wallpapers exceed
python3 -I - "$wallpaper" "$theme/Backgrounds/matugen/wallpaper.jpg" <<'PY'
import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
im = Image.open(sys.argv[1]).convert("RGB")
scale = max(2560 / im.width, 1440 / im.height)
if scale < 1:
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
im.save(sys.argv[2], quality=92)
PY
{ cat "$src"; echo 'Background="Backgrounds/matugen/wallpaper.jpg"'; } > "$theme/Themes/astronaut.conf.user"
