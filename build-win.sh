#!/bin/sh
#
# PyInstaller: https://pyinstaller.org/en/stable/index.html
# ImageToIcons:
#   https://apps.apple.com/us/app/image2icon-make-your-icons/id992115977?mt=12
#
# Win11:
#    Settings->Privacy & Security->Virus & threat protection->Manage aettings
#      Exclusions:
#        Add Folder: build/PWVault
#
set -x

PYINST="/cygdrive/c/opt/python/Scripts/pyinstaller.exe"

if [ "$1" = "clean" ]; then
  rm -rf spec build dist
  exit
fi

if [ -e win-PWVault.spec ]; then

  if [ ! -e spec ]; then
    mkdir spec
  fi
  cp win-PWVault.spec spec/PWVault.spec

  "$PYINST" --noconfirm \
            spec/PWVault.spec

else
  if [ ! -e spec ]; then
    mkdir spec
  fi

  "$PYINST" --windowed \
            --noconfirm \
            --specpath spec \
            --onedir \
            --name PWVault \
            pwvuiapp.py
fi
