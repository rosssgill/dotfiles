# dotfiles

Arch Linux + Hyprland (Lua config) desktop, themed from the current wallpaper with matugen. Managed with [GNU Stow](https://www.gnu.org/software/stow/).

| Package | What it configures |
|---|---|
| `hypr` | Hyprland: keybinds, autostart, workspaces, window rules |
| `waybar` | Top bar, plus scripts for workspace icons and now playing |
| `matugen` | Templates that generate colours for everything below from the wallpaper |
| `kitty` | Terminal |
| `waypaper` | Wallpaper picker (runs matugen after each change) |
| `wofi`, `dunst` | Launcher and notifications (only matugen-generated files, so empty in git) |
| `gtk-3.0`, `gtk-4.0` | Dark `adw-gtk3` theme for GTK apps |
| `zsh` | `.zshrc` (Oh My Zsh) |
| `git` | `.gitconfig` |
| `vscode` | Local "Matugen" VS Code colour theme |

## Dependencies

### Official repos

```sh
sudo pacman -S --needed \
  hyprland hyprlauncher xdg-desktop-portal-hyprland hyprpolkitagent \
  waybar kitty wofi dunst dolphin \
  awww matugen adw-gtk-theme ttf-jetbrains-mono-nerd \
  python playerctl pavucontrol pamixer wireplumber brightnessctl \
  network-manager-applet blueman btop \
  grim satty wl-clipboard imv \
  firefox discord \
  zsh git stow less
```

| Package | Used for |
|---|---|
| `hyprland`, `xdg-desktop-portal-hyprland`, `hyprpolkitagent` | Compositor, screen sharing, auth prompts |
| `hyprlauncher` | App launcher (`menu` in hyprland.lua) |
| `waybar` | Bar |
| `kitty` | Terminal (also opens `btop`/`nmtui` from the bar) |
| `wofi` | App launcher from the bar's Arch logo |
| `dunst` | Notifications |
| `dolphin` | File manager |
| `awww` | Wallpaper daemon (the renamed swww) |
| `matugen` | Generates colour schemes from the wallpaper |
| `adw-gtk-theme` | `adw-gtk3-dark` GTK theme |
| `ttf-jetbrains-mono-nerd` | Bar font and icons (uses the "Propo" variant) |
| `python` | Waybar workspace and media scripts |
| `playerctl` | Now-playing in the bar, media keys |
| `pavucontrol`, `pamixer`, `wireplumber` (`wpctl`) | Volume dropdown, mute, volume keys |
| `brightnessctl` | Brightness keys / bar scroll |
| `network-manager-applet` | Tray applet and `nm-connection-editor` |
| `blueman` | Bluetooth manager (bar click) |
| `btop` | System monitor (CPU/memory click) |
| `grim`, `satty`, `wl-clipboard` | Screenshots, annotation, clipboard |
| `imv` | Image viewer |
| `firefox`, `discord` | Autostarted on workspaces 2 and 3 |
| `zsh`, `less` | Shell, pager |
| `git`, `stow` | These dotfiles |

### AUR (via `paru`)

```sh
paru -S --needed waypaper wttrbar grimblast-git python-pywalfox pear-desktop-bin visual-studio-code-bin
```

| Package | Used for |
|---|---|
| `waypaper` | Wallpaper picker GUI |
| `wttrbar` | Weather in the bar |
| `grimblast-git` | Screenshot keybinds (Print, Shift/Ctrl/Alt+Print) |
| `python-pywalfox` | Firefox theming (with the Pywalfox extension) |
| `pear-desktop-bin` | YouTube Music app, autostarted on workspace 4 |
| `visual-studio-code-bin` | Editor |

### Other

- [Oh My Zsh](https://ohmyz.sh/): `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --keep-zshrc`
- [Pywalfox Firefox extension](https://addons.mozilla.org/firefox/addon/pywalfox/)

## Setting up a new machine

1. Install the dependencies above.
2. Clone and link:
   ```sh
   git clone git@github.com:<you>/dotfiles.git ~/.dotfiles
   cd ~/.dotfiles
   stow */
   ```
   If stow reports conflicts, an app has already created its own config there. Move it aside (`mv ~/.config/<app> ~/.config/<app>.orig`) and run `stow */` again.
3. Add wallpapers and create the screenshot folder:
   ```sh
   mkdir -p ~/Pictures/Wallpapers ~/Pictures/Screenshots
   ```
4. Log into Hyprland, open Waypaper and pick a wallpaper. This runs matugen, which generates all the colour files that aren't in git.
5. One-off app setup:
   - **GTK:** `gsettings set org.gnome.desktop.interface gtk-theme adw-gtk3-dark && gsettings set org.gnome.desktop.interface color-scheme prefer-dark`
   - **Firefox:** `pywalfox install --manifest-path ~/.config/mozilla/native-messaging-hosts`, then click "Fetch Pywal colors" in the extension.
   - **Pear Desktop:** add `~/.config/matugen/generated/pear-desktop.css` under Options → Visual Tweaks → Themes (or `options.themes` in `~/.config/YouTube Music/config.json`). Press Ctrl+R in the app after changing wallpaper.
   - **VS Code:** Preferences → Color Theme → **Matugen**.
   - **Shell:** `chsh -s /usr/bin/zsh`

### Machine-specific bits

`hypr/.config/hypr/hyprland.lua` assumes two monitors, `DP-2` (left) and `DP-3` (right), with workspaces 2–4 on the right. Check yours with `hyprctl monitors` and adjust the `hl.monitor` and `hl.workspace_rule` lines.

## Day to day

Edit configs in `~/.config` as normal (they're symlinks into this repo), then commit here:

```sh
cd ~/.dotfiles && git add -A && git commit -m "..." && git push
```

To track a new app's config:

```sh
mkdir -p ~/.dotfiles/<app>/.config
mv ~/.config/<app> ~/.dotfiles/<app>/.config/
cd ~/.dotfiles && stow <app>
```

Files generated by matugen are listed in `.gitignore` and are recreated whenever the wallpaper changes.
