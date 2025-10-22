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

MAKO_CFG_PATH="$HOME/.config/mako"
mkdir -p "$MAKO_CFG_PATH"
cp ./config "$MAKO_CFG_PATH"

set +x

echo "Config files copied successfully"
