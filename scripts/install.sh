#!/bin/bash

set -euo pipefail

curdir=$(realpath "$(dirname "$0")")
rootdir=$(dirname "$curdir")

cat >~/.config/autostart/background-switcher.desktop <<EOF
[Desktop Entry]
Name=Background switcher
Exec=/usr/bin/bash -c "source $rootdir/.env && $rootdir/background-switcher"
EOF

echo "Script installed successfully in ~/.config/autostart/background-switcher.desktop"
