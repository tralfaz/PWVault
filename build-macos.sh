#!/bin/sh
#
# PyInstaller: https://pyinstaller.org/en/stable/index.html
#   pip install pyinstaller
# ImageToIcons:
#   https://apps.apple.com/us/app/image2icon-make-your-icons/id992115977?mt=12
#
set -x

if [ -e macos-PWVault.spec ]; then
  if [ macos-PWVault.spec -nt PWVault.spec ]; then
    cp macos-PWVault.spec PWVault.spec
  fi

  pyinstaller --noconfirm PWVault.spec

else
  pyinstaller --windowed \
              --noconfirm \
              --osx-bundle-identifier com.midoma.pyapps.pwvault pwvuiapp.py \
              --name PWVault
fi
