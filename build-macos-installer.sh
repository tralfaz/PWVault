#!/bin/bash
#
# CreateDMG: https://github.com/create-dmg/create-dmg
#  brew install create-dmg
#
CREATEDMG=/opt/homebrew/bin/create-dmg

# Create a folder to prepare our DMG in (if it doesn't already exist).
if [ -e dist/dmg ]; then
    rm -rf dist/dmg
fi
mkdir -p dist/dmg

# Copy the app bundle to the dmg folder.
cp -r "dist/PWVault.app" dist/dmg

# If the DMG already exists, delete it.
if [ -e "dist/PWVault.dmg" ]; then
    rm "dist/PWVAult.dmg"
fi

"$CREATEDMG" \
  --volname "PWVault" \
  --volicon "assets/pwvault-app.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "PWVault.app" 175 120 \
  --hide-extension "PWVault.app" \
  --app-drop-link 425 120 \
  "dist/PWVault.dmg" \
  "dist/PWVault.app"
