#!/usr/bin/env bash
# Builds the rEFInd theme from the current wallpaper and installs it, plus the folded Arch boot entry. Run with: sudo ~/.dotfiles/refind/install.sh
set -euo pipefail
[ "$EUID" -eq 0 ] || { echo "Run with sudo: the EFI partition is root-only" >&2; exit 1; }

user_home=$(getent passwd "${SUDO_USER:?run via sudo}" | cut -d: -f6)
refind=/boot/EFI/refind
theme=$refind/themes/nox-matugen
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT

python3 -I "$(dirname "$(realpath "$0")")/build.py" "$user_home/.config/matugen/generated/refind.env" "$build/theme"
mkdir -p "$refind/themes"
rm -rf "$theme"
cp -r "$build/theme" "$theme"

cp "$(dirname "$(realpath "$0")")/arch.conf" "$refind/arch.conf"

for line in 'include arch.conf' 'include themes/nox-matugen/theme.conf'; do
    grep -qxF "$line" "$refind/refind.conf" || printf '\n%s\n' "$line" >> "$refind/refind.conf"
done
echo "Installed $theme"
