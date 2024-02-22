#!/bin/sh
#
# PyInstaller: https://pyinstaller.org/en/stable/index.html
#
set -x
PYINST=$HOME/.local/bin/pyinstaller

if [ -e PWVault.spec ]; then
  $PYINST --noconfirm PWVault.spec

else
  cp linux-PWVault.spec PWVault.spec
  $PYINST --windowed \
          --noconfirm \
          --name PWVault pwvuiapp.py
fi
