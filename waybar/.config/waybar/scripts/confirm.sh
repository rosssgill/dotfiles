#!/usr/bin/env bash
# Usage: confirm.sh "Question?" command [args...]  Runs the command only if "Yes" is chosen.
question=$1; shift
pkill -x rofi
choice=$(printf 'Yes\nNo\n' | rofi -dmenu -no-custom -selected-row 1 -mesg "$question" -theme-str '
    window { width: 260px; }
    mainbox { children: [ message, listview ]; }
    message { padding: 6px 10px; }
    textbox { horizontal-align: 0.5; }
    listview { lines: 2; }
    element { children: [ element-text ]; }
    element-text { horizontal-align: 0.5; }')
[ "$choice" = "Yes" ] && exec "$@"
