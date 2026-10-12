#!/usr/bin/env python3
"""Waybar button for one Hyprland workspace.

Usage: workspace.py <id>

Shows the app's icon when every window on the workspace belongs to the same known
app, otherwise the workspace number. Emits one JSON line per change, with CSS
classes: active (focused), visible (shown on the other monitor), empty.
"""
import json
import os
import socket
import subprocess
import sys

WS = int(sys.argv[1])

# Window class (lowercase) -> Nerd Font icon
ICONS = {
    "firefox": "\U000F0239",
    "discord": "\U000F066F",
    "vesktop": "\U000F066F",
    "kitty": "\U000F011B",
    "org.kde.dolphin": "\U000F024B",
    "steam": "\U000F04D3",
    "spotify": "\U000F04C7",
    "code": "\U000F0A1E",
    "com.microsoft.vscode": "\U000F0A1E",
    "chromium": "\U000F02AF",
    "com.github.th-ch.youtube-music": "\U000F075A",
}

# Events that can change what this button should show
EVENTS = {
    "workspace", "workspacev2", "focusedmon", "focusedmonv2",
    "openwindow", "closewindow", "movewindow", "movewindowv2",
    "createworkspace", "destroyworkspace", "moveworkspace", "moveworkspacev2",
}


def hyprctl(what):
    out = subprocess.run(["hyprctl", "-j", what], capture_output=True, text=True).stdout
    return json.loads(out or "[]")


def render():
    windows = [c for c in hyprctl("clients") if c["workspace"]["id"] == WS and c["mapped"]]
    monitors = hyprctl("monitors")

    classes = []
    if any(m["focused"] and m["activeWorkspace"]["id"] == WS for m in monitors):
        classes.append("active")
    elif any(m["activeWorkspace"]["id"] == WS for m in monitors):
        classes.append("visible")
    if not windows:
        classes.append("empty")

    text = str(WS)
    apps = {w["class"].lower() for w in windows}
    if len(apps) == 1:
        text = ICONS.get(apps.pop(), text)

    tooltip = "\n".join(w["title"] for w in windows) or f"Workspace {WS}"
    return json.dumps({"text": text, "class": classes, "tooltip": tooltip})


def main():
    path = os.path.join(
        os.environ["XDG_RUNTIME_DIR"], "hypr",
        os.environ["HYPRLAND_INSTANCE_SIGNATURE"], ".socket2.sock",
    )
    sock = socket.socket(socket.AF_UNIX)
    sock.connect(path)

    last = None
    buf = b""
    while True:
        line = render()
        if line != last:
            print(line, flush=True)
            last = line

        # Block until a relevant event arrives
        while True:
            data = sock.recv(4096)
            if not data:
                return
            buf += data
            *lines, buf = buf.split(b"\n")
            if any(l.split(b">>", 1)[0].decode() in EVENTS for l in lines):
                break


if __name__ == "__main__":
    main()
