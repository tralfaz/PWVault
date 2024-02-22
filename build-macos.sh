#!/bin/sh
#
# PyInstaller: https://pyinstaller.org/en/stable/index.html
# ImageToIcons:
#   https://apps.apple.com/us/app/image2icon-make-your-icons/id992115977?mt=12
#
set -x

if [ -e PWVault.spec ]; then
  pyinstaller --noconfirm PWVault.spec

else
  pyinstaller --windowed \
              --noconfirm \
              --osx-bundle-identifier com.midoma.pyapps.pwvault pwvuiapp.py \
              --name PWVault
fi
