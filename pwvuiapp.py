import os
import sys

from PyQt6 import QtGui
from PyQt6.QtCore    import QEvent
from PyQt6.QtWidgets import QApplication

from pwvsettings import PWVUiSettings


class PWVApp(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        self._mainWin = None
        
        self.focusChanged.connect(self._focusChangedCB)

        self._loadSettings()
        self._loadAssets()
        self._setAppWideStyles()

    def asset(self, name):
        return self._assets.get(name)

    def findActive(self):
        actwgt = None
        for tlwgt in QApplication.topLevelWidgets():
#            print(f"TOP WGT: {tlwgt.windowTitle()}  Active: {tlwgt.isActiveWindow()}")
            if tlwgt.isActiveWindow():
                actwgt = tlwgt
        return actwgt

    def mainWin(self):
        return self._mainWin

    def recentFileOpens(self):
        return self._settings.recentOpens()

    def recentFileUpdate(self, path):
        recentOpens = self._settings.recentOpens()
        if path in recentOpens:
            recentOpens.remove(path)
        recentOpens.append(path)
        maxRecents = 6
        rfLen = len(recentOpens)
        if rfLen > maxRecents:
            recentOpens = recentOpens[rfLen-maxRecents:]
        self._settings.setRecentOpens(recentOpens)
    
    def setMainWin(self, mainWin):
        self._mainWin = mainWin

    def settings(self):
        return self._settings
    
    def _focusChangedCB(fromWgt, toWgt):
        if type(fromWgt) is PWVApp:
            return
        
#        print(f"_focusChangedCB: From: {fromWgt}  To: {toWgt}")
        fromWin = fromWgt.window() if fromWgt else fromWgt
        toWin = toWgt.window() if toWgt else toWgt
#        print(f"    FromWin: {fromWin}  ToWin: {toWin}")
        self.findActive()

    def _loadAssets(self):
        folder = os.path.dirname(__file__)
        folder = os.path.join(folder, "assets")
        self._assets = {}
        icon = QtGui.QIcon(os.path.join(folder, "copy-button-icon.png"))
        self._assets["dark-copy-button-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "copy-black.svg"))
        self._assets["light-copy-button-icon"] = icon
#        icon = QtGui.QIcon(os.path.join(folder, "edit-button-icon.png"))
        icon = QtGui.QIcon(os.path.join(folder, "edit_red3.svg"))
        self._assets["edit-button-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "padlock-icon.png"))
        self._assets["padlock-icon"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-open-yellow.svg"))
        self._assets["eye-open-yellow"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-blocked-yellow.svg"))
        self._assets["eye-blocked-yellow"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-open-black.svg"))
        self._assets["eye-open-black"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "eye-blocked-black.svg"))
        self._assets["eye-blocked-black"] = icon
        icon = QtGui.QIcon(os.path.join(folder, "search-icon-yellow.svg"))
        self._assets["search-icon-yellow"] = icon
        if sys.platform[0:3] == "win":
            icon = QtGui.QIcon(os.path.join(folder, "assets/vault-icon.ico"))
        else:
            icon = QtGui.QIcon(os.path.join(folder, "assets/vault-icon.png"))
        self._assets["vault-icon"] = icon

        # set entries for dark/light themes
        theme = self.settings().appViewTheme()
        if theme == "Light":
            self._assets["copy-button-icon"] = self._assets["light-copy-button-icon"]
            self._assets["eye-open"] = self._assets["eye-open-black"]
            self._assets["eye-blocked"] = self._assets["eye-blocked-black"]
        else:
            self._assets["copy-button-icon"] = self._assets["dark-copy-button-icon"]
            self._assets["eye-open"] = self._assets["eye-open-yellow"]
            self._assets["eye-blocked"] = self._assets["eye-blocked-yellow"]

        try:
            from ctypes import windll  # Only exists on Windows.
            myappid = 'midoma.pwvault.PWVault.1.0.0'
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except ImportError:
            pass

    def _loadSettings(self):
        self._settings = PWVUiSettings(self)
        self._settings.load()

    def _setAppWideStyles(self):
        pass
#        self.setStyleSheet("""
#        QLineEdit[echoMode="2"] {
#          lineedit-password-character: 9679;
#        }
#        QInputDialog QLineEdit[echoMode="2"] {
#              lineedit-password-character: 9679;
#            }
#        """)

### BEGIN EVENT HANDLERS

    def event(self, qev):
        if qev.type() == QEvent.Type.FileOpen:
            if not self._mainWin:
                return False
            url = qev.url()
            if url.isLocalFile():
                localFile = url.toLocalFile()
                self._mainWin.openVaultPath(localFile)
            elif url.isValid():
                print(f"DEBUG: Valid URL {url}")
            else:
                print(f"DEBUG: Open File {qev.file()}")
                self._mainWin.openVaultPath(localFile)                

        return super().event(qev)

### END   EVENT HANDLERS


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        from pwvcliapp import CLIMain
        argv = [sys.argv[0]] + sys.argv[2:] 
        CLIMain(argv)
        sys.exit(0)
            
    from pwvuimain import PWVMainWin
    
    app = PWVApp()

    mainWin = PWVMainWin()
    app.setMainWin(mainWin)

    app.setWindowIcon(app.asset("vault-icon"))

    mainWin.show()

    status = app.exec()
    sys.exit(status)
