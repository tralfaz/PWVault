Section "File Association"
#    !insertmacro APP_ASSOCIATE "pwv" "pwvault.vaultfile" "PWVault Password Vault File" "$INSTDIR\\pwvault.exe,0" "Open with PWVault" "$INSTDIR\\pwvault.exe $\\"%1$\\""

WriteRegStr HKCR ".pwv" "" "PWVault.Document"

WriteRegStr HKCR "PWVault.Document" "" "PWVault Document"
WriteRegStr HKCR "PWVault.Document\DefaultIcon" "" "$INSTDIR\pwvault.exe,1"

WriteRegStr HKCR "PWVault.Document\shell\open\command" "" \
    '"$INSTDIR\pwvault.exe" "%1"'
#WriteRegStr HKCR "PWVault.Document\shell\print\command" "" \
#    '"$INSTDIR\pwvault.exe" /p "%1"'

SectionEnd
