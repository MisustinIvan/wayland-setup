#!/bin/sh
echo "Copying config files..."

set -x

NIRI_CFG_PATH="$HOME/.config/niri"
mkdir -p "$NIRI_CFG_PATH"
cp ./config.kdl "$NIRI_CFG_PATH"

FUZZEL_CFG_PATH="$HOME/.config/fuzzel"
mkdir -p "$FUZZEL_CFG_PATH"
cp ./fuzzel.ini "$FUZZEL_CFG_PATH"

WAYBAR_CFG_PATH="$HOME/.config/waybar"
mkdir -p "$WAYBAR_CFG_PATH"
cp ./config.jsonc "$WAYBAR_CFG_PATH"
cp ./style.css "$WAYBAR_CFG_PATH"
cp ./elapsed.sh "$WAYBAR_CFG_PATH"

MAKO_CFG_PATH="$HOME/.config/mako"
mkdir -p "$MAKO_CFG_PATH"
cp ./config "$MAKO_CFG_PATH"

WALLPAPER_PATH="$HOME/Pictures/Wallpapers"
mkdir -p "$WALLPAPER_PATH"
cp -r ./Wallpapers "$WALLPAPER_PATH"

KEYBOARD_DAEMON_PATH="$HOME/.local/bin/keyboard_daemon.py"
cp -r ./keyboard_daemon.py "$KEYBOARD_DAEMON_PATH"

set +x

echo "Config files copied successfully"
