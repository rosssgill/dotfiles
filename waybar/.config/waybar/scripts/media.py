#!/usr/bin/env python3
"""Waybar media module: shows the active player's song via `playerctl --follow`.

Replaces Waybar's built-in mpris module, which segfaults in Waybar 0.15 when
players appear or disappear. Emits one JSON line per change; empty text hides it.
"""
import html
import json
import subprocess

MAX_LENGTH = 35
FORMAT = "\t".join(["{{status}}", "{{artist}}", "{{title}}", "{{album}}", "{{playerName}}"])

proc = subprocess.Popen(
    ["playerctl", "--follow", "metadata", "--format", FORMAT],
    stdout=subprocess.PIPE, text=True, bufsize=1,
)
for line in proc.stdout:
    status, artist, title, album, player = (line.rstrip("\n").split("\t") + [""] * 5)[:5]
    if status not in ("Playing", "Paused"):
        print(json.dumps({"text": "", "class": "stopped"}), flush=True)
        continue

    label = " - ".join(p for p in (artist, title) if p)
    if len(label) > MAX_LENGTH:
        label = label[: MAX_LENGTH - 1] + "…"
    label = html.escape(label)
    text = f"🎵 {label}" if status == "Playing" else f"⏸ <i>{label}</i>"

    tooltip = "\n".join(html.escape(p) for p in (title, artist, album, f"via {player}") if p)
    print(json.dumps({"text": text, "tooltip": tooltip, "class": status.lower()}), flush=True)
