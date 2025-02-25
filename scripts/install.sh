#!/bin/bash

set -euo pipefail

curdir=$(realpath "$(dirname "$0")")
executable_path=$(dirname "$curdir")/background-switcher

cat >~/.config/autostart/background-switcher.desktop <<EOF
[Desktop Entry]
Name=Background switcher
Exec=$executable_path
EOF

echo "Script installed successfully in ~/.config/autostart/background-switcher.desktop"
